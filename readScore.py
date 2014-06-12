#!/usr/bin/python

import ioScore, ioMisc 
import os.path

PROTEIN_DIR     = '/home/dat/WORK/DB/'

TEST_LIST_PDB   = ['/home/dat/WORK/output/PDBbind_test12.txt',
                   '',
                   '',
                   '',
                   '',
                   '/home/dat/WORK/output/PDBbind_test07.txt']

TEST_LIST_CSAR  = ['/home/dat/WORK/DB/CSAR_NRC_HiQ_Set_24Sept2010/Separation/set1.txt',
                   '/home/dat/WORK/DB/CSAR_NRC_HiQ_Set_24Sept2010/Separation/set2.txt']

OUTPUT_DIR      = '/home/dat/WORK/output/'

PROTEIN_STATUS  = ('unprepared', 'prepared')

tPROTEIN_DB      = ('PDBbind', 'CSAR')

DB_PDBbind      = ('v2012', 'v2011', 'v2010', 'v2009', 'v2008', 'v2007')
DB_CSAR         = ('set1', 'set2')

#PROTEIN_DB      = [[''.join(('PDBbind/', entry)) for entry in DB_PDBbind]]
#PROTEIN_DB.append([''.join(('CSAR/', entry)) for entry in DB_CSAR])

PROTEIN_DB      = {tPROTEIN_DB[0]:DB_PDBbind, 
                   tPROTEIN_DB[1]:DB_CSAR}

TEST_LIST       = {tPROTEIN_DB[0]:TEST_LIST_PDB, 
                   tPROTEIN_DB[1]:TEST_LIST_CSAR}

scoreListGOLD   = ['plp', 'goldscore', 'chemscore', 'asp']
scoreListXSCORE = ['HPScore', 'HMScore', 'HSScore']
scoreListPARA   = ['DrugScore', 'pScore', 'PMF']



proteinStatus = 0 # unprepared
#proteinStatus = 1 # prepared
#DBset   = 0 # PDBbind
#DBver   = 0 # v2012
#DBver   = 5 # v2007
DBset   = 1 # CSAR

#DBver   = 0 # CSAR set1
DBver   = 1 # CSAR set2

proteinDict = ioMisc.readDictFile(TEST_LIST[tPROTEIN_DB[DBset]][DBver])

pathOutput  = os.path.join(OUTPUT_DIR, PROTEIN_STATUS[proteinStatus], tPROTEIN_DB[DBset], PROTEIN_DB[tPROTEIN_DB[DBset]][DBver])

scoreDict   = {}

for protein in proteinDict.keys():
    scoreDict[protein] = [float(proteinDict[protein])]
    ##### read score from GOLD #####
    for score in scoreListGOLD:
        scoreFile = os.path.join(pathOutput, 'gold', score, protein, 'rescore.log')
        readScore   = ioScore.readGOLDScore(scoreFile)
        #print protein, ' ', score,'\t', readScore
        scoreDict[protein].append(readScore)
    ##### read score from XScore #####        
    scoreFile = os.path.join(pathOutput, 'xscore', protein+'.table')
    readScore = ioScore.readXScore(scoreFile)
    for eachScore in readScore:
        scoreDict[protein].append(eachScore)
    ##### read score from DSX #####
    if proteinStatus == 0:
        scoreFile = os.path.join(pathOutput, 'dsx', 'DSX_'+protein+'_protein_'+protein+'_ligand.txt')
    else:
        scoreFile = os.path.join(pathOutput, 'dsx', 'DSX_'+protein+'_protein_proton_'+protein+'_ligand.txt')
    readScore   = ioScore.readDSXScore(scoreFile)
    scoreDict[protein].append(readScore)
    ##### read score from ParaDocks #####
    if ((proteinStatus == 1) and (DBset == 0)) or (DBset==1): # ParaDocks still won't work with original PDBbind protein
        scoreFile = os.path.join(pathOutput, 'paradocks', protein ,'ParaDockS_results.table')
        readScore = ioScore.readPARAScore(scoreFile)
        for eachScore in readScore:
            scoreDict[protein].append(eachScore)

scoreList   = ['PDB','experimental'] + scoreListGOLD + scoreListXSCORE + ['DSX']
if ((proteinStatus == 1) and (DBset == 0)) or (DBset==1):
    scoreList = scoreList + scoreListPARA
CSVfile     = os.path.join(OUTPUT_DIR, PROTEIN_STATUS[proteinStatus], tPROTEIN_DB[DBset]+'_'+PROTEIN_DB[tPROTEIN_DB[DBset]][DBver]+'_'+PROTEIN_STATUS[proteinStatus]+'.csv') 
print CSVfile
ioScore.writeScoreCSV(scoreList, scoreDict, outFile=CSVfile)

#for a in sorted(proteinCoreList, key=attrgetter('cluster', 'ECnum')):
#    print a

#count = 0
#for protein in proteinRefinedList:
#    if protein.name.find('TRYPSIN') > -1:    
#    if protein.name=='TRYPSIN':
#        count = count + 1
#        print protein

