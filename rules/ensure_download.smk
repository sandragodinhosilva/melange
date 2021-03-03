localrules:
    download_pfam,
    download_merops,
    download_cog,
    download_cazymes

rule ensure_download:
    input: 
        DBDIR/"Pfam-A.hmm",
        DBDIR/"merops_scan.lib",
        DBDIR/"cdd2cog2.pl",
        DBDIR/"whog",
        DBDIR/"dbCAN.txt"
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

rule download_merops:
    """Download latest Merops """
    output:
        DBDIR/"merops_scan.lib"
    log:
        str(LOGDIR/"downloads/merops_download.log")
    shadow: "shallow"
    conda: "../envs/blast.yaml"
    params: db = DBDIR
    shell:
        """
        cd {params.db}
        wget ftp://ftp.ebi.ac.uk/pub/databases/merops/current_release/merops_scan.lib
        makeblastdb -in merops_scan.lib -dbtype prot -input_type fasta
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
    """Download CAZYdb"""
    output:
        DBDIR/"dbCAN.txt"
    log:
        str(LOGDIR/"downloads/cazy_database_download.log")
    shadow:
        "shallow"
    conda: "../envs/dbcan.yaml"
    params: db = DBDIR
    shell:
        """
        cd {params.db}    
        wget http://bcb.unl.edu/dbCAN2/download/CAZyDB.07312019.fa.nr && diamond makedb --in CAZyDB.07312019.fa.nr -d CAZy     && wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN-HMMdb-V8.txt && mv dbCAN-HMMdb-V8.txt dbCAN.txt && hmmpress dbCAN.txt     && wget http://bcb.unl.edu/dbCAN2/download/Databases/tcdb.fa && diamond makedb --in tcdb.fa -d tcdb     && wget http://bcb.unl.edu/dbCAN2/download/Databases/tf-1.hmm && hmmpress tf-1.hmm     && wget http://bcb.unl.edu/dbCAN2/download/Databases/tf-2.hmm && hmmpress tf-2.hmm     && wget http://bcb.unl.edu/dbCAN2/download/Databases/stp.hmm && hmmpress stp.hmm     && cd ../ && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.fna     && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.faa     && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.gff
        """