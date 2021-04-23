localrules:
    download_pfam,
    download_cog

rule ensure_download:
    input: 
        DBDIR/"Pfam-A.hmm",
        DBDIR/"cdd2cog2.pl",
        DBDIR/"whog",
    output: DBDIR/"dbs_done.txt"
    log: LOGDIR/"dbs.log"
    shell: "echo done > {output}"


rule download_pfam:
    """Download latest Pfam-A.hmm"""
    output:
        DBDIR/"Pfam-A.hmm"
    log:
        str(LOGDIR/"downloads/pfam_database_download.log")
    shadow:
        "shallow"
    conda: "../envs/hmmer.yaml"
    params: db = DBDIR
    shell:
        """
        cd {params.db}
        wget ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
        gunzip Pfam-A.hmm.gz
        """


rule download_cog:
    """Download necessary COG files"""
    output:
        DBDIR/"whog"
    log:
        str(LOGDIR/"downloads/cog_database_download.log")
    shadow:
        "shallow"
    params: db = DBDIR
    conda: "../envs/hmmer.yaml"
    shell:
        """
        cd {params.db}
        # wget https://raw.githubusercontent.com/aleimba/bac-genomics-scripts/master/cdd2cog/cdd2cog.pl
        wget ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cddid.tbl.gz
        gunzip cddid.tbl.gz
        wget ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/little_endian/Cog_LE.tar.gz
        tar xvfz Cog_LE.tar.gz
        wget ftp://ftp.ncbi.nlm.nih.gov/pub/COG/COG/fun.txt
        wget ftp://ftp.ncbi.nlm.nih.gov/pub/COG/COG/whog
        """