
# This python program reads in user options and creates lists of instances (held in text files)
# that are to be created.
import sys

# read in the user options
directories = []
options = []
numInstances = []
correctness = []
with open(sys.argv[1]) as opts:
    for line in opts:
        row = line.split()
        if not len(row) == 0:
            directories.append(row[0])
            options.append(row[1])
            numInstances.append(int(row[2]))
            correctness.append(row[3])


# create the instance names file
instanceNameFile = open("instanceGenerator/instanceNames.txt","w") 
bfInstanceNameFile = open("instanceGenerator/ipInstanceNames.txt","w") 
notbfInstanceNameFile = open("instanceGenerator/nonipInstanceNames.txt","w") 

# create instances
for x in range(len(directories)):
    numInstancesForExp = numInstances[x]
    corrOpt = correctness[x]
    for y in range(numInstancesForExp):
        instance = sys.argv[2] + directories[x] + "/Instances/" + options[x] + "_" + str(y) + ".txt\n"
        # add instance to the list of all instances
        instanceNameFile.write(instance)

        # if correctness option is set then also add this to the correctness instance list
        if corrOpt == "c":
            bfInstanceNameFile.write(instance)
        # if correctness option is not set then add to the other list
        else:
            notbfInstanceNameFile.write(instance)

# close files
instanceNameFile.close()
bfInstanceNameFile.close()
notbfInstanceNameFile.close()





