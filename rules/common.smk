# --- VARIABLES
INPUTDIR = Path(config["inputdir"])
OUTDIR = Path(config["outdir"])
OUTDIR_ANNO = Path(config["outdir_anno"])
LOGDIR = Path(config["logdir"])
DBDIR = Path(config["dbdir"])
NUCLEOTIDE_EXTENSION = config["nucleotide_extension"]
AMINOACID_EXTENSION = config["aminoacid_extension"]


# --- GET GENOMES
if (
    config["aminoacid_file"] == False
):  # files need to go through Prokka first (gene calling)
    GENOMES = set(glob_wildcards(INPUTDIR / NUCLEOTIDE_EXTENSION).genome)
else:  # files after gene calling (amino acid files)
    GENOMES = set(glob_wildcards(INPUTDIR / AMINOACID_EXTENSION).genome)


myoutput = [OUTDIR / "Annotation_results/Orfs_per_genome/{genome}_all_features.csv"]
extensions = []
databases_in_use = []


def setup(genome):
    l = [expand(myoutput, genome=GENOMES), OUTDIR / "Annotation_results/Statistics.csv"]
    return l

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




