"""Beamformer module for Spear AI.

This module defines the Beamformer class, which represents a conventional
beamformer used in signal processing. The class includes methods for setting
configuration, processing acoustic data, and handling array rotations.

"""

from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Self

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)

NONE_TYPE = type(None)


class Beamformer:
    """Beamformer class for Spear AI.

    The beamformer object holds a representation of the array in local coordinates.

    Reference frame:
    X - Forward
    Y - Port
    Z - Up

    """

    def __init__(self: Beamformer) -> None:
        """
        Initialize a Beamformer instance with default configuration.

        Sets default parameters such as speed of sound, sample rate, and array
        element positions. Initializes frequency vector, element matrices,
        and observation angles for elevation and bearing.
        """
        self.c = 1500.00
        # element position matrix P is 3xN
        self.P = np.empty([3, 0])
        # pre-allocate internal _P matrix as well; used by get_v()
        self._P = np.empty([3, 0])

        self.NFFT = 1024
        self.noverlap = self.NFFT // 2
        self.sample_rate_hz = 1.0
        self._start_freq_hz = 0.0
        self._end_freq_hz: float | None = None

        self._update_freq_vec()

        self.elevation_rad = np.deg2rad(np.arange(-30, 30 + 1e-2, 10))
        self.bearing_rad = np.linspace(-np.pi, np.pi, 91)[:-1]

    @classmethod
    def from_config_json(cls: type[Self], config_file: str) -> Self | None:
        """
        Initialize a Beamformer instance from a configuration file.

        Parameters:
        config_file (str): Path to the JSON configuration file.

        Returns:
        Beamformer | None: A Beamformer instance if the file is successfully loaded,
        otherwise None.
        """
        bf = cls()

        # Load and parse the configuration file
        config_path = Path(config_file)
        if not config_path.is_file():
            logger.error("Could not locate requested file: %s", config_file)
            raise FileNotFoundError("Could not locate requested file: " + config_file)

        try:
            with config_path.open() as ff:
                cfg = json.load(ff)
                cfg = {key.lower(): val for key, val in cfg.items()}
        except json.JSONDecodeError:
            logger.exception("Error decoding JSON")
            return None

        # Apply general settings
        bf.set_nfft(cfg.get("nfft", bf.NFFT))
        bf.set_sample_rate_hz(cfg.get("sample_rate_hz", bf.sample_rate_hz))

        # Apply frequency range if provided
        start_freq_hz = cfg.get("start_freq_hz", 0)
        end_freq_hz = cfg.get("end_freq_hz", None)
        if start_freq_hz or end_freq_hz:
            bf.set_target_freq(start_freq_hz=start_freq_hz, end_freq_hz=end_freq_hz)

        # Add elements if specified
        element_coordinate_length = 3
        elements = cfg.get("elements_m", [])
        for element in elements:
            if len(element) != element_coordinate_length:
                error_message = "Element coordinates must be of length 3: <x, y, z>"
                raise ValueError(error_message)
            bf.add_element(*element)

        # Set elevation and bearing angles if specified
        bf.elevation_rad = np.array(cfg.get("elevation_rad", bf.elevation_rad.tolist()))
        bf.bearing_rad = np.array(cfg.get("bearing_rad", bf.bearing_rad.tolist()))

        return bf

    def save_config(
        self: Beamformer,
        out_dir: str | None = None,
        filename: str = "beamformer_config.json",
    ) -> None:
        """Save the current beamformer object's configuration to JSON for later use."""
        if out_dir is None:
            # Use a secure temporary directory
            out_dir = tempfile.gettempdir()
        elif not Path(out_dir).is_dir():
            error_message = "Provided output directory '" + out_dir + "' is not valid."
            raise ValueError(error_message)

        if "." in filename and not filename.lower().endswith(".json"):
            error_message = "Only JSON files are supported at this time."
            raise ValueError(error_message)
        if "." not in filename:
            filename += ".json"

        config = {
            "NFFT": self.NFFT,
            "sample_rate_hz": self.sample_rate_hz,
            "start_freq_hz": self._start_freq_hz,
            "end_freq_hz": self._end_freq_hz,
            "elements_m": self.P.T.tolist(),
            "elevation_rad": self.elevation_rad.tolist(),
            "bearing_rad": self.bearing_rad.tolist(),
        }

        output_path = Path(out_dir)
        with output_path.open("w") as ff:
            json.dump(config, fp=ff)

    def add_element(
        self: Beamformer, x_m: float = 0, y_m: float = 0, z_m: float = 0
    ) -> None:
        """Add element to array at provided coordinates (values in meters)."""
        self.P = np.hstack([self.P, np.array([[x_m, y_m, z_m]]).T])
        self._P = self.P

    def set_sample_rate_hz(self: Beamformer, sample_rate_hz: float = 1.0) -> None:
        """Set the sampling rate of the expected data input (value in Hz)."""
        if not sample_rate_hz > 0:
            error_message = "A sampling rate greater than zero is strictly required!"
            raise ValueError(error_message)
        self.sample_rate_hz = sample_rate_hz
        self._update_freq_vec()

    def set_sound_speed_mps(self: Beamformer, sound_speed_mps: float = 1500) -> None:
        """Set the environment speed of sound (value in meters per second)."""
        if not sound_speed_mps > 0:
            error_message = "A sound speed greater than zero is strictly required!"
            raise ValueError(error_message)
        self.c = sound_speed_mps

    def set_nfft(self: Beamformer, nfft: int = 1024) -> None:
        """
        Set the number of FFT points for the beamformer.

        This method configures the number of FFT points (NFFT) used in frequency
        analysis and sets the overlap accordingly.

        Parameters:
            NFFT (int): The number of FFT points. Defaults to 1024.
        """
        self.NFFT = int(nfft)
        self.noverlap = self.NFFT // 2
        self._update_freq_vec()

    def _update_freq_vec(self: Beamformer) -> None:
        self.freq_vec = np.fft.rfftfreq(self.NFFT) * self.sample_rate_hz
        self._update_target_freq()

    def set_target_freq(
        self: Beamformer, start_freq_hz: float = 0, end_freq_hz: float | None = None
    ) -> None:
        """Configure the desired frequency bins to process, based on provided boundaries (values in Hz)."""
        if not end_freq_hz:
            got_end = False
            end_freq_hz = self.sample_rate_hz / 2
        else:
            got_end = True

        if start_freq_hz > np.max(self.freq_vec):
            error_message = (
                "Start frequency exceeds the maximum available frequency. "
                "Check sampling rate and use a value below the Nyquist limit."
            )
            raise ValueError(error_message)
        if end_freq_hz > np.max(self.freq_vec):
            error_message = (
                "End frequency exceeds the maximum available frequency. "
                "Check sampling rate and use a value at or below the Nyquist limit."
            )
            raise ValueError(error_message)

        fmask = (self.freq_vec >= start_freq_hz) * (self.freq_vec <= end_freq_hz)
        if np.sum(fmask) == 0:
            error_message = (
                "The start and end frequencies are too narrow."
                "No layers available within the requested bounds for the current sampling rate and NFFT."
            )
            raise ValueError(error_message)

        self._start_freq_hz = start_freq_hz
        if got_end:
            self._end_freq_hz = end_freq_hz
        self._update_target_freq()

    def _update_target_freq(self: Beamformer) -> None:
        end_freq_hz = self._end_freq_hz
        if not end_freq_hz:
            end_freq_hz = self.sample_rate_hz / 2
        fmask = (self.freq_vec >= self._start_freq_hz) * (self.freq_vec <= end_freq_hz)
        self.freq_target = self.freq_vec[fmask]

    def rotate_array_euler(
        self: Beamformer,
        roll: float = 0,
        pitch: float = 0,
        yaw: float = 0,
        *,
        degrees: bool = False,
    ) -> None:
        """Rotates the reference array and stores the result for use while beamforming.

        This allows the beamformer to maintain a global / non-rotating reference frame.
        Rotations are always applied as absolute transforms relative to original array
        layout; not an incremental transform.

        Rotations follow right-hand rule with respect to reference frame:
        X : roll  - Positive roll moves top (+Z) towards starboard
        Y : pitch - Positive pitch moves front (+X) downwards
        Z : yaw   - Positive yaw moves front (+X) towards port
        """
        rot = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=degrees)
        self._P = rot.as_matrix().dot(self.P)

    def get_v(
        self: Beamformer,
        bearing_rad: float | None = None,
        elevation_rad: float | None = None,
    ) -> np.ndarray:
        """Return the 4D replica matrix for the current array layout.

        If bearing and elevation angles are given, only those angles are
        processed; otherwise, the full matrix for all observation angles
        is produced.

        Uses current array orientation as recorded in self._P. Default is
        a copy of the original array layout from self.P, unless modified by
        calls to rotate_array_euler()
        """
        if bearing_rad is not None:
            if type(bearing_rad) not in [float, int]:
                msg = (
                    "Only single-point requests are currently supported;"
                    " to process an observation field, set "
                    "self.bearing_rad to the desired ndarray"
                )
                raise TypeError(msg)
            _bearing_rad = np.array([bearing_rad])
        else:
            _bearing_rad = self.bearing_rad

        if elevation_rad is not None:
            if type(elevation_rad) not in [float, int]:
                msg = (
                    "Only single-point requests are currently supported;"
                    " to process an observation field, set "
                    "self.elevation_rad to the desired ndarray"
                )
                raise TypeError(msg)
            _elevation_rad = np.array([elevation_rad])
        else:
            _elevation_rad = self.elevation_rad

        v_mat = np.zeros(
            [
                len(self.freq_target),
                len(_elevation_rad),
                len(_bearing_rad),
                self.P.shape[1],
            ],
            dtype=np.complex128,
        )

        for ifreq, freq in enumerate(self.freq_target):
            velev, vbear = np.meshgrid(_elevation_rad, _bearing_rad)
            k_mat = (2 * np.pi * freq) / self.c * self.get_a(vbear, velev)

            v_mat[ifreq, :] = np.exp(-1j * np.dot(k_mat.T, self._P))

        return v_mat

    @staticmethod
    def get_a(
        bearing_rad: float | np.ndarray = 0,
        elevation_rad: float | np.ndarray = 0,
    ) -> np.ndarray:
        """Return the direction vector(s) for arriving waves aligned with the provided observation angles."""
        a = np.array(
            [
                -np.cos(elevation_rad) * np.cos(bearing_rad),
                -np.cos(elevation_rad) * np.sin(bearing_rad),
                -np.sin(elevation_rad),
            ]
        )
        if len(a.shape) == 1:
            a = np.expand_dims(a, -1)
        return a

    def get_beampattern(
        self: Beamformer,
        bearing_rad: float | None = None,
        elevation_rad: float | None = None,
    ) -> np.ndarray:
        """Produce the beampattern response at a given set of steering angles."""
        v_mat = self.get_v()
        v_steer = self.get_v(bearing_rad, elevation_rad)[:, 0, 0, :]
        v_steer = np.expand_dims(v_steer, -1)

        b = np.zeros(v_mat[0, :].dot(v_steer[0, :]).shape)

        # Ignore "divide by zero encountered" warning and accept NaN in output
        with np.errstate(invalid="ignore", divide="ignore"):
            for ii in range(len(self.freq_target)):
                b += 10 * np.log10(
                    np.abs(1 / self.P.shape[1] * v_mat[ii, :].dot(v_steer[ii, :]))
                )
        b /= len(self.freq_target)
        return np.squeeze(b, -1)

    @staticmethod
    def _check_file(file_path: str) -> None:
        if not file_path:
            msg = "A file path must be provided!"
            raise ValueError(msg)
        if not Path(file_path).is_file():
            msg = "Not a valid file path!"
            raise ValueError(msg)
        if not file_path.lower().endswith(".csv"):
            msg = "Only CSVs are supported at this time"
            raise ValueError(msg)

    def process_file(self: Beamformer, aco_file: str) -> Iterator[np.ndarray]:
        """Process acoustic data file.

        Ingests acoustic data from CSV in chunks, rather than holding
        all data in memory at once.

        Returns generator of beamformer responses based on configured
        NFFT, noverlap.
        """
        if aco_file is None:
            error_message = "aco_file cannot be None"
            raise ValueError(error_message)
        self._check_file(aco_file)

        nstep = self.NFFT - self.noverlap
        aco_data = pd.read_csv(aco_file, nrows=0)
        v_mat = self.get_v()
        n = self.P.shape[1]
        freq_mask = [x in self.freq_target for x in self.freq_vec]

        for chunk in pd.read_csv(aco_file, chunksize=nstep):
            aco_data = pd.concat([aco_data, chunk])
            if len(aco_data) >= self.NFFT:
                _v_fft = np.fft.rfft(
                    aco_data.drop(columns=["timestamp_ns"]).iloc[: self.NFFT], axis=0
                )[freq_mask]

                b = np.zeros(v_mat[0, :].dot(_v_fft.T[:, 0]).shape)
                for ii in range(len(self.freq_target)):
                    b += 10 * np.log10(
                        np.abs(1 / n * v_mat[ii, :].dot(_v_fft.T[:, ii]))
                    )
                b /= len(self.freq_target)
                yield b
                aco_data = aco_data.iloc[nstep:]

    def process_file_with_pose(
        self: Beamformer,
        aco_file: str,
        pose_file: str | None = None,
        *,
        degrees: bool = False,
    ) -> Iterator[np.ndarray]:
        """Process acoustic data file alongside pose data file.

        When pose data is given, rotation updates are applied before beamforming.
        Time comparison between pose and acoustic data is based on the midpoint of
        the observation window for the acoustic data.

        If pose data file is None (default), reverts to process_file()

        Acoustic data is loaded from CSV in chunks, rather than holding
        all data in memory at once. Pose data is loaded to memory for
        timestamp comparison.

        Returns generator of beamformer responses based on configured
        NFFT, noverlap.
        """
        if aco_file is None:
            error_message = (
                "The `aco_file` path must be a valid string and cannot be None."
            )
            raise ValueError(error_message)

        if not pose_file:
            yield from self.process_file(aco_file=aco_file)
            return

        self._check_file(aco_file)
        self._check_file(pose_file)

        nstep = self.NFFT - self.noverlap

        aco_data = pd.read_csv(aco_file, nrows=0).drop(columns=["timestamp_ns"])
        v_mat = self.get_v()
        n = self.P.shape[1]
        freq_mask = [x in self.freq_target for x in self.freq_vec]

        pose = pd.read_csv(pose_file)

        _last_pose = None
        for chunk in pd.read_csv(aco_file, chunksize=nstep):
            aco_data = pd.concat([aco_data, chunk])
            if len(aco_data) >= self.NFFT:
                _pose_t = aco_data.iloc[self.NFFT // 2]["timestamp_ns"]
                _pose = pose[pose["timestamp_ns"] <= _pose_t]
                _pose = _pose.iloc[-1] if len(_pose) > 0 else None
                if _pose is not None and _pose is not _last_pose:
                    logger.info(
                        "%.2f ms : rotate to %s, %s, %s",
                        _pose_t / 1e6,
                        _pose["roll"],
                        _pose["pitch"],
                        _pose["yaw"],
                    )
                    _last_pose = _pose
                    self.rotate_array_euler(
                        _pose["roll"], _pose["pitch"], _pose["yaw"], degrees=degrees
                    )
                    v_mat = self.get_v()

                _v_fft = np.fft.rfft(
                    aco_data.drop(columns=["timestamp_ns"]).iloc[: self.NFFT], axis=0
                )[freq_mask]

                b = np.zeros(v_mat[0, :].dot(_v_fft.T[:, 0]).shape)
                for ii in range(len(self.freq_target)):
                    b += 10 * np.log10(
                        np.abs(1 / n * v_mat[ii, :].dot(_v_fft.T[:, ii]))
                    )
                b /= len(self.freq_target)
                yield b
                aco_data = aco_data.iloc[nstep:]

    def get_p_matrix(self: Beamformer) -> np.ndarray:
        """
        Get the internal `_P` matrix representing the rotated array coordinates.

        Returns:
        np.ndarray: The current rotated positions of the array elements as a 3xN matrix.
        """
        return self._P
