rule cog2:
    input: OUTDIR/"{genome}.cog.out"
    output: OUTDIR/"{genome}protein-id_cog.txt"
    threads: 8
    conda: "../envs/perl.yaml"
    params: dbdir=DBDIR, outdir=OUTDIR
	log: LOGDIR/"cog2/{genome}.log"
	shell: "perl {params.dbdir}/cdd2cog2.pl -r {input} -c {params.dbdir}/cddid.tbl -f {params.dbdir}/fun.txt -w {params.dbdir}/whog -o {params.outdir}/{wildcards.genome} 2> {log}"
