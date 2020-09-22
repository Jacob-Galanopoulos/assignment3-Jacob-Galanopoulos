from unittest import TestCase
from tCurve.prob import prob as prob, _integrate, _f
import json


class ProbTest(TestCase):

    def setUp(self):
        self.nominalN = 4
        self.nominalT = 1.4398
        self.nominalTails = 1
        self.inputDictionary = {}
        self.errorValue = "error:"
        self.errorKey = "error"
        self.solutionKey = "probability"
        
    def tearDown(self):
        self.inputDictionary = {}

    def setT(self, t):
        self.inputDictionary["t"] = t

    def setN(self, n):
        self.inputDictionary["n"] = n

    def setTails(self, tails):
        self.inputDictionary["tails"] = tails
        
    def setExtra(self, extra):
        self.inputDictionary["extra"] = extra

    # 100 prob
    #    Desired level of confidence:    boundary value analysis
    #    Input-output Analysis
    #        inputs:        n -> integer, .GE.3, mandatory, unvalidated
    #                       t ->    float > 0.0, mandatory, unvalidated
    #                       tails -> integer, 1 or 2, optional, defaults to 1
    #        outputs:    float .GT. 0 .LE. 1.0
    #    Happy path analysis:
    #       n:       nominal value    n=6
    #                low bound        n=3
    #        t:      nominal value    t=1.4398
    #                low bound        t>0.0
    #        tails:  value 1          tails = 1
    #                value 2          tails = 2
    #                missing tails
    #        output:
    #                The output is an interaction of t x tails x n:
    #                    nominal t, 1 tail
    #                    nominal t, 2 tails
    #                    low n, low t, 1 tail
    #                    low n, low t, 2 tails
    #                    high n, low t, 1 tail
    #                    high n, low t, 2 tails
    #                    low n, high t, 1 tail
    #                    low n, high t, 2 tails
    #                    high n, high t, 1 tail
    #                    high n, high t, 2 tails
    #                    nominal t, default tails
    #    Sad path analysis:
    #        n:      missing n
    #                out-of-bound n   n<3
    #                non-integer n    n = 2.5
    #        t:      missing t
    #                out-of-bounds n  t<0.0
    #                non-numeric t    t="abc"
    #        tails:  invalid tails    tails = 3
    #
    # Happy path
    def test100_010ShouldCalculateNominalCase1TailHttp(self):
        self.setT(1.8946)
        self.setN(7)
        self.setTails(1)
        self.setExtra("a")
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.950, 3)
    
    def test100_010ShouldCalculateNominalCase1Tail(self):
        self.setT(1.8946)
        self.setN(7)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.950, 3)
 
    def test100_020ShouldCalculateNominalCase2Tail(self):
        self.setT(1.8946)
        self.setN(7)
        self.setTails(2)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.900, 3)
 
    def test100_030ShouldCalculateLowNLowT1TailEdgeCase(self):
        self.setT(0.2767)
        self.setN(3)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.600, 3)
 
    def test100_040ShouldCalculateLowNLowT2TailEdgeCase(self):
        self.setT(0.2767)
        self.setN(3)
        self.setTails(2)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.200, 3)
 
    def test100_050ShouldCalculateHighNLowT1TailEdgeCase(self):
        self.setT(0.2567)
        self.setN(20)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.600, 3)
 
    def test100_060ShouldCalculateHighNLowT2TailEdgeCase(self):
        self.setT(0.2567)
        self.setN(20)
        self.setTails(2)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.200, 3)
 
    def test100_070ShouldCalculateLowNHighT1EdgeCase(self):
        self.setT(5.8409)
        self.setN(3)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.995, 3)
 
    def test100_080ShouldCalculateLowNHighT2EdgeCase(self):
        self.setT(5.8409)
        self.setN(3)
        self.setTails(2)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.990, 3)
 
    def test100_090ShouldCalculateHighHighT1TailEdgeCase(self):
        self.setT(2.8453)
        self.setN(20)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.995, 3)
 
    def test100_100ShouldCalculateHighHighT2TailEdgeCase(self):
        self.setT(2.8453)
        self.setN(20)
        self.setTails(2)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.990, 3)
 
    def test100_110ShouldCalculateWithDefaultTails(self):
        self.setT(1.8946)
        self.setN(7)
        result = prob(self.inputDictionary)
        self.assertAlmostEqual(result[self.solutionKey], 0.900, 3)
 
    # Sad path
    def test100_910ShouldRaiseExceptionOnMissingT(self):
        self.setN(self.nominalN)
        self.setTails(self.nominalTails)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
 
    def test100_920ShouldRaiseExceptionOnOutOfBoundsT(self):
        self.setT(-1.0)
        self.setN(self.nominalN)
        self.setTails(self.nominalTails)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
 
    def test100_930ShouldRaiseExceptionOnNonNumericT(self):
        self.setT("abc")
        self.setN(self.nominalN)
        self.setTails(self.nominalTails)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
 
    def test100_940ShouldRaiseExceptionOnInvalidTails(self):
        self.setTails(0)
        self.setT(self.nominalT)
        self.setN(self.nominalN)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
 
    def test100_950ShouldRaiseExceptionOnMissingN(self):
        self.setT(self.nominalT)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
 
    def test100_960ShouldRaiseExceptionOnOutOfBoundN(self):
        self.setN(0)
        self.setT(self.nominalT)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
 
    def test100_970ShouldRaiseExceptionOnNonIntegerN(self):
        self.setN(2.5)
        self.setT(self.nominalT)
        self.setTails(1)
        result = prob(self.inputDictionary)
        self.assertIn(self.errorKey, result)
        self.assertIn(self.errorValue, result[self.errorKey])
        
    #Integrate Tests
    #    Integrate takes in 3 parameters: t, n, and _f
    #    t is an number greater than or equal to zero
    #    n is an integer that must be greater than zero
    #    _f is a function that should exist.
    #Happy Path
    def test100_110IntegrateCorrectOutput(self):
        n = 1
        t = 0.3249
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 0.3141414498, 4)
    
    def test100_120IntegrateCorrectOutput(self):
        n = 2
        t = 0.6172
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 0.5656751087, 4)
    
    def test100_130IntegrateCorrectOutput(self):
        n = 3
        t = 0.5844
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 0.5441480893, 4)
    
    def test100_140IntegrateCorrectOutput(self):
        n = 5
        t = 1.4759
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 1.233791314, 4)
    
    def test100_150IntegrateCorrecOutput(self):
        n = 7
        t = 1.8946
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 1.168861209, 4)
    
    def test100_160IntegrateCorrecOutput(self):
        n = 9
        t = 3.2498
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 1.27565769, 4)
    
    def test100_170IntegrateCorrecOutput(self):
        n = 30
        t = 2.7500
        actualResult = _integrate(t, n, _f)
        self.assertAlmostEqual(actualResult, 1.251162245, 4)
    
    #Sad Path
    #Since it isn't state in the project what we should return
    #in case of a failure in integrate, I'm electing to use None
    #because there would be a null value in the function if integration
    #isn't done correctly. - JDG
    def test100_910IntegrateMissingT(self):
        n = 1
        t = None
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)
    
    def test100_920IntegrateNegativeT(self):
        n = 1
        t = -1
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)

    def test100_930IntegrateNonNumberT(self):
        n = 1
        t = "abc"
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)
    
    def test100_940IntegrateMissingN(self):
        n = None
        t = 1.4786
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)
    
    def test100_950IntegrateOutOfBoundsN(self):
        n = 0
        t = 0.7864
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)
    
    def test100_960IntegrateNonIntegerT(self):
        n = 2.8
        t = 0.9873
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)

    def test100_970IntegrateNonNumberN(self):
        n = "abc"
        t = 0.5796
        expectedResult = None
        actualResult = _integrate(t, n, _f)
        self.assertEqual(expectedResult, actualResult)

    def test100_980IntegrateMissing_f(self):
        n = 1
        t = 0.5796
        _b = None
        expectedResult = None
        actualResult = _integrate(t, n, _b)
        self.assertEqual(expectedResult, actualResult)