import subprocess
import os 

file_list = os.listdir("preped_ligands")
receptor_path = os.path.join("preped_receptors", "AF-P22303-2-F1-model_v6.pdbqt") 

os.makedirs("output", exist_ok=True)
os.makedirs("output/logs", exist_ok=True)
os.makedirs("output/pdbqts", exist_ok=True)

for file in file_list: 
    ligand_name = file.split(".")[0]
    if file.endswith(".pdbqt"): 
        with open (f"output/logs/{ligand_name}_log.txt", "w") as log_file:

            subprocess.run(["vina", "--receptor", receptor_path, "--ligand", os.path.join("preped_ligands", file), 
                            "--center_x", "4.144", "--center_y", "10.064", "--center_z", "-3.626", 
                           "--size_x", "25", "--size_y", "25", "--size_z", "25", "--out", 
                           f"output/pdbqts/{ligand_name}_output.pdbqt"], stdout=log_file)