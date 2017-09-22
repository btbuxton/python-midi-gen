import mido
from midi_gen.note import Note

# These classes are to wrap pygame's midi api
        
class Channel(object):
    def __init__(self, midi_output, number):
        self._output = midi_output
        self._number = number
    
    def __str__(self):
        return 'Channel(%d)' % (self._number + 1)
    
    def note_on(self, note = Note['C2'], velocity = 100):
        self._output.send(mido.Message('note_on', channel = self._number, note = note.value, velocity = velocity))
    
    def note_off(self, note = Note['C2'], velocity = 0):
        self._output.send(mido.Message('note_off', channel = self._number, note = note.value, velocity = velocity))
        
    def cc(self, control_number, value):
        self._output.send(mido.Message('control_change', channel = self._number, control = control_number, value = value))
    
class Output(object):
    def __init__(self, midi_out):
        self._midi_out = midi_out
    
    def __str__(self):
        return self._midi_out
        
    def channel(self, number):
        if number < 1 or number > 16:
            raise ValueError('channel needs to be between 1 and 16, but was %d' % number)
        return Channel(self._midi_out, number - 1)

