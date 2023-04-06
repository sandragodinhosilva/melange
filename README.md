# Melange: A Snakemake workflow that streamlines structural and functional annotation of prokaryote genomes

![Header](logo/melangev2_small.png) 


[![Snakemake](https://img.shields.io/badge/snakemake-≥7.5.0-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)
<!-- [![Actions Status](https://github.com/sandragodinhosilva/melange/workflows/tests.yml/badge.svg)](https://github.com/sandragodinhosilva/melange/actions) -->


Full documentation: https://sandragodinhosilva.github.io/melange/


## 1 Overview 

- Melange is a novel genomic annotation tool for large-scale comparative studies of prokaryote genomes or metagenomes with up to five different databases (Pfam, COG, KEGG, CAZyme, MEROPS).
- Melange can handle unassembled and assembled sequencing data and amino acid sequences, with automatic download and configuration of necessary tools and databases.
- As a Snakemake pipeline, Melange is highly scalable, reproducible and has a transparent workflow, and can be used to annotate one to thousands of genomes, producing several easy-to-analyze, tabular outputs.


<img src="https://github.com/sandragodinhosilva/melange/tree/master/docs/images/abstract.png" width="100">

**Sinopse:** Melange - a versatile and user-friendly genome annotation tool that enables the simultaneous annotation of large genome datasets using multiple databases. Melange is designed to be continuously updated and its implementation in Snakemake allows flexibility and scalability. The unified output tables facilitate further analysis and are suitable for various comparative studies. It is publicly available and well-documented, making it easy to use and customize for a variety of annotation needs.

## 2 System requirements

Melange is designed to run on Linux systems and requires installation of Python (v≥3.8), Snakemake (v≥5.19.2) and Conda (v≥4.10.1). Optionally, git can also be installed for easy download of the repository. 

A test dataset (available in the "example_data" directory) is provid to allow for a test run to confirm the correct installation. 

Melange utilizes Snakemake for modularity and automatic parallelization of jobs, making it suitable for implementation on high-performance computational clusters. 


## 3 Customization

Melange is designed to be an easy-to-use and highly customizable  tool for the functional annotation of genomes. To accomplish this, only databases selected in the config.yml file are downloaded and configured locally, reducing storage requirements to run Melange. 

![Workflow](docs/images/workflow.png) 
**Melange workflow** \
Melange allows the simultaneous functional annotation of prokaryote genomes or metagenomes with multiple annotation schemes, including Pfam, COG, KEGG Orthology, CAZymes, and MEROPS. This figure illustrates all steps performed within Melange: the three possible data inputs (unassembled fastq, nucleotide fasta or amino acid fasta files), the annotation databases (Pfam, COG, KEGG, CAZymes or MEROPS) and the outputs provided after a successful Melange run. The respective search algorithm used to query the proteins is shown next to each database. 



## 4 Usage
This is a simple description on how to use melange. For more details, please see [Melange documentation](https://sandragodinhosilva.github.io/melange/).

### Step 0: Install conda and Snakemake
[Conda](https://conda.io/docs/) and
[Snakemake](https://snakemake.readthedocs.io) are required to be able to use
Melange. \
Conda is easy to install via its lightweight version 
[Miniconda](https://conda.io/miniconda.html). \
After installing Conda, install [Snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html):

    # As described in Snakemake documentation:
    conda install -c conda-forge mamba
    mamba create -c conda-forge -c bioconda -n snakemake snakemake
    conda activate snakemake


### Step 1: Clone workflow
To use Melange, you need a local copy of the workflow repository. Start by
creating a clone of the repository: 

    git clone https://github.com/sandragodinhosilva/melange.git

### Step 2: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

Here you can select which **databases** (Pfam, COG, Kegg, CAZymes and/or Merops) are to be used.

You can also define if input files are either fasta nucleotide files (e.g. fna, fa) or fasta aminoacid files.

More information about configuration settings can be found at: [config/README.md](https://github.com/sandragodinhosilva/melange/tree/master/config)

### Step 3: Execute workflow
Execute the workflow locally with `N` cores:

    snakemake --use-conda --cores N
    
Execution on a cluster, example:

    snakemake --use-conda --cluster qsub --jobs 8
    
For more information about running on a computational cluster, please check snakemake documentation about it: [https://snakemake.readthedocs.io/en/stable/executing/cluster.html](https://snakemake.readthedocs.io/en/stable/executing/cluster.html)
