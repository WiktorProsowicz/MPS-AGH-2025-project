import os
from mps_agh_2025_project import utils, sim_pympdata, sim_pde

test_results_path = os.getenv('TEST_RESULTS_PATH')
sim_output_path = os.path.join(test_results_path, 'sim_output')


def test_similarity():

    std_args = {
        'grid_bounds': (-5.0, 5.0),
        'grid_points': 64,
        'initial_value': 1.0,
        'sim_time': 100.0,
        'dt': 1e-3,
    }

    sim_args = utils.SimulationArgs(sim_name='pympdata_sim', **std_args)
    sim_pympdata.run_simulation(sim_output_path, sim_args)
    mpdata_res_path = utils.get_sim_output_path_by_args(sim_output_path, sim_args)


    sim_args = utils.SimulationArgs(sim_name='pypde_sim', **std_args)
    sim_pde.run_simulation(sim_output_path, sim_args)
    pde_res_path = utils.get_sim_output_path_by_args(sim_output_path, sim_args)

    assert True
