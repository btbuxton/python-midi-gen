# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi import Engine
from midi_gen.note import Note
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.lfo import Sine
from midi_gen.util import Chain, Loop, Parallel
import random


resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

engine = Engine()
output = engine.output(port)
channel = output.channel(1)

#TODO
class QtrNote(object):
    def __init__(self, channel, note, reso):
        self._channel = channel
        self._note = note
        self._max = reso.ppqn
        self._len = int(0.9 * self._max)
        self.reset()
        
    def __call__(self, pulse):
        if 0 == self._offset:
            self._channel.note_on(self._note)
        if self._max <= self._offset:
            return False
        elif self._len == self._offset:
            self._channel.note_off(self._note)
        self._offset = self._offset + 1
        return True
    
    def reset(self):
        self._offset = 0

class SendFilter(object):
    def __init__(self):
        self.counter = 0
        
    def __call__(self, value):
        self.counter = self.counter + 1
        if self.counter >= 24:
            to_send = 64 + int(value * 32)
            #channel.cc(52, to_send)
            self.counter = 0
    
lfo = Sine(consumer = SendFilter(), cpqn = 2, resolution = resolution)

notes = Note['D2'].scale(Note.min_pent)
random.shuffle(notes)
seq = Chain(*[QtrNote(channel, note, resolution) for note in notes])
all_consumer = Parallel(lfo, seq)
all_consumer = Loop(all_consumer)
keeper.start(all_consumer)
del engine