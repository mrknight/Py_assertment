
import subprocess
import os
from constConf import *

SOURCE_CONF     = '/home/dat/WORK/docking_config/gold_pose.conf'
TMP_FILE        = '/home/dat/rmsd.tmp'
GAruns = 50
searchEff = 10

# create a config file to generate docking poses with gold, for any given protein and ligand, output to config dir and outputdir stores the docking results
def createGoldPose(path2protein, proteinID, path2ligand, ligandID, dockingMethod, outputDir, outputConfDir, GAruns = GAruns, searchEff = searchEff):
    outputConf  = 'gold_' + proteinID + '_' + ligandID + '_' + dockingMethod + '.conf'
    if not os.path.exists(outputConfDir): # try to create the dir path first
        os.makedirs(outputConfDir)
    if not os.path.exists(outputDir): # try to create the dir path first
        os.makedirs(outputDir)

    outputConf = os.path.join(outputConfDir, outputConf)
    OUTFILE = open(outputConf, 'w')
    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()
    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')
    if (ligandID[-4:] != "mol2"):
        ligandID = ligandID + ".mol2"

    SHFILE  = open(os.path.join(outputConfDir, 'gold_run_'+dockingMethod+'.sh'), 'a')
    for line in INFILE:
        if line.find('cavity_file =') > -1:
            line = 'cavity_file = ' + os.path.join(path2ligand, ligandID) + '\n'
        elif line.find('ligand_data_file') > -1:
            line = 'ligand_data_file ' + os.path.join(path2ligand, ligandID) + ' ' + str(GAruns) + '\n'
        elif line.find('directory =') > -1:
            line = 'directory = ' + os.path.join(outputDir, proteinID) + '\n'
        elif line.find('protein_datafile =') > -1:
            line = 'protein_datafile = ' + os.path.join(path2protein, proteinID) + '_protein.pdb\n'

        elif line.find('gold_fitfunc_path =') > -1:
            line = 'gold_fitfunc_path = ' + dockingMethod + '\n'
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('gold_auto ' + outputConf + '\n')
    #SHFILE.write('gold_cluster -l h_rt=20:00:00 ' + outputConf + " " + dockingMethod + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def createGoldPosePDBbind(path2PDBbind, PDBbindSet, proteinID, dockingMethod, GAruns = GAruns, searchEff = searchEff):
    path2protein = os.path.join(path2PDBbind, PDBbindSet, proteinID)
    path2ligand = path2protein
    ligandID = proteinID + "_ligand"
    outputDir       = os.path.join(OUTPUT_DIR, PDBbindSet, dockingMethod)
    outputConfDir   = os.path.join(OUTPUT_DIR, "conf", PDBbindSet, dockingMethod)
    createGoldPose(path2protein, proteinID, path2ligand, ligandID, dockingMethod, outputDir, outputConfDir, GAruns = GAruns, searchEff = searchEff)

def createGoldPosePDBbindFromSet(path2PDBbind, PDBbindSet, dockingMethod, GAruns = GAruns, searchEff = searchEff):
    path2protein = os.path.join(path2PDBbind, PDBbindSet)
    index = 0
    for proteinID in os.listdir(path2protein):
        if os.path.isdir(os.path.join(path2protein, proteinID)):
            index = index + 1 # count the number of ligands to be submitted
            #print(proteinID)
            if index > 10000: # can't submit too many jobs at once
                # add a sleep timer to the bash script
                SHFILE  = open(os.path.join(OUTPUT_DIR, 'gold_run_'+dockingMethod+'.sh'), 'a')
                SHFILE.write("sleep 2m\n")
                # reset the counter
                index = 0
            createGoldPosePDBbind(path2PDBbind, PDBbindSet, proteinID, dockingMethod, GAruns = GAruns, searchEff = searchEff)

def createGoldPosePDBbindAllMethods(PDBbindSet):
    for dockingMethod in lSCORE:
        createGoldPosePDBbindFromSet(PDBBIND_DIR, PDBbindSet, dockingMethod, GAruns = GAruns, searchEff = searchEff)


def checkSuccessDocking(outputDir):
    count = 0
    for proteinID in os.listdir(outputDir):
        if os.path.isdir(os.path.join(outputDir, proteinID)):
            match = [1 for x in os.listdir(os.path.join(outputDir, proteinID)) if x.find("gold_soln") > -1]
            if match != []:
                count = count + 1
    return (count)

def calcRMSD(refLigand, calcLigand):
    f = open(TMP_FILE, "w")
    run_cmd = "rms_analysis " + refLigand + " " + calcLigand
    subprocess.call(run_cmd.split(), stdout=f)

def parseRMSDoutput(outputFile = TMP_FILE):
    FILE  = open(outputFile, 'r')
    for line in FILE:
        if line.find('Distance') > -1:
            break # found the identified line
    line = FILE.readline() # read the next line
    return(line.split()[0])

# return a list of RMSDs for all poses in poseDir, pose files are assumed to start with prefix gold_soln
# \TODO: change the prefix
def calcRMSDPoses(refLigand, poseDir):
    RMSDs = {}
    for ligand in os.listdir(poseDir):
        if ligand.startswith("gold_soln"):
            rmsd = calcRMSD(refLigand, os.path.join(poseDir, ligand))
            RMSDs[ligand] = parseRMSDoutput()
    return (RMSDs)

def writeRMSD2CSV(RMSDs, output):
    FILE = open(output, 'w')
    CSV = csv.writer(FILE, delimiter=',')
    # write the csv header
    CSV.writerow(["ID", "RMSDs"])

    for ligandID in RMSDs.keys():
        CSV.writerow(ligandID, RMSDs[ligandID])
    FILE.close()

def main():
    PDBbindSet = "v2012-refined"
    #createGoldPosePDBbindAllMethods(PDBbindSet)
    #createGoldPose("/home/dat/WORK/DB/PDBbind/v2014-refined/3ejp/", "3ejp",
    #               "/home/dat/WORK/DB/PDBbind/v2014-refined/3ejp/", "3ejp_ligand.mol2", dockingMethod, "/home/dat/WORK/output/test/")
    #createGoldPosePDBbind(PDBBIND_DIR, PDBbindSet , "3ejp", dockingMethod)
    calcLigand = "/home/dat/WORK/output/v2014-refined/plp/1hee/" + "gold_soln_1hee_ligand_m1_2.mol2"
    refLigand = "/home/dat/WORK/DB/PDBbind/v2014-refined/1hee/" + "1hee_ligand.mol2"
    calcRMSD(refLigand, calcLigand)
    print(calcRMSDPoses(refLigand, "/home/dat/WORK/output/v2014-refined/plp/1hee/"))
    # print(checkSuccessDocking("/home/dat/WORK/output/v2014-refined/plp/"))
main()