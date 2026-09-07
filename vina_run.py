import subprocess
import os 

file_list = os.listdir("preped_ligands")
receptor_path = os.path.join("preped_receptors", "AChE_1_ec9a4_relaxed_rank_001_alphafold2_ptm_model_2_seed_000.pdbqt") 
os.makedirs("output", exist_ok=True)
os.makedirs("output/logs", exist_ok=True)
os.makedirs("output/pdbqts", exist_ok=True)
results = []

for file in file_list: 
    ligand_name = file.split(".")[0]
    output_path = os.path.join ("output", "pdbqts", ligand_name + "_output.pdbqt")

    if os.path.exists(output_path) == False and file.endswith(".pdbqt"):
        with open (f"output/logs/{ligand_name}_log.txt", "w") as log_file:
            subprocess.run(["vina", "--receptor", receptor_path, "--ligand", os.path.join("preped_ligands", file), 
                            "--center_x", "0.317", "--center_y", "-1.521", "--center_z", "-8.229", 
                           "--size_x", "25", "--size_y", "25", "--size_z", "25", "--out", 
                           f"output/pdbqts/{ligand_name}_output.pdbqt"], stdout=log_file)

    else: results.append (file + " already exists")

print (results)