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


# --- VARIABLES
INPUTDIR = Path(config["inputdir"])
OUTDIR = Path(config["outdir"])
OUTDIR_ANNO = Path(config["outdir_anno"])
LOGDIR = Path(config["logdir"])
NUCLEOTIDE_EXTENSION = config["nucleotide_extension"]
AMINOACID_EXTENSION = config["aminoacid_extension"]


if (
    config["aminoacid_file"] == False
):  # files need to go through Prokka first (gene calling)
    GENOMES = set(glob_wildcards(INPUTDIR / NUCLEOTIDE_EXTENSION).genome)
else:  # files after gene calling (amino acid files)
    GENOMES = set(glob_wildcards(INPUTDIR / AMINOACID_EXTENSION).genome)


def setup(genome):
    l = [expand(myoutput, genome=GENOMES), OUTDIR / "Annotation_results/Statistics.csv"]
    return l


# --- ALL RULE
rule all:
    input:
        unpack(setup),


include: "rules/common.smk"
include: "rules/ensure_download.smk"
include: "rules/ensure_faa.smk"
include: "rules/prokka.smk"
include: "rules/pfam.smk"
include: "rules/cog.smk"
include: "rules/kegg.smk"
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
