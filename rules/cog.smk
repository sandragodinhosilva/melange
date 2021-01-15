rule cog:
    """
    Cog annotation. Default e-value: 1e-5
    """
    input: OUTDIR/"{genome}.faa"
    output: OUTDIR/"{genome}.cog.out"
    threads: 8
    conda: "../envs/blast.yaml"
    log: LOGDIR/"cog/{genome}.log"
    params: evalue=config["cog_evalue"], dbdir=DBDIR
    shell: "rpsblast -query {input} -db  {params.dbdir}/Cog -out {output} -outfmt 6 -evalue {params.evalue} 2> {log}"