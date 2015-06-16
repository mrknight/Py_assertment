
import os
import csv
import ioPDBbind
from constConf import *

XSCORE_HEADER = ["ID", "MW", "LogP", "VDW", "HB", "HP", "HM", "HS", "RT"]
SOURCE_CONF   = '/home/dat/WORK/scripts/xscore.conf'


def readFromLog(path, ligandID):
    file = os.path.join(path, ligandID + '.log')
    LOGFILE = open(file, 'r')
    for line in LOGFILE:
        if (line.split() != []):
            if (line.split()[0]) == "Total":
                return (line.split()[1:7])

def readFromTable(path, ligandID):
    file = os.path.join(path, ligandID + '.table')
    LOGFILE = open(file, 'r')
    line = LOGFILE.readline() # skip the first line
    line = LOGFILE.readline()
    return (line.split()[2:4])

def writeXScoreDesc(path, ligandList, output):
    FILE = open(output, 'w')
    CSV = csv.writer(FILE, delimiter=',')
    # write the csv header
    CSV.writerow(XSCORE_HEADER)

    for ligandID in ligandList:
        desc = [ligandID] + readFromTable(path, ligandID) + readFromLog(path, ligandID)
        CSV.writerow(desc)
    FILE.close()

# create xscore config file for a protein and a ligand, output config file will be written to outputDir
def createXScoreConf(path2protein, proteinID, path2ligand, ligandID, outputDir, outputConfDir):
#   read the exemplary config and create the new config from given param
    outputConf  = 'xscore_' + ligandID + '.conf'
    confPath = os.path.join(outputConfDir, outputConf)
    OUTFILE = open(confPath, 'w')

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'xscore_run_'+proteinID+'.sh'), 'a')
    if (ligandID[-4:] != "mol2"):
        ligandID = ligandID + ".mol2"
    for line in INFILE:
        if line.find('RECEPTOR_PDB_FILE ') > -1:
            line = 'RECEPTOR_PDB_FILE ' + os.path.join(path2protein, proteinID + '.pdb\n')
        elif line.find('REFERENCE_MOL2_FILE ') > -1:
            line = 'REFERENCE_MOL2_FILE ' + os.path.join(path2ligand, ligandID + '\n')
        elif line.find('LIGAND_MOL2_FILE ') > -1:
            line = 'LIGAND_MOL2_FILE ' + os.path.join(path2ligand, ligandID + '\n')
        elif line.find('OUTPUT_TABLE_FILE ') > -1:
            line = 'OUTPUT_TABLE_FILE ' + os.path.join(outputDir, ligandID + '.table\n')
        elif line.find('OUTPUT_LOG_FILE ') > -1:
            line = 'OUTPUT_LOG_FILE ' + os.path.join(outputDir, ligandID + '.log\n')
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('xscore ' + confPath + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def createXScoreConfFromDir(path2protein, proteinID, path2ligand, outputDir, outputConfDir):
    for ligandID in os.listdir(path2ligand):
        createXScoreConf(path2protein, proteinID, path2ligand, ligandID, outputDir, outputConfDir)

def main():
    proteinList = ioPDBbind.readProteinInfo("/home/dat/WORK/DB/PDBbind/v2012-refined/INDEX_refined_data.2012", "/home/dat/WORK/DB/PDBbind/v2012-refined/INDEX_refined_name.2012")
    proteinDict = ioPDBbind.convertList2Dict(proteinList)
    createXScoreConfFromDir("/home/dat/WORK/DB/DUD-E/docked_by_Rognan/FGFR1/", "protein_prep",
                     "/home/dat/WORK/DB/DUD-E/docked_by_Rognan/FGFR1/docked",
                     "/home/dat/WORK/output/DUD-E/FGFR1/",
                     "/home/dat/WORK/output/conf/DUD-E/FGFR1/")


main()