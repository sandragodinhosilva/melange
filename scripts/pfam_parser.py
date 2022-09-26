#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################

import argparse
import sys

parser = argparse.ArgumentParser(description="""Parse pfam file""")

__file__ = "pfam_parser.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "0.8"
__date__ = "December 3rd, 2020"

parser.add_argument("inputFile", help="Full path to input file")

# Execute parse_args()
args = parser.parse_args()

# import standard Python modules
import os
import re

###############################################################################
file = sys.argv[1]

filename = os.path.basename(file)
filename = filename.replace("_pfam.txt", "")
output_dir = os.path.dirname(file)
out = os.path.join(output_dir, filename + "_pfam_out.txt")


protein2hit_dict = {}
protein2bit_dict = {}
dic = {}
with open(file, "r") as f:
    i = 0
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()  # This removes the whitespace at the end of the line
        if line.startswith(
            "#"
        ):  # We only want to analyze lines with HMMER matches, so we can pass on all the lines that start with a #
            pass
        else:
            newline = re.sub(
                "\s+", "\t", line
            )  # Now we can replace the whitespace in the lines with tabs, which are easier to work with.
            tabs = newline.split(
                "\t"
            )  # And now we can create a list by splitting each line into pieces based on where the tabs are.
            hit = tabs[3]
            i += 1
            query = tabs[
                0
            ]  # The first item in the line is the query protein. We can assign the variable "query" to it.
            bit_score = tabs[
                5
            ]  # The fifth item is the bit score. We can assign the variable "bit_score" to it.
            dic[i] = query
            protein2bit_dict[i] = float(bit_score)
            protein2hit_dict[i] = hit
        with open(out, "w") as outputfile:
            outputfile.write("Query\tHit\tScore\n")
            for proteins in protein2hit_dict:
                outputfile.write(
                    dic[proteins]
                    + "\t"
                    + protein2hit_dict[proteins]
                    + "\t"
                    + str(protein2bit_dict[proteins])
                    + "\n"
                )
        outputfile.close()
print("File " + str(out) + " was created.")
f.close()
