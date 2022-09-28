rule fastaq_to_fasta:
    """Convert fastq files into readable format by Prokka."""
    input: 
        fastq=INPUTDIR/FASTQ_EXTENSION,
        db ="workflow/databases/dbs_done.txt",
    output:
        fasta=INPUTDIR/NUCLEOTIDE_EXTENSION,
    conda: 
        "../envs/general.yaml",
    shell: 
        "seqret -sequence {input.fastq} -outseq {output.fasta}"