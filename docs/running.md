---
layout: default
title: Running MeLanGE
nav_order: 3
---

# How to run MeLanGE
## Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

## Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 

#### Optional: 
#### Examine workflow

    snakemake --dag  | dot -Tsvg > dag.svg

##### Investigate results
After successful execution, you can create a self-contained interactive HTML report with all results via:

    snakemake --report report.html