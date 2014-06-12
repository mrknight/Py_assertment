#!/usr/bin/python

##########################################################
#
#    create the % ratio of ranking from a given score
#
##########################################################


import os.path
import ioPDBbind, ioScore, ioMisc
import libRank

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
scoreListML     = ['BRT','SVM','RF']

proteinStatus = 0 # unprepared
#proteinStatus = 1 # prepared
DBset   = 0 # PDBbind
#DBver   = 0 # v2012
DBver   = 5 # v2007

#DBset   = 1 # CSAR
#DBver   = 0 # CSAR set1
#DBver   = 1 # CSAR set2

####################################################
# read scores matrix from CSV
####################################################

scoresMatrix = {}
import csv

CSVinput  = os.path.join(OUTPUT_DIR, PROTEIN_STATUS[proteinStatus], 
                          tPROTEIN_DB[DBset] + '_' + PROTEIN_DB[tPROTEIN_DB[DBset]][DBver] + '_' +
                          #PROTEIN_STATUS[proteinStatus] + '.csv') 
                          PROTEIN_STATUS[proteinStatus] + '_all.csv')
                          #PROTEIN_STATUS[proteinStatus] + '_SFC-RF_all.csv')
with open(CSVinput, 'rb') as f:
    reader = csv.DictReader(f)
    scoreCol = {}
    for row in reader:
        scoresMatrix[row['PDB']] = row        

scoreList   = ['experimental'] + scoreListGOLD + scoreListXSCORE + ['DSX']
if ((proteinStatus == 1) and (DBset == 0)) or (DBset==1):
    scoreList = scoreList + scoreListPARA

scoreList = scoreList + scoreListML

proteinDict = ioMisc.readDictFile(TEST_LIST[tPROTEIN_DB[DBset]][DBver])

proteinCoreList     = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileCore[DBver],ioPDBbind.PATHDB+ioPDBbind.nameFileCore[DBver])

proteinRefinedList  = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileRefined[DBver],ioPDBbind.PATHDB+ioPDBbind.nameFileRefined[DBver])

proteinRefinedDict  = ioPDBbind.convertList2Dict(proteinRefinedList)

proteinCoreDictCluster  = ioPDBbind.convertList2DictCluster(proteinCoreList)

def calcRanking(aScore, outFile):
    print aScore
    # reset the ranking count
    dRankingCount = { '123':0, '132':0, '213':0, '231':0, '312':0, '321':0 }
    # reset the clusterDict    
    clusterDict         = ioPDBbind.createClusterDict(proteinCoreList)
    
    for proteinID in proteinDict.keys(): 
        cluster = proteinCoreDictCluster[proteinID]
        proteinInCluster = clusterDict[cluster]
        for i in range(len(proteinInCluster)):
            if proteinInCluster[i] == proteinID:
                #print proteinID, scoresMatrix[proteinID][aScore], clusterDict[cluster]
                #print scoresMatrix[proteinID][aScore]
                clusterDict[cluster][i] = scoresMatrix[proteinID][aScore]

    for value in clusterDict.values():    
        #tmp = ''.join(str(i+1) for i in libRank.rank(map(float, value)))
        tmp = ''.join(str(i+1) for i in libRank.rank(map(abs, map(float, value))))
        if (tmp != '123'):
            print value, libRank.rank(value)
        dRankingCount[tmp] = dRankingCount[tmp] + 1 
    
    #print dRankingCount

    totalCluster = len(clusterDict.keys())
    
    OUTFILE = open(outFile, 'a')    
    OUTFILE.write(aScore + '\t')
    for rank in sorted(dRankingCount.keys()):
        ranking = float(dRankingCount[rank])/totalCluster * 100
        print rank, ranking
        OUTFILE.write(str(ranking)+'\t')
    OUTFILE.write('\n')
    OUTFILE.close()

        
rankOutput  = os.path.join(OUTPUT_DIR, PROTEIN_STATUS[proteinStatus], 
                          tPROTEIN_DB[DBset] + '_' + PROTEIN_DB[tPROTEIN_DB[DBset]][DBver] + '_' +
                          PROTEIN_STATUS[proteinStatus] + '_all.txt') 
                          #PROTEIN_STATUS[proteinStatus] + '_rank.txt')
                          #PROTEIN_STATUS[proteinStatus] + '_SFC-RF_rank.txt')

for aScore in scoreList:
    calcRanking(aScore, rankOutput)

