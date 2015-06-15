
import subprocess
import os

SOURCE_CONF     = '/home/dat/WORK/docking_config/gold.conf'

dataset = "v2013-core"
dockingMethod = "PLP"

def main():
    print("Main")
    f = open("/home/dat/output.txt", "w")
    run_cmd = "rms_analysis /home/dat/WORK/DB/CSAR/2013/cs/cs-confgen_all/SP/CS331_1.mol2 /home/dat/WORK/DB/CSAR/2013/cs/cs-confgen_all/SP/CS331_2.mol2"
    subprocess.call(run_cmd.split(), stdout=f)


main()