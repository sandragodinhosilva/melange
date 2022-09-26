#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#### Goal: remove "-" from begining of lines in FASTA files
#### Usage: python fasta_cleaner.py /path/to/directory_wt_all_files/
#### Note: provide full path!
###############################################################################

import argparse
import fileinput
import os, sys

parser = argparse.ArgumentParser(
    description="""Goal: remove "-" from begining of lines in FASTA files."""
)

__file__ = "orf_annotation.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "0.2"
__date__ = "05-12-2020"

parser.add_argument(
    "inputDirectory", help="Specify the directory containing *.fa files"
)

# Execute parse_args()
args = parser.parse_args()

inputDirectory = sys.argv[1]
###############################################################################
curdir = inputDirectory
os.chdir(curdir)

entries = os.listdir(curdir)

print("Starting...")

for filename in entries:
    if ".fa" in filename:
        filepath = os.path.join(curdir, filename)
        with fileinput.FileInput(filepath, inplace=True) as file:
            for line in file:
                if line.strip().startswith("-"):
                    line = line.replace("-", "")
                sys.stdout.write(line)
            fileinput.close()

print("Removed '-' from the beginning of all lines that started with it.")
###############################################################################
