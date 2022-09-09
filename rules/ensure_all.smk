rule ensure_all:
    input: 
        OUTDIR_ANNO/"{genome}_tblout_pfam.txt",
        OUTDIR_ANNO/"{genome}protein-id_cog.txt",
        OUTDIR_ANNO/"{genome}.ko.out",
        OUTDIR_ANNO/"{genome}_merops_out.txt",
        OUTDIR_ANNO/"{genome}_cazymes_3tools.txt",
    output: OUTDIR_ANNO/"{genome}_done.txt"
    log: LOGDIR/"all/{genome}.log"
    shell: "echo done > {output}"