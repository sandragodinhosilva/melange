---
layout: default
title: Melange configuration
nav_order: 3
---

# Melange configuration
To adapt Melange to your needs, change the default parameters in the configuration file `config.yaml`:

## Input
    # --- Input
    inputdir: "data"
    genome_extension: "{genome}.fa" 

Change the input directory where your genome files are located, or simply add them to the 'data' folder in the Melange repository.
Make sure that all genomes have the same extension (e.g. `.fa`, `.fna` or `.fasta`) and change this setting in the configuration file accordingly.

## Output
    # --- Output directory
    outdir: "results" 
    outdir_anno: "results/Annotation" 

## Expectation value threshold
    # --- Evalues:
    cog_evalue: "1e-5"
    pfam_evalue: "1e-5"
