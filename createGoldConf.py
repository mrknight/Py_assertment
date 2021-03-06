#!/usr/bin/python

"""
    create the gold config for gold_auto
"""

import os.path
import ioPDBbind, ioMisc
# import constant
from constConf import *

SOURCE_CONF     = '/home/dat/WORK/docking_config/gold.conf'

#################################################################
i = 0

proteinList = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileCore[i],ioPDBbind.PATHDB+ioPDBbind.nameFileCore[i])


# TODO: replace with parse_index
proteinDict = ioPDBbind.convertList2Dict(proteinList)

proteinDir  = os.path.join(PROTEIN_DIR, lPROTEIN_DB[0], lPROTEIN_DB_VER[i])


proteinStatus = 0 # unprepared
#proteinStatus = 1 # prepared

def createGoldConf(proteinStatus, proteinDB, DBver, proteinID, score):
#   read the exemplary config and create the new config from given param
    outputConf  = 'gold_' + proteinID + '_' + score + '.conf'
    path = os.path.join(OUTPUT_DIR, 'conf', lPROTEIN_STATUS[proteinStatus], proteinDB, DBver, 'gold', score)
    outputConf  = os.path.join(path, outputConf)
    print(outputConf)
    if not os.path.exists(path): # try to create the dir path first
        os.makedirs(path) 
    OUTFILE = open(outputConf, 'w')
    
    outputScore = os.path.join(OUTPUT_DIR, lPROTEIN_STATUS[proteinStatus], proteinDB, DBver, 'gold', score)
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)
    
    # open conf file 
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()
    
    # open file for reading and writing 
    INFILE  = open(SOURCE_CONF, 'r')
    
    SHFILE  = open(os.path.join(OUTPUT_DIR, 'gold_run_'+score+'_'+lPROTEIN_STATUS[proteinStatus]+'.sh'), 'a')
    
    for line in INFILE:
        if line.find('cavity_file =') > -1:
            line = 'cavity_file = ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + '\n')
        elif line.find('ligand_data_file') > -1:
            line = 'ligand_data_file ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX) + ' 10\n'         
        elif line.find('directory =') > -1:
            line = 'directory = ' + os.path.join(outputScore, proteinID + '\n')
        elif line.find('protein_datafile =') > -1:
            line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + lPROTEIN_SUFFIX[proteinStatus] + '\n')
            if ((proteinID == '1xgj') or (proteinID == '2pu2')) and (proteinStatus == 1): #prepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_proton_f.pdb\n')
            if ((proteinID == '1w3l')) and (proteinStatus == 0): #unprepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_f.pdb\n')
            if ((proteinID == '1b9j')) and (proteinStatus == 0) and (DBver=="v2007"): #unprepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_del.pdb\n')
            if ((proteinID == '1b7h')) and (proteinStatus == 0) and (DBver=="v2007"): #unprepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_del.pdb\n')
                
        elif line.find('gold_fitfunc_path =') > -1:
            line = 'gold_fitfunc_path = ' + score + '\n'
        OUTFILE.write(line)
    
    # write sh script
    SHFILE.write('gold_auto ' + outputConf + '\n')
    
    SHFILE.close()
    INFILE.close()
    OUTFILE.close()


def main():
    for aScore in lSCORE:
        for entry in proteinDict.keys():
            if os.path.isdir(os.path.join(proteinDir, entry)):
                proteinFile = entry + lPROTEIN_SUFFIX[proteinStatus]
                ligandFile  = entry + LIGAND_SUFFIX
                if os.path.exists(os.path.join(proteinDir, entry, proteinFile)) and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                    # only create config file if the ligand and the protein exist
                    #createGoldConf(lPROTEIN_STATUS[0], lPROTEIN_DB[0], lPROTEIN_DB_VER[0], entry, lSCORE[0])
                    createGoldConf(proteinStatus, lPROTEIN_DB[0], lPROTEIN_DB_VER[i], entry, aScore)
                else:
                    print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                    quit()
            else:
                print(os.path.join(proteinDir, entry) + " is not exist\n")
        print('Finish creating gold_run for '+ aScore + lPROTEIN_STATUS[proteinStatus])

main()