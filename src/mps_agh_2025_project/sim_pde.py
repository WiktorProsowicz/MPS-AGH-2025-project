# -*- coding: utf-8 -*-
"""Contains functions for running the simulation using pyPDE."""

import os
import logging

from mps_agh_2025_project import utils
import numpy as np

from pde import PDE, CartesianGrid, MemoryStorage, ScalarField, plot_kymograph


def run_simulation(sim_output_path: str,
                   args: utils.SimulationArgs) -> utils.SimulationResult:
    """Runs the simulation using pyPDE."""

    output_path = utils.get_sim_output_path_by_args(sim_output_path, args)

    logging.info('Running pyPDE simulation with output path: %s', output_path)

    term_1 = "(1.01 + tanh(x)) * laplace(c)"
    term_2 = "dot(gradient(1.01 + tanh(x)), gradient(c))"
    eq = PDE({"c": f"{term_1} + {term_2}"}, bc={"value": 0})

    grid = CartesianGrid([list(args.grid_bounds)], args.grid_points)
    field = ScalarField(grid, args.initial_value)

    storage = MemoryStorage()
    res = eq.solve(field,
                   args.sim_time,
                   dt=args.dt,
                   tracker=storage.tracker(1))

    plot_path = os.path.join(output_path, "kymograph.png")
    plot_kymograph(storage, filename=plot_path, action="none")

    res = []
    times = []
    for t, field in storage.items():
        img_data = field.get_line_data(scalar="auto", extract="auto")
        res.append(img_data["data_y"])
        times.append(t)

    res = np.array(res)
    times = np.array(times)

    return utils.SimulationResult(
        result_matrix=res
    )
