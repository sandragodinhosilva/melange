---
layout: default
title: Running MeLanGE
nav_order: 4
---

# Running MeLanGE
## Step 1: Configure workflow
Configure the workflow according to your needs by editing the file
`config.yaml`.

## Step 2: Execute workflow
Test your configuration by performing a dry-run via

    snakemake --use-conda -n

Execute the workflow locally via

    snakemake --use-conda --cores N

This will run the workflow locally using `N` cores. 

## Step 3: Verify workflow & results 

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