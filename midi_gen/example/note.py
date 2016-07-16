# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi.pulse import PulseTimer, BPM, PPQN
from midi_gen.midi.lfo import Sine

import pygame.midi

pygame.midi.init()

resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

midi_out = pygame.midi.Output(port)
        
class Parallel(object):
    def __init__(self, *consumers):
        self._consumers = consumers
        
    def __call__(self, pulse):
        for each in self._consumers:
            if not each(pulse):
                return False
        return True
    
class Chain(object):
    def __init__(self, *consumers):
        #self._consumers = consumers
        self._iter = iter(consumers)
        self._current = next(self._iter)
        
    def __call__(self, pulse):
        if not self._current(pulse):
            try:
                self._current = next(self._iter)
            except StopIteration:
                return False
        return True
        
            

class QtrNote(object):
    def __init__(self, midi_out, note, ppqn):
        self._midi_out = midi_out
        self._note = note
        self._ppqn = ppqn
        self._len = int(0.9 * ppqn)
        self._offset = 0
        
    def __call__(self, pulse):
        if 0 == self._offset:
            self._midi_out.note_on(self._note, velocity = 127, channel=0)
        if self._ppqn <= self._offset:
            return False
        elif self._len == self._offset:
            self._midi_out.note_off(self._note, velocity = 127, channel = 0)
        self._offset = self._offset + 1
        return True
        
def send_filter(value):
    to_send = 64 + int(value * 32)
    midi_out.write_short(0xb0, 74, to_send)
lfo = Sine(consumer = send_filter, cpqn = 2, resolution = resolution, max_pulses = resolution.ppqn * 100)

seq = Chain(
                QtrNote(midi_out, 65, resolution.ppqn), 
                QtrNote(midi_out, 64, resolution.ppqn),
                QtrNote(midi_out, 62, resolution.ppqn),
                QtrNote(midi_out, 60, resolution.ppqn)
                )
all_consumer = Parallel(lfo, seq)
keeper.start(all_consumer)
del midi_out
pygame.midi.quit()