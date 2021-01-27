#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
import pandas as pd
import numpy as np

#%%
df = pd.read_csv("/home/sandra/faw-snakemake/results/Annotation_results/Pfam_counts.csv")
df = df.set_index("index").T

# %%
metadata = pd.read_csv("/home/sandra/faw-snakemake/data/metadata.csv", names =["Genome","Metadata_field"], index_col=None)


#%%
merge = pd.merge(df,metadata, how="left", left_index=True,right_on="Genome")

merge.to_csv("Ready_FS.csv", index=False)
# %%
