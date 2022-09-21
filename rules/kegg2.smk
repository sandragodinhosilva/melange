DBDIR = config["dbdir"]

rule kegg2:
    """
    Kegg annotation with kofamscan.
    """
    input: OUTDIR_ANNO/"{genome}.faa"
    output: OUTDIR_ANNO/"{genome}_kegg2.txt"
    threads: 4
    conda: "../envs/kegg.yaml"
    params: dbdir=DBDIR
    log: LOGDIR/"kegg2/{genome}.log"
    shell:
        """
        databases/exec_annotation -o {output} {input} --cpu=8 --ko-list {params.dbdir}/"ko_list" --profile {params.dbdir}/"prokaryote.hal"
        """