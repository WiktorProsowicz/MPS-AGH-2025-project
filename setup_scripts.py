
import argparse
import logging
import os
import pathlib
import shutil
import subprocess
import sys
from os import environ

HOME_PATH = pathlib.Path(__file__).absolute().parent.as_posix()

def run_tests() -> None:
    """Run available unit tests from the 'tests/unit' directory."""

    current_env = environ.copy()

    logging.info('Cleaning test results directory...')

    shutil.rmtree(os.path.join(HOME_PATH, 'test_results'), ignore_errors=True)
    os.makedirs(os.path.join(HOME_PATH, 'test_results'))

    current_env["TEST_RESULTS_PATH"] = os.path.join(HOME_PATH, 'test_results')

    test_report_path = os.path.join(HOME_PATH, 'test_results', 'test_report.xml')

    try:

        logging.info('Running tests...')

        command = (f'python -m pytest --import-mode=prepend -s test --tb=short -v'
                   f' --junitxml={test_report_path} -W ignore::DeprecationWarning'
                   f' --cov=src --rootdir=test'
                   ' --disable-warnings')

        subprocess.run(command.split(), check=True, env=current_env)

        command = 'coverage report'

        subprocess.run(command.split(), check=True, env=current_env)

    except subprocess.CalledProcessError as proc_error:
        logging.critical('Tests failed: %s', proc_error)
        sys.exit(1)

def main(function: str) -> None:
    """Main function delegating the flow to other ones.

    Args:
        function (str): Name of the function to be called.
    """

    if function == 'run_tests':
        run_tests()
        return

    logging.critical("Couldn't find the function '%s'.", function)
    sys.exit(1)

if __name__ == '__main__':
    
    program_desc = """Script contains functions helping with project management.
    Available functions:
        run_tests - runs unit tests from the "test" directory.
    """

    arg_parser = argparse.ArgumentParser(
        description=program_desc, formatter_class=argparse.RawDescriptionHelpFormatter)

    arg_parser.add_argument(
        'function_name', help='name of the function to be used')

    sys.path.append(os.path.join(HOME_PATH, 'src'))

    arguments = arg_parser.parse_args()

    main(arguments.function_name)
