import re
import subprocess
import sys
from glob import iglob
from os import chdir
from os.path import dirname, realpath, basename

sys.path.append(dirname(dirname(realpath(__file__))))

from console import dir_path
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run = config['Run Settings']['run']
database_selection = config['Run Settings']['database_selection']
read_type = config['Run Settings']['read_type']
classifier_database = config['Databases']['classifier_database']

# Change into working directory
chdir(run)

# Run kraken2
if read_type == 'paired':

    for filename in iglob('results/reads/*_paired_1.fastq'):
        filename = basename(filename)

        sampleid = re.findall('^(.+?(?=_))', filename)[0]

        subprocess.run(['kraken2',
                        '--db', f'{classifier_database}',
                        '--threads', '8',
                        '--use-names',
                        '--output', f'results/kraken2/{sampleid}_output.txt',
                        '--report', f'reports/kraken2/{sampleid}_report.txt',
                        '--paired', f'results/reads/{sampleid}_paired_1.fastq',
                        f'results/reads/{sampleid}_paired_2.fastq'])

elif read_type == 'single':

    for filename in iglob('results/reads/*.fastq'):
        filename = basename(filename)

        sampleid = re.findall('^(.+?(?=_))', filename)[0]

        subprocess.run(['kraken2',
                        '--db', f'{classifier_database}',
                        '--threads', '8',
                        '--use-names',
                        '--output', f'results/kraken2/{sampleid}_output.txt',
                        '--report', f'reports/kraken2/{sampleid}_report.txt',
                        '--paired', f'results/reads/{sampleid}.fastq'])
