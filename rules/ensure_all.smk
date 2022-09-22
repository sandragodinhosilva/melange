myoutput= []

if config["PFAM"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_pfam_out.txt")
if config["COG"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}protein-id_cog.txt")
if config["KEGG"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_kegg.txt")
if config["CAZYMES"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_cazymes_3tools.txt")
if config["MEROPS"] == True:
    myoutput.append(OUTDIR_ANNO/"{genome}_merops_out.txt")


rule ensure_all:
    input: myoutput
    output: OUTDIR_ANNO/"{genome}_done.txt"
    log: LOGDIR/"all/{genome}.log"
    shell: "echo done > {output}"