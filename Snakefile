# The main entry point of the workflow.
# After configuring, running snakemake -n in a clone of this repository should successfully execute a dry-run of the workflow.
# Run: 
#   snakemake --use-conda --cores 8 -j
# To create workflow view: 
#   snakemake --dag | dot -Tpdf > dag.pdf
# To view report: 
#   snakemake --report report/report.html

from pathlib import Path
import textwrap
from snakemake.utils import min_version
min_version("5.30.0")

report: "report/workflow.rst"

container: "docker://continuumio/miniconda3:4.4.10"

configfile: "config.yaml"

from rules.publications import publications
#citations = {publications["Snakemake"]}

# --- VARIABLES 
INPUTDIR = Path(config["inputdir"])
OUTDIR = Path(config["outdir"])
OUTDIR_ANNO = Path(config["outdir_anno"])
LOGDIR = Path(config["logdir"])
DBDIR = Path(config["dbdir"])
NUCLEOTIDE_EXTENSION = config["nucleotide_extension"]
AMINOACID_EXTENSION = config["aminoacid_extension"]


# --- GET GENOMES
if config["aminoacid_file"] == False:  #files need to go through Prokka first (gene calling)
    GENOMES = set(glob_wildcards(INPUTDIR/NUCLEOTIDE_EXTENSION).genome)
else:                              #files after gene calling (amino acid files)
    GENOMES = set(glob_wildcards(INPUTDIR/AMINOACID_EXTENSION).genome)

myoutput= [OUTDIR/"Annotation_results/Orfs_per_genome/{genome}_all_features.csv"]
extensions = []
databases_in_use = []

# --- SELECTION OF DATABASES TO USE
if config["PFAM"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_tblout_pfam.txt")
    extensions.append("_tblout_pfam.txt")
    databases_in_use.append("pfam")
if config["COG"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}protein-id_cog.txt")
    extensions.append("protein-id_cog.txt")
    databases_in_use.append("cog")
if config["KEGG"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_kegg2.txt")
    extensions.append("_kegg2.txt")
    databases_in_use.append("kegg")
if config["CAZYMES"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_cazymes_3tools.txt")
    extensions.append("_cazymes_3tools.txt")
    databases_in_use.append("cazymes")
if config["MEROPS"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_merops_out.txt")
    extensions.append("_merops_out.txt")
    databases_in_use.append("merops")

def setup(genome):
    l = [expand(myoutput,  genome=GENOMES),
    OUTDIR/"Annotation_results/Statistics.csv"]
    return l

# --- ALL RULE 
rule all:
    input: unpack(setup)

include: "rules/ensure_download.smk"
include: "rules/prokka.smk"
include: "rules/ensure_faa.smk"
include: "rules/pfam.smk"
include: "rules/cog.smk"
include: "rules/kegg2.smk"
include: "rules/merops.smk"
include: "rules/cazymes.smk"
include: "rules/ensure_all.smk"
include: "rules/join_all.smk"

onstart:
    print("Starting, files that will be annotated:")
    print(GENOMES)

onsuccess:
    print("Workflow finished, no error")

onerror:
    print("An error occurred")