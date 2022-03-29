---
layout: default
title: Quick setup
nav_order: 3
---

# Quick setup

## Step 0: Install conda, snakemake and ensure git
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

## Step 1: Clone workflow
To use MeLanGE, you need a local copy of the workflow repository. Start by
making a clone of the repository: 

    git clone https://github.com/sandragodinhosilva/MeLanGE.git

## Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

## Step 3: Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 

## Optional steps 
**Examine workflow:**

    snakemake --dag  | dot -Tsvg > dag.svg

**Investigate results:** 

After successful execution, you can create a self-contained interactive HTML report with all results via:

    snakemake --report report.html

* * *

