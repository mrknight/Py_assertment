#!/usr/bin/python

"""
    create the xscore conf for input file
"""

#/prog/drugscore/2011/dsx_linux_64.lnx -P /home/dat/WORK/DB/PDBbind/v2012/1px4/1px4_protein.pdb -L /home/dat/WORK/DB/PDBbind/v2012/1px4/1px4_ligand.mol2 -D /prog/drugscore/2011/pdb_pot_0511/

import os.path
import ioMisc

SOURCE_CONF     = '/home/dat/WORK/scripts/xscore.conf'
PROTEIN_DIR     = '/home/dat/WORK/DB/'

PROTEIN_LIST    = [#'/home/dat/WORK/output/PDBbind_test12.txt',
                   '/home/dat/WORK/output/PDBbind_training12.txt',
                   '',
                   '',
                   '',
                   '',
                   '/home/dat/WORK/output/PDBbind_test07.txt']

lPROTEIN_DB_VER  = ['v2012', 'v2011', 'v2010', 'v2009', 'v2008', 'v2007']


#OUTPUT_DIR      = '/home/dat/DB/output/'

OUTPUT_DIR      = '/home/dat/WORK/output/'

lPROTEIN_STATUS  = ['unprepared', 'prepared', 'nowater']

lPROTEIN_SUFFIX  = ['_protein.pdb', '_protein_proton.pdb']

lPROTEIN_DB      = ['PDBbind', 'CSAR']

LIGAND_SUFFIX    = '_ligand.mol2'  

#################################################################
i = 0

proteinDir  = os.path.join(PROTEIN_DIR, lPROTEIN_DB[0], lPROTEIN_DB_VER[i])

proteinDict = ioMisc.readDictFile(PROTEIN_LIST[i])

#proteinStatus = 0 # unprepared
proteinStatus = 1 # prepared

OUTFILE = open(os.path.join(OUTPUT_DIR, 'dsx_run_'+lPROTEIN_STATUS[proteinStatus]+'.sh'), 'w')

outDir = os.path.join(OUTPUT_DIR, lPROTEIN_STATUS[proteinStatus], lPROTEIN_DB[0], lPROTEIN_DB_VER[i], 'dsx')

OUTFILE.write('cd '+outDir+'\n')

if not os.path.exists(outDir): # try to create the dir path first
    os.makedirs(outDir)

for entry in proteinDict.keys():
    if os.path.isdir(os.path.join(proteinDir, entry)):
        proteinFile = entry + lPROTEIN_SUFFIX[proteinStatus]
        ligandFile  = entry + LIGAND_SUFFIX
        proteinFileWithPath = os.path.join(proteinDir, entry, proteinFile)
        ligandFileWithPath  = os.path.join(proteinDir, entry, ligandFile)            
        if os.path.exists(proteinFileWithPath) and  os.path.exists(ligandFileWithPath):
            # only create config file if the ligand and the protein exist
            OUTFILE.write('/prog/drugscore/2011/dsx_linux_64.lnx -P '+ proteinFileWithPath + ' -L ' + ligandFileWithPath + ' -D /prog/drugscore/2011/pdb_pot_0511/\n')
        else:
            print "File not found ", proteinFile, ' or ', ligandFile, ' in ', os.path.join(proteinDir, entry)
            quit()

print 'Finish creating dsx run.'

OUTFILE.close()

