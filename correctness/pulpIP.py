from pulp import *
import numpy as np
import sys
import datetime

# Tests that all stable matchings are found using an IP (and pulp).
# @author Frances

# recording the duration
start = datetime.datetime.now()

# inputting 
numMen = -1
menPrefs = []
womenPrefs = []
inFileName = sys.argv[1]
timeLimitSecs = int(sys.argv[2])
with open(inFileName) as f:
    for index,line in enumerate(f):
        if index == 0:
            # check for upstream issue
            firstToken = line.split()[0]
            if "timeout" in firstToken:
                exit(4)
            numMen = int(firstToken)

        # mens preferences
        elif index > 0 and index <= numMen:
            menPrefs.append([int(a) for a in line.split()[1:]])

        # womens preferences
        elif index > numMen and index <= numMen * 2:
            womenPrefs.append([int(a) for a in line.split()[1:]])


# labels for agents (just a list of indices)
menOrWomen = []
for i in range(numMen):
    menOrWomen.append(i)
men = menOrWomen
women = menOrWomen

# labels for preference lists
menPrefsIndices = [[0 for x in range(numMen)] for y in range(numMen)] 
womenPrefsIndices = [[0 for x in range(numMen)] for y in range(numMen)] 

for i in range(numMen):
    for j in range(numMen):
        menPrefsIndices[i][j] = menPrefs[i][j] - 1
        womenPrefsIndices[i][j] = womenPrefs[i][j] - 1


# creating the model
global prob
prob = LpProblem("Stable matchings",LpMinimize)
menChoices = LpVariable.dicts("MenChoices", (menOrWomen, menOrWomen),0,1,LpInteger)
womenChoices = LpVariable.dicts("WomenChoices", (menOrWomen, menOrWomen),0,1,LpInteger)

prob += 0, "Arbitrary Objective Function"

# if man m is assigned to woman w then woman w is assigned to man m
for m in range(numMen):
    for indw, w in enumerate(menPrefsIndices[m]):
        womanPref = womenPrefsIndices[w]
        for indwm, wm in enumerate(womanPref):
            if wm == m:
                prob += menChoices[m][indw] == womenChoices[w][indwm],"assigning_{}_{}".format(m, w)
                

# each man and woman is assigned to one partner (complete preference lists)
for i in range(numMen):
    prob += pulp.lpSum([menChoices[i][j] for j in range(numMen)]) == 1,"menlimit_{}".format(i)
    prob += pulp.lpSum([womenChoices[i][j] for j in range(numMen)]) == 1,"womenlimit_{}".format(i)


# add blocking pair constraint
def addBPConstraints(prob, mInd, mPrefInd):
    # cannot have that the man wants to move and the woman wants to move
    # so sum allocations for man from this rank up and woman from this rank up and ensure sum is greater than 0
    varsToSum = []

    for i in range(mPrefInd + 1):
        varsToSum.append(menChoices[mInd][i])

    wInd = menPrefsIndices[mInd][mPrefInd]
    wPrefs = womenPrefsIndices[wInd]
    wPrefInd = -1
    index = 0
    while wPrefInd == -1:
        if wPrefs[index] == mInd:
            wPrefInd = index
        index = index + 1

    for i in range(wPrefInd + 1):
        varsToSum.append(womenChoices[wInd][i])

    prob += pulp.lpSum(varsToSum) >= 1,"blockingPair_{}_{}".format(mInd, mPrefInd)
    return prob


# for each man woman pair - ensure that the man and woman don't create a blocking pair
for mInd in range(numMen):
    for mPrefInd in range(numMen):
        prob = addBPConstraints(prob, mInd, mPrefInd)


# solve the problem
# keep iterating, outputting solutions, until I stop finding them
print("\nsolutions_found_by_ip:")

statusOpt = "Optimal"
global status
status = statusOpt
solnIndex = 0
while (status == statusOpt):
    timeLeft = timeLimitSecs - (datetime.datetime.now() - start).total_seconds() + 1 # adding 10s to give slack - will not output later if beyone time limit
      
    if timeLeft >= 0:
        solver_options = ['set timelimit {}'.format(timeLeft),
                'set threads {}'.format(1),
                ]
        prob.solve(CPLEX_CMD(msg=0, options=solver_options))
        # prob.solve(GUROBI_CMD(msg=0, options=[("TimeLimit",timeLeft), ("Threads",1), ("OutputFlag",0)]))
        # prob.solve(PULP_CBC_CMD(maxSeconds = timeLeft, threads = 1, msg = 0))
    # prob.writeLP("test.lp")
    status = LpStatus[prob.status]
    timeLeft = timeLimitSecs - (datetime.datetime.now() - start).total_seconds()
    if (status == statusOpt and timeLeft >= 0):
        
        assignments = [-1] * numMen
        varsToSum = []

        out = "men\n"
        for m in range(numMen):
            for w in range(numMen):
                value = menChoices[m][w].varValue
                out += str(value) + " "
                if value >= 0.9:

                    assignments[m] = menPrefs[m][w]
                    varsToSum.append(menChoices[m][w])
            out+="\n"

        out += "\nwomen\n"
        for m in men:
            for w in women:
                value = womenChoices[m][w].varValue
                out += str(value) + " "
            out+="\n"
        print(' '.join(str(x) for x in assignments))

        # add constraint that blocks this current solution
        prob += pulp.lpSum(varsToSum) <= (len(assignments) - 1),"solutionConstraint_{}".format(solnIndex)
        solnIndex = solnIndex + 1
    
    # if we have run out of time
    if timeLeft < 0:
        exit(5)
 

# print the final stats
print("\nnum_solutions_found_by_ip: " + str(solnIndex))
end = datetime.datetime.now()
duration = end - start
durationMs = (duration.days * 86400000) + (duration.seconds * 1000) + (duration.microseconds / 1000)
print("\nDuration_ip_milliseconds: " + str(durationMs))
