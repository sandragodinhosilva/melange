rule join_all:
    """Run python script that joins all annotations."""
    input:
        expand(OUTDIR_ANNO / "{genome}_done.txt", zip, genome=GENOMES),
    output:
        expand(
            OUTDIR / "Annotation_results/Orfs_per_genome/{genome}_all_features.csv",
            zip,
            genome=GENOMES,
        ),
        OUTDIR / "Annotation_results/Pfam_PA.csv",
        report(
            OUTDIR / "Annotation_results/Statistics.csv",
            category="Annotation statistics",
            caption=os.path.join(workflow.basedir, "report/statistics.rst"),
        ),
    params:
        i=OUTDIR_ANNO,
        input_dir=os.path.join(workflow.basedir, "results/Annotation"),  #lambda wildcards, input : os.path.dirname(input[0]),
        databases_in_use=list(databases_in_use),
        output_dir=OUTDIR,
        db_dir="databases"
    threads: 4
    conda:
        "../envs/general.yaml"
    log:
        LOGDIR / "all/all.log",
    shell:
        "python3 scripts/orf_annotation.py {params.input_dir} {params.databases_in_use} 2> {log}"  
