rule ensure_faa:
    input: input_to_copy=INPUTDIR/AMINOACID_EXTENSION, db ="databases/dbs_done.txt"
    output: OUTDIR_ANNO/AMINOACID_EXTENSION
   	log: LOGDIR/"faa/{genome}_ensure.log"
    shell: "cp {input.input_to_copy} {output} 2> {log}"