localrules:
    cazymes2

rule cazymes:
    """
    CAZYmes annotation.
    """
    input: 
        genome_faa=OUTDIR/"{genome}.faa", db ="databases/dbs_done.txt"
    output: OUTDIR/"{genome}overview.txt"
    threads: 8
    conda: "../envs/dbcan.yaml"
    params:  dbdir=lambda wildcards, output: DBDIR, outdir=OUTDIR_ANNO
    log: LOGDIR/"cazymes/{genome}.log"
	shell: 
		"""
        path=$(basename "{wildcards.genome}")
        echo $path
		run_dbcan --db_dir {params.dbdir} --out_pre $path {input.genome_faa} protein 2> {log} 
		mv output/* {params.outdir}
		"""

rule cazymes2:
    """ Parse  files """
    input: OUTDIR_ANNO/"{genome}overview.txt"
    output: OUTDIR_ANNO/"{genome}_cazymes_3tools.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"cazymes/{genome}_cazymes_parse.log"
    shell: "python3 scripts/cazymes_parser.py {input} 2> {log}"
