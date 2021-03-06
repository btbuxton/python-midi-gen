# simple example to run lfo over filter cc, change port for your system
from midi_gen.pulse import PulseTimer, BPM, PPQN
from midi_gen.lfo import Sine
import pygame.midi
#TODO REWRITE
pygame.midi.init()

resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

midi_out = pygame.midi.Output(port, 0)

def send_filter(value):
    to_send = 64 + int(value * 32)
    midi_out.write_short(0xb0, 74, to_send)
    #print(value)
    
lfo = Sine(cpm = 2, resolution = resolution, consumer = send_filter, max_pulses = resolution.ppqn * 100)

# Do 100 measures and stop
keeper.start(lfo)
del midi_out
pygame.midi.quit()