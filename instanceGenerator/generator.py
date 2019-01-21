# Generates a single instance from argument parameters

import sys
import numpy as np
import random
import time

# retrieve parameters
inputPath = sys.argv[1]
inputPathSplit = inputPath.split("/")
finalpartSplit = inputPathSplit[len(inputPathSplit) - 1].split("_")
parameters = finalpartSplit[0].split("-")

numMenOrWomen = int(parameters[0])
minLenPref = int(parameters[1])
maxLenPref = int(parameters[2])
skew = int(parameters[3])

instanceInfo = "instance parameter information\n"
instanceInfo = instanceInfo + "numMenOrWomen: " + str(numMenOrWomen) + "\n"
instanceInfo = instanceInfo + "minLenPref: " + str(minLenPref) + "\n"
instanceInfo = instanceInfo + "maxLenPref: " + str(maxLenPref) + "\n"
instanceInfo = instanceInfo + "skew: " + str(skew) + "\n"


# create random lists of men and women
randomCompPrefListMen = np.arange(1, numMenOrWomen + 1)
randomCompPrefListWomen = np.arange(1, numMenOrWomen + 1)
random.shuffle(randomCompPrefListMen)
random.shuffle(randomCompPrefListWomen)


# create distribution
distribution = [0.0] * numMenOrWomen
distribution[0] = 1.0
for x in range(1, numMenOrWomen):
    distribution[x] = float(x * skew + 1)
distribution = distribution / np.sum(distribution)

prefListsMen = [[]] * numMenOrWomen
prefListsWomen = [[]] * numMenOrWomen


# creating preference lists
for x in range(numMenOrWomen):
    #lengthList = np.random.randint(minLenPref, maxLenPref + 1)
    lengthList = numMenOrWomen
    preflistMen = np.random.choice(randomCompPrefListMen, lengthList, replace=False, p=distribution)
    prefListsMen[x] = preflistMen

    #lengthList = np.random.randint(minLenPref, maxLenPref + 1)
    lengthList = numMenOrWomen
    preflistWomen = np.random.choice(randomCompPrefListWomen, lengthList, replace=False, p=distribution)
    prefListsWomen[x] = preflistWomen



# output
print(str(numMenOrWomen))

for x in range(numMenOrWomen):
    manNum = x + 1
    prefList = ' '.join(str(e) for e in prefListsMen[x])
    print(str(manNum) + ": " + prefList)


for x in range(numMenOrWomen):
    womanNum = x + 1
    prefList = ' '.join(str(e) for e in prefListsWomen[x])
    print(str(womanNum) + ": " + prefList)

print("\n" + instanceInfo)








