from midi_gen.pulse import PPQN
from math import radians, sin

# cpqn = cycles per quarter notes
#cpm = cycles per measure
#Abstract class, implement next in subclasses
class LFO(object):
    def __init__(self, consumer = lambda (pulse): None, cpm=4, resolution=PPQN(24), max_pulses = None):
        self.__consumer = consumer
        self.resolution = resolution
        self.cpqn = float(cpm) / 4
        self.__max_pulses = max_pulses
        self.reset()
    
    def __call__(self, pulse):
        self._consume_pulse(pulse, self.__consumer)
        self.__current_pulse = self.__current_pulse + 1
        if self.__max_pulses is not None and (self.__max_pulses <= self.__current_pulse):
            return False
        return True
        
    def _consume_pulse(self, pulse, consumer):
        pass
    
    def reset(self):
        self.__current_pulse = 0
        self._wave_init()

            
class Sine(LFO):
    def _wave_init(self):
        deg = 360.0 / self.resolution.ppqn * self.cpqn
        self.rads = radians(deg)
        self.current = 0.0
    
    def _consume_pulse(self, pulse, consumer):
        pos = sin(self.current)
        consumer(pos)
        self.current = self.current + self.rads