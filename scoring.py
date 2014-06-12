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
# create protein dict with pKd value 
coreDict    = ioPDBbind.convertList2Dict(core)

ioMisc.writeListWithScore2File(coreDict.keys(), coreDict, '/home/dat/WORK/core')