rule join_metadata:
    input: 
        metadata = METADATA,
        input_file = OUTDIR/"Annotation_results/Pfam_PA.csv"
    output: 
        out_file = OUTDIR/"Annotation_results/Pfam_PA_metadata.csv"
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    threads: 4
    conda: 
        "../envs/general.yaml"
    log: 
        LOGDIR/"all/metadata.log"
    shell: "python3 add_metadata.py {params.input_dir} {input.metadata} 2> {log}"	# {params.output_dir} {params.db_dir}

