rule kegg:
    """
    Kegg annotation.
    """
    input: OUTDIR_ANNO/"{genome}.gbk"
    output: OUTDIR_ANNO/"{genome}.ko.out"
    threads: 4
    conda: "../envs/prokka.yaml"
    log: LOGDIR/"kegg/{genome}.log"
    shell:
        """
        python3 scripts/prokka2kegg.py -i {input} -d databases/idmapping_KO.tab.gz -o {output} 2> {log} 
        """