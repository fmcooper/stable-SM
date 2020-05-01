import unittest
import math
import motivationClasses as mc



class TestBitCalculations(unittest.TestCase):
    def test_exponential(self):
        """
        Calculation of the number of bits required to hold an exponential number
        """
        data = [0, 2, 0, 0, 1, -3, 0]
        exp = mc.experiment([])
        result = exp.calculateBitsExponential(data)
        expNum = 2*(7**5) + 7**2 - 3*(7)
        numBits = math.ceil(math.log(expNum, 2)) + 1 + 32
        self.assertEqual(result, numBits)

    def test_compressed(self):
        """
        Calculation of the number of bits required to hold a compressed vector based number
        """
        data = [0, 2, 0, 0, 1, -3, 0]
        exp = mc.experiment([])
        result = exp.calculateBitsCompressed(data)
        numNunZero = 3
        indicesBits = numNunZero * math.ceil(math.log(len(data), 2))
        valuesBits = numNunZero * (math.ceil(math.log(2 * len(data), 2)) + 1)
        numBits = indicesBits + valuesBits
        self.assertEqual(result, numBits)

    def test_space(self):
        """
        Calculation of the number of bits required to hold a compressed vector based number
        """
        data = [[-1, 2, -1, 0], [0, -1, 1, 0]]
        exp = mc.experiment(data)
        maxDegree = 3
        
        # 1st rotation
        # exponential
        rot1expNum = -1*(maxDegree**2) + 2*maxDegree - 1
        rot1numBitsExp = math.ceil(math.log(abs(rot1expNum), 2)) + 1 + 32
        # compressed
        numNunZero = 3
        rot1indicesBits = numNunZero * math.ceil(math.log(maxDegree, 2))
        rot1valuesBits = numNunZero * (math.ceil(math.log(2 * maxDegree, 2)) + 1)
        rot1numBitsComp = rot1indicesBits + rot1valuesBits

        # 2nd rotation
        # exponential
        rot2expNum = -1*maxDegree + 1
        rot2numBitsExp = math.ceil(math.log(abs(rot2expNum), 2)) + 1 + 32
        # compressed
        numNunZero = 2
        rot2indicesBits = numNunZero * math.ceil(math.log(maxDegree, 2))
        rot2valuesBits = numNunZero * (math.ceil(math.log(2 * maxDegree, 2)) + 1)
        rot2numBitsComp = rot2indicesBits + rot2valuesBits

        self.assertEqual(exp.bitsRequiredExponential, rot1numBitsExp + rot2numBitsExp)
        self.assertEqual(exp.bitsRequiredCompressed, rot1numBitsComp + rot2numBitsComp + 64)

if __name__ == '__main__':
    unittest.main()
