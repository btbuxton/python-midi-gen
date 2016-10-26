# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi import Engine
from midi_gen.note import Note
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.util import Chain, Loop, Parallel
from midi_gen.event import NoteEvent

import random

resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

engine = Engine()
output = engine.output(port)
channel = output.channel(2)

notes1 = Note['D2'].scale(Note.min_pent)
random.shuffle(notes1)
seq1 = Chain(*[NoteEvent(resolution, channel, note, len_m = 0.25, gate = 1.0) for note in notes1])
notes2 = Note['D3'].scale(Note.min_pent)
random.shuffle(notes2)
seq2 = Chain(*[NoteEvent(resolution, channel, note, len_m = 0.30, velocity = 50, gate = 0.5) for note in notes2])
all_consumer = Parallel(seq1, seq2)
all_consumer = Loop(all_consumer)
keeper.start(all_consumer)
del engine