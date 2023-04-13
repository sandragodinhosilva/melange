localrules:
    cazymes2

rule cazymes:
    """CAZYmes annotation."""
    input: 
        genome_faa=OUTDIR/"Annotation/{genome}.faa", db ="workflow/databases/dbs_done.txt"
    output: OUTDIR/"Annotation/{genome}overview.txt",
    threads: 8
    conda: "../envs/dbcan.yaml"
    log: "logs/cazymes1_{genome}.log"
    params: outdir=OUTDIR/"Annotation/",
    group: "cazymes"
    benchmark: "benchmarks/cazymes1_{genome}.benchmark.txt"
    shell: 
        """
        path=$(basename "{wildcards.genome}")
        echo $path
		run_dbcan --db_dir workflow/databases --out_pre $path {input.genome_faa} protein 2> {log} 
		mv output/* {params.outdir}
		"""

rule cazymes2:
    """Step2: Parse CAZyme files."""
    input: OUTDIR/"Annotation/{genome}overview.txt"
    output: OUTDIR/"Annotation/{genome}_cazymes_3tools.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
    group: "cazymes"
    log: "logs/{genome}_cazymes2_parse.log"
    benchmark: "benchmarks/cazymes2_{genome}.benchmark.txt"
    shell: "python3 workflow/scripts/cazymes_parser.py {input} 2> {log}"
