import subprocess
from os import chdir, makedirs
from os.path import isdir

from console import dir_path, logger
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run_name = config['Run Settings']['run_name']
run = config['Run Settings']['run']

# Change into working directory
chdir(run)

# Check if output folders exist
is_dir = isdir('reports/fastqc/before_trimming')
if is_dir == 1:
    logger.warning('Skipping quality control (fastqc) for raw sequence read(s)...')
    exit()
else:
    makedirs('reports/fastqc/before_trimming')

# Run fastqc
subprocess.run(f'fastqc -t 8 reads/*.fastq.gz -outdir=reports/fastqc/before_trimming',
               shell=True, executable='/bin/bash')
