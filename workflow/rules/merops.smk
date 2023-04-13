localrules:
    merops2

rule merops:
    """Merops annotation. 
    Default e-value: 1e-5"""
    input: inputfile=OUTDIR/"Annotation/{genome}.faa", db ="workflow/databases/dbs_done.txt"
    output: OUTDIR/"Annotation/{genome}_merops.txt"
    threads: 8
    params: evalue=config["merops_evalue"],dbdir=lambda w, input: os.path.dirname(input[1]),
    conda: "../envs/blast.yaml"
    group: "merops"
    log: "logs/merops/{genome}.log"
    benchmark: "benchmarks/merops1_{genome}.benchmark.txt"
    shell: "blastp -query {input.inputfile} -db {params.dbdir}/merops_scan.lib -out {output} -evalue {params.evalue} -outfmt 6 -num_threads {threads} 2> {log}" 

rule merops2:
    """Step2: Parse blastp files."""
    input: OUTDIR/"Annotation/{genome}_merops.txt",
    output: OUTDIR/"Annotation/{genome}_merops_out.txt",
    params: input_dir=lambda wildcards, input : os.path.dirname(input[0]),
    conda: "../envs/general.yaml",
    group: "merops"
    log: "logs/merops/{genome}_merops_parse.log",
    benchmark: "benchmarks/merops2_{genome}.benchmark.txt"
    shell: "python3 workflow/scripts/merops_parser.py {input} 2> {log}"
