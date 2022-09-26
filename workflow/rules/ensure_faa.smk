rule ensure_faa:
    """Make sure that fasta aminoacid files are in the right folder."""
    input: input_to_copy=INPUTDIR/AMINOACID_EXTENSION, db ="workflow/databases/dbs_done.txt",
    output: OUTDIR_ANNO/AMINOACID_EXTENSION,
   	log: "logs/faa/{genome}.log"
    shell: "cp {input.input_to_copy} {output} 2> {log}"