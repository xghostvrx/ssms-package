import subprocess
from os import chdir, mkdir, makedirs
from os.path import isdir, isfile
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
    project_name = config['Project Settings']['project_name']
    run_name = config['Run Settings']['run_name']

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

    # chdir(dir_path)

    sleep(3)

    # Quality control (RAW)
    logger.info('Running raw sequence read(s) through quality control...')

    sleep(3)

    is_dir = isdir('reports/fastqc/before_trimming')
    if is_dir == 1:
        logger.warning('Skipping quality control (fastqc) for raw sequence read(s)...')
    else:
        makedirs('reports/fastqc/before_trimming')

        chdir(dir_path)

        is_dir = isdir(dir_path + '/.ssms-package/conda/fastqc')
        if not is_dir == 1:
            subprocess.run(f'conda env create -f envs/fastqc.yml --prefix {dir_path}/.ssms-package/conda/fastqc',
                           shell=True, executable='/bin/bash')

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/fastqc python=3 python3 subprocesses/fastqc.py',
            shell=True, executable='/bin/bash')

    sleep(3)

    is_dir = isdir('reports/multiqc/before_trimming')
    if is_dir == 1:
        logger.warning('Skipping quality control (multiqc) for raw sequence read(s)...')
    else:
        makedirs('reports/multiqc/before_trimming')

        chdir(dir_path)

        is_dir = isdir(dir_path + '/.ssms-package/conda/multiqc')
        if not is_dir == 1:
            subprocess.run(f'conda env create -f envs/multiqc.yml --prefix {dir_path}/.ssms-package/conda/multiqc',
                           shell=True, executable='/bin/bash')

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/multiqc python=3 python3 subprocesses/multiqc.py',
            shell=True, executable='/bin/bash')

    sleep(3)

    is_dir = isdir('results/reads')
    if is_dir == 1:
        logger.warning('Skipping quality control (kneaddata) for raw sequence read(s)...')
    else:
        chdir(dir_path)

        is_dir = isdir(dir_path + '/.ssms-package/conda/kneaddata')
        if not is_dir == 1:
            subprocess.run(f'conda env create -f envs/kneaddata.yml --prefix {dir_path}/.ssms-package/conda/kneaddata',
                           shell=True, executable='/bin/bash')

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/kneaddata python=3 python3 subprocesses/kneaddata.py',
            shell=True, executable='/bin/bash')

    sleep(3)

    # Quality control (CLEAN)
    logger.info('Running clean sequence read(s) through quality control...')

    sleep(3)

    is_dir = isdir('reports/fastqc/after_trimming')
    if is_dir == 1:
        logger.warning('Skipping quality control (fastqc) for clean sequence read(s)...')
    else:
        makedirs('reports/fastqc/after_trimming')

        chdir(dir_path)

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/fastqc python=3 python3 subprocesses/fastqc.py',
            shell=True, executable='/bin/bash')

    sleep(3)

    is_dir = isdir('reports/multiqc/after_trimming')
    if is_dir == 1:
        logger.warning('Skipping quality control (multiqc) for clean sequence read(s)...')
    else:
        makedirs('reports/multiqc/after_trimming')

        chdir(dir_path)

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/multiqc python=3 python3 subprocesses/multiqc.py',
            shell=True, executable='/bin/bash')

    sleep(3)

    # kraken2
    logger.info('Running clean sequence read(s) through kraken2...')

    is_dir = isdir('reports/kraken2')
    if is_dir == 1:
        logger.warning('Skipping kraken2 for clean sequence read(s)...')
    else:
        makedirs('reports/kraken2')

        chdir(dir_path)

        is_dir = isdir(dir_path + '/.ssms-package/conda/kraken2')
        if not is_dir == 1:
            subprocess.run(f'conda env create -f envs/kraken2.yml --prefix {dir_path}/.ssms-package/conda/kraken2',
                           shell=True, executable='/bin/bash')

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/kraken2 python=3 python3 subprocesses/kraken2.py',
            shell=True, executable='/bin/bash')

    # bracken
    logger.info('Running clean sequence read(s) through bracken...')

    is_dir = isdir('reports/kraken2/bracken')
    if is_dir == 1:
        logger.warning('Skipping bracken for clean sequence read(s)...')
    else:
        makedirs('reports/kraken2/bracken')

        chdir(dir_path)

        is_dir = isdir(dir_path + '/.ssms-package/conda/bracken')
        if not is_dir == 1:
            subprocess.run(f'conda env create -f envs/bracken.yml --prefix {dir_path}/.ssms-package/conda/bracken',
                           shell=True, executable='/bin/bash')

        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/bracken python=3 python3 subprocesses/bracken.py',
            shell=True, executable='/bin/bash')

    # kraken-biom

    is_file = isfile(f'{project_name}-{run_name}-kraken2-results.biom') or isfile(
        f'{project_name}-{run_name}-bracken-results.biom')
    if is_file == 1:
        logger.warning('Skipping biom for clean sequence read(s)...')
    else:
        chdir(dir_path)

        is_dir = isdir(dir_path + '/.ssms-package/conda/kraken-biom')
        if not is_dir == 1:
            subprocess.run(
                f'conda env create -f envs/kraken-biom.yml --prefix {dir_path}/.ssms-package/conda/kraken-biom',
                shell=True, executable='/bin/bash')
        subprocess.run(
            f'conda run --prefix {dir_path}/.ssms-package/conda/kraken-biom python=3 python3 subprocesses/kraken-biom.py',
            shell=True, executable='/bin/bash')
