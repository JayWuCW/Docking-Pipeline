from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation
import pandas as pd
import os
from rdkit.Chem import rdDistGeom #type:ignore

os.makedirs("preped_ligands", exist_ok=True)
EF = rdDistGeom.EmbedFailureCauses

non_retryable = [EF.FINAL_CHIRAL_BOUNDS, EF.CHECK_CHIRAL_CENTERS2,
                 EF.BAD_DOUBLE_BOND_STEREO, EF.LINEAR_DOUBLE_BOND]

rungs = [
    {"randomSeed": 42, "maxIterations": 50,  "useRandomCoords": False},
    {"randomSeed": 7,  "maxIterations": 200, "useRandomCoords": False},
    {"randomSeed": 1,  "maxIterations": 500, "useRandomCoords": True},
]

fired = []
results = []
files = os.listdir()
for file in files:
    if file.endswith(".csv"):
        ligands_df = pd.read_csv(file)

        for index, row in ligands_df.iterrows():
            name = row["name"]
            smiles = row["smiles"]
            completed = "preped_ligands/" + name + ".pdbqt"

            if os.path.exists(completed):
                results.append(name + " already exists, skipped")
                continue

            mol = Chem.MolFromSmiles(smiles) # type: ignore
            if mol is None:
                fired.append(name + " smiles corrupted")
                continue

            else: 
                mol = Chem.AddHs(mol) #type: ignore

                for rung in rungs:
                    params = AllChem.ETKDGv3() #type: ignore
                    params.trackFailures = True
                    params.randomSeed = rung["randomSeed"]
                    params.maxIterations = rung["maxIterations"]
                    params.useRandomCoords = rung["useRandomCoords"]
                    embedded_results = AllChem.EmbedMolecule(mol, params) #type: ignore

                    if embedded_results != -1: #if it succeed
                        break

                    counts = params.GetFailureCounts() # this is the else which is if it fails and got a non retryable
                    for b in non_retryable:
                        if counts[int(b)] > 0:
                            fired.append(name + " " + b.name)
                            break

                if embedded_results == -1:
                    results.append(name + " Failed all rungs")
                    continue

                AllChem.MMFFOptimizeMolecule(mol) # type: ignore
                preparator = MoleculePreparation() # type: ignore
                preparator.prepare(mol)
                preparator.write_pdbqt_file(f"preped_ligands/{name}.pdbqt")

print(fired, results)