import subprocess
from os import chdir, makedirs
from os.path import isdir

from console import dir_path, logger
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run = config['Run Settings']['run']

# Change into working directory
chdir(run)

# Check if output folders exist
is_dir = isdir('reports/multiqc/before_trimming')
if is_dir == 1:
    logger.warning('Skipping quality control (multiqc) for raw sequence read(s)...')
    exit()
else:
    makedirs('reports/multiqc/before_trimming')

# Run multiqc
subprocess.run(['multiqc', 'reports/fastqc/before_trimming', '--outdir=reports/multiqc/before_trimming'])
