import pygame.midi
from midi_gen.note import Note

# These classes are to wrap pygame's midi api
        
class Channel(object):
    def __init__(self, midi_output, number):
        self._output = midi_output
        self._number = number
    
    def __str__(self):
        return 'Channel(%d)' % (self._number + 1)
    
    def note_on(self, note = Note['C2'], velocity = 100):
        self._output.note_on(note.value, velocity = velocity, channel = self._number)
    
    def note_off(self, note = Note['C2'], velocity = 0):
        self._output.note_off(note.value, velocity = velocity, channel = self._number)
        
    def cc(self, control_number, value):
        self._output.write_short(0xb0 + self._number, control_number, value)
    
class Output(object):
    def __init__(self, midi_out, desc):
        self._midi_out = midi_out
        self._desc = desc
    
    def __str__(self):
        return self._desc
        
    def channel(self, number):
        if number < 1 or number > 16:
            raise ValueError('channel needs to be between 1 and 16, but was %d' % number)
        return Channel(self._midi_out, number - 1)
    
    def close(self):
        if self._midi_out:
            self._midi_out.close()
            del self._midi_out    
        
class Engine(object):
    def __init__(self):
        self._ports = {}
        pygame.midi.init()
        
    def __enter__(self):
        self.open()
        return self
        
    def __exit__(self, _type, value, traceback):
        self.close()
        
    def open(self):
        pygame.midi.init();
        
    def close(self):
        for each in self._ports.values():
            each.close()
        pygame.midi.quit() #This causes an error
        
    def output(self, port):
        result = self._ports.get(port, None)
        if result is None:
            result = Output(pygame.midi.Output(port), pygame.midi.get_device_info(port)[1])
            self._ports[port] = result
        return result