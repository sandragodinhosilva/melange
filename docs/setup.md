---
layout: default
title: Installation
nav_order: 2
---

# Installation & Execution

MeLanGE is designed as a [Snakemake](https://snakemake.readthedocs.io) workflow, allowing to run all the steps in parallel on a cluster. 


## Step 0: MeLanGE dependencies
To run MeLanGE you need to have installed [conda](https://docs.conda.io/en/latest/) (or the lightest version - miniconda), snakemake and git.

### Install conda 

To install conda, follow the instructions in conda documentation: [Conda](https://conda.io/docs/).
Most people would probably want to install [Miniconda](https://conda.io/miniconda.html). 

If you haven't done it already you need to configure conda with the bioconda-channel and the conda-forge channel. This are sources for packages beyond the default one:

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

### Install mamba (optional)
Conda can be a bit slow because there are so many packages. A good way around this is to use [mamba] (another snake).

    conda install mamba

From now on you can replace ``conda install`` with ``mamba install`` (check how much faster this snake is!)

### Install snakemake
After having conda (and mamba installed), install [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html):

    mamba create -c conda-forge -c bioconda -n snakemake snakemake
    conda activate snakemake

### Install git
To run MeLange, you need to have git installed to clone the MeLanGE repository.

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

For more information on how to costumize this configuration file, see section [MeLanGE Configuration](https://sandragodinhosilva.github.io/MeLanGE/configuration.html)



## Step 3: Execute workflow

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 

### Optional steps 
**Examine workflow:**

Snakemake has some cool features which are implemented in MeLanGE. One of them is the possibility of automatically creating directed acyclic graph (DAG) of jobs that allows the visualization of the whole workflow.

By running a single command:

    snakemake --dag  | dot -Tsvg > dag.svg

A DAG (saved as a .svg figure) is created. It contains a node for each job with the edges connecting them representing the dependencies. The frames of jobs that don’t need to be run (because their output is up-to-date) are dashed. 

Example:
![dag](https://github.com/sandragodinhosilva/MeLanGE/blob/master/docs/dag.png)

**Investigate results:**

After successful execution, you can create a self-contained interactive HTML report with all results via:

    snakemake --report report.html
