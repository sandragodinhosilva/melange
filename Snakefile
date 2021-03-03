# The main entry point of the workflow.
# After configuring, running snakemake -n in a clone of this repository should successfully execute a dry-run of the workflow.
# Run: snakemake --use-conda --cores 8 -j

from pathlib import Path
import textwrap

from snakemake.utils import min_version
min_version("5.30.0")

onstart:
    print("Starting")

report: "report/workflow.rst"

container: "docker://continuumio/miniconda3:4.4.10"

configfile: "config.yaml"

from rules.publications import publications
#citations = {publications["Snakemake"]}

# --- VARIABLES 
INPUTDIR = Path(config["inputdir"])
OUTDIR = Path(config["outdir"])
LOGDIR = Path(config["logdir"])
DBDIR = Path(config["dbdir"])
GENOME_EXTENSION = config["genome_extension"]
METADATA = config["metadata"]

# --- GET GENOMES
GENOMES = set(glob_wildcards(INPUTDIR/GENOME_EXTENSION).genome)

#if len(GENOMES) < 1:
#    raise WorkflowError("Found no samples! Check input file pattern and path in config.yaml")
#else:
#    print(f"Found the following samples in inputdir using input filename pattern '{config['genome_extension']}':\n{GENOMES}")

# --- ALL RULE 
rule all:
    input:
       expand([OUTDIR/"Annotation_results/Orfs_per_genome/{genome}_all_features.csv"],  genome=GENOMES), 
       OUTDIR/"Annotation_results/Pfam_PA_metadata.csv",
       #DBDIR/"dbs_done.txt"

include: "rules/ensure_download.smk"
include: "rules/prokka.smk"
include: "rules/pfam.smk"
include: "rules/cog.smk"
include: "rules/cazymes.smk"
include: "rules/kegg.smk"
include: "rules/merops.smk"
include: "rules/ensure_all.smk"
include: "rules/join_all.smk"
include: "rules/join_metadata.smk"

onsuccess:
    print("Workflow finished, no error")

onerror:
    print("An error occurred")