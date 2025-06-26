#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kalyanashisjana
"""

import requests
import csv
import time

# SMILES for carboxylic acid group
cooh_smiles = "C(=O)O"

# Output CSV file
output_file = "chembl_cooh_filtered_molecules.csv"

# CSV Header
header = ["chembl_id", "smiles", "molecular_weight", "logP"]

# Property filters
min_mw = 100
max_mw = 500
min_logp = -2
max_logp = 5

# Open CSV to write results
with open(output_file, mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    offset = 0
    limit = 100
    max_entries = 1000  # Change as needed
    total_saved = 0

    while total_saved < max_entries:
        url = f"https://www.ebi.ac.uk/chembl/api/data/substructure.json?smiles={cooh_smiles}&limit={limit}&offset={offset}"
        res = requests.get(url)
        data = res.json()

        if "molecules" not in data or len(data["molecules"]) == 0:
            print("No more molecules found.")
            break

        for mol in data["molecules"]:
            chembl_id = mol["molecule_chembl_id"]

            # Get full molecule info to extract SMILES, MW, logP
            mol_url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
            mol_res = requests.get(mol_url)
            mol_data = mol_res.json()

            try:
                smiles = mol_data["molecule_structures"]["canonical_smiles"]
                props = mol_data.get("molecule_properties", {})
                mw = float(props.get("full_mwt", 0))
                logp = float(props.get("alogp", 0))

                if min_mw <= mw <= max_mw and min_logp <= logp <= max_logp:
                    writer.writerow([chembl_id, smiles, mw, logp])
                    total_saved += 1
                    print(f"Saved: {chembl_id} | MW: {mw:.1f}, logP: {logp:.2f}")
            except (TypeError, KeyError, ValueError):
                print(f"Skipping {chembl_id} - missing data.")

            time.sleep(0.1)  # Be respectful of the API

        offset += limit
