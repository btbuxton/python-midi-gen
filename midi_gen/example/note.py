# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi import Engine
from midi_gen.note import Note
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.lfo import Sine
from midi_gen.util import Chain, Loop, Parallel


resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

engine = Engine()
output = engine.output(port)
channel = output.channel(1)

class QtrNote(object):
    def __init__(self, channel, note, ppqn):
        self._channel = channel
        self._note = note
        self._ppqn = ppqn
        self._len = int(0.9 * ppqn)
        self.reset()
        
    def __call__(self, pulse):
        if 0 == self._offset:
            self._channel.note_on(self._note)
        if self._ppqn <= self._offset:
            return False
        elif self._len == self._offset:
            self._channel.note_off(self._note)
        self._offset = self._offset + 1
        return True
    
    def reset(self):
        self._offset = 0
        
def send_filter(value):
    to_send = 32 + int(value * 32)
    channel.cc(71, to_send)
    
lfo = Sine(consumer = send_filter, cpqn = 2, resolution = resolution)

seq = Chain(
                QtrNote(channel, Note(65), resolution.ppqn), 
                QtrNote(channel, Note(64), resolution.ppqn),
                QtrNote(channel, Note(62), resolution.ppqn),
                QtrNote(channel, Note(60), resolution.ppqn)
                )
all_consumer = Parallel(lfo, seq)
all_consumer = Loop(all_consumer)
keeper.start(all_consumer)
del engine