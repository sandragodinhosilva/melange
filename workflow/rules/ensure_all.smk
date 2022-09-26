rule ensure_all:
    """Verify that all annotations were performed."""
    input:
        myoutput,
    output:
        OUTDIR_ANNO / "{genome}_done.txt",
    log:
        "logs/all/{genome}.log",
    shell:
        "echo done > {output}"
