GENOME_EXTENSION = config["genome_extension"]
DBDIR = config["dbdir"]

rule prokka:
    input: input_genome= INPUTDIR/GENOME_EXTENSION , db ="databases/dbs_done.txt"
	output: 
		faa=OUTDIR/"{genome}.faa", 
		gbk=OUTDIR/"{genome}.gbk"
	threads: 8
	conda: "../envs/prokka.yaml"
	log: LOGDIR/"prokka/{genome}.log"
	shell:
		"""
		prokka --cpus {threads} --outdir results/ --force --prefix {wildcards.genome} --locustag {wildcards.genome} {input.input_genome} 2> {log}
		"""