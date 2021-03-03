localrules:
    merops2

rule merops2:
    """ Parse merops blastp output files """
    input: OUTDIR/"{genome}_merops.txt"
    output: OUTDIR/"{genome}_merops_out.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"merops/{genome}_parse.log"
    shell: "python3 merops_parser.py {input} 2> {log}"	

rule merops:
    """
    Merops annotation. Default e-value: 1e-5
    """
    input: 
        genome_faa = OUTDIR/"{genome}.faa"
    output: OUTDIR/"{genome}_merops.txt"
    threads: 8
    conda: "../envs/blast.yaml"
   	log:  LOGDIR/"merops/{genome}.log"
    params: evalue=config["merops_evalue"], dbdir=DBDIR
    shell: """
    blastp -query {input.genome_faa} -db {params.dbdir}/merops_scan.lib -out {output} -evalue {params.evalue} -outfmt 6 -num_threads {threads} 2> {log} """
