import subprocess
import sys
from glob import iglob, glob
from os import chdir, mkdir, getcwd, rename
from os import path
from shutil import copy, move, rmtree

sys.path.append(path.dirname(path.dirname(path.realpath(__file__))))

from console import dir_path
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run = config['Run Settings']['run']
run_name = config['Run Settings']['run_name']
project_name = config['Project Settings']['project_name']


def export_kraken2():
    chdir(run + '/reports/kraken2')

    is_dir = 'temp'
    if not is_dir == 1:
        mkdir('temp')

    for filename in iglob(f'*_report.txt'):
        basename = path.basename(filename)
        copy(f'{filename}', f'temp/{basename}')
        break

    chdir('temp')

    subprocess.run('kraken-biom *.txt -o reports.biom --fmt json',
                   shell=True, executable='/bin/bash')

    subprocess.run('biom summarize-table -i reports.biom -o reports-summary.txt',
                   shell=True, executable='/bin/bash')

    # Move biom files to the main directory
    directory = getcwd()
    move(f'{directory}/reports.biom', run)
    move(f'{directory}/reports-summary.txt', run)

    # Remove temporary folder
    chdir(run)
    rmtree('reports/kraken2/temp')

    # Rename biom files
    directory = getcwd()
    rename(f'{directory}/reports.biom', f'{project_name}-{run_name}-kraken2-results.biom')
    rename(f'{directory}/reports-summary.txt', f'{project_name}-{run_name}-kraken2-summary.txt')


def export_bracken():
    chdir(run + '/reports/kraken2/bracken')

    mkdir('temp')

    if glob('*_species_report.txt'):
        for filename in iglob('*_species_report.txt'):
            basename = path.basename(filename)
            copy(f'{filename}', f'temp/{basename}')
            break
    elif glob('*_genus_report.txt'):
        for filename in iglob('*_genus_report.txt'):
            basename = path.basename(filename)
            copy(f'{filename}', f'temp/{basename}')
            break
    elif glob('*_phylum_report.txt'):
        for filename in iglob('*_phylum_report.txt'):
            basename = path.basename(filename)
            copy(f'{filename}', f'temp/{basename}')
            break

    chdir('temp')

    subprocess.run('kraken-biom *.txt -o reports.biom --fmt json',
                   shell=True, executable='/bin/bash')

    subprocess.run('biom summarize-table -i reports.biom -o reports-summary.txt',
                   shell=True, executable='/bin/bash')

    # Move biom files to the main directory
    directory = getcwd()
    move(f'{directory}/reports.biom', run)
    move(f'{directory}/reports-summary.txt', run)

    # Remove temporary folder
    chdir(run)
    rmtree('reports/kraken2/bracken/temp')

    # Rename biom files
    directory = getcwd()
    rename(f'{directory}/reports.biom', f'{project_name}-{run_name}-bracken-results.biom')
    rename(f'{directory}/reports-summary.txt', f'{project_name}-{run_name}-bracken-summary.txt')


export_kraken2()
export_bracken()
