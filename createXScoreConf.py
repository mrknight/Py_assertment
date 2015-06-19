#!/usr/bin/python

"""
    create the xscore conf for input file
"""

import os.path
import ioMisc, ioPDBbind
# import constant
from constConf import *

SOURCE_CONF     = '/home/dat/WORK/scripts/xscore.conf'
dockingMethods = ["asp", "plp", "chemscore", "goldscore"]

#################################################################
i = 0

#proteinList = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileCore[i],ioPDBbind.PATHDB+ioPDBbind.nameFileCore[i])
proteinList = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileRefined[i],ioPDBbind.PATHDB+ioPDBbind.nameFileRefined[i])
# TODO: replace with parse_index
proteinDict = ioPDBbind.convertList2Dict(proteinList)


# DEPRECATED: compare the protein list from PDBbind with the used true protein list, to ensure to have the same list
#proteinDict_manual = ioMisc.readDictFile(PROTEIN_INDEXFILE[i])
#if (len(proteinDict_manual.keys()) != len(proteinDict.keys())):
#    proteinDict = proteinDict_manual

proteinDir  = os.path.join(PROTEIN_DIR, lPROTEIN_DB[0], lPROTEIN_DB_VER[i])

print(proteinDir)
#print(proteinDict)

proteinStatus = 0 # unprepared
#proteinStatus = 1 # prepared

def createXScoreConf(proteinStatus, proteinDB, DBver, proteinID):
#   read the exemplary config and create the new config from given param
    outputConf  = 'xscore_' + proteinID + '.conf'
    path = os.path.join(OUTPUT_DIR, 'conf', lPROTEIN_STATUS[proteinStatus], proteinDB, DBver, 'xscore')
    outputConf  = os.path.join(path, outputConf)

    if not os.path.exists(path): # try to create the dir path first
        os.makedirs(path)
    OUTFILE = open(outputConf, 'w')

    outputScore = os.path.join(OUTPUT_DIR, lPROTEIN_STATUS[proteinStatus], proteinDB, DBver, 'xscore')
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)

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

def listFiles(path, pattern):
    if not os.path.exists(path):
        print(path + " not exists")
        return []
    match = [x for x in os.listdir(path) if x.find(pattern) > -1]
    return (match)

def createXScoreConfForDockingPoses(proteinStatus, proteinDB, DBver, proteinID, dockingMethod):
#   read the exemplary config and create the new config from given param

    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'xscore_run_'+DBver+"_RMSD_"+dockingMethod+'.sh'), 'a')


    pose_path = os.path.join(OUTPUT_DIR, DBver, dockingMethod, proteinID)
    outputPath = os.path.join(OUTPUT_DIR, 'conf', "RMSD", DBver, 'xscore', method)
    if not os.path.exists(outputPath): # try to create the dir path first
        os.makedirs(outputPath)

    outputScore = os.path.join(OUTPUT_DIR, "RMSD", DBver, 'xscore', method)
    if not os.path.exists(outputScore): # try to create the output dir for scores
        os.makedirs(outputScore)

    lig_pattern = "gold_soln"
    for pose in listFiles(pose_path, lig_pattern):

        outputConf  = 'xscore_' + '_' + pose + '_' + dockingMethod + '.conf'
        outputConf  = os.path.join(outputPath, outputConf)
    
        OUTFILE = open(outputConf, 'w')
    
        lig_path = os.path.join(OUTPUT_DIR, DBver, dockingMethod, proteinID, pose)
        # open file for reading and writing
        INFILE  = open(SOURCE_CONF, 'r')

        for line in INFILE:
            if line.find('RECEPTOR_PDB_FILE ') > -1:
                line = 'RECEPTOR_PDB_FILE ' + os.path.join(proteinDir, proteinID, proteinID + lPROTEIN_SUFFIX[proteinStatus] + '\n')
            elif line.find('REFERENCE_MOL2_FILE ') > -1:
                line = 'REFERENCE_MOL2_FILE ' + os.path.join(lig_path+'\n')
            elif line.find('LIGAND_MOL2_FILE ') > -1:
                line = 'LIGAND_MOL2_FILE ' + os.path.join(lig_path+'\n')
            elif line.find('OUTPUT_TABLE_FILE ') > -1:
                line = 'OUTPUT_TABLE_FILE ' + os.path.join(outputScore, pose+'_'+method+'.table\n')
            elif line.find('OUTPUT_LOG_FILE ') > -1:
                line = 'OUTPUT_LOG_FILE ' + os.path.join(outputScore, pose+'_'+method+'.log\n')
            OUTFILE.write(line)
    
        # write sh script
        SHFILE.write('xscore ' + outputConf + '\n')
        OUTFILE.close()
        INFILE.close()
    
    SHFILE.close()

# end createXScoreConfFprDockingPoses

def main_old():
    for entry in proteinDict.keys():
        print(entry)
        if os.path.isdir(os.path.join(proteinDir, entry)):
            proteinFile = entry + lPROTEIN_SUFFIX[proteinStatus]
            ligandFile  = entry + LIGAND_SUFFIX
            if os.path.exists(os.path.join(proteinDir, entry, proteinFile)):# and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                # only create config file if the ligand and the protein exist
                #createGoldConf(lPROTEIN_STATUS[0], lPROTEIN_DB[0], lPROTEIN_DB_VER[0], entry, lSCORE[0])
                createXScoreConf(proteinStatus, lPROTEIN_DB[0], lPROTEIN_DB_VER[i], entry)
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()

for entry in proteinDict.keys():
    print(entry)
    if os.path.isdir(os.path.join(proteinDir, entry)):
        proteinFile = entry + lPROTEIN_SUFFIX[proteinStatus]
        for method in dockingMethods:
            #ligandFile  = entry + LIGAND_SUFFIX
            if os.path.exists(os.path.join(proteinDir, entry, proteinFile)):# and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
                # only create config file if the ligand and the protein exist
                #createGoldConf(lPROTEIN_STATUS[0], lPROTEIN_DB[0], lPROTEIN_DB_VER[0], entry, lSCORE[0])
                createXScoreConfForDockingPoses(proteinStatus, lPROTEIN_DB[0], lPROTEIN_DB_VER[i], entry, method)
            else:
                print("File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry))
                quit()

print('Finish creating xscore run.')

