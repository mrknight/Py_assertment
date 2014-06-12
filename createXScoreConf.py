#!/usr/bin/python

"""
    create the xscore conf for input file
"""

import os.path
import ioMisc, ioPDBbind

SOURCE_CONF     = '/home/dat/WORK/scripts/xscore.conf'
PROTEIN_DIR     = '/home/dat/WORK/DB/'

PROTEIN_LIST    = ['/home/dat/WORK/output/PDBbind_test12.txt',
                   '',
                   '',
                   '',
                   '',
                   '/home/dat/WORK/output/PDBbind_test07.txt']

lPROTEIN_DB_VER  = ['v2012', 'v2011', 'v2010', 'v2009', 'v2008', 'v2007']

OUTPUT_DIR      = '/home/dat/WORK/output/'

#lSCORE          = ['HPScore', 'HMScore', 'HSScore']

lPROTEIN_STATUS  = ['unprepared', 'prepared']

lPROTEIN_DB      = ['PDBbind', '']

lPROTEIN_SUFFIX   = ['_protein.pdb', '_protein_proton.pdb',]
LIGAND_SUFFIX    = '_ligand.mol2'  

#################################################################
i = 5
proteinList = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileCore[i],ioPDBbind.PATHDB+ioPDBbind.nameFileCore[i])

proteinDict = ioPDBbind.convertList2Dict(proteinList)

# compare the protein list from PDBbind with the used true protein list, to ensure to have the same list
proteinDict_manual = ioMisc.readDictFile(PROTEIN_LIST[i]) 

if (len(proteinDict_manual.keys()) != len(proteinDict.keys())):    
    proteinDict = proteinDict_manual

proteinDir  = os.path.join(PROTEIN_DIR, lPROTEIN_DB[0], lPROTEIN_DB_VER[i])

#proteinStatus = 0 # unprepared
proteinStatus = 1 # prepared

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
        print "File not found ", SOURCE_CONF   
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


for entry in proteinDict.keys():
    if os.path.isdir(os.path.join(proteinDir, entry)):
        proteinFile = entry + lPROTEIN_SUFFIX[proteinStatus]
        ligandFile  = entry + LIGAND_SUFFIX
        if os.path.exists(os.path.join(proteinDir, entry, proteinFile)) and  os.path.exists(os.path.join(proteinDir, entry, ligandFile)):
            # only create config file if the ligand and the protein exist
            #createGoldConf(lPROTEIN_STATUS[0], lPROTEIN_DB[0], lPROTEIN_DB_VER[0], entry, lSCORE[0])
            createXScoreConf(proteinStatus, lPROTEIN_DB[0], lPROTEIN_DB_VER[i], entry)
        else:
            print "File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry)
            quit()

print 'Finish creating xscore run.'

