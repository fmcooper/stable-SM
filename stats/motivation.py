import matplotlib
# matplotlib.use('Agg')
import sys
import numpy as np
import matplotlib.pylab as plt
import glob
import math
from scipy.stats import sem
from scipy.interpolate import interp1d, splrep, splev
from scipy.optimize import curve_fit
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
                     "S200", "S300", "S400", "S500", "S600", "S700", "S800", "S900", "S1000", "S2000", "S3000", "S4000", "S5000"]
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

    # # calculate results
    now = datetime.datetime.now()
    avstatsFile = open(avstats, 'w')
    avstatsFile.write("Stats runthrough conducted at: " + now.strftime("%Y-%m-%d %H:%M") + "\n\n")
    avstatsFile.close()

    # for each experiment type
    for ind, exptype in enumerate(expTypeNames):
        print(exptype)
        postPathResults = "/Results_stable/"

        calculateResults(exptype, prePath, postPathResults)

        # get averages
        getAverages(exptype)

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
    avstatsFile.write('{}avNumRotations {:0.1f}\n'.format(exptype, getAverage([len(exp.rotations) for exp in expStats])))
    avstatsFile.write('{}avMaxRotDegree {:0.1f}\n'.format(exptype, getAverage([exp.maxDegree for exp in expStats])))
    avstatsFile.write('{}avBitsExp {:0.1f}\n'.format(exptype, getAverage([exp.bitsRequiredExponential for exp in expStats])))
    avstatsFile.write('{}avBitsIndices {:0.1f}\n'.format(exptype, getAverage([exp.bitsRequiredCompressed for exp in expStats])))

    avstatsFile.write('{}medianBitsExp {:0.1f}\n'.format(exptype, getMedian([exp.bitsRequiredExponential for exp in expStats])))
    avstatsFile.write('{}medianBitsIndices {:0.1f}\n'.format(exptype, getMedian([exp.bitsRequiredCompressed for exp in expStats])))
    
    avstatsFile.write('{}5PerBitsExp {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredExponential for exp in expStats], 5.0)))
    avstatsFile.write('{}5PerBitsIndices {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredCompressed for exp in expStats], 5.0)))
    
    avstatsFile.write('{}95PerBitsExp {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredExponential for exp in expStats], 95.0)))
    avstatsFile.write('{}95PerBitsIndices {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredCompressed for exp in expStats], 95.0)))
    
    avstatsFile.write('{}16PerBitsExp {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredExponential for exp in expStats], 16.0)))
    avstatsFile.write('{}16PerBitsIndices {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredCompressed for exp in expStats], 16.0)))
    
    avstatsFile.write('{}84PerBitsExp {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredExponential for exp in expStats], 84.0)))
    avstatsFile.write('{}84PerBitsIndices {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredCompressed for exp in expStats], 84.0)))
    
    avstatsFile.write('{}2p5PerBitsExp {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredExponential for exp in expStats], 2.5)))
    avstatsFile.write('{}2p5PerBitsIndices {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredCompressed for exp in expStats], 2.5)))
    
    avstatsFile.write('{}97p5PerBitsExp {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredExponential for exp in expStats], 97.5)))
    avstatsFile.write('{}97p5PerBitsIndices {:0.1f}\n'.format(exptype, getPercentile([exp.bitsRequiredCompressed for exp in expStats], 97.5)))
    
    avstatsFile.close()



# collect the raw data from each instance file
def collectRawData(exp, pathResults):
    print(pathResults) 

    expStats = []
    totalInstances = 0
    totalTimeout = 0



    # run over the results
    for name in os.listdir(pathResults):
        if os.path.isfile(pathResults + name):
            totalInstances+=1
            timeout = False
            rotations = []
            with open(pathResults + name) as f:
                content = f.readlines()
                for s in content:
                    # general info
                    if "timeout" in s:
                        totalTimeout += 1
                        timeout = True
                    if "rotProfileCombined_" in s:
                        prof = s.split()
                        profNum = []
                        for x in range(1,len(prof)):
                            profNum.append(int(prof[x]))
                        rotations.append(profNum)

                if not timeout:
                    # we are only going to look at instances where the number of rotations is > 0
                    if len(rotations) > 0:
                        print(name, rotations)
                        exp = experiment(rotations)
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



# matplotlib plots
def createPlot():
    # collect the data
    avBitsExp = []
    z5PerBitsExp = []
    z95PerBitsExp = []
    z16PerBitsExp = []
    z84PerBitsExp = []
    z2p5PerBitsExp = []
    z97p5PerBitsExp = []
    avBitsIndices = []
    z5PerBitsIndices = []
    z95PerBitsIndices = []
    z16PerBitsIndices = []
    z84PerBitsIndices = []
    z2p5PerBitsIndices = []
    z97p5PerBitsIndices = []
    n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000]

    
    for exp in expTypeNames:
        avBitsExp.append(float(d[exp+'medianBitsExp'][0]))
        z5PerBitsExp.append(float(d[exp+'5PerBitsExp'][0]))
        z95PerBitsExp.append(float(d[exp+'95PerBitsExp'][0]))
        z16PerBitsExp.append(float(d[exp+'16PerBitsExp'][0]))
        z84PerBitsExp.append(float(d[exp+'84PerBitsExp'][0]))
        z2p5PerBitsExp.append(float(d[exp+'2p5PerBitsExp'][0]))
        z97p5PerBitsExp.append(float(d[exp+'97p5PerBitsExp'][0]))

        # avBitsTruncated.append(float(d[exp+'avBitsTruncated'][0]))
        avBitsIndices.append(float(d[exp+'medianBitsIndices'][0]))
        z5PerBitsIndices.append(float(d[exp+'5PerBitsIndices'][0]))
        z95PerBitsIndices.append(float(d[exp+'95PerBitsIndices'][0]))
        z16PerBitsIndices.append(float(d[exp+'16PerBitsIndices'][0]))
        z84PerBitsIndices.append(float(d[exp+'84PerBitsIndices'][0]))
        z2p5PerBitsIndices.append(float(d[exp+'2p5PerBitsIndices'][0]))
        z97p5PerBitsIndices.append(float(d[exp+'97p5PerBitsIndices'][0]))
        

    # converting to np arrays
    n = np.array(n)
    avBitsExp = np.array(avBitsExp)
    avBitsIndices = np.array(avBitsIndices)
    avBitsExp[ avBitsExp==-1.0 ] = np.nan
    avBitsIndices[ avBitsIndices==-1.0 ] = np.nan

    # datapoints that are not involved in the curve calc (NCD - Non Curve Data)
    nNCD = np.concatenate((n[:9],n[19:]))
    avBitsExpNCD = np.concatenate((avBitsExp[:9],avBitsExp[19:]))
    avBitsIndicesNCD = np.concatenate((avBitsIndices[:9],avBitsIndices[19:]))

    # datapoints involved in creating the curves
    nCurveData = n[9:19]
    avBitsExpCurveData = avBitsExp[9:19]
    z5PerBitsExpCurveData = z5PerBitsExp[9:19]
    z95PerBitsExpCurveData = z95PerBitsExp[9:19]
    avBitsIndicesCurveData = avBitsIndices[9:19]
    z5PerBitsIndicesCurveData = z5PerBitsIndices[9:19]
    z95PerBitsIndicesCurveData = z95PerBitsIndices[9:19]

    # curve function
    newx = np.logspace(0, 5, 250)
    def func(x, a, b, c):
        return a + b*x + c*x*x

    poptExpAv,_ = curve_fit(func, np.log(nCurveData), np.log(avBitsExpCurveData))
    poptExp5,_ = curve_fit(func, np.log(nCurveData), np.log(z5PerBitsExpCurveData))
    poptExp95,_ = curve_fit(func, np.log(nCurveData), np.log(z95PerBitsExpCurveData))
    poptIndAv,_ = curve_fit(func, np.log(nCurveData), np.log(avBitsIndicesCurveData))
    poptInd5,_ = curve_fit(func, np.log(nCurveData), np.log(z5PerBitsIndicesCurveData))
    poptInd95,_ = curve_fit(func, np.log(nCurveData), np.log(z95PerBitsIndicesCurveData))
    
    print(poptExpAv)
    print(poptIndAv)

    # plotting
    plt.figure(facecolor='w', edgecolor='k', figsize=(7, 5))
    plt.xlabel("$n$")
    plt.ylabel("bits required")

    expColor = 'orangered'
    plt.plot(nCurveData, avBitsExpCurveData, 'o', color=expColor, label="Exponential representation")
    plt.plot(nNCD, avBitsExpNCD, 'o', color=expColor, fillstyle='none', label="Exponential representation (not used to calculate curve)")
    plt.plot(newx, np.exp(func(np.log(newx), poptExpAv[0], poptExpAv[1], poptExpAv[2])), '-', color=expColor)
    plt.fill_between(newx, np.exp(func(np.log(newx), poptExp5[0], poptExp5[1], poptExp5[2])), np.exp(func(np.log(newx), poptExp95[0], poptExp95[1], poptExp95[2])), color=expColor, alpha=.5)

    indColor = 'seagreen'
    plt.plot(nCurveData, avBitsIndicesCurveData, 'o', color=indColor, label="Compressed representation")
    plt.plot(nNCD, avBitsIndicesNCD, 'o', color=indColor, fillstyle='none', label="Compressed representation (not used to calculate curve)")
    plt.plot(newx, np.exp(func(np.log(newx), poptIndAv[0], poptIndAv[1], poptIndAv[2])), '-', color=indColor)
    plt.fill_between(newx, np.exp(func(np.log(newx), poptInd5[0], poptInd5[1], poptInd5[2])), np.exp(func(np.log(newx), poptInd95[0], poptInd95[1], poptInd95[2])), color=indColor, alpha=.5)


    # horizontal lines
    gb = 8589934592
    mb100 = 838860800
    mb10 = 83886080
    mb1 = 8388608
    ax = plt.subplot()
    ax.axhline(y=mb1, xmin=0.0, xmax=1.0, color='gray', linestyle='-', linewidth=.5)
    ax.axhline(y=mb10, xmin=0.0, xmax=1.0, color='gray', linestyle='-', linewidth=.5)
    ax.axhline(y=mb100, xmin=0.0, xmax=1.0, color='gray', linestyle='-', linewidth=.5)
    ax.axhline(y=gb, xmin=0.0, xmax=1.0, color='gray', linestyle='-', linewidth=.5)
    ax.annotate('1MB', xy=(1.5, mb1+1000000), xytext=(1.5, mb1+1000000), color='gray')
    ax.annotate('10MB', xy=(1.5, mb10+10000000), xytext=(1.5, mb10+10000000), color='gray')
    ax.annotate('100MB', xy=(1.5, mb100+100000000), xytext=(1.5, mb100+100000000), color='gray')
    ax.annotate('1GB', xy=(1.5, gb+1000000000), xytext=(1.5, gb+1000000000), color='gray')


    # general plot info
    plt.legend()
    ax = plt.subplot()
    # ax.spines["right"].set_visible(False)    
    # ax.spines["top"].set_visible(False) 
    ax.set_xlim(1, 100000)
    plt.xscale('log')
    plt.yscale('log')
    # plt.grid()
    ax.xaxis.grid(True)
    # plt.show()
    plt.tight_layout()
    plt.savefig("./stats/motivation/spaceComparison.pdf")


# gets the average of an array or returns -1 if array is 0 in length
def getAverage(array):
    if len(array) == 0:
        return -1
    else:
        return np.mean(array, dtype=np.float64)


# gets the median of an array or returns -1 if array is 0 in length
def getMedian(array):
    if len(array) == 0:
        return -1
    else:
        return np.median(array)

# gets a given percentile of an array or returns -1 if array is 0 in length
def getPercentile(array, percentile):
    if len(array) == 0:
        return -1
    else:
        return np.percentile(array, percentile)



#####################################
# main def
#####################################
if __name__ == '__main__':
    main()

