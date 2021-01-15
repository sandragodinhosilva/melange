# FAW-snakemake

[![Snakemake](https://img.shields.io/badge/snakemake-≥4.8.1-brightgreen.svg)](https://snakemake.bitbucket.io)


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

    git clone git@github.com:ctmrbio/stag-mwc

If you use StaG-mwc in a publication, please credit the authors by citing
either the URL of this repository or the project's DOI. Also, don't forget to
cite the publications of the other tools used in your workflow.

### Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`. The most common changes include setting the paths to input and
output folders, and configuring what steps of the workflow should be included
when running the workflow.

### Step 3: Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. It is also possible to run
it in a Slurm-managed cluster environment, e.g. on UPPMAX Rackham:


## Testing
A very basic continuous integration test is currently in place. It merely
validates the syntax by trying to let Snakemake build the dependency graph if
all outputs are activated.

## Contributing
Refer to the contributing guidelines in `CONTRIBUTING.md` for instructions on
how to contribute to FAW.

If you intend to modify or further develop this workflow, you are welcome to
fork this reposity. Please consider sharing potential improvements via a pull
request.

## Citing


