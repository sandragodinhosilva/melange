NUCLEOTIDE_EXTENSION = config["nucleotide_extension"]
OUTDIR_ANNO = Path(config["outdir_anno"])

rule prokka:
    """Run Prokka."""
    input: input_genome = INPUTDIR/NUCLEOTIDE_EXTENSION, db ="workflow/databases/dbs_done.txt"
	output: faa=OUTDIR_ANNO/"{genome}.faa",gbk=OUTDIR_ANNO/"{genome}.gbk", 
	params: outdir=lambda wildcards, output: OUTDIR_ANNO,
	threads: 8
	conda: "../envs/prokka.yaml"
	log: "logs/prokka/{genome}.log" 
	benchmark: "benchmarks/prokka_{genome}.benchmark.txt"
	shell:
		"""
		python3 workflow/scripts/contig_namer.py {input.input_genome} 
		prokka --cpus {threads} --outdir {params.outdir} --force --locustag PROKKA --prefix {wildcards.genome} {input.input_genome} 
		"""