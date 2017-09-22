# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi import Output
from midi_gen.note import Note
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.util import Chain, Loop, Parallel
from midi_gen.event import NoteEvent

import mido
import random

resolution = PPQN(24)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

outputs = mido.get_output_names()
print(outputs)
port_name = next((each for each in outputs if 'electribe' in each), outputs[0])

with mido.open_output(port_name) as port:
    print ("using output %s" % port)
    channel = Output(port).channel(1)

    notes1 = Note['D2'].scale(Note.min_pent)
    random.shuffle(notes1)
    seq1 = Chain(*[NoteEvent(resolution, channel, note, len_m = 0.25, gate = 1.0) for note in notes1])
    notes2 = Note['D3'].scale(Note.min_pent)
    random.shuffle(notes2)
    seq2 = Chain(*[NoteEvent(resolution, channel, note, len_m = 0.30, velocity = 50, gate = 0.5) for note in notes2])
    all_consumer = Parallel(seq1, seq2)
    all_consumer = Loop(all_consumer)
    keeper.start(all_consumer)