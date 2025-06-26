# ChEMBL_data_extraction
These Python scripts can be used to download the SMILES ID of molecules having a particular functional group. There are two types of script given. ChEMBLonline2data.py script can directly extract data from the ChEMBL molecules list. On the other hand, ChEMBLcsv2data.py can extract data from the downloaded CSV file. A CSV file of 2.5 million small molecule can be downloaded from "https://www.ebi.ac.uk/chembl/explore/compounds/STATE_ID:H0G-XSIEQn93qa0ndtL4sw%3D%3D"


In these scripts, I extracted molecules with the "C(=O)O" SMILES string, focusing on carboxylic group-containing molecules. I have also applied the molecular weight and logP cut-off. Depending on the application, any other cut-off can also be applied. 

#  beta-lactam antibiotic series
For the beta-lactam antibiotic series, a **Generalized SMARTS** pattern for beta-lactam
beta_lactam_smarts = "[NX3;R][CX4;R][CX4;R][CX3;R](=O)"
# Sulfonamides series
NS(=O)(=O)c
