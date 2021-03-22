---
layout: default
title: Index
nav_exclude: true
---

# MeLanGE - Read The Docs 

![Header](bitmap3.jpeg)


[![Snakemake](https://img.shields.io/badge/snakemake-≥5.31-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)


## Tool description
Machine learning is a field of artificial intelligence gaining popularity in all areas of knowledge, including modern research in biological sciences. However, its use in bacterial comparative genomics, specifically as an aid in microbiome studies, is still in its infancy. This is mainly due to the inexistence of easy-to-use tools that correspond to researchers’ needs. With the advent of high-throughput DNA sequencing technologies, the amount of genomic data available far outweighs the amount of data being thoroughly exploited. This can be partially explained by the difficulties in sorting and cross-comparing large amounts of data, which usually renders computationally intensive and oftentimes intractable. However, such large comparative genomics studies can be essential to delineate key genomic or functional traits of different groups of organisms based on phylogeny, taxonomy, ecosystem provenance, etc. In this context, MeLanGe (Machine Learning for Genomics) aims to facilitate large-scale comparative genomics studies by blending different annotation schemes and machine learning procedures to rapidly discern hallmark features between genome/metagenome groups in highly complex datasets. MeLanGe performs automatic, multi parallel genome annotations using diverse databases such as Pfam, COG, Kegg and CAZYmes, and returns these annotations in a tabular format that can be used in further studies. In addition, given user-input metadata, MeLanGe can perform a semi-automatic feature selection process that identifies which key functions better characterize each genome group. In a pilot study, from 6986 Pfam functions identified across 1256 marine and terrestrial bacterial genomes of the Flavobacteriaceae family, MeLanGe was able to reduce dataset complexity to as few as 81 traits that possess high correlation with organism origin, serving thus as indicators of environmental specialization. In conclusion, this tool can be an important player in the transition of microbiome studies to the “big data” era and provide an unprecedented opportunity to easily explore large groups of genomes. 

* * *

### Quick setup

#### Step 0: Install conda and Snakemake
[Conda](https://conda.io/docs/) and
[Snakemake](https://snakemake.readthedocs.io) are required to be able to use
MeLanGE. \
Most people would probably want to install
[Miniconda](https://conda.io/miniconda.html). \
After having conda installed, install [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html):

    # As described in Snakemake documentation:
    conda install -c conda-forge mamba
    mamba create -c conda-forge -c bioconda -n snakemake snakemake
    conda activate snakemake


#### Step 1: Clone workflow
To use MeLanGE, you need a local copy of the workflow repository. Start by
making a clone of the repository: 

    git clone https://github.com/sandragodinhosilva/MeLanGE.git

#### Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

#### Step 3: Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 

#### Examine workflow

    snakemake --dag  | dot -Tsvg > dag.svg

#### Step 4: Investigate results
After successful execution, you can create a self-contained interactive HTML report with all results via:

    snakemake --report report.html

* * *

#### Future implementations
- [ ] Also have unnotated orfs in file with results per genome
- [ ] Improve report


### Changes:

### Citing
