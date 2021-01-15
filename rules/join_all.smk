rule join_all:
    input: 
        #"results/all_genomes_done.txt",
        expand(OUTDIR/"{genome}_done.txt", zip, genome=GENOMES),#genome=config["genomes"])
    output: 
        expand("FAW_results/Orfs_per_genome/{genome}_all_features.csv", zip, genome=GENOMES),#genome=config["genomes"]),
        #"FAW_results/Statistics.csv",
        report("FAW_results/Statistics.csv", caption="FAW_results/Statistics.csv", category="Final")
    params: directory=lambda wildcards, input : os.path.dirname(input[0])
    threads: 4
    conda: "../envs/general.yaml"
    log: LOGDIR/"all/all.log"
    shell: "python3 orf_annotation.py {params.directory} 2> {log}"	
