# FAW-snakemake

[![Snakemake](https://img.shields.io/badge/snakemake-≥5.32-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)


This repo contains the code for a Snakemake workflow of the FAW tool


## Usage

### Step 0: Install conda and Snakemake
[Conda](https://conda.io/docs/) and
[Snakemake](https://snakemake.readthedocs.io) are required to be able to use
FAW. Most people would probably want to install
[Miniconda](https://conda.io/miniconda.html) and install Snakemake into their
base environment. Conda will automatically install the required versions of 
all tools required to run FAW.

### Step 1: Clone workflow
To use FAW, you need a local copy of the workflow repository. Start by
making a clone of the repository: 

    git clone git@github.com:sandragodinhosilva/FAW-snakemake

### Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

### Step 3: Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 

## Citing


