localrules:
    cog2

rule cog:
    """
    Cog annotation. Default e-value: 1e-5
    """
    input: 
        genome_faa = OUTDIR/"{genome}.faa"
    output: OUTDIR/"{genome}.cog.out"
    threads: 8
    conda: "../envs/blast.yaml"
    log: LOGDIR/"cog/{genome}.log"
    params: evalue=config["cog_evalue"], dbdir=DBDIR
    shell: "rpsblast -query {input.genome_faa} -db  {params.dbdir}/Cog -out {output} -outfmt 6 -evalue {params.evalue} 2> {log}"

rule cog2:
    input: 
        OUTDIR/"{genome}.cog.out"
    output: OUTDIR/"{genome}protein-id_cog.txt"
    threads: 8
    conda: "../envs/perl.yaml"
    params: dbdir=DBDIR, outdir=OUTDIR
	log: LOGDIR/"cog2/{genome}.log"
	shell: "perl {params.dbdir}/cdd2cog2.pl -r {input} -c {params.dbdir}/cddid.tbl -f {params.dbdir}/fun.txt -w {params.dbdir}/whog -o {params.outdir}/{wildcards.genome} 2> {log}"

