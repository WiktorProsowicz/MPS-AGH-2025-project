# -*- coding: utf-8 -*-
"""Contains functions for running the simulation using PyMPDATA."""

import logging

from mps_agh_2025_project import utils


def run_simulation(sim_output_path: str,
                   args: utils.SimulationArgs):
    """Runs the simulation using PyMPDATA."""
    
    output_path = utils.get_sim_output_path_by_args(sim_output_path, args)

    logging.debug('Running PyMPDATA simulation with output path: %s', output_path)
