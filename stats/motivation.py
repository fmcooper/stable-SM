import matplotlib
# matplotlib.use('Agg')
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
from motivationClasses import experiment
import numpy.polynomial.polynomial as poly

# Iterates over all results files and collates results.
# @author Frances

np.set_printoptions(suppress=True)
prePath = sys.argv[1]

################# variables
expTypeNames = ["S10", "S20", "S30", "S40", "S50", "S60", "S70", "S80", "S90", "S100", \
                     "S200", "S300", "S400", "S500", "S600", "S700", "S800", "S900", "S1000"]
dirName = "stats/motivation"
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
    # now = datetime.datetime.now()
    # avstatsFile = open(avstats, 'w')
    # avstatsFile.write("Stats runthrough conducted at: " + now.strftime("%Y-%m-%d %H:%M") + "\n\n")
    # avstatsFile.close()

    # for each experiment type
    for ind, exptype in enumerate(expTypeNames):
        print exptype
        postPathResults = "/Results_stable/"

        # calculateResults(exptype, prePath, postPathResults)

        # get averages
        getAverages(exptype)

    # # create table for paper
    # createLatex()

    # create plots
    createPlot()

    exit(0)


#####################################
# calculate results
#####################################
def calculateResults(exptype, prePath, postPathResults):

    infeasibleCounts = []
    pathResults = prePath + exptype + postPathResults


    # collect the raw data and calculate the averages for latex
    totalInstances, totalTimeout, expStats = collectRawData(exptype, pathResults)


    # calculate the averages and output
    avstatsFile = open(avstats, "a")
    avstatsFile.write('\n# stats file for all instance types of ' + exptype + '\n')
    avstatsFile.write('{}totalInstances {:0.1f}\n'.format(exptype, totalInstances))
    avstatsFile.write('{}totalInstancesUsedInCalcs {:0.1f}\n'.format(exptype, len(expStats)))
    avstatsFile.write('{}avNumRotations {:0.1f}\n'.format(exptype, getAverage([exp.numRotations for exp in expStats])))
    avstatsFile.write('{}avMinRotDegree {:0.1f}\n'.format(exptype, getAverage([exp.minRotDegree for exp in expStats])))
    avstatsFile.write('{}avMaxRotDegree {:0.1f}\n'.format(exptype, getAverage([exp.maxRotDegree for exp in expStats])))
    avstatsFile.write('{}avAvRotDegree {:0.1f}\n'.format(exptype, getAverage([exp.avRotDegree for exp in expStats])))
    avstatsFile.write('{}avAvNpDegree {:0.1f}\n'.format(exptype, getAverage([exp.avNpDegree for exp in expStats])))
    avstatsFile.write('{}avBitsExp {:0.1f}\n'.format(exptype, getAverage([exp.bitsExp for exp in expStats])))
    avstatsFile.write('{}avBitsTruncated {:0.1f}\n'.format(exptype, getAverage([exp.bitsTruncated for exp in expStats])))
    avstatsFile.write('{}avBitsIndices {:0.1f}\n'.format(exptype, getAverage([exp.bitsIndices for exp in expStats])))
    
    avstatsFile.close()



# collect the raw data from each instance file
def collectRawData(exp, pathResults):
    print(pathResults) 

    expStats = []
    totalInstances = 0
    totalTimeout = 0

    rotations = []


    # run over the results
    for name in os.listdir(pathResults):
        if os.path.isfile(pathResults + name):
            totalInstances+=1
            timeout = False
            exp = experiment()
            with open(pathResults + name) as f:
                content = f.readlines()
                for s in content:
                    # general info
                    if "timeout" in s:
                        totalTimeout += 1
                        timeout = True
                    if "numRotations" in s:
                        exp.numRotations = int(s.split()[1])
                    if "rotProfileCombined_" in s:
                        prof = s.split()
                        profNum = []
                        for x in range(1,len(prof)):
                            profNum.append(int(prof[x]))
                        rotations.append(profNum)

                if not timeout:
                    minDegree, maxDegree, avDegree = getMinMaxAvDegree(rotations)
                    avNpSize = getNumpyAvSize(rotations)
                    exp.minRotDegree = minDegree
                    exp.maxRotDegree = maxDegree
                    exp.avRotDegree = avDegree
                    exp.avNpDegree = avNpSize
                    if len(rotations) > 0:
                        exp.calculateSpaceRequirements(len(rotations[0]))
                        # we are only going to look at instances where the number of rotations is > 0
                        expStats.append(exp)

    return totalInstances, totalTimeout, expStats
    


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


# # create latex tables
# def createLatex():
#     # instance info
#     latexpaper = dirName + "/" + "latex_table_instance_info.txt"
#     latexPaperFile = open(latexpaper, 'w')
#     latexPaperFile.write('\\begin{table}[] \centerline{')
#     latexPaperFile.write('\\begin{tabular}{ p{1.5cm} | p{1.5cm} p{1.5cm} p{1.5cm} p{2.5cm} }') 
#     latexPaperFile.write('\hline\hline ')
#     latexPaperFile.write('Case & $N_I$ & Timeout & $n$ & time (ms) \\\\ \n')
#     latexPaperFile.write('\hline ')

#     for i in xrange(0, len(expTypeNames)):
#         exp = expTypeNames[i]
#         latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
#             exp,  d[exp+'numInstances'][0], d[exp+'numTimeout'][0], d[exp+'numMenOrWomen'][0], d[exp+'AvD_Total'][0] ))

#     # finishing the latex results file
#     latexPaperFile.write('\hline\hline \end{tabular}} \caption{General instance information.} \label{} \end{table} ')
#     latexPaperFile.close 



#     # # table 1 - basic stats
#     latexpaper = dirName + "/" + "latex_table_generalStats.txt"
#     latexPaperFile = open(latexpaper, 'w')
#     latexPaperFile.write('\\begin{table}[] \centerline{')
#     latexPaperFile.write('\\begin{tabular}{ p{1.5cm} | p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} p{1.5cm} }') 
#     latexPaperFile.write('\hline\hline ')
#     latexPaperFile.write('Case & $|\mathcal{R}|$ & $|\mathcal{M}|$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
#     latexPaperFile.write('\hline ')

#     for i in xrange(0, len(expTypeNames)):
#         exp = expTypeNames[i]
#         latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
#             exp, d[exp+'avNumRotations'][0], d[exp+'avNumStableMatchings'][0], \
#             # d[exp+'minDegree'][0], d[exp+'maxDegree'][0], d[exp+'avDegree'][0], \
#             d[exp+'minEgalCost'][0], d[exp+'maxEgalCost'][0], d[exp+'avEgalCost'][0], \
#             d[exp+'minSeCost'][0], d[exp+'maxSeCost'][0], d[exp+'avSeCost'][0]))

#     # finishing the latex results file
#     latexPaperFile.write('\hline\hline \end{tabular}} \caption{General stats results.} \label{} \end{table} ')
#     latexPaperFile.close 


#     # table 2 - RM info
#     latexpaper = dirName + "/" + "latex_table_RM.txt"
#     latexPaperFile = open(latexpaper, 'w')
#     latexPaperFile.write('\\begin{table}[] \centerline{')
#     latexPaperFile.write('\\begin{tabular}{ p{1.1cm} | p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.1cm} }') 
#     latexPaperFile.write('\hline\hline ')
#     latexPaperFile.write('Case & $\min(f)$ & $\max(f)$ & av$(f)$ & $\min(l_{10})$ & $\max(l_{10})$ & av$(l_{10})$ & $\min(d)$ & $\max(d)$ & av$(d)$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
#     latexPaperFile.write('\hline ')

#     for i in xrange(0, len(expTypeNames)):
#         exp = expTypeNames[i]
#         profile = ' '.join(str(e) for e in d[exp+'avRMprofile'][0:])
#         latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
#             exp, \
#             d[exp+'minRMfirstChoices'][0], d[exp+'maxRMfirstChoices'][0], d[exp+'avRMfirstChoices'][0], \
#             d[exp+'minRMlast10pc'][0], d[exp+'maxRMlast10pc'][0], d[exp+'avRMlast10pc'][0], \
#             d[exp+'minRMdegree'][0], d[exp+'maxRMdegree'][0], d[exp+'avRMdegree'][0], \
#             d[exp+'minRMegalCost'][0], d[exp+'maxRMegalCost'][0], d[exp+'avRMegalCost'][0], \
#             d[exp+'minRMseCost'][0], d[exp+'maxRMseCost'][0], d[exp+'avRMseCost'][0]))

#     # finishing the latex results file
#     latexPaperFile.write('\hline\hline \end{tabular}} \caption{Rank-maximal results.} \label{} \end{table} ')
#     latexPaperFile.close 


#     # # table 3 - GEN info
#     latexpaper = dirName + "/" + "latex_table_GEN.txt"
#     latexPaperFile = open(latexpaper, 'w')
#     latexPaperFile.write('\\begin{table}[] \centerline{')
#     latexPaperFile.write('\\begin{tabular}{ p{1.1cm} | p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.1cm} }') 
#     latexPaperFile.write('\hline\hline ')
#     latexPaperFile.write('Case & $\min(f)$ & $\max(f)$ & av$(f)$ & $\min(l_{50})$ & $\max(l_{50})$ & av$(l_{50})$ & $\min(d)$ & $\max(d)$ & av$(d)$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
#     latexPaperFile.write('\hline ')

#     for i in xrange(0, len(expTypeNames)):
#         exp = expTypeNames[i]
#         profile = ' '.join(str(e) for e in d[exp+'avGENprofile'][0:])
#         latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
#             exp, \
#             d[exp+'minGENfirstChoices'][0], d[exp+'maxGENfirstChoices'][0], d[exp+'avGENfirstChoices'][0], \
#             d[exp+'minGENlast50pc'][0], d[exp+'maxGENlast50pc'][0], d[exp+'avGENlast50pc'][0], \
#             d[exp+'minGENdegree'][0], d[exp+'maxGENdegree'][0], d[exp+'avGENdegree'][0], \
#             d[exp+'minGENegalCost'][0], d[exp+'maxGENegalCost'][0], d[exp+'avGENegalCost'][0], \
#             d[exp+'minGENseCost'][0], d[exp+'maxGENseCost'][0], d[exp+'avGENseCost'][0]))

#     # finishing the latex results file
#     latexPaperFile.write('\hline\hline \end{tabular}} \caption{Generous results.} \label{} \end{table} ')
#     latexPaperFile.close 


#     # # table 4 - GM info
#     latexpaper = dirName + "/" + "latex_table_GM.txt"
#     latexPaperFile = open(latexpaper, 'w')
#     latexPaperFile.write('\\begin{table}[] \centerline{')
#     latexPaperFile.write('\\begin{tabular}{ p{1.1cm} | p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.4cm} p{1.1cm} p{1.1cm} p{1.1cm} }') 
#     latexPaperFile.write('\hline\hline ')
#     latexPaperFile.write('Case & $\min(f)$ & $\max(f)$ & av$(f)$ & $\min(l_{20})$ & $\max(l_{20})$ & av$(l_{20})$ & $\min(d)$ & $\max(d)$ & av$(d)$ & $\min(e)$ & $\max(e)$ & av$(e)$ & $\min(e_d)$ & $\max(e_d)$ & av$(e_d)$ \\\\ \n')
#     latexPaperFile.write('\hline ')

#     for i in xrange(0, len(expTypeNames)):
#         exp = expTypeNames[i]
#         profile = ' '.join(str(e) for e in d[exp+'avGMprofile'][0:])
#         latexPaperFile.write('{} & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ & ${}$ \\\\ \n '.format(\
#             exp, \
#             d[exp+'minGMfirstChoices'][0], d[exp+'maxGMfirstChoices'][0], d[exp+'avGMfirstChoices'][0], \
#             d[exp+'minGMlast20pc'][0], d[exp+'maxGMlast20pc'][0], d[exp+'avGMlast20pc'][0], \
#             d[exp+'minGMdegree'][0], d[exp+'maxGMdegree'][0], d[exp+'avGMdegree'][0], \
#             d[exp+'minGMegalCost'][0], d[exp+'maxGMegalCost'][0], d[exp+'avGMegalCost'][0], \
#             d[exp+'minGMseCost'][0], d[exp+'maxGMseCost'][0], d[exp+'avGMseCost'][0]))

#     # finishing the latex results file
#     latexPaperFile.write('\hline\hline \end{tabular}} \caption{Median results.} \label{} \end{table} ')
#     latexPaperFile.close 


# matplotlib plots
def createPlot():
    # collect the data
    avBitsExp = []
    avBitsTruncated = []
    avBitsIndices = []
    n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    avBitsInstanceFile = []
    for x in range(18):
        avBitsInstanceFile.append(np.nan)
    
    for exp in expTypeNames:
        avBitsExp.append(float(d[exp+'avBitsExp'][0]))
        avBitsTruncated.append(float(d[exp+'avBitsTruncated'][0]))
        avBitsIndices.append(float(d[exp+'avBitsIndices'][0]))
    for x in range(9):
        avBitsExp.append(np.nan)
        avBitsTruncated.append(np.nan)
        avBitsIndices.append(np.nan)
        n.append(1000 + ((x+1) * 1000))

    avBitsPreferenceLists = []
    for x in n:
        # nums up to n
        eachPrefElemBits = math.ceil(math.log(x, 2))
        numPrefs = 2 * x * x
        avBitsPreferenceLists.append(eachPrefElemBits * numPrefs)


    print(avBitsPreferenceLists)
    avBitsInstanceFile = avBitsInstanceFile + [65431142.4, 298634444.8, 699609907.2, 1268357529.6, 2004877312, 2909169254.4, 3981233356.8, 5221069619.2, 6628678041.6, 8204058624]


    print(n[-1])
    n = np.array(n)
    avBitsExp = np.array(avBitsExp)
    avBitsTruncated = np.array(avBitsTruncated)
    avBitsIndices = np.array(avBitsIndices)
    # avBitsExp = np.log(avBitsExp)
    # avBitsTruncated = np.log(avBitsTruncated)
    # avBitsIndices = np.log(avBitsIndices)
    # n = np.log(n)



    avBitsExp[ avBitsExp==-1.0 ] = np.nan
    avBitsTruncated[ avBitsTruncated==-1.0 ] = np.nan
    avBitsIndices[ avBitsIndices==-1.0 ] = np.nan

    print(avBitsExp, avBitsTruncated, avBitsIndices)

    plt.figure()
    plt.figure(facecolor='w', edgecolor='k', figsize=(8, 5))
    plt.xlabel("$n$")
    plt.ylabel("bits required")
    # plt.xlabel("$log(n)$")
    # plt.ylabel("log(bits required)")

    plt.plot(n, avBitsExp, 'o', color='black', label="exponential")
    idx = np.isfinite(n) & np.isfinite(avBitsExp)
    coefs = poly.polyfit(n[idx], avBitsExp[idx], 2)
    ffit = poly.polyval(n, coefs)
    plt.plot(n, ffit, '-', color='black')

    plt.plot(n, avBitsTruncated, 'o', color='blue', label="truncated")
    idx = np.isfinite(n) & np.isfinite(avBitsTruncated)
    coefs = poly.polyfit(n[idx], avBitsTruncated[idx], 2)
    ffit = poly.polyval(n, coefs)
    plt.plot(n, ffit, '-', color='blue')

    plt.plot(n, avBitsIndices, 'o', color='red', label="indices")
    idx = np.isfinite(n) & np.isfinite(avBitsIndices)
    coefs = poly.polyfit(n[idx], avBitsIndices[idx], 2)
    ffit = poly.polyval(n, coefs)
    plt.plot(n, ffit, '-', color='red')

    # plt.plot(n, avBitsInstanceFile, 'o', color='purple', label="text file")
    # idx = np.isfinite(avBitsInstanceFile)
    # coefs = poly.polyfit(n[idx], avBitsIndices[idx], 2)
    # ffit = poly.polyval(n, coefs)
    # plt.plot(n, ffit, '-', color='purple')

    # plt.plot(n, avBitsPreferenceLists, 'o', color='orange', label="preference lists in memory")
    # idx = np.isfinite(avBitsIndices)
    # coefs = poly.polyfit(n, avBitsPreferenceLists, 2)
    # ffit = poly.polyval(n, coefs)
    # plt.plot(n, ffit, '-', color='orange')


    plt.legend()

    ax = plt.subplot()
    gb = 8589934592
    mb100 = 838860800
    mb10 = 83886080
    mb1 = 8388608
    ax.axhline(y=mb1, xmin=0.0, xmax=1.0, color='green')
    ax.axhline(y=mb10, xmin=0.0, xmax=1.0, color='green')
    # ax.axhline(y=mb100, xmin=0.0, xmax=1.0, color='green')
    # ax.axhline(y=gb, xmin=0.0, xmax=1.0, color='green')
    # ax.axhline(y=math.log(mb1), xmin=0.0, xmax=1.0, color='green')
    # ax.axhline(y=math.log(mb10), xmin=0.0, xmax=1.0, color='green')
    # ax.axhline(y=math.log(mb100), xmin=0.0, xmax=1.0, color='green')
    # ax.axhline(y=math.log(gb), xmin=0.0, xmax=1.0, color='green')


    plt.show()

    # # create the plot
    # plt.figure()
    # plt.figure(facecolor='w', edgecolor='k', figsize=(8, 5))
    # plt.xlabel("$n$ $\ln$ $n$")
    # plt.ylabel("Average number of stable matchings $|\mathcal{M}|$")
    # plt.xlim(0,7300)
    # plt.ylim(0,1190)
    # ax = plt.subplot(111)
    # ax.spines["right"].set_visible(False)    
    # ax.spines["top"].set_visible(False) 
    # plt.plot(nlogn, avstable, 'o', linestyle='-', markersize=4)
    # for y in range(0, 1190, 200):    
    #     plt.plot(range(0, 7300), [y] * len(range(0, 7300)), "--", lw=0.5, color="black", alpha=0.3) 
    # for x in range(0, 7300, 1000):    
    #     plt.plot([x] * len(range(0, 1190)), range(0, 1190), "--", lw=0.5, color="black", alpha=0.3)
    # plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on") 
    # plt.savefig("./stats/tempStatsResults/nlogn.pdf")


# gets the average of an array or returns -1 if array is 0 in length
def getAverage(array):
    if len(array) == 0:
        return -1
    else:
        return np.mean(array, dtype=np.float64)


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


def getNumpyAvSize(array2D):
    totalSize = 0.0
    averageSize = -1
    if len(array2D) == 0:
        return averageSize
    else:
        converted = np.array(array2D)
        for array in converted:
            nonZeroIndices = np.nonzero(array)
            totalSize = totalSize + len(nonZeroIndices[0])
        return totalSize / float(len(array2D))




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


#####################################
# main def
#####################################
if __name__ == '__main__':
    main()

