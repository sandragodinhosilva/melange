#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
import argparse
import sys

parser = argparse.ArgumentParser(
    description="""Join CAZyme annotations in one table."""
)

__file__ = "cazymes_parser.py"
__author__ = "Sandra Godinho Silva (sandragodinhosilva@gmail.com)"
__version__ = "0.1"
__date__ = "September 9th, 2022"

parser.add_argument("inputFile", help="Full path to input file")

# Execute parse_args()
args = parser.parse_args()
###############################################################################
# import standard Python modules
import os
import pandas as pd
import re

###############################################################################
# in_file = "/home/sandra/MeLanGE/results/Annotation/GCF_003018455.1_ASM301845v1_genomic_merops.txt"
in_file = sys.argv[1]

filename = os.path.basename(in_file)
filename = filename.replace("overview.txt", "")
output_dir = os.path.dirname(in_file)

list_stacked = pd.DataFrame()

df = pd.read_csv(in_file, sep="	")
df["sample"] = filename
# remove parentheses and everything inside from HMMER column
df["HMMER"] = df["HMMER"].str.replace(r"\(.*\)", "")
list_stacked = pd.concat([list_stacked, df])

# dataframe with all results
list_stacked.to_csv(os.path.join(output_dir, filename + "_all_cazymes.csv"))

# rearranging the data
df_treated = list_stacked.copy()

# create table for orfs that were annotated by all 3 tools
df_treated_3 = df_treated[df_treated["#ofTools"] == 3]
df_treated_3[["Gene ID", "HMMER"]].to_csv(
    os.path.join(output_dir, filename + "_cazymes_3tools.txt"), sep="\t", index=False
)

# create table for orfs that were annotated by all 2 tools
# df_treated_2 = df_treated[df_treated["#ofTools"] == 2]
# df_treated_2 = df_treated_3[["HMMER", "sample"]]
# df_final2 = df_treated_2[["HMMER","sample"]].value_counts().reset_index().pivot_table(index=["HMMER"],columns=["sample"] ).fillna(0).droplevel(0, axis=1)
# df_final2 = df_final2.apply(pd.to_numeric, errors = 'coerce', downcast="integer")
# df_final2.to_csv(os.path.join(output_dir,  filename + "_cazymes_2tools.csv"))

###############################################################################
print("Finished with success!")
