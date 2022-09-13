# The main entry point of the workflow.
# After configuring, running snakemake -n in a clone of this repository should successfully execute a dry-run of the workflow.
# Run: snakemake --use-conda --cores 8 -j
# to create workflow view: snakemake --dag | dot -Tpdf > dag.pdf
# snakemake --cores 10 --use-conda --edit-notebook results/Feature_selection.csv
# snakemake --report report/report.html

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
OUTDIR_ANNO = Path(config["outdir_anno"])
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

myoutput= [OUTDIR/"Annotation_results/Orfs_per_genome/{genome}_all_features.csv"]
extensions = []
databases_in_use = []

if config["PFAM"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_tblout_pfam.txt")
    extensions.append("_tblout_pfam.txt")
    databases_in_use.append("pfam")
if config["COG"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}protein-id_cog.txt")
    extensions.append("protein-id_cog.txt")
    databases_in_use.append("cog")
if config["KEGG"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}.ko.out")
    extensions.append(".ko.out")
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
    if config["FS"] == True:
        l = [expand(myoutput,  genome=GENOMES),
        OUTDIR/"Annotation_results/Statistics.csv",
        OUTDIR/"Feature_selection.csv"]
    else:
        l = [expand(myoutput,  genome=GENOMES),
        OUTDIR/"Annotation_results/Statistics.csv"]
    return l


# --- ALL RULE 
rule all:
    input: unpack(setup)

include: "rules/ensure_download.smk"
include: "rules/prokka.smk"
include: "rules/pfam.smk"
include: "rules/cog.smk"
include: "rules/kegg.smk"
include: "rules/merops.smk"
include: "rules/cazymes.smk"
include: "rules/ensure_all.smk"
include: "rules/join_all.smk"
include: "rules/feature_selection.smk"

onsuccess:
    print("Workflow finished, no error")

onerror:
    print("An error occurred")