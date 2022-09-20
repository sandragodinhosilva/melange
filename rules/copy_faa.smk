rule copy_faa:
    input: INPUTDIR/AMINOACID_EXTENSION
    output: OUTDIR_ANNO/AMINOACID_EXTENSION
    shell: "cp {input} {output}"