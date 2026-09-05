import subprocess
import os
os.makedirs("cleaned_receptors", exist_ok=True)
os.makedirs("preped_receptors", exist_ok=True)

if not os.path.exists ("uncleaned_receptors"):
    os.makedirs("uncleaned_receptors")
    print ("put all receptor pdbs in uncleaned_receptors, run script again after.")
    exit()
    
files = os.listdir("uncleaned_receptors") 

for file in files:
    if not file.endswith (".pdb"):
        continue 
    
    elif not os.path.exists("preped_receptors/" + os.path.splitext(file)[0] + ".pdbqt"):

        input_path = os.path.join("uncleaned_receptors", file)
        list = []     
        with open (input_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith("ATOM") or line.startswith("TER"):
                list.append(line)

        with open ("cleaned_receptors" +"/" + file, "w") as w:
            w.writelines(list)

        cleaned_input = os.path.join ("cleaned_receptors", file)
        output_path = f"preped_receptors/{os.path.splitext(file)[0]}"
        result = subprocess.run(["python", "-m", "meeko.cli.mk_prepare_receptor", "--read_pdb", cleaned_input , "-o", output_path, "-p", "-x",
                                  "--default_altloc", "A"], capture_output=True, text=True)
        print(f"--- {file} ---")
        print(result.stdout)
        print(result.stderr)

    else:
        print (file + " already  exists")