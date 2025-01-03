#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Script to shorten contig headers
#### Usage: python conting_name.py /path/to/file/
###############################################################################

import argparse
import fileinput
import os, sys

parser = argparse.ArgumentParser(
    description="""Script to rename contig headers, starting in contig1, 
            including ncbi accession number."""
)

__file__ = "contig_namer.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "0.3"
__date__ = "03-03-2021"

parser.add_argument(
    "inputFile", help="Full path to the input directory where all files are"
)

os.sync()

args = parser.parse_args()
###############################################################################
# Input file
in_file = os.path.abspath(sys.argv[1])
# in_file="/home/sandra/faw-snakemake/data/Endozoicomonas_numazuensis_DSM25634_GCA_000722635.fna"
filename = os.path.basename(in_file)

print("Input file: " + str(in_file))


# Remove file extension (can be fna or fasta)
try:
    name = filename.replace(".fna", "")
except:
    name = name.replace(".fasta", "")
else:
    name = name.replace(".fa", "")

if len(name) > 27:
    name = name[:25]

with open(in_file, "r") as f:
    count = 0
    lines = f.readlines()
    for line in lines:
        if line.strip().startswith(">"):
            count += 1
            k = len(str(count))
f.close()

i = 1
with fileinput.FileInput(in_file, inplace=True) as file:
    for line in file:
        if line.strip().startswith(">"):
            if i < 10:
                kf = k - 1
                title = ">{}_contig".format(name) + kf * "0" + "{}\n".format(i)
                line = title
                i += 1
            elif i < 100:
                kf = k - 2
                title = ">{}_contig".format(name) + kf * "0" + "{}\n".format(i)
                line = title
                i += 1
            elif i < 1000:
                kf = k - 3
                title = ">{}_contig".format(name) + kf * "0" + "{}\n".format(i)
                line = title
                i += 1
            elif i >= 1000 & i < 10000:
                kf = k - 4
                title = ">{}_contig".format(name) + kf * "0" + "{}\n".format(i)
                line = title
                i += 1
        sys.stdout.write(line)
fileinput.close()
###############################################################################
