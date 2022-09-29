# Melange Configuration

To adapt Melange to your needs, change the default parameters in the configuration file `config.yaml`:

## Input
By default, Melange looks for the input files in the 'example_data' directory. You can either change these definitions or transfer your data to this folder (delete example data so that it doesn't appear in the final output).

    # --- Input
    inputdir: "example_data"
    
Melange can accept three file formats: Fasta nucleotide files, Fasta amino acid files and Fastq files. To be recognisable by Melange, make sure the following extensions are correct or change them accordingly: 

      nucleotide_extension: "{genome}.fa"
      aminoacid_extension: "{genome}.faa" 
      fastq_extension: "{genome}.fastq"

Finally, specify what kind of files Melange should start with.

      file_type: "nucleotide" # OPTIONS: "nucleotide" "aminoacid" "fastq"

## Output
Directories where your output files will appear. 

    outdir: "results" 
    outdir_anno: "results/Annotation" 

Predefined expectation value thresholds. Only change this if you know what you are doing.
    
    # --- Evalues:
    cog_evalue: "1e-5" #for rpsblast
    pfam_evalue: "1e-5" #for hmmsearch
    merops_evalue: "1e-5" #for blastp
    kegg_evalue: "1e-5" #for hmmsearch 
