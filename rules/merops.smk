localrules:
    merops2

rule merops:
    """Merops annotation. 
    Default e-value: 1e-5"""
    input: inputfile=OUTDIR_ANNO/"{genome}.faa", db ="databases/dbs_done.txt"
    output: OUTDIR_ANNO/"{genome}_merops.txt"
    threads: 4
    conda: "../envs/blast.yaml"
    log: LOGDIR/"merops/{genome}.log"
    params: evalue=config["merops_evalue"], dbdir=lambda wildcards, output: DBDIR
    shell: "blastp -query {input.inputfile} -db {params.dbdir}/merops_scan.lib -out {output} -evalue {params.evalue} -outfmt 6 -num_threads {threads} 2> {log}" 

rule merops2:
    """Step2: Parse blastp files."""
    input: OUTDIR_ANNO/"{genome}_merops.txt"
    output: OUTDIR_ANNO/"{genome}_merops_out.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"merops/{genome}_merops_parse.log"
    shell: "python3 scripts/merops_parser.py {input} 2> {log}"
