# simple example to run midi clock, change port for your system
# TODO: add convenience methods to PPQN for gen
from midi_gen.midi.pulse import PulseTimer, BPM, PPQN
import pygame.midi

pygame.midi.init()


resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)
class Clock(object):
    def __init__(self, midi_out, max_pulses):
        self.midi_out = midi_out
        self.max_pulses = max_pulses
        self.current = 0
        
    def __call__(self, pulse):
        if 0 == (self.current % 10):
            midi_out.write_short(0xF8)
        self.current = self.current + 1
        if self.max_pulses <= self.current:
            return False
        return True


port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

midi_out = pygame.midi.Output(port, 0)

# Do 100 measures and stop
keeper.start(Clock(midi_out, 240*100))
del midi_out
pygame.midi.quit()
