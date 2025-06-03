"""Contains project-wide utility functions."""

from typing import Tuple
import dataclasses
import os

@dataclasses.dataclass(frozen=True)
class SimulationArgs:
    """Dataclass to hold simulation arguments."""
    sim_name: str
    grid_bounds: Tuple[float, float]
    grid_points: int
    initial_value: float
    sim_time: float
    dt: float
    

def get_sim_output_path_by_args(simulations_path: str, args: SimulationArgs) -> str:
    """Generates the output path for a simulation based on its arguments"""

    args_hash = str(hash(dataclasses.astuple(args)))

    return os.path.join(simulations_path, args_hash)