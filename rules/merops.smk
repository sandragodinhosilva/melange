localrules:
    merops2
    
rule merops2:
    """ Parse blastp files """
    input: OUTDIR_ANNO/"{genome}_merops.txt"
    output: OUTDIR_ANNO/"{genome}_merops_out.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"merops/{genome}_merops_parse.log"
    shell: "python3 scripts/merops_parser.py {input} 2> {log}"

rule merops:
    """
    Merops annotation. Default e-value: 1e-5
    """
    input: OUTDIR_ANNO/"{genome}.faa"
    output: OUTDIR_ANNO/"{genome}_merops.txt"
    threads: 4
    conda: "../envs/blast.yaml"
    log: LOGDIR/"merops/{genome}.log"
    params: evalue=config["merops_evalue"], dbdir=DBDIR
    shell: "blastp -query {input} -db {params.dbdir}/pepunit.lib -out {output} -evalue {params.evalue} -outfmt 6 -num_threads {threads} 2> {log}"
