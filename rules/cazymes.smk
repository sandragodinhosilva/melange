rule cazymes:
    """
    CAZYmes annotation.
    """
    input: 
        genome_faa=OUTDIR/"{genome}.faa"
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

