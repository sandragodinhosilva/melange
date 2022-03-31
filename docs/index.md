---
layout: default
title: Home
nav_exclude: false
---

# MeLanGE - Documentation

[![Snakemake](https://img.shields.io/badge/snakemake-≥5.31-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)

![Header](bitmap3.jpeg)

MeLanGE is a automated pipeline for the genomic annotation of a group of genomes, followed by the detection of the most important features to distinguish a group of genomes, as determined by a metadata label.

MeLanGE has two independent, but connected, components:  
* **Genome annotation**
* **Feature selection**  

MeLanGE is implemented in a [Snakemake](https://snakemake.readthedocs.io/en/stable/#) workflow, thus contributing to reproducible and scalable data analysis. 

* * *


## 1) Genome annotation
MeLanGE allows the quick annotation of a group 
of genomes with several databases and gives as final output formatted tables with 
the annotations per genome. \
All the tools in use are from third-parties. To get more information about them, 
please check the links and references.

### 1.1) Third-parties databases and scripts:
**Gene calling and general annotation**

* [Prokka](https://github.com/tseemann/prokka)

**Functional annotation** 
* **Pfam** \
To annotate the genomes into Pfams, a local database is created.
Lastest [Pfam-A.hmm](ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release)

* **COG** \
[cdd2cog](https://github.com/aleimba/bac-genomics-scripts/tree/master/cdd2cog)

* **Kegg** \
[prokka2kegg](https://github.com/SilentGene/Bio-py/tree/master/prokka2kegg) - script that converts prokka annotation output into the respective KEGG IDs.

### 1.2) Output files
- Statistics.csv - % of Orfs annotated with each database.

- for each database: counts, presence/absence (PA) and relative abundance tables.

- Pfam_description.csv, Cog_description.csv, Kegg_description.csv - the mapping of the identified annotation with clans, names, descriptions, etc.

- folder Orf_per_genome: each genome has a unique file containing all orfs identified by Prokka and the subsequent annotations with the four different databases.

* * *

## 2) Feature Selection

After the annotation step, MeLanGE offers the opportunity to identify the most important genome functions to distinguish genomes according to a category such as isolation source, environment characteristics, etc. Such mapping information should be mentioned in the medatata.csv file.

As a default, MeLanGE only performs the functional annotation pipeline. To also run the feature selection pipeline, substitute in config.yml for True to perform feature selection:

    # --- Run Feature Selection (True or False)
    FS: True

* * *

## Future implementations
- [ ] Improve report output.

* * *

## Citing
For now MeLanGE does not have a publication describing its functionalities (we are working on it). Please use a link to MeLanGE github when you reference this tool.

### Contributions
Sandra Godinho Silva (1,2), Masun Nabhan Homsi (3), Tina Keller-Costa (1,2), Ulisses Nunes da Rocha (3) and Rodrigo Costa (1,2)

(1) Institute for Bioengineering and Biosciences, Department of Bioengineering, Instituto Superior Técnico da Universidade de Lisboa, Lisbon, Portugal \
(2) Associate Laboratory, Institute for Health and Bioeconomy, Instituto Superior Técnico, University of Lisbon, Lisbon, Portugal \
(3) Department of Environmental Microbiology, Helmholtz Centre for Environmental Research – UFZ, Leipzig, Germany 

![iBB](/docs/images/IBB-Logo.png)

### Funding
This work was supported by the Portuguese Foundation for Science and Technology (FCT) through the research project PTDC/MAR-BIO/1547/2014 and by ‘Direção-Geral de Política do Mar’, Ministry of the Sea through the “Fundo the Azul” funding program of  (grant number FA_05_2017_032). SGS is the recipient of a PhD scholarship conceded by FCT (PD/BD/143029/2018) and was supported by a FEMS-GO-2019-511 research and training grant conceded by the Federation of European Microbiological Societies (FEMS). Further support was provided from national funds through FCT in the scope of the projects UIDB/04565/2020 and UIDP/04565/2020 of the Research Unit Institute for Bioengineering and Biosciences - iBB and the project LA/P/0140/2020 of the Associate Laboratory Institute for Health and Bioeconomy - i4HB. UNR was funded by the Helmholtz Young Investigator grant VH-NG-1248 Micro “Big Data”.
