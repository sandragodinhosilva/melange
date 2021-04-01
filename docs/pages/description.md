---
layout: default
title: Tool description
nav_order: 1
---

# What is MeLanGE

MeLanGE is a automated pipeline for the genomic annotation of a group of genomes, followed by the th detection of the most important features to distinguish a group of genomes, as determined by a metadata label.  
MeLanGE has two independent, but connected, components: [1) Genome annotation](#1-genome-annotation) + [2) Feature selection](#2-feature-selection).  
MeLanGE is a [Snakemake](https://snakemake.readthedocs.io/en/stable/#) pipeline.

## 1 Genome annotation
MeLanGE allows the quick annotation of a group 
of genomes with several databases and gives as final output formatted tables with 
the annotations per genome. \
All the tools in use are from third-parties. To get more information about them, 
please check the links and references.

### 1.1 Third-parties databases and scripts:
##### Gene calling and general annotation
* [Prokka](https://github.com/tseemann/prokka)

##### Functional annotation 
* **Pfam** \
To annotate the genomes into Pfams, a local database is created.\
Lastest [Pfam-A.hmm](ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release)

* **COG** \
[cdd2cog](https://github.com/aleimba/bac-genomics-scripts/tree/master/cdd2cog)

* **Kegg** \
[prokka2kegg](https://github.com/SilentGene/Bio-py/tree/master/prokka2kegg)
Script that converts prokka annotation output into the respective KEGG IDs.

* **CAZymes** \
Tool [dbcan](https://github.com/linnabrown/run_dbcan)
Standalone version of dbcan.

* **MEROPS** \
A local database is created from [MEROPS](ftp://ftp.ebi.ac.uk/pub/databases/merops/current_release/merops_scan.lib).
Then a blastp against faa files is performed.

### 1.2 Output files:
- Statistics.csv - % of Orfs annotated with each database.

- for each database: counts, presence/absence (PA) and relative abundance tables.

- Pfam_description.csv, Cog_description.csv, Kegg_description.csv - the mapping of the identified annotation with clans, names, descriptions, etc.

- folder Orf_per_genome: each genome has a unique file containing all orfs identified by Prokka and the subsequent annotations with the four different databases.

## 2 Feature Selection
