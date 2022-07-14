import subprocess
from os import chdir, mkdir
from os.path import isdir
from time import sleep

from console import clear_console, logger, dir_path
from settings import config


def start():
    clear_console()

    # Create a termination function
    def terminate_process():
        logger.error('The workspace for this configuration appears to have been modified.')
        logger.error('The user must start a new configuration, and maintain their folder structure.')
        logger.critical('Terminating SSMS Package Workflow...')
        exit()

    config.read('workspace/config.ini')

    # Determine if a workspace exists (if not terminate)
    workspace = config['General Settings']['workspace']
    is_dir = isdir(workspace)
    if not is_dir == 1:
        terminate_process()

    # Determine if the workspace has been modified (if so terminate)
    is_dir = isdir(workspace + '/adapters') and isdir(workspace + '/databases') and isdir(workspace + '/projects')
    if not is_dir == 1:
        terminate_process()

    # Determine if projects/project_name/run_name/ has been modified (if so terminate)
    run = config['Run Settings']['run']
    is_dir = isdir(run)
    if not is_dir == 1:
        terminate_process()

    # Determine if projects/project_name/run_name/reads/ has been modified (if so terminate)
    reads = config['Run Settings']['reads']
    is_dir = isdir(reads)
    if is_dir == 1:

        # If directory exists, do the following:
        chdir(run)

        is_dir = isdir('results')
        if not is_dir == 1:
            mkdir('results')

        is_dir = isdir('reports')
        if not is_dir == 1:
            mkdir('reports')

    else:
        terminate_process()

    chdir(dir_path)

    sleep(3)

    # Quality control
    logger.info('Running raw sequence read(s) through quality control...')

    is_dir = isdir(dir_path + '/.ssms-package/conda/fastqc')
    if not is_dir == 1:
        subprocess.run(f'conda env create -f envs/fastqc.yml --prefix {workspace}/.ssms-package/conda/fastqc',
                       shell=True, executable='/bin/bash')

    subprocess.run(f'conda run --prefix {workspace}/.ssms-package/conda/fastqc python=3 python3 subprocesses/fastqc.py',
                   shell=True, executable='/bin/bash')

    is_dir = isdir(dir_path + '/.ssms-package/conda/multiqc')
    if not is_dir == 1:
        subprocess.run(f'conda env create -f envs/multiqc.yml --prefix {workspace}/.ssms-package/conda/multiqc',
                       shell=True, executable='/bin/bash')

    subprocess.run(
        f'conda run --prefix {workspace}/.ssms-package/conda/multiqc python=3 python3 subprocesses/multiqc.py',
        shell=True, executable='/bin/bash')
