# Melange Configuration

To configure this workflow, modify config/config.yaml according to your needs.

### Input files
Sample input files are in directory "example_data". Replace these files with your input or change the input directory:

      inputdir: "example_data"
      
Define the correct extensions so that Melange can detect input files:
      
      nucleotide_extension: "{genome}.fa"
      aminoacid_extension: "{genome}.faa" 
      
Input files are nucleotide or aminoacid files?

      aminoacid_file: True #if True - gene calling (Prokka) won't be run



### Output directory
      outdir: "results" 
      outdir_anno: "results/Annotation" 

### Configure databases in use

    PFAM: True
    COG: True
    KEGG: True
    CAZYMES: True
    MEROPS: True

Change default Evalues:

      cog_evalue: "1e-5" #for rpsblast
      pfam_evalue: "1e-5" #for hmmsearch
      merops_evalue: "1e-5" #for blastp
      kegg_evalue: "1e-5" #for hmmsearch - implement
