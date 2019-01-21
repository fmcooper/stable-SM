import sys
import numpy as np
import matplotlib.pylab as plt
import glob
from scipy.stats import sem
from sys import argv
import matplotlib.ticker as FormatStrFormatter
import os, os.path
import datetime

# Iterates over all correctness files and collates results.
# @author Frances

np.set_printoptions(suppress=True)
prePath = sys.argv[1]

################# variables
correctnessNames = ["S10", "S20", "S30", "S40", "S50", "S60", "S70", "S80", "S90", "S100", \
                    "S200", "S300", "S400", "S500", "S600", "S700", "S800", "S900", "S1000"]
dirName = "stats/tempCorrectnessResults"
outFileName = dirName + "/correctness.txt"

#####################################
# main
#####################################
def main():
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    now = datetime.datetime.now()
    outFile = open(outFileName, 'w')
    outFile.write("Correctness runthrough conducted at: " + now.strftime("%Y-%m-%d %H:%M") + "\n\n")
    outFile.close()

    errorFnames = ""
    failFnames = ""

    # for each experiment type
    for cname in correctnessNames:
        pathResults = prePath + cname + "/Correctness/"

        totalCorrectnessChecked = 0
        totalTimeout = 0
        totalIPTimeout = 0
        totalPassed = 0
        totalFailed = 0

        # run over the results to get the optimal matching indices
        for name in os.listdir(pathResults):
            if os.path.isfile(pathResults + name):
                totalCorrectnessChecked+=1
                with open(pathResults + name) as f:
                    numStable = -1
                    numAcc = -2
                    numCap = -3
                    numSta = -4
                    numIP = -5
                    thisInstTimeout = False
                    content = f.readlines()
                    for s in content:
                        # general info
                        if "ip_timeout" in s:
                            totalIPTimeout += 1
                        elif "timeout" in s:        # elif to differentiate
                            thisInstTimeout = True
                            totalTimeout += 1
                        if "**uncontrolled error**" in s:
                            errorFnames += name + "\n";
                        if "numStableMatchings" in s:
                            numStable = int(s.split()[1])
                        if "numPassedAcceptability" in s:
                            numAcc = int(s.split()[1])
                        if "numPassedCapacity" in s:
                            numCap = int(s.split()[1])
                        if "numPassedStability" in s:
                            numSta = int(s.split()[1])
                        if "num_solutions_found_by_ip" in s:
                            numIP = int(s.split()[1])
                        

                    if numStable == numAcc and numAcc == numCap and numCap == numSta and (numSta == numIP or numIP == -5):
                        totalPassed = totalPassed + 1
                    elif not thisInstTimeout:
                        totalFailed = totalFailed + 1
                        failFnames += name + "\n";


        outFile = open(outFileName, 'a')
        outFile.write("# experiment: " + cname + "\t")
        outFile.write("totalChecked: " + str(totalCorrectnessChecked) + "\t")
        outFile.write("totalTimeout: " + str(totalTimeout) + "\t")
        outFile.write("totalIPTimeout: " + str(totalIPTimeout) + "\t")
        outFile.write("totalPassed: " + str(totalPassed) + "\t")
        outFile.write("totalFailedOrError: " + str(totalFailed) + "\t")
        outFile.write("\n")
        outFile.close()

    outFile = open(outFileName, 'a')
    outFile.write("\n# errors: \n" + errorFnames)
    outFile.write("\n\n# fails: \n" + failFnames)
    outFile.close()

    exit(0)



#####################################
# main def
#####################################
if __name__ == '__main__':
    main()

