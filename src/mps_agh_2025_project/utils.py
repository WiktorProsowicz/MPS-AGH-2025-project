"""Contains project-wide utility functions."""

from typing import Tuple
import dataclasses
import os

import numpy as np

@dataclasses.dataclass(frozen=True)
class SimulationArgs:
    """Dataclass to hold simulation arguments."""
    sim_name: str
    grid_bounds: Tuple[float, float]
    grid_points: int
    initial_value: float
    sim_time: float
    dt: float

@dataclasses.dataclass(frozen=True)
class SimulationResult:
    """Dataclass to hold simulation results."""
    result_matrix: np.ndarray
    
    

def get_sim_output_path_by_args(simulations_path: str, args: SimulationArgs) -> str:
    """Generates the output path for a simulation based on its arguments"""

    args_hash = str(hash(str(args)))

    return os.path.join(simulations_path, args_hash)