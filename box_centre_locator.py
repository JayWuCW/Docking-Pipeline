#TRIAD SER234 GLU365 HIS478 = catalytic triad for specifc enzyme
residue_filter = ["CA  SER A 234", "CA  GLU A 365", "CA  HIS A 478"] #replace residues here to run the code
x = []
y = []
z = []

with open("uncleaned_receptors/AChE_1_ec9a4_relaxed_rank_001_alphafold2_ptm_model_2_seed_000.pdb", "r") as f:
    lines = f.readlines()
    for line in lines:
        for residue in residue_filter:
            if residue in line:
                coords = line.split()
                x.append (float(coords[6]))
                y.append (float(coords[7]))
                z.append (float(coords[8]))              

box_centre = round(sum(x)/len(x),3), round(sum(y)/len(y),3), round(sum(z)/len(z),3)
print (box_centre) 