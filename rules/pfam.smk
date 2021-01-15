rule pfam:
    """
    Pfam annotation. Default e-value: 1e-5
    """
    input: OUTDIR/"{genome}.faa"
    output: OUTDIR/"{genome}_tblout.txt"
    threads: 8
    conda: "../envs/hmmer.yaml"
   	log: "logs/pfam/{genome}.log"
    params: evalue=config["pfam_evalue"], dbdir=DBDIR
    shell: "hmmsearch --cpu {threads} --tblout {output} -E {params.evalue} {params.dbdir}/Pfam-A.hmm {input} 2> {log}"