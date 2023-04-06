# Melange: A Snakemake workflow that streamlines structural and functional annotation of prokaryote genomes

![Header](logo/melangev2_small.png) 


[![Snakemake](https://img.shields.io/badge/snakemake-≥7.5.0-brightgreen.svg)](https://snakemake.bitbucket.io)
[![python](https://img.shields.io/badge/python-≥3.8-brightgreen.svg)](https://www.python.org/)
<!-- [![Actions Status](https://github.com/sandragodinhosilva/melange/workflows/tests.yml/badge.svg)](https://github.com/sandragodinhosilva/melange/actions) -->


Full documentation: https://sandragodinhosilva.github.io/melange/


## 1 Overview 

- Melange is a novel genomic annotation tool for large-scale comparative studies of prokaryote genomes or metagenomes with up to five different databases (Pfam, COG, KEGG, CAZyme, MEROPS).
- Melange can handle unassembled and assembled sequencing data and amino acid sequences, with automatic download and configuration of necessary tools and databases.
- As a [Snakemake](https://snakemake.readthedocs.io/en/stable/#) pipeline, Melange is highly scalable, reproducible and has a transparent workflow, and can be used to annotate one to thousands of genomes, producing several easy-to-analyze, tabular outputs.

<p align="center" width="100%">
    <img src="./docs/images/abstract.png" width="700" >
</p>

**Sinopse:** Melange - a versatile and user-friendly genome annotation tool that enables the simultaneous annotation of large genome datasets using multiple databases. Melange is designed to be continuously updated and its implementation in Snakemake allows flexibility and scalability. The unified output tables facilitate further analysis and are suitable for various comparative studies. It is publicly available and well-documented, making it easy to use and customize for a variety of annotation needs.


## 2 System requirements

Melange is designed to run on Linux systems and requires installation of Python (v≥3.8), Snakemake (v≥5.19.2) and Conda (v≥4.10.1). Optionally, git can also be installed for easy download of the repository. 

A test dataset (available in the "example_data" directory) is provided to allow for a test run to confirm the correct installation. 

Melange utilizes Snakemake for modularity and automatic parallelization of jobs, making it suitable for implementation on high-performance computational clusters. 


## 3 Customization

Melange is designed to be an easy-to-use and highly customizable  tool for the functional annotation of genomes. To accomplish this, only databases selected in the config.yml file are downloaded and configured locally, reducing storage requirements to run Melange. 


<p align="center" width="100%">
    <img src="./docs/images/workflow.png" title="Workflow" width="700" >
</p>

**Melange workflow** \
Melange allows the simultaneous functional annotation of prokaryote genomes or metagenomes with multiple annotation schemes. This figure illustrates all possible steps performed within Melange: 
- * [1) Input files](#1-input): unassembled fastq, nucleotide fasta or amino acid fasta files
- * [2) Genome annotation](#2-genome-annotation): annotation databases (and respective search algorithm used to query the proteins): [Pfam](#pfam), COG, KEGG, CAZymes or MEROPS
- * [3) Outputs](#3-outputs) 

### 1) Input
Melange accepts three types of input files: unassembled (meta)genomic data (.fastq), (meta)genome assemblies (.fna, .fasta, .ffn, .faa, .frn, .fa), and predicted amino acid sequences (.faa). The directory  and file types that Melange accepts  as input are defined in the config.yml file. If fastq files are inputted, Melange will convert them to fasta nucleotide files using the EMBOSS tool seqret before annotation [REF]. 

### 2) Genome annotation
Melange allows functional annotation of genomes with up to five databases: Pfam, COG, KEGG, CAZymes and MEROPS.  
The databases to be used can be selected by editing the "config.yml" file. This feature intends to enhance flexibility and reduce any unnecessary computational burden by only running the desired annotation procedures. 

#### 2.1) Gene calling and general annotation
When nucleotide files are submitted, Melange first performs a structural annotation step using [Prokka v1.14.5](https://github.com/tseemann/prokka) [1] with default settings. This gene calling step, performed by Prodigal v2.6 [REF], predicts ORFs, and outputs the corresponding translations into amino acid sequences in a fasta file. In addition to this output, which will be used in all subsequent steps, Prokka also generates other additional file formats, such as GenBank files, per genome. 

#### 2.2) Functional annotation
Functional annotation can be conducted with five databases: Pfam [2], COG [3], KEGG [4], CAZymes and Merops.

**Pfam**: For the annotation with Pfam identifiers, a local database is created using HMMER v3.3 from the latest version of Pfam-A.hmm downloaded from the [Pfam official website](http://pfam.xfam.org/). Then, a hmmscan search is performed on all input genomes and the best hit per ORF (cut-off: -E 1e-5) is selected. 

**COG
To perform the annotation regarding Clusters of Orthologous Genes (COG), the script [cdd2cog v0.2](https://github.com/aleimba/bac-genomics-scripts/tree/master/cdd2cog)  was adapted. In summary, query proteins are blasted with RPS-BLAST+ (Reverse Position-Specific BLAST) function, from the blast+ v2.9.0 suite, against COGs database, implemented within NCBI's Conserved Domain Database (CDD), and the best hit per ORF (cut-off: -E 1e-5) is selected. 

**KEGG
To obtain the KEGG Orthology (KO) for protein identification, the [prokka2KEGG script](https://github.com/SilentGene/Bio-py/tree/master/prokka2kegg) was adapted. Here, the UniProtKB IDs previously annotated by Prokka are converted into KO IDs using a cross-reference database provided by [UniProt](https://www.uniprot.org/). 

**CAZymes


**Merops


Summary of the most important characteristics of each database-specific workflow



### 3) Outputs
Melange outputs formatted tables of annotations per genome as final output. \
- Statistics.csv - % of Orfs annotated with each database.

- for each database: counts, presence/absence (PA) and relative abundance tables.

- Pfam_description.csv, Cog_description.csv, Kegg_description.csv - the mapping of the identified annotation with clans, names, descriptions, etc.

- folder Orf_per_genome: each genome has a unique file containing all orfs identified by Prokka and the subsequent annotations with the four different databases.

* * *


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


## Citing Melange
At the moment, Melange does not have a publication describing its features (we are working on it). Please use a link to Melange Github when referring to this tool.


### Melange Contributions
* Sandra Godinho Silva <sup>1,2</sup> - [MicroEcoEvo](https://www.facebook.com/MicroEcoEvo/) - [iBB, IST](https://ibb.tecnico.ulisboa.pt/).
* Tina Keller-Costa <sup>1,2</sup> - [MicroEcoEvo](https://www.facebook.com/MicroEcoEvo/) - [iBB, IST](https://ibb.tecnico.ulisboa.pt/).
* Ulisses Nunes da Rocha <sup>3</sup> - [Microbial Systems Data Science](https://www.ufz.de/index.php?de=43659) - [UFZ, Leipzig](https://www.ufz.de/).
* Rodrigo Costa <sup>1,2</sup> - [MicroEcoEvo](https://www.facebook.com/MicroEcoEvo/) - [iBB, IST](https://ibb.tecnico.ulisboa.pt/).

<sup>1</sup> Institute for Bioengineering and Biosciences, Department of Bioengineering, Instituto Superior Técnico da Universidade de Lisboa, Lisbon, Portugal \
<sup>2</sup> Associate Laboratory, Institute for Health and Bioeconomy, Instituto Superior Técnico, University of Lisbon, Lisbon, Portugal \
<sup>3</sup> Department of Environmental Microbiology, Helmholtz Centre for Environmental Research – UFZ, Leipzig, Germany 



<img src="./docs/images/ibb.png" alt="iBB" width="250">
<img src="./docs/images/ufz.png" width="250">
 

### Funding
<font size="2"> This work was supported by the Portuguese Foundation for Science and Technology (FCT) through the research project PTDC/MAR-BIO/1547/2014 and by ‘Direção-Geral de Política do Mar’, Ministry of the Sea through the “Fundo the Azul” funding program of  (grant number FA_05_2017_032). SGS is the recipient of a PhD scholarship conceded by FCT (PD/BD/143029/2018) and was supported by a FEMS-GO-2019-511 research and training grant conceded by the Federation of European Microbiological Societies (FEMS). Further support was provided from national funds through FCT in the scope of the projects UIDB/04565/2020 and UIDP/04565/2020 of the Research Unit Institute for Bioengineering and Biosciences - iBB and the project LA/P/0140/2020 of the Associate Laboratory Institute for Health and Bioeconomy - i4HB. UNR was funded by the Helmholtz Young Investigator grant VH-NG-1248 Micro “Big Data”. </font>

* * *

## References

* [1]	Seemann T. Prokka: rapid prokaryotic genome annotation. Bioinformatics. 2014;30(14):2068-9. 
* [2]	Galperin MY, Kristensen DM, Makarova KS, Wolf YI, Koonin EV. Microbial genome analysis: the COG approach. Brief Bioinform. 2019;20(4):1063-70. 
* [3]	Mistry J, Chuguransky S, Williams L, Qureshi M, Salazar GA, Sonnhammer ELL, et al. Pfam: The protein families database in 2021. Nucleic Acids Res. 2020. 
* [4]	Kanehisa M, Goto S. KEGG: kyoto encyclopedia of genes and genomes. Nucleic Acids Res. 2000;28(1):27-30.
