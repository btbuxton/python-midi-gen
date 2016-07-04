# simple example to run lfo over filter cc, change port for your system
from midi_gen.midi.time_keeper import TimeKeeper, BPM, PPQN
from midi_gen.midi.lfo import LFO
import pygame.midi

pygame.init()
pygame.midi.init()

resolution = PPQN(240)
keeper = TimeKeeper(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

midi_out = pygame.midi.Output(port, 0)

lfo = LFO(cpqn = 0.5, resolution = resolution)
# Do 100 measures and stop

#figure out why song start is sent...hmmm
def send_filter(value):
    to_send = 64 + int(value * 32)
    midi_out.write_short(0xb0, 74, to_send)

keeper.start(lfo(send_filter, pulses = resolution.ppqn * 100))
pygame.midi.quit()