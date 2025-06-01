# -*- coding: utf-8 -*-
"""Contains functions for running the simulation using pyPDE."""

import utils
import logging

def run_simulation(sim_output_path: str,
                   args: utils.SimulationArgs):
    """Runs the simulation using pyPDE."""
    
    output_path = utils.get_sim_output_path_by_args(sim_output_path, args)

    logging.debug('Running pyPDE simulation with output path: %s', output_path)