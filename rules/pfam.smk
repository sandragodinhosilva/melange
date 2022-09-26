localrules:
    pfam2

rule pfam:
    """Pfam annotation. 
    Default e-value: 1e-5"""
    input: genome_faa = OUTDIR_ANNO/"{genome}.faa", db ="databases/dbs_done.txt",
    output: OUTDIR_ANNO/"{genome}_pfam.txt"
    threads: 8
    conda: "../envs/hmmer.yaml"
   	log: LOGDIR/"pfam/{genome}.log"
    params: evalue=config["pfam_evalue"], dbdir=lambda wildcards, output: DBDIR
    shell: "hmmsearch --cpu {threads} --tblout {output} -E {params.evalue} {params.dbdir}/Pfam-A.hmm {input.genome_faa} 2> {log}"

rule pfam2:
    """Step2: Parse tblout files."""
    input: OUTDIR_ANNO/"{genome}_pfam.txt", 
    output: OUTDIR_ANNO/"{genome}_pfam_out.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"pfam/{genome}_pfam_parse.log"
    shell: "python3 scripts/pfam_parser.py {input} 2> {log}"	
