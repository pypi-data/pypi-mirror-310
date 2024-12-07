"""
Beamformer main execution module.

This module defines the `run_beamformer` function, which serves as the entry point for running
the beamforming process. It parses command-line arguments for input and output file paths,
loads configurations, processes acoustic data, and saves the output in a compressed file format.

"""

import argparse
import logging
import tempfile
from pathlib import Path

import numpy as np

from .beamformer_core import Beamformer

logger = logging.getLogger(__name__)


def run_beamformer() -> None:
    """
    Run the beamforming process based on input arguments.

    This function sets up logging, parses command-line arguments for input and output
    file paths, loads a Beamformer configuration (if provided), and processes acoustic
    and pose data. The processed data is then saved in a compressed file format.

    Command-line Arguments:
        --aco_file (str): Path to the acoustic data file (CSV).
        --pose_file (str): Path to the pose data file (CSV).
        --config_file (str): Path to the Beamformer configuration file (JSON).
        --outdir (str): Output directory for the results (default: "/tmp/").
        --outfile (str): Output filename (default: "beamformer_output").

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
    )

    parser = argparse.ArgumentParser(
        prog="Beamformer",
        description="Processes acoustic data and pose files",
        epilog="",
    )

    parser.add_argument(
        "--aco_file", required=True, type=str, help="Acoustic data file (CSV)"
    )
    parser.add_argument(
        "--pose_file", default=None, type=str, help="Pose data file (CSV)"
    )
    parser.add_argument(
        "--config_file", default=None, type=str, help="Beamformer config file (JSON)"
    )
    parser.add_argument(
        "--outdir", default=tempfile.gettempdir(), type=str, help="Output directory"
    )
    parser.add_argument(
        "--outfile",
        default="beamformer_output",
        help="Output filename",
        type=str,
    )

    args, _ = parser.parse_known_args()

    logger.info(args)

    if args.config_file and Path(args.config_file).is_file():
        bf = Beamformer.from_config_json(args.config_file)
    else:
        bf = Beamformer()

    if bf is None:
        logger.error("Beamformer instance could not be created from config file.")
        return

    b_all = list(bf.process_file_with_pose(args.aco_file, args.pose_file))
    b_all_array = np.array(b_all)
    output_path = Path(args.outdir) / f"{args.outfile}.npz"
    logger.info(
        "Writing to %s : %d %s",
        output_path,
        len(b_all),
        b_all[0].shape,
    )
    output_path = Path(args.outdir) / f"{args.outfile}.npz"
    np.savez_compressed(output_path, beamformer_response=b_all_array)
