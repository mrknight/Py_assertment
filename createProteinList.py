#!/usr/bin/python

##########################################################
#
#    
#
##########################################################

import  ioMisc
import  ioPDBbind

i = 0
core    = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileCore[i],ioPDBbind.PATHDB+ioPDBbind.nameFileCore[i])

refined = ioPDBbind.readProteinInfo(ioPDBbind.PATHDB+ioPDBbind.dataFileRefined[i],ioPDBbind.PATHDB+ioPDBbind.nameFileRefined[i])

# create protein dict with pKd value 
coreDict    = ioPDBbind.convertList2Dict(core)
refinedDict = ioPDBbind.convertList2Dict(refined)

test        = ioMisc.createDisjointList(refinedDict.keys(), coreDict.keys())

for each in test:
    print each

ioMisc.writeListWithScore2File(test, refinedDict, '/home/dat/WORK/output/training.2012')
ioMisc.writeListWithScore2File(coreDict.keys(), coreDict, '/home/dat/WORK/output/core.2012')