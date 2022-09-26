localrules:
    cog2

rule cog:
    """Cog annotation. 
    Default e-value: 1e-5"""
    input: 
        genome_faa = OUTDIR_ANNO/"{genome}.faa", db ="databases/dbs_done.txt",
    output: OUTDIR_ANNO/"{genome}_cog.txt",
    threads: 8
    conda: "../envs/blast.yaml"
    log: LOGDIR/"cog/{genome}.log"
    params: evalue=config["cog_evalue"], dbdir="databases"
    shell: "rpsblast -query {input.genome_faa} -db  {params.dbdir}/Cog -out {output} -outfmt 6 -evalue {params.evalue} 2> {log}"

rule cog2:
    """Step2: Parse rplsblast files.""" 
    input: 
        inputfile=OUTDIR_ANNO/"{genome}_cog.txt",
    output: OUTDIR_ANNO/"{genome}protein-id_cog.txt"
    threads: 8
    conda: "../envs/perl.yaml"
    params: dbdir="databases", outdir=lambda wildcards, output: OUTDIR_ANNO
	log: LOGDIR/"cog/{genome}_cog_parser.log"
	shell: "perl {params.dbdir}/cdd2cog2.pl -r {input.inputfile} -c {params.dbdir}/cddid.tbl -f {params.dbdir}/fun.txt -w {params.dbdir}/whog -o {params.outdir}/{wildcards.genome} 2> {log}"
