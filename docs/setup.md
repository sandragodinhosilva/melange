---
layout: default
title: Installation
nav_order: 2
---

# Installation

MeLanGE is based on snakemake workflow manager, allowing to run all the steps of the workflow in parallel on a cluster. \
Apart from [conda](https://docs.conda.io/en/latest/), all databases and dependencies are installed **on the fly**.

## Step 0: Install conda, snakemake and ensure git
[Conda](https://conda.io/docs/) and
[Snakemake](https://snakemake.readthedocs.io) are required to be able to use
MeLanGE. \
Most people would probably want to install
[Miniconda](https://conda.io/miniconda.html). \

If you haven't done it already you need to configure conda with the bioconda-channel and the conda-forge channel. This are sources for packages beyond the default one:

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

### Install mamba
Conda can be a bit slow because there are so many packages. A good way around this is to use [mamba] (another snake).

    conda install mamba

From now on you can replace ``conda install`` with ``mamba install`` (check how much faster this snake is!)

### Install snakemake
After having manba installed, install [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html):

    mamba create -c conda-forge -c bioconda -n snakemake snakemake
    conda activate snakemake

### Install git
To run MeLange, the only necessary step is to have git installed in your computer and clone MeLanGE repository.

For instructions on how to install git: [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


## Step 1: Clone MeLanGE workflow
To use MeLanGE, you need a local copy of the workflow repository. Start by making a clone of the repository: 

    git clone https://github.com/sandragodinhosilva/MeLanGE.git

### Optional: test correct installation with example data
To test MeLanGE correct installation, you can use [example data](https://github.com/sandragodinhosilva/MeLanGE/tree/master/example_data). This data is automatically downloaded once you clone MeLanGE repository. Just ensure the following setting in the config.yaml file:
    
    # --- Input
    inputdir: "example_data"

Test your configuration by performing a dry-run via:

    snakemake --use-conda -n


## Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.


## Step 3: Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 


### Optional steps 
**Examine workflow:**

    snakemake --dag  | dot -Tsvg > dag.svg

**Investigate results:** 

After successful execution, you can create a self-contained interactive HTML report with all results via:

    snakemake --report report.html
