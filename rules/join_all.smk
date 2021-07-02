rule join_all:
    input: 
        expand(OUTDIR_ANNO/"{genome}_done.txt", zip, genome=GENOMES),
    output: 
        expand(OUTDIR/"Annotation_results/Orfs_per_genome/{genome}_all_features.csv", zip, genome=GENOMES),
        OUTDIR/"Annotation_results/Pfam_PA.csv",
        report(OUTDIR/"Annotation_results/Statistics.csv",
            category="Annotation statistics",
            caption=os.path.join(workflow.basedir, "report/statistics.rst"))
    params: 
        i= OUTDIR_ANNO,
        input_dir= os.path.join(workflow.basedir, "results/Annotation"), #lambda wildcards, input : os.path.dirname(input[0]),
        output_dir = OUTDIR, 
        db_dir = DBDIR
    threads: 4
    conda: 
        "../envs/general.yaml"
    log: 
        LOGDIR/"all/all.log"
    shell: "python3 scripts/orf_annotation.py {params.input_dir} 2> {log}"	# {params.output_dir} {params.db_dir}

