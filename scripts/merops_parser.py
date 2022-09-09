#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
import argparse
import sys
parser=argparse.ArgumentParser(
    description='''Parse merops file''')

__file__ = "merops_parser.py"
__author__ = 'Sandra Godinho Silva (sandragodinhosilva@gmail.com)'
__version__ = '0.8'
__date__ = 'December 3rd, 2020'

parser.add_argument('inputFile', 
		help='Full path to the input directory where all files are')

# Execute parse_args()
args = parser.parse_args()
###############################################################################
# import standard Python modules
import os
import re
###############################################################################
in_file = "/home/sandra/MeLanGE/results/Annotation/GCF_000009045.1_ASM904v1_genomic_merops.txt"
#in_file = sys.argv[1]

filename = os.path.basename(in_file)
filename = filename.replace("_merops.txt","")
output_dir = os.path.dirname(in_file)
out = os.path.join(output_dir,  filename + "_merops_out.txt")
 
protein2hit_dict = {}
protein2bit_dict = {}
dic = {}

with open(in_file, 'r') as f:
    i=0
    lines = f.readlines()
    for line in lines:
        line = line.rstrip() # This removes the whitespace at the end of the line
        if line.startswith("#"): # We only want to analyze lines with HMMER matches, so we can pass on all the lines that start with a #
            pass
        else:
            newline = re.sub("\s+", "\t", line) # Now we can replace the whitespace in the lines with tabs, which are easier to work with. 
            tabs = newline.split("\t") 
            hit = tabs[1]             
            query = tabs[0] # The first item in the line is the query protein. We can assign the variable "query" to it. 
            bit_score = tabs[10] # The fifth item is the bit score. We can assign the variable "bit_score" to it. 
    
            if query in protein2bit_dict: # If query is in prtein2bit_dict, it means we have seen this protein before, so now we want to see what bit score it had to the previous hit. 
                if protein2bit_dict[query] > float(bit_score):
                    pass
                else: 
                    protein2bit_dict[query] = float(bit_score)
                    protein2hit_dict[query] = hit
            else:
                protein2bit_dict[query] = float(bit_score)
                protein2hit_dict[query] = hit
with open(out, "w") as outputfile: 
    outputfile.write("Query\tHit\tScore\n")
    for proteins in protein2hit_dict:
        outputfile.write(proteins + "\t" + protein2hit_dict[proteins] + "\t" + str(protein2bit_dict[proteins]) +"\n")
outputfile.close()
print("File " + str(out) + " was created.")
f.close()