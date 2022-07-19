import subprocess
from os import chdir, mkdir
from shutil import move

from console import dir_path
from settings import config

workspace = str(dir_path + '/workspace')
config.read(workspace + '/config.ini')
run = config['Run Settings']['run']
project_name = config['Project Settings']['project_name']
run_name = config['Run Settings']['run_name']

# Change into working directory
chdir(run)


def plot_kraken():
    # All biological domains
    subprocess.run(['qiime', 'tools', 'import',
                    '--input-path', f'{project_name}-{run_name}-kraken2-results.biom',
                    '--type', "'FeatureTable[Frequency]'",
                    '--input-format', 'BIOMV100Format',
                    '--output-path', f'{project_name}-{run_name}-kraken2-table.qza'])
    subprocess.run(['biom', 'convert',
                    '-i', f'{project_name}-{run_name}-kraken2-results.biom',
                    '-o', f'{project_name}-{run_name}-kraken2-hdf5-table.biom',
                    '--table-type', '"OTU table"',
                    '--to-hdf5'])
    subprocess.run(['qiime', 'tools', 'import',
                    '--input-path', f'{project_name}-{run_name}-kraken2-hdf5-table.biom',
                    '--type', "'FeatureData[Taxonomy]'",
                    '--input-format', 'BIOMV210Format',
                    '--output-path', f'{project_name}-{run_name}-kraken2-taxonomy.qza'])
    subprocess.run(['qiime', 'taxa', 'barplot',
                    '--i-table', f'{project_name}-{run_name}-kraken2-table.qza',
                    '--i-taxonomy', f'{project_name}-{run_name}-kraken2-taxonomy.qza',
                    '--m-metadata-file', f'',
                    '--o-visualization', f'{project_name}-{run_name}-kraken2-taxa-barplot.qzv'])
    # Filter for bacteria only
    subprocess.run(['qiime', 'taxa', 'filter-table',
                    '--i-table', f'{project_name}-{run_name}-kraken2-table.qza',
                    '--i-taxonomy', f'{project_name}-{run_name}-kraken2-taxonomy.qza',
                    '--p-include', 'k__bacteria',
                    '--o-filtered-table', f'{project_name}-{run_name}-kraken2-table-bacteria.qza'])
    subprocess.run(['qiime', 'taxa', 'barplot',
                    '--i-table', f'{project_name}-{run_name}-kraken2-table-bacteria.qza',
                    '--i-taxonomy', f'{project_name}-{run_name}-kraken2-taxonomy.qza',
                    '--m-metadata-file', f'',
                    '--o-visualization', f'{project_name}-{run_name}-kraken2-taxa-barplot-bacteria.qzv'])


def plot_bracken():
    # All biological domains
    subprocess.run(['qiime', 'tools', 'import',
                    '--input-path', f'{project_name}-{run_name}-bracken-results.biom',
                    '--type', "'FeatureTable[Frequency]'",
                    '--input-format', 'BIOMV100Format',
                    '--output-path', f'{project_name}-{run_name}-bracken-table.qza'])
    subprocess.run(['biom', 'convert',
                    '-i', f'{project_name}-{run_name}-bracken-results.biom',
                    '-o', f'{project_name}-{run_name}-bracken-hdf5-table.biom',
                    '--table-type', '"OTU table"',
                    '--to-hdf5'])
    subprocess.run(['qiime', 'tools', 'import',
                    '--input-path', f'{project_name}-{run_name}-bracken-hdf5-table.biom',
                    '--type', "'FeatureData[Taxonomy]'",
                    '--input-format', 'BIOMV210Format',
                    '--output-path', f'{project_name}-{run_name}-bracken-taxonomy.qza'])
    subprocess.run(['qiime', 'taxa', 'barplot',
                    '--i-table', f'{project_name}-{run_name}-bracken-table.qza',
                    '--i-taxonomy', f'{project_name}-{run_name}-bracken-taxonomy.qza',
                    '--m-metadata-file', f'',
                    '--o-visualization', f'{project_name}-{run_name}-bracken-taxa-barplot.qzv'])
    # Filter for bacteria only
    subprocess.run(['qiime', 'taxa', 'filter-table',
                    '--i-table', f'{project_name}-{run_name}-bracken-table.qza',
                    '--i-taxonomy', f'{project_name}-{run_name}-bracken-taxonomy.qza',
                    '--p-include', 'k__bacteria',
                    '--o-filtered-table', f'{project_name}-{run_name}-bracken-table-bacteria.qza'])
    subprocess.run(['qiime', 'taxa', 'barplot',
                    '--i-table', f'{project_name}-{run_name}-bracken-table-bacteria.qza',
                    '--i-taxonomy', f'{project_name}-{run_name}-bracken-taxonomy.qza',
                    '--m-metadata-file', f'',
                    '--o-visualization', f'{project_name}-{run_name}-bracken-taxa-barplot-bacteria.qzv'])


plot_kraken()
plot_bracken()

# Cleanup files
mkdir('results/qiime2')

move(f'{run}/{project_name}-{run_name}-kraken2-table.qza', 'results/qiime2')
move(f'{run}/{project_name}-{run_name}-kraken2-hdf5-table.biom', 'results/qiime2')
move(f'{run}/{project_name}-{run_name}-kraken2-taxonomy.qza', 'results/qiime2')
move(f'{run}/{project_name}-{run_name}-kraken2-table-bacteria.qza', 'results/qiime2')

move(f'{run}/{project_name}-{run_name}-bracken-table.qza', 'results/qiime2')
move(f'{run}/{project_name}-{run_name}-bracken-hdf5-table.biom', 'results/qiime2')
move(f'{run}/{project_name}-{run_name}-bracken-taxonomy.qza', 'results/qiime2')
move(f'{run}/{project_name}-{run_name}-bracken-table-bacteria.qza', 'results/qiime2')
