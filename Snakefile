report: "report/workflow.rst"
configfile: "config.yaml"

rule all:
    input:
       expand(["FAW_results/Orfs_per_genome/{genome}_all_features.csv"], genome=config["genomes"])

rule get_data:
    input: "{genome}"
    output: "data/{genome}"
    shell: "cp {input} data"

rule prokka:
    input: "data/{genome}.fna"
	output: 
		faa="prokka/{genome}.faa", 
		gbk="prokka/{genome}.gbk"
	threads: 4
	conda: "envs/prokka.yaml"
	log: "logs/prokka/{genome}.log"
	shell:
		"""
		prokka --cpus {threads} --outdir prokka/ --force --prefix {wildcards.genome} --locustag {wildcards.genome} {input} 2> {log}
		"""

rule pfam:
    input: "prokka/{genome}.faa"
    output: "results/{genome}_tblout.txt"
    threads: 4
    conda: "envs/hmmer.yaml"
   	log: "logs/pfam/{genome}.log"
    shell:
        "hmmsearch --cpu {threads} --tblout {output} -E 1e-5 databases/Pfam-A.hmm {input} 2> {log}"

rule cog:
    input: "prokka/{genome}.faa"
    output: "results/{genome}.cog.out"
    threads: 4
    conda: "envs/blast.yaml"
	log: "logs/cog/{genome}.log"
	shell:
		"rpsblast -query {input} -db  databases/Cog -out {output} -outfmt 6 -evalue 1e-5 2> {log}"

rule cog2:
    input: "results/{genome}.cog.out"
    output: "results/{genome}protein-id_cog.txt"
    threads: 4
    conda: "envs/perl.yaml"
	log: "logs/cog2/{genome}.log"
	shell:
		"perl databases/cdd2cog2.pl -r {input} -c databases/cddid.tbl -f databases/fun.txt -w databases/whog -o results/{wildcards.genome} 2> {log}"

rule cazymes:
    input: "prokka/{genome}.faa",
    output: "results/{genome}overview.txt"
    threads: 4
    conda: "envs/dbcan.yaml"
    log: "logs/cazymes/{genome}.log"
	shell: 
		"""
		python3 scripts/run_dbcan.py --db_dir ./databases/db/  --out_pre {wildcards.genome}  {input} protein 2> {log} 
		mv output/* ./results
		"""

rule kegg:
    input: "prokka/{genome}.gbk"
    output: "results/{genome}.ko.out"
    threads: 4
    conda:
        "envs/prokka.yaml"
    log: "logs/kegg/{genome}.log"
    shell:
        """
        python3 scripts/prokka2kegg.py -i {input} -d databases/idmapping_KO.tab.gz -o {output} 2> {log} 
        """

rule ensure_all:
    input: 
        "results/{genome}_tblout.txt",
        "results/{genome}protein-id_cog.txt",
        "results/{genome}overview.txt",
        "results/{genome}.ko.out"
    output: "results/{genome}_done.txt"
    shell: "echo done > {output}"


rule join_all:
    input: expand("results/{{genome}}_done.txt", zip, genome=config["genomes"])
    output: "FAW_results/Orfs_per_genome/{genome}_all_features.csv"
    params: directory=lambda wildcards, input : os.path.dirname(input[0])
    threads: 4
    conda: "envs/prokka.yaml"
    log: "logs/all/all.log"
    shell: "python3 orf_annotation.py {params.directory} 2> {log} "	



    