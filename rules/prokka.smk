rule prokka:
    input: INPUTDIR/"{genome}"genome_extension
	output: 
		faa=OUTDIR/"{genome}.faa", 
		gbk=OUTDIR/"{genome}.gbk"
	threads: 8
	conda: "../envs/prokka.yaml"
	log: LOGDIR/"{genome}.log"
	shell:
		"""
		prokka --cpus {threads} --outdir results/ --force --prefix {wildcards.genome} --locustag {wildcards.genome} {input} 2> {log}
		"""