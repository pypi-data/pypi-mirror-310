"""
Beamformer package initialization.

Provides core functionality and main execution for beamforming processes.
"""

from .beamformer_core import Beamformer
from .beamformer_main import run_beamformer

__all__ = ["Beamformer", "run_beamformer"]

VERSION = "0.0.1"
