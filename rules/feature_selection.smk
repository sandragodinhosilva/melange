rule feature_selection:
    input: ind = METADATA, out = OUTDIR
    output:
        "test.txt"
    conda: "../envs/jupyter.yaml"
    log:
        # optional path to the processed notebook
        notebook="logs/notebooks/processed_notebook.ipynb"
    notebook:
        "notebook2.py.ipynb"