---
layout: default
title: MeLanGE configuration
nav_order: 3
---

# MeLanGE configuration
To adapt MeLanGE to your needs, change the default parameters in the configuration file `config.yaml`:

## Input
    # --- Input
    inputdir: "data"
    genome_extension: "{genome}.fa" 

Change the input directory where your genome files are or simply paste them on the folder `data` inside MeLanGE repository.
Please make sure all genomes have the same extension (e.g. `.fa`, `.fna` or `.fasta`) and change this setting in the configuration file accordingly.

## Output
    # --- Output directory
    outdir: "results" 
    outdir_anno: "results/Annotation" 
    logdir: "logs"

## Expectation value threshold
    # --- Evalues:
    cog_evalue: "1e-5"
    pfam_evalue: "1e-5"

## Run Feature Selection
To run feature selection on the annotation results, change in configuration file `config.yaml`:

    # --- Run Feature Selection (True or False)
    FS: True

Upload the respective metadata file and change its path in the input section:

    # --- Input
    (...)
    metadata: "data/metadata.csv" 
