rule ensure_faa:
    """Make sure that fasta aminoacid files are in the right folder."""
    input: 
        input_to_copy=INPUTDIR/AMINOACID_EXTENSION,
        db ="workflow/databases/dbs_done.txt"
    output:
        OUTDIR_ANNO/"{genome}.faa"
    conda: 
        "../envs/general.yaml"
    shell: 
        "cp {input.input_to_copy} {output}"