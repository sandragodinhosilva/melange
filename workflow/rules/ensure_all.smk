rule ensure_all:
    """Verify that all annotations were performed."""
    input:
        myoutput,
    output:
        OUTDIR / "Annotation/{genome}_done.txt",
    log:
        "logs/all/{genome}.log",
    shell:
        "echo done > {output}"
