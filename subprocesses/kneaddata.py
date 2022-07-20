import re
import subprocess
import sys
from glob import iglob
from os import chdir, mkdir, getcwd
from os.path import dirname, realpath, basename
from shutil import move

sys.path.append(dirname(dirname(realpath(__file__))))

from console import dir_path
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
miniconda = config['General Settings']['miniconda']
run_name = config['Run Settings']['run_name']
run = config['Run Settings']['run']
reads = config['Run Settings']['reads']
read_type = config['Run Settings']['read_type']
trimmomatic_options = config['Run Settings']['trimmomatic_options']
trimmer_database = config['Databases']['trimmer_database']

# Change into working directory
chdir(run)

# Run kneaddata
for filename in iglob(f'{reads}/*_R1_*.fastq.gz'):

    filename = basename(filename)
    sampleid = re.findall('^(.+?(?=_))', filename)[0]
    barcode = re.findall('([0-9][0-9]+?(?=_L))', filename)[0]
    lane = re.findall('(L[0-9][0-9]+?(?=_R))', filename)[0]
    direction = re.findall('(R[0-2]+?(?=_))', filename)[0]
    set = re.findall('R[0-2]_([0-9][0-9][0-9])', filename)[0]

    if read_type == 'paired':

        subprocess.run(['kneaddata',
                        '--input', f'{reads}/{sampleid}_{barcode}_{lane}_R1_{set}.fastq.gz',
                        '--input', f'{reads}/{sampleid}_{barcode}_{lane}_R2_{set}.fastq.gz',
                        '--trimmomatic', f'{dir_path}/.ssms-package/conda/kneaddata/share/trimmomatic-0.39-2',
                        f'--trimmomatic-options="{trimmomatic_options}"',
                        '--reference-db', f'{trimmer_database}',
                        '--max-memory', '40g', '-p', '8', '-t', '8',
                        '--output-prefix', f'{sampleid}',
                        '--output', f'{run}/results'])

        break

    elif read_type == 'single':

        subprocess.run(['kneaddata',
                        '--input', f'{reads}/{sampleid}_{barcode}_{lane}_R1_{set}.fastq.gz',
                        '--trimmomatic', f'{dir_path}/.ssms-package/conda/kneaddata/share/trimmomatic-0.39-2',
                        f'--trimmomatic-options="{trimmomatic_options}"',
                        '--reference-db', f'{trimmer_database}',
                        '--max-memory', '40g', '-p', '8', '-t', '8',
                        '--output-prefix', f'{sampleid}',
                        '--output', f'{run}/results'])

        break

chdir('results')

mkdir('bowtie2')
mkdir('logs')
mkdir('repeats')
mkdir('trimmomatic')
mkdir('unmatched')
mkdir('reads')

directory = getcwd()
for filename in iglob(f'{directory}/*_bowtie2_paired*'):
    move(filename, 'bowtie2')
for filename in iglob(f'{directory}/*_bowtie2_unmatched_*'):
    move(filename, 'bowtie2')
for filename in iglob(f'{directory}/*log'):
    move(filename, 'logs')
for filename in iglob(f'{directory}/*repeats*'):
    move(filename, 'repeats')
for filename in iglob(f'{directory}/*trimmed*'):
    move(filename, 'trimmomatic')
for filename in iglob(f'{directory}/*unmatched*'):
    move(filename, 'unmatched')
for filename in iglob(f'{directory}/*.fastq'):
    move(filename, 'reads')
