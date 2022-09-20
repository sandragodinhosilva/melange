localrules:
    download_pfam,
    download_cog,
    download_cazymes,
    download_merops

rule ensure_download:
    input: 
        DBDIR/"Pfam-A.hmm",
        DBDIR/"cdd2cog2.pl",
        DBDIR/"whog",
        DBDIR/"EscheriaColiK12MG1655.gff",
        DBDIR/"merops_new.lib"
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

rule download_cazymes:
    """Download necessary CAZyme files"""
    output:
        DBDIR/"EscheriaColiK12MG1655.gff"
    log:
        str(LOGDIR/"downloads/cazymes_database_download.log")
    shadow:
        "shallow"
    params: db = DBDIR
    conda: "../envs/dbcan.yaml"
    shell:
        """
        cd {params.db}
        wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/CAZyDB.08062022.fa && diamond makedb --in CAZyDB.08062022.fa -d CAZy \
        && wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/dbCAN-HMMdb-V11.txt && mv dbCAN-HMMdb-V11.txt dbCAN.txt && hmmpress dbCAN.txt \
        && wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/tcdb.fa && diamond makedb --in tcdb.fa -d tcdb \
        && wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-1.hmm && hmmpress tf-1.hmm \
        && wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-2.hmm && hmmpress tf-2.hmm \
        && wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/stp.hmm && hmmpress stp.hmm \
        && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.fna \
        && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.faa \
        && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.gff
    """

rule download_merops:
    """Download latest Merops library"""
    output:
        DBDIR/"merops_new.lib"
    log:
        str(LOGDIR/"downloads/merops_database_download.log")
    shadow:
        "shallow"
    conda: "../envs/blast.yaml"
    params: db = DBDIR
    shell:
        """
        cd {params.db}
        wget ftp://ftp.ebi.ac.uk/pub/databases/merops/current_release/pepunit.lib
        makeblastdb -in pepunit.lib -dbtype nucl
        """