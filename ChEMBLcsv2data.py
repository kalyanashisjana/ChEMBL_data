#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kalyanashisjana
"""

import pandas as pd
from rdkit import Chem

# Load CSV (with tolerant parsing)
df = pd.read_csv(
    "DOWNLOAD-Z1ne6qrt4wu91Pko505qNL8HRHmP9w9SFGyvEarzIcM_eq_.csv",
    sep=';',
    engine='python',
    on_bad_lines='skip'
)


df_filtered = df[
    (df['Molecular Weight'] <= 400) &
    (df['AlogP'] <= 3.5) &
    (df['QED Weighted'] >= 0.5)
]

# Take first 10000 matching entries
df_limited = df_filtered.head(10000)


# Limit to first 1000 entries
#df_limited = df.head(1000)

#print(df[['ChEMBL ID', 'Smiles', 'AlogP', 'HBA', 'HBD']].head())
# Define COOH filter
def has_carboxylic_acid(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        patt = Chem.MolFromSmarts('C(=O)[OH]')
        return mol.HasSubstructMatch(patt)
    except:
        return False

# Apply COOH filter (only to rows with valid SMILES)
df_limited = df_limited[df_limited['Smiles'].notnull()]
df_limited['has_cooh'] = df_limited['Smiles'].apply(has_carboxylic_acid)

# Filter those with COOH
df_cooh = df_limited[df_limited['has_cooh']]

# Save to new CSV
df_cooh.to_csv("carboxylic-mol.csv", index=False)
print("Filtered COOH molecules saved to carboxylic-mol.csv")


columns_to_keep = ['ChEMBL ID', 'Name', 'Smiles', 'AlogP', 'QED Weighted']
df_filtered = df_cooh[columns_to_keep]

df_filtered.to_csv("carboxylic-mol-short.csv", index=False)
print("Saved selected fields to carboxylic-mol-short.csv")
