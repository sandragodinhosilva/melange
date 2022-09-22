DBDIR = config["dbdir"]

rule kegg2:
    """
    Kegg annotation with kofamscan.
    """
    input: inputfile= OUTDIR_ANNO/"{genome}.faa", db ="databases/dbs_done.txt"
    output: OUTDIR_ANNO/"{genome}_kegg2.txt"
    threads: 8
    conda: "../envs/kegg.yaml"
    params: dbdir=DBDIR
    log: LOGDIR/"kegg2/{genome}.log"
    shell:
        """
        databases/exec_annotation -o {output} {input.inputfile} --cpu=8 --ko-list {params.dbdir}/"ko_list" --profile {params.dbdir}/"profiles/prokaryote.hal" --tmp-dir={params.dbdir}/tmp
        """