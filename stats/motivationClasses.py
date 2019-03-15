# Used by the python motivation program to collect results for each experiment together
# @author Frances
import math


class experiment:
    numRotations = -1
    minRotDegree = -1
    maxRotDegree = -1
    avRotDegree = -1.0
    avNpDegree = -1.0
    bitsExp = -1
    bitsTruncated = -1
    bitsIndices = -1

    def calculateSpaceRequirements(self, n):
        # exponential number
        expNum = self.maxRotDegree**(self.maxRotDegree - 1)
        self.bitsExp = math.ceil(math.log(expNum, 2)) * self.numRotations

        # truncating zeros
        # the numbers that can appear in an element of a vector based profile array are between -2n and 2n
        elementBitsReq = math.ceil(math.log(2*n, 2)) + 1
        self.bitsTruncated = elementBitsReq * self.avRotDegree * self.numRotations

        # storing indices of non-zeros
        # (1) indices: we have avNpDegree number of numbers up to n
        # (2) values: we have avNpDegree number of numbers between -2n and 2n
        indicesBitsReq = math.ceil(math.log(n, 2)) * self.avNpDegree
        elemBitsReq = elementBitsReq * self.avNpDegree
        self.bitsIndices = (indicesBitsReq + elemBitsReq) * self.numRotations


    def printExp(self):
        print("numRotations: " + str(self.numRotations))
        print("minRotDegree: " + str(self.minRotDegree))
        print("maxRotDegree: " + str(self.maxRotDegree))
        print("avRotDegree: " + str(self.avRotDegree))
        print("avNpDegree: " + str(self.avNpDegree))
        print("bitsExp: " + str(self.bitsExp))
        print("bitsTruncated: " + str(self.bitsTruncated))
        print("bitsIndices: " + str(self.bitsIndices))




