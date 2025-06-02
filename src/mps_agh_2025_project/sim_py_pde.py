# -*- coding: utf-8 -*-
"""Contains functions for running the simulation using py-pde."""

import logging

from pde import PDE, CartesianGrid, MemoryStorage, ScalarField, plot_kymograph

from mps_agh_2025_project import utils


# def run_simulation(sim_output_path: str,
#                    args: utils.SimulationArgs):
#     """Runs the simulation using py-pde."""
    
#     output_path = utils.get_sim_output_path_by_args(sim_output_path, args)

#     logging.debug('Running py-pde simulation with output path: %s', output_path)


def run_simulation(
    diffusivity_expr="1.01 + tanh(x)",
    grid_bounds=[-5, 5],
    grid_points=64,
    initial_value=1,
    time=100,
    dt=1e-3,
    bc_value=0,
    tracker_interval=1,
    display_plot=False,
    plot_save_path=None
):
    term_1 = f"({diffusivity_expr}) * laplace(c)"
    term_2 = f"dot(gradient({diffusivity_expr}), gradient(c))"
    eq = PDE({"c": f"{term_1} + {term_2}"}, bc={"value": bc_value})

    grid = CartesianGrid([grid_bounds], grid_points)
    field = ScalarField(grid, initial_value)

    storage = MemoryStorage()
    res = eq.solve(field, time, dt=dt, tracker=storage.tracker(tracker_interval))

    if display_plot:
        plot_kymograph(storage)

    if plot_save_path:
        plot_kymograph(storage, filename=plot_save_path, action="none")

    return res, storage


if __name__ == "__main__":
    run_simulation(plot_save_path="diffusion_pde_plot.png")
