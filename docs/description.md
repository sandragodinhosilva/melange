---
layout: default
title: MeLanGE description
nav_order: 1
---

# MeLanGE context

## The problem
Machine learning is a field of artificial intelligence gaining popularity in all areas of knowledge, including modern research in biological sciences. However, its use in bacterial comparative genomics, specifically as an aid in microbiome studies, is still in its infancy. This is mainly due to the inexistence of easy-to-use tools that correspond to researchers’ needs. **With the advent of high-throughput DNA sequencing technologies, the amount of genomic data available far outweighs the amount of data being thoroughly exploited.** This can be partially explained by the difficulties in sorting and cross-comparing large amounts of data, which usually renders computationally intensive and oftentimes intractable. However, such large comparative genomics studies can be essential to delineate key genomic or functional traits of different groups of organisms based on phylogeny, taxonomy, ecosystem provenance, etc. 

## Our solution
**MeLanGe** (**Machine Learning for Genomics**) aims to facilitate large-scale comparative genomics studies by blending different annotation schemes and machine learning procedures to rapidly discern hallmark features between genome/metagenome groups in highly complex datasets. MeLanGe performs automatic, multi parallel genome annotations using diverse databases such as Pfam, COG, Kegg and CAZYmes, and returns these annotations in a tabular format that can be used in further studies. In addition, given user-input metadata, MeLanGe can perform a semi-automatic feature selection process that identifies which key functions better characterize each genome group. 

## Performance
In a pilot study, from 6986 Pfam functions identified across 1256 marine and terrestrial bacterial genomes of the Flavobacteriaceae family, MeLanGe was able to reduce dataset complexity to as few as 81 traits that possess high correlation with organism origin, serving thus as indicators of environmental specialization. In conclusion, this tool can be an important player in the transition of microbiome studies to the “big data” era and provide an unprecedented opportunity to easily explore large groups of genomes. 


## 1 Genome annotation
MeLanGE allows the quick annotation of a group 
of genomes with several databases and gives as final output formatted tables with 
the annotations per genome. \
All the tools in use are from third-parties. To get more information about them, 
please check the links and references.

## 1.1 Third-parties databases and scripts:
**Gene calling and general annotation**

* [Prokka](https://github.com/tseemann/prokka)

**Functional annotation** 
* **Pfam** \
To annotate the genomes into Pfams, a local database is created.

Lastest [Pfam-A.hmm](ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release)

* **COG** \
[cdd2cog](https://github.com/aleimba/bac-genomics-scripts/tree/master/cdd2cog)

* **Kegg** \
[prokka2kegg](https://github.com/SilentGene/Bio-py/tree/master/prokka2kegg) - script that converts prokka annotation output into the respective KEGG IDs.

### 1.2 Output files:
- Statistics.csv - % of Orfs annotated with each database.

- for each database: counts, presence/absence (PA) and relative abundance tables.

- Pfam_description.csv, Cog_description.csv, Kegg_description.csv - the mapping of the identified annotation with clans, names, descriptions, etc.

- folder Orf_per_genome: each genome has a unique file containing all orfs identified by Prokka and the subsequent annotations with the four different databases.

## 2 Feature Selection
