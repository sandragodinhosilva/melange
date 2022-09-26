localrules:
    cazymes2

rule cazymes:
    """CAZYmes annotation."""
    input: 
        genome_faa=OUTDIR/"{genome}.faa", db ="workflow/databases/dbs_done.txt"
    output: OUTDIR/"{genome}overview.txt",
    threads: 8
    conda: "../envs/dbcan.yaml"
    log: "logs/cazymes/{genome}.log"
    params: outdir=OUTDIR_ANNO,
	shell: 
		"""
        path=$(basename "{wildcards.genome}")
        echo $path
		run_dbcan --db_dir workflow/databases --out_pre $path {input.genome_faa} protein 2> {log} 
		mv output/* {params.outdir}
		"""

rule cazymes2:
    """Step2: Parse CAZyme files."""
    input: OUTDIR_ANNO/"{genome}overview.txt"
    output: OUTDIR_ANNO/"{genome}_cazymes_3tools.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: "logs/cazymes/{genome}_cazymes_parse.log"
    shell: "python3 workflow/scripts/cazymes_parser.py {input} 2> {log}"
