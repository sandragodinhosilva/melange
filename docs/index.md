---
layout: default
title: Home
nav_exclude: false
---

# MeLanGE - Documentation

[![Snakemake](https://img.shields.io/badge/snakemake-≥5.31-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)

![Header](bitmap3.jpeg)

MeLanGE is an automated pipeline for the genomic annotation of a group of genomes, followed by the detection of the most important features to distinguish a group of genomes, as determined by a metadata label.

MeLanGE has two independent, but connected, components:  
* [1) Genome annotation](#1-genome-annotation)
* [2) Feature selection](#2-feature-selection)  

MeLanGE is implemented in a [Snakemake](https://snakemake.readthedocs.io/en/stable/#) workflow, thus contributing to reproducible and scalable data analysis. 

* * *


## 1) Genome annotation
MeLanGE allows the quick annotation of a group 
of genomes with several databases and gives as final output formatted tables with 
the annotations per genome. \
To get more information about the third-parties databases and tools that MeLanGE uses, 
please check the respective links and references. 


### 1.1) Gene calling and general annotation
MeLanGE starts with gene calling performed with [Prokka v1.14.5](https://github.com/tseemann/prokka) [1]. Prokka provides several output files per genome, including .gbk and .faa files, which are made available and used in the following steps. 

### 1.2) Functional annotation
Functional annotation is conducted with three databases: Pfam [2], COG [3] and KEGG [4]. 
#### Pfam
For the annotation using Pfam identifiers, a local database using HMMER v3.3 is constructed from the latest Pfam-A.hmm release, downloaded from the [Pfam official website](http://pfam.xfam.org/). Then, a hmmscan search is performed on all input genomes and the best hit per ORF (cut-off: -E 1e-5) is selected. 

#### COG
To perform the annotation regarding Clusters of Orthologous Genes (COG), the [cdd2cog v0.2 script](https://github.com/aleimba/bac-genomics-scripts/tree/master/cdd2cog)  was adapted. In summary, query proteins are blasted with RPS-BLAST+ (Reverse Position-Specific BLAST) function, from the blast+ v2.9.0 suite, against COGs database, implemented within NCBI's Conserved Domain Database (CDD), and the best hit per ORF (cut-off: -E 1e-5) is selected. 

#### KEGG
To obtain the KEGG Orthology (KO) identification of the proteins, the [prokka2KEGG script](https://github.com/SilentGene/Bio-py/tree/master/prokka2kegg) was adapted. Here, previously annotated UniProtKB IDs by Prokka are converted into KO ids using a cross-reference database provided by [UniProt](https://www.uniprot.org/). 

### 1.3) Output files
- Statistics.csv - % of Orfs annotated with each database.

- for each database: counts, presence/absence (PA) and relative abundance tables.

- Pfam_description.csv, Cog_description.csv, Kegg_description.csv - the mapping of the identified annotation with clans, names, descriptions, etc.

- folder Orf_per_genome: each genome has a unique file containing all orfs identified by Prokka and the subsequent annotations with the four different databases.

* * *

## 2) Feature Selection

After the annotation step, MeLanGE offers the opportunity to identify the most important genome functions to distinguish genomes according to a category such as isolation source, environment characteristics, etc. Such mapping information should be mentioned in the medatata.csv file.

As a default, MeLanGE only performs the functional annotation pipeline. To also run the feature selection pipeline, substitute in `config.yml` for True to perform feature selection:

    # --- Run Feature Selection (True or False)
    FS: True
    

* * *

## Future implementations
- [ ] Improve report output.

* * *


## Citing MeLanGE
For now, MeLanGE does not have a publication describing its functionalities (we are working on it). Please use a link to MeLanGE Github when you reference this tool.


### MeLanGE Contributions
* Sandra Godinho Silva <sup>1,2</sup> - [MicroEcoEvo](https://www.facebook.com/MicroEcoEvo/) - [iBB, IST](https://ibb.tecnico.ulisboa.pt/).
* Masun Nabhan Homsi <sup>3</sup> - [UFZ, Leipzig](https://www.ufz.de/).
* Tina Keller-Costa <sup>1,2</sup> - [MicroEcoEvo](https://www.facebook.com/MicroEcoEvo/) - [iBB, IST](https://ibb.tecnico.ulisboa.pt/).
* Ulisses Nunes da Rocha <sup>3</sup> - [Microbial Systems Data Science](https://www.ufz.de/index.php?de=43659) - [UFZ, Leipzig](https://www.ufz.de/).
* Rodrigo Costa <sup>1,2</sup> - [MicroEcoEvo](https://www.facebook.com/MicroEcoEvo/) - [iBB, IST](https://ibb.tecnico.ulisboa.pt/).

<sup>1</sup> Institute for Bioengineering and Biosciences, Department of Bioengineering, Instituto Superior Técnico da Universidade de Lisboa, Lisbon, Portugal \
<sup>2</sup> Associate Laboratory, Institute for Health and Bioeconomy, Instituto Superior Técnico, University of Lisbon, Lisbon, Portugal \
<sup>3</sup> Department of Environmental Microbiology, Helmholtz Centre for Environmental Research – UFZ, Leipzig, Germany 

\
<img src="./images/IBB-Logo.png" width="175">  <img src="./images/IST.jpg" width="175">   

<img src="./images/ufz.png" width="250">
 

### Funding
<font size="2"> This work was supported by the Portuguese Foundation for Science and Technology (FCT) through the research project PTDC/MAR-BIO/1547/2014 and by ‘Direção-Geral de Política do Mar’, Ministry of the Sea through the “Fundo the Azul” funding program of  (grant number FA_05_2017_032). SGS is the recipient of a PhD scholarship conceded by FCT (PD/BD/143029/2018) and was supported by a FEMS-GO-2019-511 research and training grant conceded by the Federation of European Microbiological Societies (FEMS). Further support was provided from national funds through FCT in the scope of the projects UIDB/04565/2020 and UIDP/04565/2020 of the Research Unit Institute for Bioengineering and Biosciences - iBB and the project LA/P/0140/2020 of the Associate Laboratory Institute for Health and Bioeconomy - i4HB. UNR was funded by the Helmholtz Young Investigator grant VH-NG-1248 Micro “Big Data”. </font>

* * *

## References

* [1]	Seemann T. Prokka: rapid prokaryotic genome annotation. Bioinformatics. 2014;30(14):2068-9. 
* [2]	Galperin MY, Kristensen DM, Makarova KS, Wolf YI, Koonin EV. Microbial genome analysis: the COG approach. Brief Bioinform. 2019;20(4):1063-70. 
* [3]	Mistry J, Chuguransky S, Williams L, Qureshi M, Salazar GA, Sonnhammer ELL, et al. Pfam: The protein families database in 2021. Nucleic Acids Res. 2020. 
* [4]	Kanehisa M, Goto S. KEGG: kyoto encyclopedia of genes and genomes. Nucleic Acids Res. 2000;28(1):27-30.

