#!/usr/bin/python

##########################################################
#
#    create the % ratio of ranking from a given score
#
##########################################################


import os.path
import ioPDBbind, ioScore
import libRank
# from ioPDBbind import *

scoreDir    = '/home/dat/WORK/output/unprepared/PDBbind/v2012/gold/asp/'

dRankingCount = { '123':0, '132':0, '213':0, '231':0, '312':0, '321':0 }

#for i in range(6):
#    proteinList = readProteinInfo(PATHDB+dataFile[i],PATHDB+nameFile[i])
#
#    for aProtein in proteinList:
#        if aProtein.id == '2f80':
#            print i, aProtein

i = 0

proteinCoreList     = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileCore[i],ioPDBbind.PATHDB+ioPDBbind.nameFileCore[i])

proteinRefinedList  = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileRefined[i],ioPDBbind.PATHDB+ioPDBbind.nameFileRefined[i])

proteinRefinedDict  = ioPDBbind.convertList2Dict(proteinRefinedList)

clusterDict         = ioPDBbind.createClusterDict(proteinCoreList)

proteinCoreDictCluster  = ioPDBbind.convertList2DictCluster(proteinCoreList)

##
pathOutput      = '/home/dat/WORK/output/'

#print clusterDict[proteinCoreDictCluster['1w3l']] 
for entry in os.listdir(scoreDir):    
    if os.path.isdir(os.path.join(scoreDir, entry)):
        proteinID = entry
        scoreFile = os.path.join(scoreDir, proteinID, 'rescore.log')
        ##
        scoreFile = os.path.join(pathOutput, 'prepared/PDBbind/v2012/xscore', proteinID+'.table')
        cluster = proteinCoreDictCluster[proteinID]
        proteinInCluster = clusterDict[cluster]
        for i in range(len(proteinInCluster)):
            if proteinInCluster[i] == proteinID:
                ##clusterDict[cluster][i] = ioScore.readGOLDScore(scoreFile)
                clusterDict[cluster][i] = ioScore.readXScore(scoreFile)[1]
print proteinCoreDictCluster
print clusterDict['368']
print clusterDict[proteinCoreDictCluster['1w3l']]
print libRank.rank(clusterDict[proteinCoreDictCluster['1w3l']])
for value in clusterDict.values():
    tmp = ''.join(str(i+1) for i in libRank.rank(value))
    dRankingCount[tmp] = dRankingCount[tmp] + 1 
    
print dRankingCount

totalCluster = len(clusterDict.keys())

print totalCluster

for rank in sorted(dRankingCount.keys()):
    print rank, float (dRankingCount[rank])/totalCluster * 100

