# simple example to run lfo over filter cc and generate random quarter notes
from midi_gen.midi.pulse import PulseTimer, BPM, PPQN
from midi_gen.midi.lfo import Sine

import pygame.midi

pygame.midi.init()

resolution = PPQN(240)
keeper = PulseTimer(tempo = BPM(120), resolution = resolution)

port = 2 #pygame.midi.get_default_output_id()
print ("using output_id :%s" % port)

midi_out = pygame.midi.Output(port)

lfo = Sine(cpqn = 4, resolution = resolution)
def send_filter(value):
    to_send = 64 + int(value * 32)
    midi_out.write_short(0xb0, 74, to_send)
    
def qtr_note(midi_out, note, ppqn):
    off = int(0.9 * ppqn)
    midi_out.note_on(note, 127, 0)
    for _ in xrange(0, off):
        yield
    midi_out.note_off(note, 127, 0)
    for _ in xrange(off, ppqn):
        yield
    

def parallel(*gens):
    for each in gens:
        each.send(None)
    while True:
        pulse = yield
        for each in gens:
            each.send(pulse)
            
def chain(*gens):
    for each in gens:
        each.send(None)
        try:
            while True:
                pulse = yield
                each.send(pulse)
        except StopIteration:
            pass

lfo_gen = lfo(send_filter, pulses = resolution.ppqn * 100)
seq_gen = chain(
                qtr_note(midi_out, 65, resolution.ppqn), 
                qtr_note(midi_out, 64, resolution.ppqn),
                qtr_note(midi_out, 62, resolution.ppqn),
                qtr_note(midi_out, 60, resolution.ppqn)
                )
all_gen = parallel(lfo_gen, seq_gen)
keeper.start(all_gen)
del midi_out
pygame.midi.quit()