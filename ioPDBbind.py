'''
Created on 17.04.2013

@author: dat

read and write function for PDBbind
'''

import os.path
import collections

# some constant
PATHDB          = '/home/dat/WORK/DB/PDBbind/'

#PATHDB          = '/mnt/DATABASES/BENCHMARK/'

CLUSTERFILE     = 'v2012/INDEX_core_cluster.2012'

PDBbindYear     = collections.namedtuple('Year', 'y2012 y2011 y2010 y2009 y2008 y2007')

dataFileCore    = PDBbindYear(y2012='v2012/INDEX_core_data.2012',
                              y2011='v2011/INDEX_core_data.2011',
                              y2010='v2010/INDEX.core.data.2010',
                              y2009='v2009/INDEX.core.data.2009',
                              y2008='v2008/INDEX.core.data.2008',
                              y2007='v2007/INDEX.2007.core.data_fix') 

#dataFileCore    = PDBbindYear(y2012='v2012/INDEX_core_data.2012',
#                              y2011='v2011/INDEX_core_data.2011',
#                              y2010='v2010/INDEX.core.data.2010',
#                              y2009='v2009/INDEX.core.data.2009',
#                              y2008='v2008/INDEX.core.data.2008',
#                              y2007='v2007/INDEX.2007.core.data') 

#dataFileCore    = (    'v2012/INDEX_core_data.2012',
#                       'v2011/INDEX_core_data.2011',
#                       'v2010/INDEX.core.data.2010',
#                       'v2009/INDEX.core.data.2009',
#                       'v2008/INDEX.core.data.2008',
#                       'v2007/INDEX.2007.core.data')

nameFileCore    = PDBbindYear(y2012='v2012/INDEX_core_name.2012',
                              y2011='v2011/INDEX_core_name.2011',
                              y2010='v2010/INDEX.core.name.2010',
                              y2009='v2009/INDEX.core.name.2009',
                              y2008='v2008/INDEX.core.name.2008',
                              y2007='v2007/INDEX.2007.core.name_fix')
#nameFileCore    = (    'v2012/INDEX_core_name.2012',
#                       'v2011/INDEX_core_name.2011',
#                       'v2010/INDEX.core.name.2010',
#                       'v2009/INDEX.core.name.2009',
#                       'v2008/INDEX.core.name.2008',
#                       'v2007/INDEX.2007.core.name')

dataFileRefined = PDBbindYear(y2012='v2012/INDEX_refined_data.2012',
                              y2011='v2011/INDEX_refined_data.2011',
                              y2010='v2010/INDEX.refined.data.2010',
                              y2009='v2009/INDEX.refined.data.2009',
                              y2008='v2008/INDEX.refined.data.2008',
                              y2007='v2007/INDEX.2007.refined.data')

#dataFileRefined    = (    'v2012/INDEX_refined_data.2012',
#                          'v2011/INDEX_refined_data.2011',
#                          'v2010/INDEX.refined.data.2010',
#                          'v2009/INDEX.refined.data.2009',
#                          'v2008/INDEX.refined.data.2008',
#                          'v2007/INDEX.2007.refined.data')

nameFileRefined = PDBbindYear(y2012='v2012/INDEX_refined_name.2012',
                              y2011='v2011/INDEX_refined_name.2011',
                              y2010='v2010/INDEX.refined.name.2010',
                              y2009='v2009/INDEX.refined.name.2009',
                              y2008='v2008/INDEX.refined.name.2008',
                              y2007='v2007/INDEX.2007.refined.name')

#nameFileRefined    = (    'v2012/INDEX_refined_name.2012',
#                          'v2011/INDEX_refined_name.2011',
#                          'v2010/INDEX.refined.name.2010',
#                          'v2009/INDEX.refined.name.2009',
#                          'v2008/INDEX.refined.name.2008',
#                          'v2007/INDEX.2007.refined.name')


def readNameFile(nameFile):
# read ECnumber and protein name from name list file
# return a dict of tuples with key = protein id and 1.index = EC number, 2.index = protein name
    if not os.path.exists(nameFile):
        print "File not found ", nameFile   
        quit()
    
    FILE = open(nameFile, 'r')
    
    Protein = collections.namedtuple('Protein', 'ECnum name') 
    
    proteinDict = {}
    # read each line
    for line in FILE:
        # skip comments
        if not (line[0] == '#'):
            protein = line.split()
            if len(protein[1])==4: # detect release year entry, for PDBbind version after 2010
                tmpProtein = Protein(ECnum=protein[2], name=''.join(protein[3:]))
            else: # if no release year entry, then PDBbind version is prior 2010
                tmpProtein = Protein(ECnum=protein[1], name=''.join(protein[2:]))
            proteinDict[protein[0]] = tmpProtein
        
    FILE.close()
    return proteinDict

def readClusterFile(clusterFile):
# read cluster info (since PDBbind ver 2012)
    if not os.path.exists(clusterFile):
        print "File not found ", clusterFile   
        quit()   
    
    FILE = open(clusterFile, 'r')
    proteinDict = {}
    for line in FILE:
        # skip comment
        if not (line[0] == '#'):
            protein = line.split(None)            
            proteinDict[protein[0]] = ''.join(protein[5:6])
    
    FILE.close()
    return proteinDict
        

def readProteinInfo(dataFile, nameFile):
# read the whole protein information from PDBbind list file 
    if not os.path.exists(dataFile):
        print "File not found ", dataFile   
        quit()
    
    FILE = open(dataFile, 'r')

    Protein = collections.namedtuple('Protein', 'id resolution pKd Kd ECnum name cluster') 
    
    proteinList = []
    # read ECnumber and protein name
    proteinName = readNameFile(nameFile)
    
    # read each line
    for line in FILE:
        # skip comments
        if not (line[0] == '#'):
            protein = line.split(None)
            proteinID = protein[0]
            if protein[5] == '//': # detect refined protein list file, then cluster info is not available
                #print dataFile, (dataFile.find('refined'))
                if (dataFile.find('2012')>-1) and (dataFile.find('core')>-1): # 2012 data file doesnt contain cluster info anymore, get it from cluster file, ONLY FOR CORE DATA
                    tmpCluster = readClusterFile(PATHDB + CLUSTERFILE)[proteinID]
                else:
                    tmpCluster = ''  
            else: # cluster info is available (in core list file)
                tmpCluster = ''.join(protein[5:6])
            tmpProtein = Protein(id=proteinID, resolution=float(protein[1]), pKd=float(protein[3]), Kd=protein[4], ECnum=proteinName[proteinID].ECnum, name=proteinName[proteinID].name, cluster =tmpCluster)
            proteinList.append(tmpProtein)
        
    FILE.close()
    return proteinList

def convertList2Dict(proteinList):
# convert a protein list to dict with key = id and value = pKd
    proteinDict = {}
    for protein in proteinList:
        proteinDict[protein.id] = protein.pKd
    return proteinDict

def convertList2DictCluster(proteinList):
# convert a protein list to dict with key = id and value = cluster
    proteinDict = {}
    for protein in proteinList:
        proteinDict[protein.id] = protein.cluster
    return proteinDict

def createClusterDict(proteinList):
    """
    create a dict of cluster, with each entry is the protein IDs of this cluster
    """
    
    from operator import attrgetter
    
    cluster = ''
    clusterDict = {}
    proteinCluster = []
    for aProtein in sorted(proteinList, key=attrgetter('cluster', 'pKd', 'ECnum'), reverse = True):
        if aProtein.cluster != cluster: # detect new cluster
            clusterDict[cluster] = proteinCluster 
            proteinCluster = [aProtein.id]                        
            cluster = aProtein.cluster
        else: # same cluster
            proteinCluster.append(aProtein.id) # add the protein ID to the cluster
    # add the last cluster
    clusterDict[cluster] = proteinCluster
    # remove the empty key entry
    clusterDict.pop('', None)
    return clusterDict

