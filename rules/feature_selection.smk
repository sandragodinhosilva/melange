rule feature_selection:
    output:
        "test.txt"
    conda: "../envs/jupyter.yaml"
    log:
        # optional path to the processed notebook
        notebook="logs/featureselection/processed_notebook.ipynb"
    notebook:
        "FeatureSelection/Feature_selection.ipynb"