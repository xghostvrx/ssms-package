import re
import subprocess
from glob import iglob
from os import chdir, mkdir
from shutil import move

from console import dir_path
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run = config['Run Settings']['run']
classifier_database = config['Databases']['classifier_database']

# Change into working directory
chdir(run + '/reports/kraken2')

# Run bracken
for filename in iglob('*_report.txt'):
    sampleid = re.findall('^(.+?(?=_))', filename)[0]

    # Generate bracken reports
    subprocess.run(['bracken',
                    '-d', f'{classifier_database}',
                    '-r', '150',
                    '-l', 'S',
                    '-i', f'{filename}',
                    '-o', f'bracken/{sampleid}_species_output.txt',
                    '-w', f'bracken/{sampleid}_species_report.txt'])
    subprocess.run(['bracken',
                    '-d', f'{classifier_database}',
                    '-r', '150',
                    '-l', 'G',
                    '-i', f'{filename}',
                    '-o', f'bracken/{sampleid}_genus_output.txt',
                    '-w', f'bracken/{sampleid}_genus_report.txt'])
    subprocess.run(['bracken',
                    '-d', f'{classifier_database}',
                    '-r', '150',
                    '-l', 'P',
                    '-i', f'{filename}',
                    '-o', f'bracken/{sampleid}_phylum_output.txt',
                    '-w', f'bracken/{sampleid}_phylum_report.txt'])

chdir(run + '/reports/kraken2/bracken')

# Combine bracken outputs
for filename in iglob('*_output.txt'):

    sampleid = re.findall('^(.+?(?=_))', filename)[0]

    is_file = f'{sampleid}_species_output.txt'
    if is_file == 1:
        subprocess.run(['combine_bracken_outputs.py',
                        '--files', f'{sampleid}_species_output.txt',
                        '-o', 'all_species_output.txt'])

    is_file = f'{sampleid}_genus_output.txt'
    if is_file == 1:
        subprocess.run(['combine_bracken_outputs.py',
                        '--files', f'{sampleid}_genus_output.txt',
                        '-o', 'all_genus_output.txt'])

    is_file = f'{sampleid}_phylum_output.txt'
    if is_file == 1:
        subprocess.run(['combine_bracken_outputs.py',
                        '--files', f'{sampleid}_phylum_output.txt',
                        '-o', 'all_phylum_output.txt'])

mkdir('outputs')

for filename in iglob(f'*_output.txt'):
    move(filename, 'outputs')
