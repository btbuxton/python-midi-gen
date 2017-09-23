# simple example to run midi clock, change port for your system
# TODO: add convenience methods to PPQN for gen
import mido
from midi_gen.pulse import PulseTimer, BPM, PPQN


resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)
class Clock(object):
    def __init__(self, midi_out, max_pulses):
        self.midi_out = midi_out
        self.max_pulses = max_pulses
        self.current = 0
        
    def __call__(self, pulse):
        if 0 == (self.current % 10):
            midi_out.send(mido.Message('clock'))
        self.current = self.current + 1
        if self.max_pulses <= self.current:
            return False
        return True


outputs = mido.get_output_names()
print(outputs)
port_name = next((each for each in outputs if 'electribe' in each), outputs[0])

print ("using output :%s" % port_name)

with mido.open_output(port_name, autoreset=True) as midi_out:
    # Do 100 measures and stop
    keeper.start(Clock(midi_out, 240*100))
