import os
from mps_agh_2025_project import utils, sim_pympdata, sim_py_pde

TEST_RESULTS_PATH = os.getenv('TEST_RESULTS_PATH')
SIM_OUTPUT_DIR = os.path.join(TEST_RESULTS_PATH, 'sim_output')


def test_similarity():

    sim_args = utils.SimulationArgs(sim_name='pympdata_sim')
    sim_pympdata.run_simulation(SIM_OUTPUT_DIR, sim_args)
    mpdata_res_path = utils.get_sim_output_path_by_args(SIM_OUTPUT_DIR, sim_args)


    sim_args = utils.SimulationArgs(sim_name='py_pde_sim')
    sim_py_pde.run_simulation(sim_output_path=os.join(SIM_OUTPUT_DIR, 'py_pde_sim_output.png'))
    py_pde_res_path = utils.get_sim_output_path_by_args(SIM_OUTPUT_DIR, sim_args)

