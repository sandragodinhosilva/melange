---
layout: default
title: Setup
nav_order: 3
---

# Setup

MeLanGE is based on snakemake workflow manager, allowing to run all the steps of the workflow in parallel on a cluster. \
Apart from [conda](https://docs.conda.io/en/latest/), all databases and dependencies are installed **on the fly**.

## Conda package manager

MeLanGE has **one dependency**: [conda](https://docs.conda.io/en/latest/). \
You need to install [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or [miniconda](https://docs.conda.io/en/latest/miniconda.html). \
If you haven't done it already you need to configure conda with the bioconda-channel and the conda-forge channel. This are sources for packages beyond the default one:

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

## Install mamba
Conda can be a bit slow because there are so many packages. A good way around this is to use [mamba] (another snake).

    conda install mamba

From now on you can replace ``conda install`` with ``mamba install`` (check how much faster this snake is!)

## Install MeLanGE
To run MeLange, the only necessary step is to have git installed in your computer and clone MeLanGE repository.

For instructions on how to install git: [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Clone the repository:
    git clone https://github.com/sandragodinhosilva/MeLanGE.git

## Test correct installation with example data
To test MeLanGE correct installation, you can use [example data](https://github.com/sandragodinhosilva/MeLanGE/tree/master/example_data). This data is automatically downloaded once you clone MeLanGE repository. Just ensure the following setting in the config.yaml file:
    
    # --- Input
    inputdir: "example_data"

Test your configuration by performing a dry-run via:

    snakemake --use-conda -n





