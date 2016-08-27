# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi import Engine
from midi_gen.note import Note
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.lfo import Sine
from midi_gen.util import Chain, Loop, Parallel
from midi_gen.event import NoteEvent

import random


resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

engine = Engine()
output = engine.output(port)
channel = output.channel(1)

class SendFilter(object):
    def __init__(self):
        self.counter = 0
        
    def __call__(self, value):
        self.counter = self.counter + 1
        if self.counter >= 24:
            to_send = 64 + int(value * 32)
            channel.cc(74, to_send)
            self.counter = 0
    
lfo = Sine(consumer = SendFilter(), cpm = 6, resolution = resolution)

notes = Note['D2'].scale(Note.min_pent)
random.shuffle(notes)
seq = Chain(*[NoteEvent(resolution, channel, note) for note in notes])
all_consumer = Parallel(lfo, seq)
all_consumer = Loop(all_consumer)
keeper.start(all_consumer)
del engine