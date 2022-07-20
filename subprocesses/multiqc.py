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
run = config['Run Settings']['run']

# Change into working directory
chdir(run)

# Run multiqc
is_dir = isdir('reports/fastqc/after_trimming')
if is_dir == 1:
    subprocess.run(['multiqc', 'reports/fastqc/after_trimming', '--outdir=reports/multiqc/after_trimming'])
else:
    subprocess.run(['multiqc', 'reports/fastqc/before_trimming', '--outdir=reports/multiqc/before_trimming'])
