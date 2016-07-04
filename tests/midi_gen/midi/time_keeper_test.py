import unittest

from midi_gen.midi.time_keeper import TimeKeeper, BPM, PPQN
from copy import copy

class TimeKeeperTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSimple(self):
        subject = TimeKeeper(tempo=BPM(120),resolution=PPQN(1))
        subject._sleep = lambda (time): None
        pulses = []
        def gen():
            for _ in xrange(0,5):
                answer = yield
                pulses.append(copy(answer))
        subject.start(gen())
        self.assertEqual(5, len(pulses), "Wrong number of pulses")
        self.assertEqual(0, pulses[0].measure(), "Wrong measure")
        self.assertEqual(0, pulses[0].counter(), "Wrong count")
        self.assertEqual(1, pulses[4].measure(), "Wrong measure")
        self.assertEqual(4, pulses[4].counter(), "Wrong count")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()