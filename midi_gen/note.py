class Note:
    '''
    Class that represent a midi note. Took it out of midi because it can
    be used in other contexts (maybe). The value is the midi number.
    I wanted to break out so I could add scales and other things and keep
    midi module clean
    '''
    def __init__(self, number):
        self.value = number
        
    def __str__(self):
        return 'Note({})' % self._number
    
    def __eq__(self, another):
        return self.value == another.value
    
    def octave_down(self):
        value = self.value - 12
        if value < 0:
            raise ValueError("octave_down failed. {}" % self)
        return Note(value)
    
    def octave_up(self):
        value = self.value + 12
        if value > 127:
            raise ValueError("octave_up failed. {}" % self)
        return Note(value)

#TODO Create this automatically
Note.C2 = Note(24)

#TODO Scales
#major: [0, 2, 4, 5, 7, 9, 11]
#minor pentatonic: [0, 3, 5, 7, 10]
#major pentatonic: [0, 2, 4, 7, 9]
