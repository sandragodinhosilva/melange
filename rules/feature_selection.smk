rule feature_selection:
    input: 
        ind = METADATA, 
        out = OUTDIR,
        file = OUTDIR/"Annotation_results/Statistics.csv"
    output:
        OUTDIR/"Annotation_results/Statistics.csv",
        report(OUTDIR/"Feature_selection.csv",
            category="Feature selection",
            caption=os.path.join(workflow.basedir, "report/feature_selection.rst"))
    conda: "../envs/jupyter.yaml"
    log:
        # optional path to the processed notebook
        notebook="logs/notebooks/processed_notebook.ipynb"
    notebook:
        "feature_selection_notebook.py.ipynb"