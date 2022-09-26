LOGDIR = Path(config["logdir"])


rule kegg:
    """Kegg annotation with kofamscan."""
    input:
        inputfile=OUTDIR_ANNO / "{genome}.faa",
        db="workflow/databases/dbs_done.txt",
    output:
        OUTDIR_ANNO / "{genome}_kegg.txt",
    threads: 8
    conda:
        "../envs/kegg.yaml"
    params:
        dbdir=lambda w, input: os.path.dirname(input[1]),
    log:
        LOGDIR / "kegg/{genome}.log",
    shell:
        """
        workflow/databases/exec_annotation -o {output} {input.inputfile} --cpu=8 --ko-list {params.dbdir}/"ko_list" --profile {params.dbdir}/"profiles/prokaryote.hal" --tmp-dir={params.dbdir}/tmp  -f mapper 2> {log}
        """
