# Used by the python motivation program to calculate results for a single experiment
# @author Frances
import math

# number of bits in a standard int
bitsStandardWord = 32

class experiment:
    def __init__(self, rotations):
        self.rotations = rotations
        # each rotation as an exponential number, where the number of bits is not longer than necessary
        self.bitsRequiredExponential = 0
        # each rotation as a compressed vector based number, saving the number and index of non-zero elements
        self.bitsRequiredCompressed = 0
        self.rotations = rotations
        _, self.maxDegree, _ = self.getMinMaxAvDegree(self.rotations)
        self.calculateSpaceRequirements()


    def calculateSpaceRequirements(self):
        for r in self.rotations:
            # exponential
            # example original rotation: < 0, 2, -3, 0, 0, 1, 0, 0, 0, 0, 0 >
            # if maxDegree over all rotations is 7, then "truncate" the above rotation to < 0, 2, -3, 0, 0, 1, 0 >
            truncatedR = r[:self.maxDegree]
            self.bitsRequiredExponential += self.calculateBitsExponential(truncatedR)

            # compressed
            self.bitsRequiredCompressed += self.calculateBitsCompressed(truncatedR)

        self.bitsRequiredCompressed += 2 * bitsStandardWord


    def calculateBitsExponential(self, r):
        exponentialNumber = 0

        if len(r) == 0:
            return bitsStandardWord
        
        # create the exact exponential number from this such that the ith value contributes a weight of n^(n-i)
        for i, v in enumerate(r):
            exponentialNumber += v*(len(r)**(len(r)-(i+1)))

        # number of bits required to store the exponential number (with the addition of a standard word 
        # to store the number of bits used)
        if exponentialNumber == 0:
            numBits = 1 + bitsStandardWord
        else:
            numBits = math.ceil(math.log(abs(exponentialNumber), 2)) + bitsStandardWord
        return numBits


    def calculateBitsCompressed(self, r):
        if len(r) == 0:
            return bitsStandardWord

        # store the index and value of non-zero elements
        numNonZero = self.getNumNonZero(r)

        if numNonZero == 0:
            return bitsStandardWord

        # (1) indices: we have numNonZero number of numbers up to n
        indicesBitsReq = math.ceil(math.log(len(r), 2)) * numNonZero

        # (2) values: we have numNonZero number of numbers between -2n and 2n
        elementsBitsReq = (math.ceil(math.log(2*len(r), 2)) + 1) * numNonZero

        # number of bits required to store the indices and values and the number of indices or values
        return indicesBitsReq + elementsBitsReq  + bitsStandardWord


    # gets the number of non-zero elements in a profile
    def getNumNonZero(self, profile):
        if len(profile) == 0:
            return -1
        else:
            count = 0
            for i in profile:
                if not i == 0:
                    count = count + 1;
            return count


    # gets the minimum and maximum profile degree of an array or returns -1 if array is 0 in length
    def getMinMaxAvDegree(self, array2D):
        minDegree = -1
        maxDegree = -1
        totalDegree = 0.0
        avDegree = -1
        # average profile
        if len(array2D) == 0:
            return minDegree, maxDegree, avDegree
        else:
            for profile in array2D:
                degree = self.getDegree(profile)
                totalDegree += degree
                if minDegree == -1 or degree < minDegree:
                    minDegree = degree
                if maxDegree == -1 or degree > maxDegree:
                    maxDegree = degree
        avDegree = float(totalDegree) / float(len(array2D))

        return minDegree, maxDegree, avDegree


    def getNumpyAvSize(self, array2D):
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
    def getDegree(self, profile):
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


    def printExp(self):
        print("rotations: " + str(self.rotations))
        print("bitsRequiredExponential: " + str(self.bitsRequiredExponential))
        print("bitsRequiredCompressed: " + str(self.bitsRequiredCompressed))



