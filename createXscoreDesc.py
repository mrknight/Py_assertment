
import os
import csv

XSCORE_HEADER = ["MW", "LogP", "VDW", "HB", "HP", "HM", "HS", "RT"]
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
        desc = readFromTable(path, ligandID) + readFromLog(path, ligandID)
        CSV.writerow(desc)

    CSV.close()

def createXScoreConf(path2Protein, path2Ligand, proteinID, ligandID, outputDir):
#   read the exemplary config and create the new config from given param
    outputConf  = 'xscore_' + ligandID + '.conf'
    OUTFILE = open(outputConf, 'w')

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'xscore_run_'+lPROTEIN_STATUS[proteinStatus]+'.sh'), 'a')

    for line in INFILE:
        if line.find('RECEPTOR_PDB_FILE ') > -1:
            line = 'RECEPTOR_PDB_FILE ' + os.path.join(proteinDir, proteinID, proteinID + lPROTEIN_SUFFIX[proteinStatus] + '\n')
        elif line.find('REFERENCE_MOL2_FILE ') > -1:
            line = 'REFERENCE_MOL2_FILE ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX+'\n')
        elif line.find('LIGAND_MOL2_FILE ') > -1:
            line = 'LIGAND_MOL2_FILE ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX+'\n')
        elif line.find('OUTPUT_TABLE_FILE ') > -1:
            line = 'OUTPUT_TABLE_FILE ' + os.path.join(outputScore, proteinID+'.table\n')
        elif line.find('OUTPUT_LOG_FILE ') > -1:
            line = 'OUTPUT_LOG_FILE ' + os.path.join(outputScore, proteinID+'.log\n')
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('xscore ' + outputConf + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()

def main():
    path        = "/Users/knight/MyClouds/"
    ligandID    = "10gs"


main()