localrules:
    download_pfam
    
rule pfam:
    """
    Pfam annotation. Default e-value: 1e-5
    """
    input: 
        genome_faa = OUTDIR/"{genome}.faa",
        db = DBDIR/"Pfam-A.hmm"
    output: OUTDIR/"{genome}_tblout.txt"
    threads: 8
    conda: "../envs/hmmer.yaml"
   	log: "logs/pfam/{genome}.log"
    params: evalue=config["pfam_evalue"], dbdir=DBDIR
    shell: "hmmsearch --cpu {threads} --tblout {output} -E {params.evalue} {params.dbdir}/Pfam-A.hmm {input.genome_faa} 2> {log}"

rule download_pfam:
    """Download latest Pfam-A.hmm"""
    output:
        DBDIR/"Pfam-A.hmm",
    log:
        str(LOGDIR/"pfam_database_download.log")
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