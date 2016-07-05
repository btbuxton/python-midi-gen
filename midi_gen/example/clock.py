# simple example to run midi clock, change port for your system
# TODO: add convenience methods to PPQN for gen
from midi_gen.midi.time_keeper import TimeKeeper, BPM, PPQN
import pygame.midi

pygame.midi.init()


resolution = PPQN(240)
keeper = TimeKeeper(tempo = BPM(120), resolution = resolution)
def clock(midi_out, pulses):
    for _ in xrange(0, pulses / 10):
        midi_out.write_short(0xF8)
        for _ in xrange(0, 10): #send out 24 PPQN, we are using 240 (so every ten pulses sends out clock)
            yield

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

midi_out = pygame.midi.Output(port, 0)

# Do 100 measures and stop
keeper.start(clock(midi_out, 240*100))
del midi_out
pygame.midi.quit()
