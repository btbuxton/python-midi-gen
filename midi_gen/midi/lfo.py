from midi_gen.midi.time_keeper import PPQN
from math import radians, sin

#TODO This is a sine wave...Need to break this out into subclasses
class LFO(object):
    def __init__(self, cpqn=1, resolution=PPQN(24)):
        self.resolution = resolution
        self.cpqn = cpqn
        deg = 360.0 / resolution.ppqn * cpqn
        self.rads = radians(deg)
        self.current = 0.0
        
    def __call__(self, func, pulses = 96):
        for _ in xrange(0, pulses):
            yield
            pos = sin(self.current)
            func(pos)
            self.current = self.current + self.rads