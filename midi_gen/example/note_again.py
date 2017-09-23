# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi import Output
from midi_gen.note import Note
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.lfo import Sine
from midi_gen.util import Chain, Loop, Parallel
from midi_gen.event import NoteEvent

import mido
import random

resolution = PPQN(24)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

outputs = mido.get_output_names()
print(outputs)
port_name = next((each for each in outputs if 'yoshimi' in each), outputs[0])

with mido.open_output(port_name, autoreset=True) as port:
    print ("using output %s" % port)
    channel = Output(port).channel(1)

    class SendFilter(object):
        def __init__(self):
            self.counter = 0
        
        def __call__(self, value):
            self.counter = self.counter + 1
            if self.counter >= 0:
                to_send = 76 + int(value * 32)
                channel.cc(74, to_send)
                self.counter = 0
    
    lfo = Sine(consumer = SendFilter(), cpm = 16, resolution = resolution)

    notes = Note['D1'].scale(Note.min_pent)
    random.shuffle(notes)
    seq = Chain(*[NoteEvent(resolution, channel, note) for note in notes])
    all_consumer = Parallel(lfo, seq)
    all_consumer = Loop(all_consumer)
    #try:
    keeper.start(all_consumer)
    #except KeyboardInterrupt:
        #channel.cc(123, 0) #send all note off