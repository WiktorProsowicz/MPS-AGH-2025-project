# -*- coding: utf-8 -*-
"""Contains functions for running the simulation using PyMPDATA."""


import logging
import os

from mps_agh_2025_project import utils

import numpy as np
import matplotlib.pyplot as plt
from PyMPDATA import Options, ScalarField, VectorField, Stepper, Solver
from PyMPDATA.boundary_conditions import Constant


def run_simulation(sim_output_path: str,
                   args: utils.SimulationArgs) -> utils.SimulationResult:
    """Runs the simulation using PyMPDATA."""

    output_path = utils.get_sim_output_path_by_args(sim_output_path, args)

    logging.info(
        'Running PyMPDATA simulation with output path: %s', output_path)

    xmin, xmax = args.grid_bounds
    dx = (xmax - xmin) / args.grid_points
    x = np.linspace(xmin + dx / 2, xmax - dx / 2, args.grid_points)

    n_steps = int(args.sim_time / args.dt)

    D_field = 1.01 + np.tanh(x)

    # initial condition - uniform field (to match py-pde reference exactly)
    c0 = np.full(args.grid_points, args.initial_value)  # Uniform concentration everywhere

    # ── build a Solver with native heterogeneous diffusion ───────────────────────────
    opts = Options(
        n_iters=10,  # more MPDATA iterations → sharper features
        non_zero_mu_coeff=True,
        heterogeneous_diffusion=True,  # Enable native heterogeneous diffusion
    )

    # Set up fields with proper boundary conditions
    advectee = ScalarField(data=c0, halo=opts.n_halo,
                           boundary_conditions=(Constant(0.0),))
    advector = VectorField(
        data=(np.zeros(args.grid_points + 1),), halo=opts.n_halo, boundary_conditions=(Constant(0.0),)
    )
    diffusivity_field = ScalarField(
        data=D_field, halo=opts.n_halo, boundary_conditions=(Constant(0.0),)
    )

    stepper = Stepper(options=opts, grid=(args.grid_points,))
    solver = Solver(
        stepper=stepper,
        advectee=advectee,
        advector=advector,
        diffusivity_field=diffusivity_field,
    )

    # ── march & record for kymograph ──────────────────────────────────────────────
    logging.info("Starting heterogeneous diffusion simulation...")
    logging.info(
        "Using native PyMPDATA implementation (should be ~3x faster than Strang splitting)"
    )

    kymo = np.empty((n_steps + 1, args.grid_points))
    kymo[0] = solver.advectee.get()

    # Use stronger mu_coeff for more realistic long-time evolution
    mu_coeff = 0.05  # Increased to get more decay over time

    logging.info(
        f"Diffusivity range: {D_field.min():.3f} to {D_field.max():.3f}")
    logging.info(f"Using balanced mu coefficient: {mu_coeff:.6f}")

    for i in range(1, n_steps + 1):
        if i % 10000 == 0:
            logging.info(f"At step {i}/{n_steps}")

        # Single call per timestep (vs 3 calls in Strang splitting!)
        solver.advance(n_steps=1, mu_coeff=(mu_coeff,))
        kymo[i] = solver.advectee.get()

    logging.info("Simulation completed!")

    res_kymo = np.empty((int(args.sim_time), args.grid_points))
    interval = int(1 / args.dt)

    for i in range(int(args.sim_time)):
        step_data = kymo[i * interval + 1: (i + 1) * interval + 1]
        res_kymo[i] = step_data[step_data.shape[0] // 2]
    
    res_kymo = np.concat((kymo[0:1], res_kymo), axis=0)

    # ── plot ───────────────────────────────────────────────────────────────────────
    T = np.linspace(0, args.sim_time, int(args.sim_time) + 1)
    X, Tgrid = np.meshgrid(x, T)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Main kymograph
    ax.pcolormesh(X, Tgrid, res_kymo, shading="auto")
    # ax.set_colorbar(label="c(x,t)")
    ax.set_xlabel("x")
    ax.set_ylabel("Time")
    ax.set_title("Native PyMPDATA Heterogeneous Diffusion")

    fig.savefig(
        os.path.join(output_path, "kymograph.png"))

    fig, ax = plt.subplots(figsize=(10, 6))

    # Diffusivity profile
    ax.plot(x, D_field, "b-", linewidth=2)
    ax.set_xlabel("x")
    ax.set_ylabel("D(x)")
    ax.set_title("Heterogeneous Diffusivity")
    ax.grid(True, alpha=0.3)

    fig.savefig(os.path.join(output_path, "diffusivity_profile.png"))

    fig, ax = plt.subplots(figsize=(10, 6))

    # Final solution
    ax.plot(x, kymo[0], "k--", alpha=0.7, label="t=0")
    ax.plot(x, kymo[-1], "r-", label=f"t={args.sim_time}")
    ax.set_xlabel("x")
    ax.set_ylabel("c(x)")
    ax.set_title("Initial vs Final")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.savefig(os.path.join(output_path, "initial_vs_final.png"))


    # ── Summary statistics ─────────────────────────────────────────────────────────
    logging.info(
        f"Mass conservation: initial={kymo[0].sum():.6f}, final={kymo[-1].sum():.6f}"
    )
    logging.info(
        f"Relative mass change: {abs(kymo[-1].sum() - kymo[0].sum()) / kymo[0].sum() * 100:.2e}%"
    )

    return utils.SimulationResult(
        result_matrix=res_kymo
    )
