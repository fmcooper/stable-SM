import matplotlib
matplotlib.use('Agg')
import sys
import numpy as np
import matplotlib.pylab as plt
import glob
import math
from scipy.stats import sem
from sys import argv
import matplotlib.ticker as FormatStrFormatter
import os, os.path
import datetime
from statsClasses import experiment
from scipy.optimize import curve_fit

# Iterates over all results files and collates results.
# @author Frances

np.set_printoptions(suppress=True)
prePath = sys.argv[1]

################# variables
expTypeNames = ["S10", "S20", "S30", "S40", "S50", "S60", "S70", "S80", "S90", "S100", \
                    "S200", "S300", "S400", "S500", "S600", "S700", "S800", "S900", "S1000"]
dirName = "stats/tempStatsResults"
avstats = dirName + '/avstats.txt'
d = {}
maxprefs = {}

#####################################
# main
#####################################
def main():
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    # calculate results
    now = datetime.datetime.now()
    avstatsFile = open(avstats, 'w')
    avstatsFile.write("Stats runthrough conducted at: " + now.strftime("%Y-%m-%d %H:%M") + "\n\n")
    avstatsFile.close()

    # for each experiment type
    for ind, exptype in enumerate(expTypeNames):
        print exptype
        postPathResultsGSNS = "/ResultsGS_notSwapped/"
        postPathResultsGSS = "/ResultsGS_Swapped/"
        postPathResults = "/Results_stable/"
        postPathInstances = "/Instances/"

        calculateResults(exptype, prePath, postPathInstances, postPathResults, postPathResultsGSNS, postPathResultsGSS)

        # get averages
        getAverages(exptype)

    # create table for paper
    createLatex()

    # create plots
    createPlot()

    exit(0)


#####################################
# calculate results
#####################################
def calculateResults(exptype, prePath, postPathInstances, postPathResults, postPathResultsGSNS, postPathResultsGSS):

    graphIndex = 1
    infeasibleCounts = []


    pathInstance = prePath + exptype + postPathInstances
    pathResults = prePath + exptype + postPathResults
    pathGSNSResults = prePath + exptype + postPathResultsGSNS
    pathGSSResults = prePath + exptype + postPathResultsGSS

    # collect the raw data and calculate the averages for latex
    totalInstances, totalTimeout, expStats, numMen, skew = collectRawData(exptype, pathInstance, pathResults)

    # remove instance result if total time for all three algs is above the timeout of 1 hour
    # also increment timeout
    expStatsLegit = []
    for exp in expStats:
        if not exp.timeout(3600000): # milliseconds 
            expStatsLegit.append(exp)
        else:
            totalTimeout = totalTimeout + 1
    expStats = expStatsLegit


    # calculate the averages and output
    avstatsFile = open(avstats, "a")
    avstatsFile.write('\n# stats file for all instance types of ' + exptype + '\n')
    avstatsFile.write('{}avNumRotations {:0.1f}\n'.format(exptype, getAverage([exp.numRotations for exp in expStats])))
    avstatsFile.write('{}avNumStableMatchings {:0.1f}\n'.format(exptype, getAverage([exp.numStableMatchings for exp in expStats])))
    avstatsFile.write('{}avEgalCost {:0.1f}\n'.format(exptype, getAverage([exp.egalCost for exp in expStats])))
    avstatsFile.write('{}minEgalCost {:d}\n'.format(exptype, getMin([exp.egalCost for exp in expStats])))
    avstatsFile.write('{}maxEgalCost {:d}\n'.format(exptype, getMax([exp.egalCost for exp in expStats])))
    avstatsFile.write('{}avSeCost {:0.1f}\n'.format(exptype, getAverage([exp.seCost for exp in expStats])))
    avstatsFile.write('{}minSeCost {:d}\n'.format(exptype, getMin([exp.seCost for exp in expStats])))
    avstatsFile.write('{}maxSeCost {:d}\n'.format(exptype, getMax([exp.seCost for exp in expStats])))


    avstatsFile.write('{}avRMprofile {:65}\n'.format(exptype, getAverageProfileString(getAverageProfile([exp.RMprofile for exp in expStats]))))
    minRMdegree, maxRMdegree, avRMdegree = getMinMaxAvDegree([exp.RMprofile for exp in expStats])
    minRMfirstChoices, maxRMfirstChoices, avRMfirstChoices = getMinMaxAvChoices([exp.RMprofile for exp in expStats], "first")
    minRMlastChoices, maxRMlastChoices, avRMlastChoices = getMinMaxAvChoices([exp.RMprofile for exp in expStats], "last")
    avstatsFile.write('{}avRMdegree {:0.1f}\n'.format(exptype, avRMdegree))
    avstatsFile.write('{}minRMdegree {:d}\n'.format(exptype, minRMdegree))
    avstatsFile.write('{}maxRMdegree {:d}\n'.format(exptype, maxRMdegree))
    avstatsFile.write('{}minRMfirstChoices {:d}\n'.format(exptype, minRMfirstChoices))
    avstatsFile.write('{}maxRMfirstChoices {:d}\n'.format(exptype, maxRMfirstChoices))
    avstatsFile.write('{}avRMfirstChoices {:0.1f}\n'.format(exptype, avRMfirstChoices))
    avstatsFile.write('{}minRMlastChoices {:d}\n'.format(exptype, minRMlastChoices))
    avstatsFile.write('{}maxRMlastChoices {:d}\n'.format(exptype, maxRMlastChoices))
    avstatsFile.write('{}avRMlastChoices {:0.1f}\n'.format(exptype, avRMlastChoices))
    avstatsFile.write('{}avRMegalCost {:0.1f}\n'.format(exptype, getAverage([exp.RMegalCost for exp in expStats])))
    avstatsFile.write('{}minRMegalCost {:d}\n'.format(exptype, getMin([exp.RMegalCost for exp in expStats])))
    avstatsFile.write('{}maxRMegalCost {:d}\n'.format(exptype, getMax([exp.RMegalCost for exp in expStats])))
    avstatsFile.write('{}avRMseCost {:0.1f}\n'.format(exptype, getAverage([exp.RMseCost for exp in expStats])))
    avstatsFile.write('{}minRMseCost {:d}\n'.format(exptype, getMin([exp.RMseCost for exp in expStats])))
    avstatsFile.write('{}maxRMseCost {:d}\n'.format(exptype, getMax([exp.RMseCost for exp in expStats])))
    minRMlast50pc, maxRMlast50pc, avRMlast50pc = getMinMaxAvLast([exp.RMprofile for exp in expStats], 0.5)
    minRMlast40pc, maxRMlast40pc, avRMlast40pc = getMinMaxAvLast([exp.RMprofile for exp in expStats], 0.4)
    minRMlast30pc, maxRMlast30pc, avRMlast30pc = getMinMaxAvLast([exp.RMprofile for exp in expStats], 0.3)
    minRMlast20pc, maxRMlast20pc, avRMlast20pc = getMinMaxAvLast([exp.RMprofile for exp in expStats], 0.2)
    minRMlast10pc, maxRMlast10pc, avRMlast10pc = getMinMaxAvLast([exp.RMprofile for exp in expStats], 0.1)
    avstatsFile.write('{}minRMlast50pc {:0.1f}\n'.format(exptype, minRMlast50pc))
    avstatsFile.write('{}minRMlast40pc {:0.1f}\n'.format(exptype, minRMlast40pc))
    avstatsFile.write('{}minRMlast30pc {:0.1f}\n'.format(exptype, minRMlast30pc))
    avstatsFile.write('{}minRMlast20pc {:0.1f}\n'.format(exptype, minRMlast20pc))
    avstatsFile.write('{}minRMlast10pc {:0.1f}\n'.format(exptype, minRMlast10pc))
    avstatsFile.write('{}maxRMlast50pc {:0.1f}\n'.format(exptype, maxRMlast50pc))
    avstatsFile.write('{}maxRMlast40pc {:0.1f}\n'.format(exptype, maxRMlast40pc))
    avstatsFile.write('{}maxRMlast30pc {:0.1f}\n'.format(exptype, maxRMlast30pc))
    avstatsFile.write('{}maxRMlast20pc {:0.1f}\n'.format(exptype, maxRMlast20pc))
    avstatsFile.write('{}maxRMlast10pc {:0.1f}\n'.format(exptype, maxRMlast10pc))
    avstatsFile.write('{}avRMlast50pc {:0.1f}\n'.format(exptype, avRMlast50pc))
    avstatsFile.write('{}avRMlast40pc {:0.1f}\n'.format(exptype, avRMlast40pc))
    avstatsFile.write('{}avRMlast30pc {:0.1f}\n'.format(exptype, avRMlast30pc))
    avstatsFile.write('{}avRMlast20pc {:0.1f}\n'.format(exptype, avRMlast20pc))
    avstatsFile.write('{}avRMlast10pc {:0.1f}\n'.format(exptype, avRMlast10pc))


    avstatsFile.write('{}avGENprofile {:65}\n'.format(exptype, getAverageProfileString(getAverageProfile([exp.GENprofile for exp in expStats]))))
    minGENdegree, maxGENdegree, avGENdegree = getMinMaxAvDegree([exp.GENprofile for exp in expStats])
    minGENfirstChoices, maxGENfirstChoices, avGENfirstChoices = getMinMaxAvChoices([exp.GENprofile for exp in expStats], "first")
    minGENlastChoices, maxGENlastChoices, avGENlastChoices = getMinMaxAvChoices([exp.GENprofile for exp in expStats], "last")
    avstatsFile.write('{}avGENdegree {:0.1f}\n'.format(exptype, avGENdegree))
    avstatsFile.write('{}minGENdegree {:d}\n'.format(exptype, minGENdegree))
    avstatsFile.write('{}maxGENdegree {:d}\n'.format(exptype, maxGENdegree))
    avstatsFile.write('{}minGENfirstChoices {:d}\n'.format(exptype, minGENfirstChoices))
    avstatsFile.write('{}maxGENfirstChoices {:d}\n'.format(exptype, maxGENfirstChoices))
    avstatsFile.write('{}avGENfirstChoices {:0.1f}\n'.format(exptype, avGENfirstChoices))
    avstatsFile.write('{}minGENlastChoices {:d}\n'.format(exptype, minGENlastChoices))
    avstatsFile.write('{}maxGENlastChoices {:d}\n'.format(exptype, maxGENlastChoices))
    avstatsFile.write('{}avGENlastChoices {:0.1f}\n'.format(exptype, avGENlastChoices))
    avstatsFile.write('{}avGENegalCost {:0.1f}\n'.format(exptype, getAverage([exp.GENegalCost for exp in expStats])))
    avstatsFile.write('{}minGENegalCost {:d}\n'.format(exptype, getMin([exp.GENegalCost for exp in expStats])))
    avstatsFile.write('{}maxGENegalCost {:d}\n'.format(exptype, getMax([exp.GENegalCost for exp in expStats])))
    avstatsFile.write('{}avGENseCost {:0.1f}\n'.format(exptype, getAverage([exp.GENseCost for exp in expStats])))
    avstatsFile.write('{}minGENseCost {:d}\n'.format(exptype, getMin([exp.GENseCost for exp in expStats])))
    avstatsFile.write('{}maxGENseCost {:d}\n'.format(exptype, getMax([exp.GENseCost for exp in expStats])))
    minGENlast50pc, maxGENlast50pc, avGENlast50pc = getMinMaxAvLast([exp.GENprofile for exp in expStats], 0.5)
    minGENlast40pc, maxGENlast40pc, avGENlast40pc = getMinMaxAvLast([exp.GENprofile for exp in expStats], 0.4)
    minGENlast30pc, maxGENlast30pc, avGENlast30pc = getMinMaxAvLast([exp.GENprofile for exp in expStats], 0.3)
    minGENlast20pc, maxGENlast20pc, avGENlast20pc = getMinMaxAvLast([exp.GENprofile for exp in expStats], 0.2)
    minGENlast10pc, maxGENlast10pc, avGENlast10pc = getMinMaxAvLast([exp.GENprofile for exp in expStats], 0.1)
    avstatsFile.write('{}minGENlast50pc {:0.1f}\n'.format(exptype, minGENlast50pc))
    avstatsFile.write('{}minGENlast40pc {:0.1f}\n'.format(exptype, minGENlast40pc))
    avstatsFile.write('{}minGENlast30pc {:0.1f}\n'.format(exptype, minGENlast30pc))
    avstatsFile.write('{}minGENlast20pc {:0.1f}\n'.format(exptype, minGENlast20pc))
    avstatsFile.write('{}minGENlast10pc {:0.1f}\n'.format(exptype, minGENlast10pc))
    avstatsFile.write('{}maxGENlast50pc {:0.1f}\n'.format(exptype, maxGENlast50pc))
    avstatsFile.write('{}maxGENlast40pc {:0.1f}\n'.format(exptype, maxGENlast40pc))
    avstatsFile.write('{}maxGENlast30pc {:0.1f}\n'.format(exptype, maxGENlast30pc))
    avstatsFile.write('{}maxGENlast20pc {:0.1f}\n'.format(exptype, maxGENlast20pc))
    avstatsFile.write('{}maxGENlast10pc {:0.1f}\n'.format(exptype, maxGENlast10pc))
    avstatsFile.write('{}avGENlast50pc {:0.1f}\n'.format(exptype, avGENlast50pc))
    avstatsFile.write('{}avGENlast40pc {:0.1f}\n'.format(exptype, avGENlast40pc))
    avstatsFile.write('{}avGENlast30pc {:0.1f}\n'.format(exptype, avGENlast30pc))
    avstatsFile.write('{}avGENlast20pc {:0.1f}\n'.format(exptype, avGENlast20pc))
    avstatsFile.write('{}avGENlast10pc {:0.1f}\n'.format(exptype, avGENlast10pc))


    avstatsFile.write('{}avGMprofile {:65}\n'.format(exptype, getAverageProfileString(getAverageProfile([exp.GMprofile for exp in expStats]))))
    minGMdegree, maxGMdegree, avGMdegree = getMinMaxAvDegree([exp.GMprofile for exp in expStats])
    minGMfirstChoices, maxGMfirstChoices, avGMfirstChoices = getMinMaxAvChoices([exp.GMprofile for exp in expStats], "first")
    minGMlastChoices, maxGMlastChoices, avGMlastChoices = getMinMaxAvChoices([exp.GMprofile for exp in expStats], "last")
    avstatsFile.write('{}avGMdegree {:0.1f}\n'.format(exptype, avGMdegree))
    avstatsFile.write('{}minGMdegree {:d}\n'.format(exptype, minGMdegree))
    avstatsFile.write('{}maxGMdegree {:d}\n'.format(exptype, maxGMdegree))
    avstatsFile.write('{}minGMfirstChoices {:d}\n'.format(exptype, minGMfirstChoices))
    avstatsFile.write('{}maxGMfirstChoices {:d}\n'.format(exptype, maxGMfirstChoices))
    avstatsFile.write('{}avGMfirstChoices {:0.1f}\n'.format(exptype, avGMfirstChoices))
    avstatsFile.write('{}minGMlastChoices {:d}\n'.format(exptype, minGMlastChoices))
    avstatsFile.write('{}maxGMlastChoices {:d}\n'.format(exptype, maxGMlastChoices))
    avstatsFile.write('{}avGMlastChoices {:0.1f}\n'.format(exptype, avGMlastChoices))
    avstatsFile.write('{}avGMegalCost {:0.1f}\n'.format(exptype, getAverage([exp.GMegalCost for exp in expStats])))
    avstatsFile.write('{}minGMegalCost {:d}\n'.format(exptype, getMin([exp.GMegalCost for exp in expStats])))
    avstatsFile.write('{}maxGMegalCost {:d}\n'.format(exptype, getMax([exp.GMegalCost for exp in expStats])))
    avstatsFile.write('{}avGMseCost {:0.1f}\n'.format(exptype, getAverage([exp.GMseCost for exp in expStats])))
    avstatsFile.write('{}minGMseCost {:d}\n'.format(exptype, getMin([exp.GMseCost for exp in expStats])))
    avstatsFile.write('{}maxGMseCost {:d}\n'.format(exptype, getMax([exp.GMseCost for exp in expStats])))
    minGMlast50pc, maxGMlast50pc, avGMlast50pc = getMinMaxAvLast([exp.GMprofile for exp in expStats], 0.5)
    minGMlast40pc, maxGMlast40pc, avGMlast40pc = getMinMaxAvLast([exp.GMprofile for exp in expStats], 0.4)
    minGMlast30pc, maxGMlast30pc, avGMlast30pc = getMinMaxAvLast([exp.GMprofile for exp in expStats], 0.3)
    minGMlast20pc, maxGMlast20pc, avGMlast20pc = getMinMaxAvLast([exp.GMprofile for exp in expStats], 0.2)
    minGMlast10pc, maxGMlast10pc, avGMlast10pc = getMinMaxAvLast([exp.GMprofile for exp in expStats], 0.1)
    avstatsFile.write('{}minGMlast50pc {:0.1f}\n'.format(exptype, minGMlast50pc))
    avstatsFile.write('{}minGMlast40pc {:0.1f}\n'.format(exptype, minGMlast40pc))
    avstatsFile.write('{}minGMlast30pc {:0.1f}\n'.format(exptype, minGMlast30pc))
    avstatsFile.write('{}minGMlast20pc {:0.1f}\n'.format(exptype, minGMlast20pc))
    avstatsFile.write('{}minGMlast10pc {:0.1f}\n'.format(exptype, minGMlast10pc))
    avstatsFile.write('{}maxGMlast50pc {:0.1f}\n'.format(exptype, maxGMlast50pc))
    avstatsFile.write('{}maxGMlast40pc {:0.1f}\n'.format(exptype, maxGMlast40pc))
    avstatsFile.write('{}maxGMlast30pc {:0.1f}\n'.format(exptype, maxGMlast30pc))
    avstatsFile.write('{}maxGMlast20pc {:0.1f}\n'.format(exptype, maxGMlast20pc))
    avstatsFile.write('{}maxGMlast10pc {:0.1f}\n'.format(exptype, maxGMlast10pc))
    avstatsFile.write('{}avGMlast50pc {:0.1f}\n'.format(exptype, avGMlast50pc))
    avstatsFile.write('{}avGMlast40pc {:0.1f}\n'.format(exptype, avGMlast40pc))
    avstatsFile.write('{}avGMlast30pc {:0.1f}\n'.format(exptype, avGMlast30pc))
    avstatsFile.write('{}avGMlast20pc {:0.1f}\n'.format(exptype, avGMlast20pc))
    avstatsFile.write('{}avGMlast10pc {:0.1f}\n'.format(exptype, avGMlast10pc))


    avstatsFile.write('{}AvD_Total {:0.1f}\n'.format(exptype, getAverage([exp.Duration_Total_ms for exp in expStats])))
    avstatsFile.write('{}numMenOrWomen {:10}\n'.format(exptype, numMen))
    avstatsFile.write('{}skew {:10}\n'.format(exptype, skew))
    avstatsFile.write('{}numInstances {:10}\n'.format(exptype, str(totalInstances)))
    avstatsFile.write('{}numTimeout {:10}\n'.format(exptype, str(totalTimeout)))
    avstatsFile.close()



# collect the raw data from each instance file
def collectRawData(exp, pathInstance, pathResults):
    print(pathResults) 

    expStats = []
    numMen = ""
    skew = ""
    totalInstances = 0
    totalTimeout = 0


    # run over the instance statistics
    name = os.listdir(pathInstance)[0]
    with open(pathInstance + name) as f:
        content = f.readlines()
        for s in content:
            # general info
            if "numMenOrWomen" in s:
                numMen = s.split()[1];
            if "skew" in s:
                skew = s.split()[1];

    rmIndex = ""
    genIndex = ""
    seIndex = ""
    egalIndex = ""
    gmIndex = "" 

    # run over the results to get the optimal matching indices
    for name in os.listdir(pathResults):
        if os.path.isfile(pathResults + name):
            #print(pathResults + name)
            totalInstances+=1
            timeout = False
            exp = experiment()
            exp = getDurationGS(exp, pathResults + name)
            with open(pathResults + name) as f:
                content = f.readlines()
                for s in content:
                    # general info
                    if "timeout" in s:
                        totalTimeout += 1;
                        timeout = True
                    if "numRotations" in s:
                        exp.numRotations = int(s.split()[1]);
                    if "numStableMatchings" in s:
                        exp.numStableMatchings = int(s.split()[1]);

                    # these optimal indices are found earlier in the file than the stable matchings
                    if "rank-maximal_index" in s:
                        rmIndex = s.split()[1]
                    if "generous_index" in s:
                        genIndex = s.split()[1]
                    if "sex_equal_index" in s:
                        seIndex = s.split()[1]
                    if "egalitarian_index" in s:
                        egalIndex = s.split()[1]
                    if "generalisedMedian_index" in s:
                        gmIndex = s.split()[1]
                    
                    # specific optimal matching info
                    # rank-maximal
                    if "profileCombined_" + rmIndex + ":" in s:
                        prof = s.split()
                        profNum = []
                        for x in range(1,len(prof)):
                            profNum.append(int(prof[x]))
                        exp.RMprofile = np.array(profNum)  
                    if "costCombined_" + rmIndex + ":" in s:
                        exp.RMegalCost = int(s.split()[1])
                    if "sexEquality_" + rmIndex + ":" in s:
                        exp.RMseCost = int(s.split()[1])
                    # generous
                    if "profileCombined_" + genIndex + ":" in s:
                        prof = s.split()
                        profNum = []
                        for x in range(1,len(prof)):
                            profNum.append(int(prof[x]))
                        exp.GENprofile = np.array(profNum)
                    if "costCombined_" + genIndex + ":" in s:
                        exp.GENegalCost = int(s.split()[1])
                    if "sexEquality_" + genIndex + ":" in s:
                        exp.GENseCost = int(s.split()[1])
                    # generalised median
                    if "profileCombined_" + gmIndex + ":" in s:
                        prof = s.split()
                        profNum = []
                        for x in range(1,len(prof)):
                            profNum.append(int(prof[x]))
                        exp.GMprofile = np.array(profNum)
                    if "costCombined_" + gmIndex + ":" in s:
                        exp.GMegalCost = int(s.split()[1])
                    if "sexEquality_" + gmIndex + ":" in s:
                        exp.GMseCost = int(s.split()[1])
                    # egalitarian
                    if "costCombined_" + egalIndex + ":" in s:
                        exp.egalCost = int(s.split()[1])
                    # sex equal
                    if "sexEquality_" + seIndex + ":" in s:
                        exp.seCost = int(s.split()[1])
                       
                    # durations                    
                    if "Duration_ModCreation" in s:    
                        exp.Duration_ModCreation_ms = float(s.split()[1])
                    if "Duration_GetSolution" in s:
                        exp.Duration_GetSolution_ms = float(s.split()[1])
                    if "Duration_CollectRes" in s:
                        exp.Duration_CollectRes_ms = float(s.split()[1])
                    if "Duration_Total" in s:
                        exp.Duration_Total_ms = float(s.split()[1])
            if not timeout:
                expStats.append(exp)
                if exp.RMseCost < 0:
                    print("dud is here: " + pathResults + name)

    return totalInstances, totalTimeout, expStats, numMen, skew
    

# collect the raw total duration from each instance file
def getDurationGS(exp, path):
    pathResultsGSNS = path.replace("Results_stable", "ResultsGS_notSwapped")
    pathResultsGSS = path.replace("Results_stable", "ResultsGS_Swapped")

    GSNSdur = -1
    GSSdur = -1
    # run over the results to get the optimal matching indices
    with open(pathResultsGSNS) as f:
        content = f.readlines()
        for s in content:
            # general info
            if "Duration_Total" in s:
                GSNSdur = float(s.split()[1])

    with open(pathResultsGSS) as f:
        for s in content:
            # general info
            if "Duration_Total" in s:
                GSSdur = float(s.split()[1])

    exp.Duration_Total_ms_GSNS = GSNSdur
    exp.Duration_Total_ms_GSS = GSSdur

    return exp


# collect the raw data from each instance file
def getAverages(expName):
    with open(avstats) as inF:
        content = inF.readlines()
        for s in content:
            if len(s) < 2 or s[0]=="#":
                continue
            else:
                ssplit = s.split()
                d[ssplit[0]] = ssplit[1:]


# create latex tables
def createLatex():
    # instance info
    latexpaper = dirName + "/" + "latex_table_instance_info.txt"
    latexPaperFile = open(latexpaper, 'w')
    latexPaperFile.write('\\begin{table}[] \centerline{')
    latexPaperFile.write('\\begin{tabular}{ p{1.5cm} | p{1.5cm} p{1.5cm} p{1.5cm} p{2.5cm} }') 
    latexPaperFile.write('\hline\hline ')
    latexPaperFile.write('Case & $N_I$ & Timeout & $n$ & time (ms) \\\\ \n')
    latexPaperFile.write('\hline ')

    for i in xrange(0, len(expTypeNames)):
        exp = expTypeNames[i]
        latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
            exp,  d[exp+'numInstances'][0], d[exp+'numTimeout'][0], d[exp+'numMenOrWomen'][0], d[exp+'AvD_Total'][0] ))

    # finishing the latex results file
    latexPaperFile.write('\hline\hline \end{tabular}} \caption{General instance information.} \label{} \end{table} ')
    latexPaperFile.close 



    # # table 1 - basic stats
    latexpaper = dirName + "/" + "latex_table_generalStats.txt"
    latexPaperFile = open(latexpaper, 'w')
    latexPaperFile.write('\\begin{table}[] \centerline{')
    latexPaperFile.write('\\begin{tabular}{ p{1.5cm} | p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} }') 
    latexPaperFile.write('\hline\hline ')
    latexPaperFile.write('Case & $|\mathcal{R}|$ & $|\mathcal{M}|$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
    latexPaperFile.write('\hline ')

    for i in xrange(0, len(expTypeNames)):
        exp = expTypeNames[i]
        latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
            exp, d[exp+'avNumRotations'][0], d[exp+'avNumStableMatchings'][0], \
            # d[exp+'minDegree'][0], d[exp+'maxDegree'][0], d[exp+'avDegree'][0], \
            d[exp+'minEgalCost'][0], d[exp+'maxEgalCost'][0], d[exp+'avEgalCost'][0], \
            d[exp+'minSeCost'][0], d[exp+'maxSeCost'][0], d[exp+'avSeCost'][0]))

    # finishing the latex results file
    latexPaperFile.write('\hline\hline \end{tabular}} \caption{General stats results.} \label{} \end{table} ')
    latexPaperFile.close 


    # table 2 - RM info
    latexpaper = dirName + "/" + "latex_table_RM.txt"
    latexPaperFile = open(latexpaper, 'w')
    latexPaperFile.write('\\begin{table}[] \centerline{')
    latexPaperFile.write('\\begin{tabular}{ p{1.1cm} | p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.1cm} }') 
    latexPaperFile.write('\hline\hline ')
    latexPaperFile.write('Case & $\min(f)$ & $\max(f)$ & av$(f)$ & $\min(l_{10})$ & $\max(l_{10})$ & av$(l_{10})$ & $\min(d)$ & $\max(d)$ & av$(d)$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
    latexPaperFile.write('\hline ')

    for i in xrange(0, len(expTypeNames)):
        exp = expTypeNames[i]
        profile = ' '.join(str(e) for e in d[exp+'avRMprofile'][0:])
        latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
            exp, \
            d[exp+'minRMfirstChoices'][0], d[exp+'maxRMfirstChoices'][0], d[exp+'avRMfirstChoices'][0], \
            d[exp+'minRMlast10pc'][0], d[exp+'maxRMlast10pc'][0], d[exp+'avRMlast10pc'][0], \
            d[exp+'minRMdegree'][0], d[exp+'maxRMdegree'][0], d[exp+'avRMdegree'][0], \
            d[exp+'minRMegalCost'][0], d[exp+'maxRMegalCost'][0], d[exp+'avRMegalCost'][0], \
            d[exp+'minRMseCost'][0], d[exp+'maxRMseCost'][0], d[exp+'avRMseCost'][0]))

    # finishing the latex results file
    latexPaperFile.write('\hline\hline \end{tabular}} \caption{Rank-maximal results.} \label{} \end{table} ')
    latexPaperFile.close 


    # # table 3 - GEN info
    latexpaper = dirName + "/" + "latex_table_GEN.txt"
    latexPaperFile = open(latexpaper, 'w')
    latexPaperFile.write('\\begin{table}[] \centerline{')
    latexPaperFile.write('\\begin{tabular}{ p{1.1cm} | p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.1cm} }') 
    latexPaperFile.write('\hline\hline ')
    latexPaperFile.write('Case & $\min(f)$ & $\max(f)$ & av$(f)$ & $\min(l_{50})$ & $\max(l_{50})$ & av$(l_{50})$ & $\min(d)$ & $\max(d)$ & av$(d)$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
    latexPaperFile.write('\hline ')

    for i in xrange(0, len(expTypeNames)):
        exp = expTypeNames[i]
        profile = ' '.join(str(e) for e in d[exp+'avGENprofile'][0:])
        latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
            exp, \
            d[exp+'minGENfirstChoices'][0], d[exp+'maxGENfirstChoices'][0], d[exp+'avGENfirstChoices'][0], \
            d[exp+'minGENlast50pc'][0], d[exp+'maxGENlast50pc'][0], d[exp+'avGENlast50pc'][0], \
            d[exp+'minGENdegree'][0], d[exp+'maxGENdegree'][0], d[exp+'avGENdegree'][0], \
            d[exp+'minGENegalCost'][0], d[exp+'maxGENegalCost'][0], d[exp+'avGENegalCost'][0], \
            d[exp+'minGENseCost'][0], d[exp+'maxGENseCost'][0], d[exp+'avGENseCost'][0]))

    # finishing the latex results file
    latexPaperFile.write('\hline\hline \end{tabular}} \caption{Generous results.} \label{} \end{table} ')
    latexPaperFile.close 


    # # table 4 - GM info
    latexpaper = dirName + "/" + "latex_table_GM.txt"
    latexPaperFile = open(latexpaper, 'w')
    latexPaperFile.write('\\begin{table}[] \centerline{')
    latexPaperFile.write('\\begin{tabular}{ p{1.1cm} | p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.1cm} }') 
    latexPaperFile.write('\hline\hline ')
    latexPaperFile.write('Case & $\min(f)$ & $\max(f)$ & av$(f)$ & $\min(l_{20})$ & $\max(l_{20})$ & av$(l_{20})$ & $\min(d)$ & $\max(d)$ & av$(d)$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
    latexPaperFile.write('\hline ')

    for i in xrange(0, len(expTypeNames)):
        exp = expTypeNames[i]
        profile = ' '.join(str(e) for e in d[exp+'avGMprofile'][0:])
        latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
            exp, \
            d[exp+'minGMfirstChoices'][0], d[exp+'maxGMfirstChoices'][0], d[exp+'avGMfirstChoices'][0], \
            d[exp+'minGMlast20pc'][0], d[exp+'maxGMlast20pc'][0], d[exp+'avGMlast20pc'][0], \
            d[exp+'minGMdegree'][0], d[exp+'maxGMdegree'][0], d[exp+'avGMdegree'][0], \
            d[exp+'minGMegalCost'][0], d[exp+'maxGMegalCost'][0], d[exp+'avGMegalCost'][0], \
            d[exp+'minGMseCost'][0], d[exp+'maxGMseCost'][0], d[exp+'avGMseCost'][0]))

    # finishing the latex results file
    latexPaperFile.write('\hline\hline \end{tabular}} \caption{Median results.} \label{} \end{table} ')
    latexPaperFile.close 


# matplotlib plots
def createPlot():
    # collect the data
    n=[]
    nlogn=[]
    avstable=[]
    secost=[]
    secostRM=[]
    secostGEN=[]
    secostGM=[]
    egalcost=[]
    egalcostRM=[]
    egalcostGEN=[]
    egalcostGM=[]
    avRMfirstChoices=[]
    avGENfirstChoices=[]
    avGMfirstChoices=[]
    avRMdegree=[]
    avGENdegree=[]
    avGMdegree=[]

    for exp in expTypeNames:
        nelem = int(exp[1:])
        n.append(nelem)
        nlogn.append(nelem * math.log(nelem))
        avstable.append(float(d[exp+'avNumStableMatchings'][0]))
        secost.append(float(d[exp+'avSeCost'][0]))
        secostRM.append(float(d[exp+'avRMseCost'][0]))
        secostGEN.append(float(d[exp+'avGENseCost'][0]))
        secostGM.append(float(d[exp+'avGMseCost'][0]))
        egalcost.append(float(d[exp+'avEgalCost'][0]))
        egalcostRM.append(float(d[exp+'avRMegalCost'][0]))
        egalcostGEN.append(float(d[exp+'avGENegalCost'][0]))
        egalcostGM.append(float(d[exp+'avGMegalCost'][0]))
        avRMfirstChoices.append(float(d[exp+'avRMfirstChoices'][0]))
        avGENfirstChoices.append(float(d[exp+'avGENfirstChoices'][0]))
        avGMfirstChoices.append(float(d[exp+'avGMfirstChoices'][0]))
        avRMdegree.append(float(d[exp+'avRMdegree'][0]))
        avGENdegree.append(float(d[exp+'avGENdegree'][0]))
        avGMdegree.append(float(d[exp+'avGMdegree'][0]))
    nlogn = nlogn[9:]
    avstable = avstable[9:]


    def func1D(x, a, b):
        return a + b*x
    def func2D(x, a, b, c):
        return a + b*x + c*x*x

    #############
    # nlogn graph
    plt.figure()
    plt.figure(facecolor='w', edgecolor='k', figsize=(7, 5))

    newx = np.linspace(460, 6900, 250)
    avStableCV,_ = curve_fit(func1D, nlogn, avstable)
    plt.plot(nlogn, avstable, 'o', color='black')
    plt.plot(newx, func1D(newx, avStableCV[0], avStableCV[1]), '-', color='black')
    
    plt.xlabel("$n$ $\log$ $n$")
    plt.ylabel("Average number of stable matchings $|\mathcal{M}|$")
    ax = plt.subplot()
    ax.spines["right"].set_visible(False)    
    ax.spines["top"].set_visible(False)
    plt.grid(linestyle="--")
    plt.savefig("./stats/tempStatsResults/sm_rm_nlogn.pdf")

    #############
    # sex equal cost
    plt.figure()
    plt.figure(facecolor='w', edgecolor='k', figsize=(7, 5))
    newx = np.logspace(1, 3, 250)
    secostCV,_ = curve_fit(func1D, np.log(n), np.log(secost))
    secostRMCV,_ = curve_fit(func1D, np.log(n), np.log(secostRM))
    secostGENCV,_ = curve_fit(func1D, np.log(n), np.log(secostGEN))
    secostGMCV,_ = curve_fit(func1D, np.log(n), np.log(secostGM))
    plt.plot(n, secostRM, 'o', color='skyblue', label="rank-maximal")
    plt.plot(n, secostGM, '*', color='orangered', label="median") 
    plt.plot(n, secostGEN, 's', color='seagreen', label="generous")
    plt.plot(n, secost, '^', color='gold', label="sex-equal")
    
    plt.plot(newx, np.exp(func1D(np.log(newx), secostRMCV[0], secostRMCV[1])), '-', color='skyblue')
    plt.plot(newx, np.exp(func1D(np.log(newx), secostGMCV[0], secostGMCV[1])), '-', color='orangered')
    plt.plot(newx, np.exp(func1D(np.log(newx), secostGENCV[0], secostGENCV[1])), '-', color='seagreen')
    plt.plot(newx, np.exp(func1D(np.log(newx), secostCV[0], secostCV[1])), '-', color='gold')
    
    plt.legend()
    plt.xlabel("$n$")
    plt.ylabel("Average sex-equal cost")
    plt.xscale('log')
    plt.yscale('log')
    ax = plt.subplot()
    ax.spines["right"].set_visible(False)    
    ax.spines["top"].set_visible(False)
    plt.grid(linestyle="--")
    plt.savefig("./stats/tempStatsResults/sm_rm_seCost.pdf")

    #############
    # egalitarian cost
    plt.figure()
    plt.figure(facecolor='w', edgecolor='k', figsize=(7, 5))
    newx = np.linspace(10, 1000, 250)
    egalcostCV,_ = curve_fit(func2D, n, egalcost)
    egalcostRMCV,_ = curve_fit(func2D, n, egalcostRM)
    egalcostGENCV,_ = curve_fit(func2D, n, egalcostGEN)
    egalcostGMCV,_ = curve_fit(func2D, n, egalcostGM)
    plt.plot(n, egalcostRM, 'o', color='skyblue', label="rank-maximal")
    plt.plot(n, egalcostGM, '*', color='orangered', label="median")
    plt.plot(n, egalcostGEN, 's', color='seagreen', label="generous")
    plt.plot(n, egalcost, '^', color='gold', label="egalitarian")
    
    plt.plot(newx, func2D(newx, egalcostRMCV[0], egalcostRMCV[1], egalcostRMCV[2]), '-', color='skyblue')
    plt.plot(newx, func2D(newx, egalcostGMCV[0], egalcostGMCV[1], egalcostGMCV[2]), '-', color='orangered')
    plt.plot(newx, func2D(newx, egalcostGENCV[0], egalcostGENCV[1], egalcostGENCV[2]), '-', color='seagreen')
    plt.plot(newx, func2D(newx, egalcostCV[0], egalcostCV[1], egalcostCV[2]), '-', color='gold')

    plt.legend()
    plt.xlabel("$n$")
    plt.ylabel("Average egalitarian cost")
    ax = plt.subplot()
    ax.spines["right"].set_visible(False)    
    ax.spines["top"].set_visible(False)
    plt.grid(linestyle="--")
    plt.savefig("./stats/tempStatsResults/sm_rm_egalCost.pdf")

    #############
    # num 1st choices
    plt.figure()
    plt.figure(facecolor='w', edgecolor='k', figsize=(7, 5))
    newx = np.linspace(10, 1000, 250)
    avRMfirstChoicesCV,_ = curve_fit(func2D, n, avRMfirstChoices)
    avGENfirstChoicesCV,_ = curve_fit(func2D, n, avGENfirstChoices)
    avGMfirstChoicesCV,_ = curve_fit(func2D, n, avGMfirstChoices)
    plt.plot(n, avRMfirstChoices, 'o', color='skyblue', label="rank-maximal")
    plt.plot(n, avGMfirstChoices, '*', color='orangered', label="median")
    plt.plot(n, avGENfirstChoices, 's', color='seagreen', label="generous")
    
    plt.plot(newx, func2D(newx, avRMfirstChoicesCV[0], avRMfirstChoicesCV[1], avRMfirstChoicesCV[2]), '-', color='skyblue')
    plt.plot(newx, func2D(newx, avGMfirstChoicesCV[0], avGMfirstChoicesCV[1], avGMfirstChoicesCV[2]), '-', color='orangered')
    plt.plot(newx, func2D(newx, avGENfirstChoicesCV[0], avGENfirstChoicesCV[1], avGENfirstChoicesCV[2]), '-', color='seagreen')

    plt.legend()
    plt.xlabel("$n$")
    plt.ylabel("Average number of first choices")
    ax = plt.subplot()
    ax.spines["right"].set_visible(False)    
    ax.spines["top"].set_visible(False)
    plt.grid(linestyle="--")
    plt.savefig("./stats/tempStatsResults/sm_rm_firstChoices.pdf")


    #############
    # av degree
    plt.figure()
    plt.figure(facecolor='w', edgecolor='k', figsize=(7, 5))
    newx = np.linspace(10, 1000, 250)
    avRMdegreeCV,_ = curve_fit(func2D, n, avRMdegree)
    avGENdegreeCV,_ = curve_fit(func2D, n, avGENdegree)
    avGMdegreeCV,_ = curve_fit(func2D, n, avGMdegree)
    plt.plot(n, avRMdegree, 'o', color='skyblue', label="rank-maximal")
    plt.plot(n, avGMdegree, '*', color='orangered', label="median")
    plt.plot(n, avGENdegree, 's', color='seagreen', label="generous")
    
    plt.plot(newx, func2D(newx, avRMdegreeCV[0], avRMdegreeCV[1], avRMdegreeCV[2]), '-', color='skyblue')
    plt.plot(newx, func2D(newx, avGMdegreeCV[0], avGMdegreeCV[1], avGMdegreeCV[2]), '-', color='orangered')
    plt.plot(newx, func2D(newx, avGENdegreeCV[0], avGENdegreeCV[1], avGENdegreeCV[2]), '-', color='seagreen')

    plt.legend()
    plt.xlabel("$n$")
    plt.ylabel("Average degree")
    ax = plt.subplot()
    ax.spines["right"].set_visible(False)    
    ax.spines["top"].set_visible(False)
    plt.grid(linestyle="--")
    plt.savefig("./stats/tempStatsResults/sm_rm_degree.pdf")



# gets the average of an array or returns -1 if array is 0 in length
def getAverage(array):
    if len(array) == 0:
        return -1
    else:
        return np.mean(array, dtype=np.float64)


# gets the minimum of an array or returns -1 if array is 0 in length
def getMin(array):
    if len(array) == 0:
        return -1
    else:
        return np.min(array)



# gets the maximum of an array or returns -1 if array is 0 in length
def getMax(array):
    if len(array) == 0:
        return -1
    else:
        return np.max(array)



# gets the average profile of an array or returns -1 if array is 0 in length
def getAverageProfile(array2D):
    avP = [];
    # average profile
    if len(array2D) == 0:
        avP.append(-1.0)
    else:
        profile = np.array(array2D)
        # print profile
        # print profile.shape
        avprofile = profile.mean(axis=0)
        avprofile = np.around(avprofile, decimals=1)
        for x in avprofile:
            avP.append(x)
    return avP


# gets the minimum and maximum profile degree of an array or returns -1 if array is 0 in length
def getMinMaxAvDegree(array2D):
    minDegree = -1
    maxDegree = -1
    totalDegree = 0.0
    avDegree = -1
    # average profile
    if len(array2D) == 0:
        return minDegree, maxDegree, avDegree
    else:
        for profile in array2D:
            degree = getDegree(profile)
            totalDegree += degree
            if minDegree == -1 or degree < minDegree:
                minDegree = degree
            if maxDegree == -1 or degree > maxDegree:
                maxDegree = degree
    avDegree = float(totalDegree) / float(len(array2D))

    return minDegree, maxDegree, avDegree


def getMinMaxAvChoices(array2D, firstOrLast):
    minChoice = -1
    maxChoice = -1
    totalChoice = 0.0
    avChoice = -1
    if len(array2D) == 0:
        return minChoice, maxChoice, avChoice
    else:
        for profile in array2D:
            numChoice = -1;
            if firstOrLast == "first":
                numChoice = profile[0]
            elif firstOrLast == "last":
                numChoice = profile[len(profile) - 1]
            totalChoice += numChoice
            if minChoice == -1 or numChoice < minChoice:
                minChoice = numChoice
            if maxChoice == -1 or numChoice > maxChoice:
                maxChoice = numChoice
    avChoice = float(totalChoice) / float(len(array2D))

    return minChoice, maxChoice, avChoice



# gets the average profile of an array or returns -1 if array is 0 in length
def getAverageProfileString(array):
    avPString = "";
    # average profile
    avPString = "$<$ "
    for x in array:
        avPString += '${:0.1f}$ '.format(x)
    avPString += "$>$"
    return avPString


# gets the degree of a profile array or returns -1 if array is 0 in length
def getDegree(profile):
    # average profile
    if len(profile) == 0:
        return -1
    else:
        count = 0
        for i in reversed(profile):
            if i == 0:
                count = count + 1;
            if not i == 0:
                return len(profile) - count
        return len(profile) - count


# returns the average number of people in a final section of the profile
def getMinMaxAvLast(array2D, fractionOfProfile):
    if len(array2D) == 0:
        return -1, -1, -1
    else:
        profile2D = np.array(array2D)
        sums = []
        indexFrom = int(len(profile2D[0]) * (1 - fractionOfProfile))
        for i in range(len(profile2D)):
            sums.append(sum(profile2D[i][indexFrom:]))
        return np.array(sums).min(), np.array(sums).max(), np.array(sums).mean()


# returns the cieling of the division of two numbers
def ceildiv(a, b):
    return -(-a // b)



#####################################
# main def
#####################################
if __name__ == '__main__':
    main()

