from _pyio import __metaclass__
class Note:
    '''
    Class that represent a midi note. Took it out of midi because it can
    be used in other contexts (maybe). The value is the midi number.
    I wanted to break out so I could add scales and other things and keep
    midi module clean
    '''
    maj = [0, 2, 4, 5, 7, 9, 11]
    min_pent = [0, 3, 5, 7, 10]
    maj_pent = [0, 2, 4, 7, 9]
    
    class MetaNote(type):
        def __getitem__(self, key):
            return self.named(key)
    __metaclass__ = MetaNote
    
    @classmethod
    def named(cls, name):
        return getattr(cls, name)
    
    @classmethod
    def middle_c(cls):
        return cls(60)
    
    def __init__(self, number, name = None):
        self.value = number
        self._name = name
        
    def __str__(self):
        return 'Note(%d:%s)' % (self.value, self.name)
    
    def __repr__(self):
        return 'Note(%d)' % self.value
    
    def __eq__(self, another):
        return self.value == another.value
    
    @property
    def name(self):
        if self._name is None:
            octave = (self.value / 12) - 2
            self._name = self.__class__.names[self.value % 12] + str(octave)
        return self._name
    
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
    
    def scale(self, formula):
        return [Note(self.value + diff_num) for diff_num in formula]
            

Note.names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def create_midi_names():
    octave = -2
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
