# --- VARIABLES
INPUTDIR = Path(config["inputdir"])
OUTDIR = Path(config["outdir"])
OUTDIR_ANNO = Path(config["outdir_anno"])
NUCLEOTIDE_EXTENSION = config["nucleotide_extension"]
AMINOACID_EXTENSION = config["aminoacid_extension"]
FASTQ_EXTENSION = config["fastq_extension"]

if (
    config["file_type"] == "aminoacid"
):  # files need to go through Prokka first (gene calling)
    GENOMES = set(glob_wildcards(INPUTDIR / NUCLEOTIDE_EXTENSION).genome)
elif(
    config["file_type"] == "nucleotide"
):  # files after gene calling (amino acid files)
    GENOMES = set(glob_wildcards(INPUTDIR / AMINOACID_EXTENSION).genome)
elif(
    config["file_type"] == "fastq"
):  # files need to go through Prokka first (gene calling)
    GENOMES = set(glob_wildcards(INPUTDIR / FASTQ_EXTENSION).genome)


def setup(genome):
    l = [expand(myoutput, genome=GENOMES), OUTDIR / "Annotation_results/Statistics.csv"]
    return l


myoutput = [OUTDIR / "Annotation_results/Orfs_per_genome/{genome}_all_features.csv"]
extensions = []
databases_in_use = []


# --- SELECTION OF DATABASES TO USE
if config["PFAM"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_pfam_out.txt")
    extensions.append("_pfam_out.txt")
    databases_in_use.append("pfam")
if config["COG"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}protein-id_cog.txt")
    extensions.append("protein-id_cog.txt")
    databases_in_use.append("cog")
if config["KEGG"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_kegg.txt")
    extensions.append("_kegg.txt")
    databases_in_use.append("kegg")
if config["CAZYMES"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_cazymes_3tools.txt")
    extensions.append("_cazymes_3tools.txt")
    databases_in_use.append("cazymes")
if config["MEROPS"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_merops_out.txt")
    extensions.append("_merops_out.txt")
    databases_in_use.append("merops")

myoutput = []

if config["PFAM"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_pfam_out.txt")
if config["COG"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}protein-id_cog.txt")
if config["KEGG"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_kegg.txt")
if config["CAZYMES"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_cazymes_3tools.txt")
if config["MEROPS"] == True:
    myoutput.append(OUTDIR_ANNO / "{genome}_merops_out.txt")
