localrules:
    cog2

rule cog:
    """Cog annotation. 
    Default e-value: 1e-5"""
    input: 
        genome_faa = OUTDIR_ANNO/"{genome}.faa", db ="workflow/databases/dbs_done.txt",
    output: OUTDIR_ANNO/"{genome}_cog.txt",
    threads: 8
    conda: "../envs/blast.yaml"
    group: "cog"
    log: "logs/cog/{genome}.log"
    benchmark: "benchmarks/cog1_{genome}.benchmark.txt"
    params: evalue=config["cog_evalue"], dbdir=lambda w, input: os.path.dirname(input[1]),
    shell: "rpsblast -query {input.genome_faa} -db  {params.dbdir}/Cog -out {output} -outfmt 6 -evalue {params.evalue} 2> {log}"

rule cog2:
    """Step2: Parse rplsblast files.""" 
    input: 
        inputfile=OUTDIR_ANNO/"{genome}_cog.txt",
    output: OUTDIR_ANNO/"{genome}protein-id_cog.txt"
    threads: 8
    conda: "../envs/perl.yaml"
    params: outdir=lambda wildcards, output: OUTDIR_ANNO
    group: "cog"
    log: "logs/cog/{genome}_cog_parser.log",
    benchmark: "benchmarks/cog2_{genome}.benchmark.txt" 
    shell: "perl workflow/databases/cdd2cog2.pl -r {input.inputfile} -c workflow/databases/cddid.tbl -f workflow/databases/fun.txt -w workflow/databases/whog -o {params.outdir}/{wildcards.genome} 2> {log}"
