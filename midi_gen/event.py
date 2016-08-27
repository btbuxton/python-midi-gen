'''
Created on Aug 26, 2016

@author: btbuxton
'''

class Event(object):
    def __init__(self, reso, len_m = 0.25, gate = 0.9):
        '''
        An event given reso (PPQN), len_m which is a percentage of a measure and a gate which is a percentage of that
        '''
        self.reset()
        self._len=reso.ppm * len_m
        self._gate=int(self._len * gate)
    
    def __call__(self, pulse):
        if 0 == self._offset:
            self.on(pulse)
        if self._len <= self._offset:
            return self.at_end()
        elif self._gate == self._offset:
            self.off(pulse)
        self._offset = self._offset + 1
        return True
    
    def reset(self):
        self._offset = 0
    
    def on(self, pulse):
        pass
    
    def off(self, pulse):
        pass
    
    def at_end(self):
        return False

class NoteEvent(Event):
    '''
    Default to quarter notes
    '''
    def __init__(self, reso, channel, note, len_m = 0.25, gate = 0.9, velocity = 100):
        super(self.__class__, self).__init__(reso, len_m, gate)
        self._channel = channel
        self._note = note
        self._velocity = velocity
    
    def on(self, pulse):
        self._channel.note_on(self._note, self._velocity)
        
    def off(self, pulse):
        self._channel.note_off(self._note, 0)
