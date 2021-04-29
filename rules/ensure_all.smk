rule ensure_all:
    input: 
        OUTDIR_ANNO/"{genome}_tblout_pfam.txt",
        OUTDIR_ANNO/"{genome}protein-id_cog.txt",
        OUTDIR_ANNO/"{genome}.ko.out",
    output: OUTDIR_ANNO/"{genome}_done.txt"
    log: LOGDIR/"all/{genome}.log"
    shell: "echo done > {output}"