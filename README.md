![Header](logo/bitmap3.jpeg) 


[![Snakemake](https://img.shields.io/badge/snakemake-≥5.31-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)


This repository contains the code for the Snakemake workflow of a functional annotation tool.

## Documentation: https://sandragodinhosilva.github.io/MeLanGE/


## Usage

### Step 0: Install conda and Snakemake
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


### Step 1: Clone workflow
To use MeLanGE, you need a local copy of the workflow repository. Start by
making a clone of the repository: 

    git clone https://github.com/sandragodinhosilva/MeLanGE.git

### Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

Here you can select wich databases to use [Pfam, COG, Kegg, CAZymes and/or Merops] and if Feature Selection will be performed in the end.

### Step 3: Execute workflow
Execute the workflow locally using `N` cores:

    snakemake --use-conda --cores N
