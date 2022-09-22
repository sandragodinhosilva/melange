localrules: 
    kegg2

DBDIR = config["dbdir"]

rule kegg:
    """
    Kegg annotation with kofamscan.
    """
    input: inputfile= OUTDIR_ANNO/"{genome}.faa", db ="databases/dbs_done.txt"
    output: OUTDIR_ANNO/"{genome}_kegg.txt"
    threads: 8
    conda: "../envs/kegg.yaml"
    params: dbdir=DBDIR
    log: LOGDIR/"kegg/{genome}.log"
    shell:
        """
        databases/exec_annotation -o {output} {input.inputfile} --cpu=8 --ko-list {params.dbdir}/"ko_list" --profile {params.dbdir}/"profiles/prokaryote.hal" --tmp-dir={params.dbdir}/tmp  2> {log}
        """

rule kegg2:
    """ Parse kegg files """
    input: OUTDIR_ANNO/"{genome}_kegg.txt", 
    output: OUTDIR_ANNO/"{genome}_kegg_out.txt"
    threads: 4
    params: 
        input_dir=lambda wildcards, input : os.path.dirname(input[0])
    conda: "../envs/general.yaml"
   	log: LOGDIR/"kegg/{genome}_kegg_parse.log"
    shell: "python3 scripts/kegg_parser.py {input} 2> {log}"	
