
import subprocess
import os

SOURCE_CONF     = '/home/dat/WORK/docking_config/gold_pose.conf'

dataset = "v2014-core"
dockingMethod = "PLP"
GAruns = 50
searchEff = 10

def createGoldPose(proteinID, ligandID, GAruns, searchEff, dockingMethod, outputDir):
    outputConf  = 'gold_' + proteinID + '_' + ligandID + dockingMethod + '.conf'
    outputConf  = os.path.join(outputDir, outputConf)
    print(outputConf)
    if not os.path.exists(outputDir): # try to create the dir path first
        os.makedirs(outputDir)
    OUTFILE = open(outputConf, 'w')
    # open conf file
    if not os.path.exists(SOURCE_CONF):
        print("File not found ", SOURCE_CONF)
        quit()
    # open file for reading and writing
    INFILE  = open(SOURCE_CONF, 'r')

    SHFILE  = open(os.path.join(OUTPUT_DIR, 'gold_run_'+score+'_'+lPROTEIN_STATUS[proteinStatus]+'.sh'), 'a')
    for line in INFILE:
        if line.find('cavity_file =') > -1:
            line = 'cavity_file = ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX + '\n')
        elif line.find('ligand_data_file') > -1:
            line = 'ligand_data_file ' + os.path.join(proteinDir, proteinID, proteinID + LIGAND_SUFFIX) + ' 10\n'
        elif line.find('directory =') > -1:
            line = 'directory = ' + os.path.join(outputScore, proteinID + '\n')
        elif line.find('protein_datafile =') > -1:
            line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + lPROTEIN_SUFFIX[proteinStatus] + '\n')
            if ((proteinID == '1xgj') or (proteinID == '2pu2')) and (proteinStatus == 1): #prepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_proton_f.pdb\n')
            if ((proteinID == '1w3l')) and (proteinStatus == 0): #unprepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_f.pdb\n')
            if ((proteinID == '1b9j')) and (proteinStatus == 0) and (DBver=="v2007"): #unprepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_del.pdb\n')
            if ((proteinID == '1b7h')) and (proteinStatus == 0) and (DBver=="v2007"): #unprepared
                line = 'protein_datafile = ' + os.path.join(proteinDir, proteinID, proteinID + '_protein_del.pdb\n')

        elif line.find('gold_fitfunc_path =') > -1:
            line = 'gold_fitfunc_path = ' + score + '\n'
        OUTFILE.write(line)

    # write sh script
    SHFILE.write('gold_auto ' + outputConf + '\n')

    SHFILE.close()
    INFILE.close()
    OUTFILE.close()


def main():
    print("Main")
    f = open("/home/dat/output.txt", "w")
    run_cmd = "rms_analysis /home/dat/WORK/DB/CSAR/2013/cs/cs-confgen_all/SP/CS331_1.mol2 /home/dat/WORK/DB/CSAR/2013/cs/cs-confgen_all/SP/CS331_2.mol2"
    subprocess.call(run_cmd.split(), stdout=f)


main()