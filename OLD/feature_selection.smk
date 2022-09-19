rule feature_selection:
    input: 
        ind = METADATA, 
        out = OUTDIR, 
        f = OUTDIR/"Annotation_results/Statistics.csv"
    output:
        report(OUTDIR/"AfterFS/Feature_selection.csv",
            category="Feature selection",
            caption=os.path.join(workflow.basedir, "report/feature_selection.rst"))
    params: 
        output_dir = OUTDIR
    conda: "../envs/jupyter.yaml"
    log:
        # optional path to the processed notebook
        notebook="logs/notebooks/processed_notebook.ipynb"
    notebook:
        "feature_selection_notebook.py.ipynb"