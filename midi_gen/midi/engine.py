import pygame.midi

# These classes are to wrap pygame's midi api

class Note: 
    def __init__(self, number):
        self._number = number
        
    def __str__(self):
        return 'Note({})' % self._number
    
    def __eq__(self, another):
        return self.number == another.number
        
    @property
    def number(self):
        return self._number
    
    def octave_down(self):
        value = self._number - 12
        if value < 0:
            raise Exception("octave_down failed. {}" % self)
        return Note(value)
    
    def octave_up(self):
        value = self._number + 12
        if value > 127:
            raise Exception("octave_up failed. {}" % self)
        return Note(value)
    
Note.C2 = Note(24)
        
class Channel(object):
    def __init__(self, output, number):
        self._output = output
        self._number = number
    
    def __str__(self):
        return 'Channel({})' % (self._number + 1)
    
    def note_on(self, note = Note.C2, velocity = 100):
        self._output.note_on(note, velocity = velocity, channel = self._number)
    
    def note_off(self, note = Note.C2, velocity = 100):
        self._output.note_off(note, velocity = velocity, channel = self._number)
    
class Output(object):
    def __init__(self, midi_out):
        self._midi_out = midi_out
    
    def __del__(self):
        del self._midi_out
        
    def channel(self, number):
        if number < 1 or number > 16:
            raise Exception('channel needs to be between 1 and 16, but was {}' % number)
        return Channel(self, number - 1)
        
class Engine(object):
    def __init__(self):
        self._ports = []
        
    def start(self):
        pygame.midi.init()
        
    def stop(self):
        for each in self._ports:
            del each
        self._ports = []
        pygame.midi.quit()
        
    def output(self, port):
        return Output(pygame.midi.Output(port))