localrules:
    pfam2

rule pfam:
    """Pfam annotation. 
    Default e-value: 1e-5"""
    input: genome_faa = OUTDIR/"Annotation/{genome}.faa", db ="workflow/databases/dbs_done.txt",
    output: OUTDIR/"Annotation/{genome}_pfam.txt"
    threads: 8
    conda: "../envs/hmmer.yaml",
    group: "pfam"
    log: "logs/pfam/{genome}.log",
    benchmark: "benchmarks/pfam1_{genome}.benchmark.txt"
    params:
        evalue=config["pfam_evalue"],
        dbdir=lambda w, input: os.path.dirname(input[1]),
    shell: "hmmsearch --cpu {threads} --tblout {output} -E {params.evalue} {params.dbdir}/Pfam-A.hmm {input.genome_faa} 2> {log}"

rule pfam2:
    """Step2: Parse tblout files."""
    input: OUTDIR/"Annotation/{genome}_pfam.txt", 
    output: OUTDIR/"Annotation/{genome}_pfam_out.txt"
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
    group: "pfam"
    log: "logs/pfam/{genome}_pfam_parse.log"
    benchmark: "benchmarks/pfam2_{genome}.benchmark.txt"
    shell: "python3 workflow/scripts/pfam_parser.py {input} 2> {log}"
