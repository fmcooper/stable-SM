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
        expNum = 2*(7**5) + 7**2 - 3*7
        numBits = math.ceil(math.log(expNum, 2)) + 1 + mc.bitsStandardWord
        self.assertEqual(result, numBits)

    def test_exponential_zeros(self):
        """
        Calculation of the number of bits required to hold an zero valued exponential number
        """
        data = [0, 0, 0, 0]
        exp = mc.experiment([])
        result = exp.calculateBitsExponential(data)
        # holds value of 0 exponential and word to hold the number of bits
        numBits = 1 + mc.bitsStandardWord
        self.assertEqual(result, numBits)

    def test_exponential_empty(self):
        """
        Calculation of the number of bits required to hold an zero valued exponential number
        """
        data = []
        exp = mc.experiment([])
        result = exp.calculateBitsExponential(data)
        # word to hold the number of bits (0)
        numBits = mc.bitsStandardWord
        self.assertEqual(result, numBits)

    def test_compressed(self):
        """
        Calculation of the number of bits required to hold a compressed vector based number
        """
        data = [0, 2, 0, 0, 1, -3, 0]
        exp = mc.experiment([])
        result = exp.calculateBitsCompressed(data)
        numNonZero = 3
        indicesBits = numNonZero * math.ceil(math.log(len(data), 2)) + mc.bitsStandardWord
        valuesBits = numNonZero * (math.ceil(math.log(2 * len(data), 2)) + 1) + mc.bitsStandardWord
        numBits = indicesBits + valuesBits
        self.assertEqual(result, numBits)

    def test_compressed_zeros(self):
        """
        Calculation of the number of bits required to hold an all zero compressed vector based number
        """
        data = [0, 0, 0, 0]
        exp = mc.experiment([])
        result = exp.calculateBitsCompressed(data)
        # a word to hold the number of indices (0)
        numBits = mc.bitsStandardWord
        self.assertEqual(result, numBits)

    def test_compressed_empty(self):
        """
        Calculation of the number of bits required to hold an all zero compressed vector based number
        """
        data = []
        exp = mc.experiment([])
        result = exp.calculateBitsCompressed(data)
        # word to hold the number of bits (0)
        numBits = mc.bitsStandardWord
        self.assertEqual(result, numBits)

    def test_space_zeros(self):
        """
        If all profiles are only zeros
        """
        data = [[0, 0, 0, 0], [0, 0, 0, 0]]
        exp = mc.experiment(data)
        self.assertEqual(exp.bitsRequiredExponential, 2 * mc.bitsStandardWord)
        # number of rotation bits for each rotation + 2 words to hold size of indices if they exist (up
        # to n) and elements (-2n to 2n)
        self.assertEqual(exp.bitsRequiredCompressed, 2 * mc.bitsStandardWord + 2 * mc.bitsStandardWord)
        

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
        rot1numBitsExp = math.ceil(math.log(abs(rot1expNum), 2)) + 1 + mc.bitsStandardWord
        # compressed
        numNonZero = 3
        rot1indicesBits = numNonZero * math.ceil(math.log(maxDegree, 2)) + mc.bitsStandardWord
        rot1valuesBits = numNonZero * (math.ceil(math.log(2 * maxDegree, 2)) + 1) + mc.bitsStandardWord
        rot1numBitsComp = rot1indicesBits + rot1valuesBits

        # 2nd rotation
        # exponential
        rot2expNum = -1*maxDegree + 1
        rot2numBitsExp = math.ceil(math.log(abs(rot2expNum), 2)) + 1 + mc.bitsStandardWord
        # compressed
        numNonZero = 2
        rot2indicesBits = numNonZero * math.ceil(math.log(maxDegree, 2)) + mc.bitsStandardWord
        rot2valuesBits = numNonZero * (math.ceil(math.log(2 * maxDegree, 2)) + 1) + mc.bitsStandardWord
        rot2numBitsComp = rot2indicesBits + rot2valuesBits

        self.assertEqual(exp.bitsRequiredExponential, rot1numBitsExp + rot2numBitsExp)
        # number of rotation bits for each rotation + 2 words to hold size of indices if they exist (up
        # to n) and elements (-2n to 2n)
        self.assertEqual(exp.bitsRequiredCompressed, rot1numBitsComp + rot2numBitsComp + 2 * mc.bitsStandardWord)

if __name__ == '__main__':
    unittest.main()
