import unittest

from midi_gen.pulse import PulseTimer, BPM, PPQN
from copy import copy

class PulseGenTest(unittest.TestCase):

    def testSimple(self):
        subject = PulseTimer(tempo=BPM(120),resolution=PPQN(1))
        subject._sleep = lambda (time): None
        pulses = []
        class Consumer(object):
            count = 0
            def __call__(self, pulse):
                pulses.append(copy(pulse))
                self.count = self.count + 1
                if 5 <= self.count:
                    return False
                return True
                
        subject.start(Consumer())
        self.assertEqual(5, len(pulses), "Wrong number of pulses")
        self.assertEqual(0, pulses[0].measure(), "Wrong measure")
        self.assertEqual(0, pulses[0].counter(), "Wrong count")
        self.assertEqual(1, pulses[4].measure(), "Wrong measure")
        self.assertEqual(4, pulses[4].counter(), "Wrong count")
        
class PPQNTest(unittest.TestCase):
    def testDiv(self):
        numerator = PPQN(240)
        denominator = PPQN(24)
        self.assertEqual(10, numerator / denominator)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()