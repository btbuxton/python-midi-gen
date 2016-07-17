from _pyio import __metaclass__
class Note:
    '''
    Class that represent a midi note. Took it out of midi because it can
    be used in other contexts (maybe). The value is the midi number.
    I wanted to break out so I could add scales and other things and keep
    midi module clean
    '''
    class MetaNote(type):
        def __getitem__(self, key):
            return self.named(key)
    __metaclass__ = MetaNote
    
    @classmethod
    def named(cls, name):
        return getattr(cls, name)
    
    def __init__(self, number):
        self.value = number
        
    def __str__(self):
        return 'Note(%d)' % self.value
    
    def __eq__(self, another):
        return self.value == another.value
    
    def octave_down(self):
        value = self.value - 12
        if value < 0:
            raise ValueError("octave_down failed. %s" % str(self))
        return Note(value)
    
    def octave_up(self):
        value = self.value + 12
        if value > 127:
            raise ValueError("octave_up failed. %s" % str(self))
        return Note(value)

Note.names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def create_midi_names():
    octave = 0
    note_names = iter(Note.names)
    for value in xrange(0, 128):
        try:
            note = next(note_names)
        except StopIteration:
            note_names = iter(Note.names)
            octave = octave + 1
            note = next(note_names)
        name = note + str(octave)
        setattr(Note, name, Note(value))
create_midi_names()


#TODO Scales
#major: [0, 2, 4, 5, 7, 9, 11]
#minor pentatonic: [0, 3, 5, 7, 10]
#major pentatonic: [0, 2, 4, 7, 9]
