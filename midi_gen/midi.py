import pygame.midi
from midi_gen.note import Note

# These classes are to wrap pygame's midi api
        
class Channel(object):
    def __init__(self, midi_output, number):
        self._output = midi_output
        self._number = number
    
    def __str__(self):
        return 'Channel({})' % (self._number + 1)
    
    #TODO get note default to be nicer and not fail checks
    def note_on(self, note = getattr(Note, 'C2'), velocity = 100):
        self._output.note_on(note.value, velocity = velocity, channel = self._number)
    
    def note_off(self, note = getattr(Note, 'C2'), velocity = 100):
        self._output.note_off(note.value, velocity = velocity, channel = self._number)
        
    def cc(self, control_number, value):
        #control_number should be 0-127
        #TODO 0xb0 with channel number ValueError
        self._output.write_short(0xb0, control_number, value)
    
class Output(object):
    def __init__(self, midi_out):
        self._midi_out = midi_out
    
    def __del__(self):
        self.close()
        
    def channel(self, number):
        if number < 1 or number > 16:
            raise ValueError('channel needs to be between 1 and 16, but was {}' % number)
        return Channel(self._midi_out, number - 1)
    
    def close(self):
        if self._midi_out:
            self._midi_out.close()
            del self._midi_out
            
            
        
class Engine(object):
    def __init__(self):
        self._ports = {}
        pygame.midi.init()
        
    def __del__(self):
        for each in self._ports.values():
            each.close()
        pygame.midi.quit() #This causes an error
        
    def output(self, port):
        result = self._ports.get(port, None)
        if result is None:
            result = Output(pygame.midi.Output(port))
            self._ports[port] = result
        return result