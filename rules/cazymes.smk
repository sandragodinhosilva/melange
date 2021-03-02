
localrules:
    download_cazymes

rule cazymes:
    """
    CAZYmes annotation.
    """
    input: 
        genome_faa=OUTDIR/"{genome}.faa",
        db = DBDIR/"dbCAN.txt"
    output: OUTDIR/"{genome}overview.txt"
    threads: 8
    conda: "../envs/dbcan.yaml"
    params: dbdir=DBDIR, outdir=OUTDIR
    log: LOGDIR/"cazymes/{genome}.log"
	shell: 
		"""
		python3 scripts/run_dbcan.py --db_dir {params.dbdir}  --out_pre {wildcards.genome}  {input.genome_faa} protein 2> {log} 
		mv output/* {params.outdir}
		"""

rule download_cazymes:
    """Download CAZYdb"""
    output:
        DBDIR/"dbCAN.txt"
    log:
        str(LOGDIR/"cazymes/cazy_database_download.log")
    shadow:
        "shallow"
    conda: "../envs/dbcan.yaml"
    params: db = DBDIR
    shell:
        """
        cd db     
        wget http://bcb.unl.edu/dbCAN2/download/CAZyDB.07312019.fa.nr && diamond makedb --in CAZyDB.07312019.fa.nr -d CAZy     && wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN-HMMdb-V8.txt && mv dbCAN-HMMdb-V8.txt dbCAN.txt && hmmpress dbCAN.txt     && wget http://bcb.unl.edu/dbCAN2/download/Databases/tcdb.fa && diamond makedb --in tcdb.fa -d tcdb     && wget http://bcb.unl.edu/dbCAN2/download/Databases/tf-1.hmm && hmmpress tf-1.hmm     && wget http://bcb.unl.edu/dbCAN2/download/Databases/tf-2.hmm && hmmpress tf-2.hmm     && wget http://bcb.unl.edu/dbCAN2/download/Databases/stp.hmm && hmmpress stp.hmm     && cd ../ && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.fna     && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.faa     && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.gff
        """