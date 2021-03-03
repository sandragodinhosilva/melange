localrules:
    pfam2
    
rule pfam2:
    """ Parse tblout files """
    input: OUTDIR/"{genome}_tblout.txt"
    output: OUTDIR/"{genome}_tblout_pfam.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"pfam/{genome}_tblout_parse.log"
    shell: "python3 pfam_parser.py {input} 2> {log}"	

rule pfam:
    """
    Pfam annotation. Default e-value: 1e-5
    """
    input: genome_faa = OUTDIR/"{genome}.faa"
    output: OUTDIR/"{genome}_tblout.txt"
    threads: 8
    conda: "../envs/hmmer.yaml"
   	log: LOGDIR/"pfam/{genome}.log"
    params: evalue=config["pfam_evalue"], dbdir=DBDIR
    shell: "hmmsearch --cpu {threads} --tblout {output} -E {params.evalue} {params.dbdir}/Pfam-A.hmm {input.genome_faa} 2> {log}"

