
# This python program reads in user options and creates lists of instances (held in text files)
# that are to be created.
import sys

# read in the user options
directories = []
options = []
numInstances = []

with open(sys.argv[1]) as opts:
    for line in opts:
        row = line.split()
        if not len(row) == 0:
            directories.append(row[0])
            options.append(row[1])
            numInstances.append(int(row[2]))



# create the instance names file
instanceNameFile = open("instanceGenerator/instanceNamesMot.txt","w") 

# create instances
for x in range(len(directories)):
    numInstancesForExp = numInstances[x]
    for y in range(numInstancesForExp):
        instance = sys.argv[2] + directories[x] + "/Instances/" + options[x] + "_" + str(y) + ".txt\n"
        # add instance to the list of all instances
        instanceNameFile.write(instance)


# close files
instanceNameFile.close()





