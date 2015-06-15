
import os
import csv

def readFromLog(path, ligandID):
    file = os.path.join(path, ligandID + '.log')
    LOGFILE = open(file, 'r')
    for line in LOGFILE:
        if (line.split() != []):
            if (line.split()[0]) == "Total":
                return (line.split()[1:7])

def readFromTable(path, ligandID):
    file = os.path.join(path, ligandID + '.table')
    LOGFILE = open(file, 'r')
    line = LOGFILE.readline() # skip the first line
    line = LOGFILE.readline()
    return (line.split()[2:4])

def main():
    path        = "/Users/knight/MyClouds/"
    ligandID    = "10gs"
    XScoreHeader = ["MW", "LogP", "VDW", "HB", "HP", "HM", "HS", "RT"]
    desc = readFromTable(path, ligandID) + readFromLog(path, ligandID)
    print(desc)
    CSV = open("/Users/knight/test.csv", 'w')
    a = csv.writer(CSV, delimiter=',')
    a.writerow(XScoreHeader)
    a.writerow(desc)
    CSV.close()

main()