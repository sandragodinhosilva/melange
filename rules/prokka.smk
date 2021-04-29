GENOME_EXTENSION = config["genome_extension"]
DBDIR = config["dbdir"]
LOGDIR = Path(config["logdir"])
 

rule prokka:
    input: input_genome = INPUTDIR/GENOME_EXTENSION, db ="databases/dbs_done.txt"#, out = OUTDIR
	output: 
		faa=OUTDIR_ANNO/"{genome}.faa", 
		gbk=OUTDIR_ANNO/"{genome}.gbk"
	threads: 8
	conda: "../envs/prokka.yaml"
	log: LOGDIR/"prokka/{genome}.log"
	shell:
		"""
		python3 scripts/contig_namer.py {input.input_genome} 
		prokka --cpus {threads} --outdir results/Annotation --force --prefix {wildcards.genome} --locustag {wildcards.genome} {input.input_genome} 2> {log} 
		"""