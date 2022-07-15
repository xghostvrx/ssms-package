import subprocess
from os import chdir
from os.path import isdir

from console import dir_path
from settings import config

# Retrieve configuration variable(s)
workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run = config['Run Settings']['run']

# Change into working directory
chdir(run)

# Run multiqc
is_dir = isdir('reports/fastqc/after_trimming')
if is_dir == 1:
    subprocess.run(['multiqc', 'reports/fastqc/after_trimming', '--outdir=reports/multiqc/after_trimming'])
else:
    subprocess.run(['multiqc', 'reports/fastqc/before_trimming', '--outdir=reports/multiqc/before_trimming'])
