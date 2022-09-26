LOGDIR = Path(config["logdir"])


localrules:
    download_pfam,
    download_cog,
    download_cazymes,
    download_merops,
    download_kegg,


rule ensure_download:
    """Verify if all databases were downloaded."""
    input:
        "workflow/databases/Pfam-A.hmm",
        "workflow/databases/whog",
        "workflow/databases/EscheriaColiK12MG1655.gff",
        "workflow/databases/merops_scan.lib",
        "workflow/databases/ko_list",
    output:
        "workflow/databases/dbs_done.txt",
    log:
        LOGDIR / "dbs.log",
    shell:
        "echo done > {output}"


rule download_pfam:
    """Download latest Pfam-A.hmm."""
    output:
        "workflow/databases/Pfam-A.hmm",
    log:
        str(LOGDIR / "downloads/pfam_database_download.log"),
    shadow:
        "shallow"
    conda:
        "../envs/hmmer.yaml"
    shell:
        """
        cd workflow/databases
        wget -nc ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
        gunzip Pfam-A.hmm.gz
        """


rule download_cog:
    """Download necessary COG files."""
    output:
        "workflow/databases/whog",
    log:
        str(LOGDIR / "downloads/cog_database_download.log"),
    shadow:
        "shallow"
    conda:
        "../envs/hmmer.yaml"
    params:
        dbdir=lambda w, input: os.path.splitext(output[0])[0],
    shell:
        """
        cd {params.dbdir}
        wget -nc ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
        gunzip cddid.tbl.gz
        wget -nc ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/little_endian/Cog_LE.tar.gz
        tar xvfz Cog_LE.tar.gz
        wget -nc ftp://ftp.ncbi.nlm.nih.gov/pub/COG/COG/fun.txt
        wget -nc ftp://ftp.ncbi.nlm.nih.gov/pub/COG/COG/whog
        """


rule download_cazymes:
    """Download necessary CAZyme files."""
    output:
        "workflow/databases/EscheriaColiK12MG1655.gff",
    log:
        str(LOGDIR / "downloads/cazymes_database_download.log"),
    shadow:
        "shallow"
    conda:
        "../envs/dbcan.yaml"
    shell:
        """
        cd workflow/databases
        rm dbCAN.txt.h3i && rm tf-1.hmm.h3i
        wget -nc http://bcb.unl.edu/dbCAN2/download/Databases/V11/CAZyDB.08062022.fa && diamond makedb --in CAZyDB.08062022.fa -d CAZy \
        && wget -nc https://bcb.unl.edu/dbCAN2/download/Databases/V11/dbCAN-HMMdb-V11.txt && mv dbCAN-HMMdb-V11.txt dbCAN.txt && hmmpress dbCAN.txt \
        && wget -nc https://bcb.unl.edu/dbCAN2/download/Databases/V11/tcdb.fa && diamond makedb --in tcdb.fa -d tcdb \
        && wget -nc http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-1.hmm && hmmpress tf-1.hmm \
        && wget -nc http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-2.hmm && hmmpress tf-2.hmm \
        && wget -nc https://bcb.unl.edu/dbCAN2/download/Databases/V11/stp.hmm && hmmpress stp.hmm \
        && wget -nc http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.fna \
        && wget -nc http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.faa \
        && wget -nc http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.gff
        """


rule download_merops:
    """Download latest Merops library."""
    output:
        "workflow/databases/merops_scan.lib",
    log:
        str(LOGDIR / "downloads/merops_database_download.log"),
    shadow:
        "shallow"
    conda:
        "../envs/blast.yaml"
    shell:
        """
        cd workflow/databases
        wget -nc ftp://ftp.ebi.ac.uk/pub/databases/merops/current_release/merops_scan.lib
        makeblastdb -in merops_scan.lib -dbtype prot
        """


rule download_kegg:
    """Download files necessary for Kegg annotation."""
    output:
        "workflow/databases/ko_list",
    log:
        str(LOGDIR / "downloads/keggabase_download.log"),
    shadow:
        "shallow"
    conda:
        "../envs/hmmer.yaml"
    shell:
        """
        cd workflow/databases
        wget -nc ftp://ftp.genome.jp/pub/db/kofam/ko_list.gz        # download the ko list 
        wget -nc ftp://ftp.genome.jp/pub/db/kofam/profiles.tar.gz         # download the hmm profiles
        gunzip ko_list.gz
        tar xf profiles.tar.gz
        """
