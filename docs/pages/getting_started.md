---
layout: default
title: Getting started
nav_order: 1
---

# Setup

MeLanGE is based on snakemake workflow manager, allowing to run all the steps of the workflow in parallel on a cluster. \
Apart from [conda](https://docs.conda.io/en/latest/), all databases and dependencies are installed **on the fly**.

## Conda package manager

MeLanGE has **one dependency**: [conda](https://docs.conda.io/en/latest/). \
You need to install [anaconda](http://anaconda.org/) or [miniconda](https://docs.conda.io/en/latest/miniconda.html). \
If you haven't done it already you need to configure conda with the bioconda-channel and the conda-forge channel. This are sources for packages beyond the default one:

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

## Install mamba
Conda can be a bit slow because there are so many packages. A good way around this is to use [mamba] (another snake).

    conda install mamba

From now on you can replace ``conda install`` with ``mamba install`` and see how much faster this snake is.

## Memory & system requirements:

To try MeLanGE, you can use [example data](https://github.com/sandragodinhosilva/MeLanGE/tree/master/example_data) for testing.

## Install MeLanGE

