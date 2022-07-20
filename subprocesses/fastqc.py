import subprocess
import sys
from os import chdir
from os.path import dirname, realpath, isdir

sys.path.append(dirname(dirname(realpath(__file__))))

from console import dir_path
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run_name = config['Run Settings']['run_name']
run = config['Run Settings']['run']

# Change into working directory
chdir(run)

# Run fastqc
is_dir = isdir('results/reads')
if is_dir == 1:
    subprocess.run(f'fastqc -t 8 results/reads/*.fastq -outdir=reports/fastqc/after_trimming',
                   shell=True, executable='/bin/bash')
else:
    subprocess.run(f'fastqc -t 8 reads/*.fastq.gz -outdir=reports/fastqc/before_trimming',
                   shell=True, executable='/bin/bash')
