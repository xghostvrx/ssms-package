# SSMS Package (simplified metagenomic workflow)

Custom workflow(s) built in collaboration with the [Pathogen & Microbiome Institute (PMI)](https://in.nau.edu/pmi/) and
others.

> A prospective bioinformatics project lead by [George Testo](https://github.com/metro1102); started as a part of
> the [2021 Helios Program](https://www.tgen.org/education/helios-scholars-at-tgen/).

![Imgur](https://i.imgur.com/DNQ0idS.png)

## Project Information

Next-generation sequencing (NGS) has become a powerful tool for human microbiome research. We can now isolate bacterial
DNA from clinical microbiome samples utilizing streamlined approaches for obtaining sequence reads from high-throughput
sequencing platforms. These platforms include [Illumina](https://www.illumina.com)
, [Ion torrent](https://www.thermofisher.com/us/en/home/brands/ion-torrent.html),
and [PacBio](https://www.pacb.com/smrt-science/smrt-sequencing/). With NGS technology constantly evolving, translational
clinical research is becoming easier to perform [(Beigh, 2016)](https://dx.doi.org/10.3390%2Fmedicines3020014).
Molecular biologists can focus more on their research, rather than bioinformatic software.

However, there is only one problem. NGS technologies such as shallow shotgun metagenomic sequencing (SSMS) requires
molecular biologists to understand the tools that they are using to perform highly complex analyses. This can become a
significant issue when scientific consistency and reproducibility is a
concern [(Sandve et al., 2013)](https://doi.org/10.1371/journal.pcbi.1003285). Many bioinformatic tools designate their
own commands, making it difficult to learn and perform diverse analyses on targeted-gene, shotgun metagenome, and other
types of sequence reads.

To address this issue, we propose the use of a customizable workflow that can reduce the time it takes to process and
analyze sequence reads. SSMS processing of clinical samples can take hours of tedious commandline entry and frustration
to produce results, whereas established targeted-gene sequencing workflows seem to be more efficient. For example, the
bioinformatics platform known as [QIIME2](https://qiime2.org) can seemlessly perform analyses without
error [(Bolyen et al., 2019)](https://doi.org/10.1038/s41587-019-0209-9). There is currently no easy way to perform SSMS
processing, other than using [bioBakery](https://github.com/biobakery/biobakery), [Galaxy](https://galaxyproject.org),
and or [CyVerse](https://cyverse.org). If seemless results is a desire, then an effective solution will be necessary.

Because SSMS provides more insight on bacterial communities than amplicon-based sequencing approaches, an easy to use,
customizable SSMS workflow can benefit overwhelmed microbiome
researchers [(Brumfield et al., 2020)](https://doi.org/10.1371/journal.pone.0228899). This is where the SSMS Package
shines. This project intends to simplify SSMS processing by automating reduntant tasks such as inputting sequence read
names into commands and generating results. Notable integrations
include: [kneaddata](https://github.com/biobakery/kneaddata), [kraken2](https://github.com/DerrickWood/kraken2)
, [metaphlan](https://github.com/biobakery/MetaPhlAn), [bracken](https://github.com/jenniferlu717/Bracken)
, [krona](https://github.com/marbl/Krona/wiki), and [biom](https://github.com/biocore/biom-format). We are currently
exploring the possibility of communicating with API accessible platforms such as [QIIME2](https://qiime2.org) via an
open-source plugin.

This project is primarily built using Python and Docker images for each integration mentioned above.

## Project Contributions

Before contributing, please consider reading the following guidelines. We would like to highlight the importance of git
workflow eitquette. For example, commit messages should be consistent with whatever is being added, removed, or changed.
Please consider opening a pull request if you would like to suggest a feature or contribute to this project. Pull
request(s) will be approved in a timely manner. :)

- Make sure to report bugs that may significantly affect research.
- Open a pull request with your changes, following these guidelines.
- Follow these guidelines and your pull request(s) shall be accepted.

## License(s)

GNU General Public License v3.0

## Citation(s)

If you plan on using SSMS Package for future publications, please include the following citation:
> Testo, G. (2022). SSMS Package (simplified metagenomic workflow) [Python]. The Pathogen & Microbiome
> Institute. https://github.com/metro1102/ssms-package
