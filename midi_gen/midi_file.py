'''
Created on Oct 4, 2016

@author: btbuxton
'''
import struct
import io

class Chunk(object):
    @classmethod
    def for_type(cls, type_name, contents):
        if "MThd" == type_name:
            return MThdChunk(type_name, contents)
        if "MTrk" == type_name:
            return MTrkChunk(type_name, contents)
        return UndefinedChunk(type_name, contents)
    
    def __init__(self, type_name, contents):
        self.type = type_name
        self.contents = contents
        
    def __str__(self):
        return self.type
    
    def if_header(self, func):
        pass
    
    def if_track(self, func):
        pass

class UndefinedChunk(Chunk):
    pass

class MThdChunk(Chunk):
    def __init__(self, type_name, contents):
        super(self.__class__, self).__init__(type_name, contents)
        self._parse(io.BytesIO(contents))
        
    def _parse(self, stream):
        self.fmt = struct.unpack('>h', stream.read(2))[0]
        self.tracks = struct.unpack('>h', stream.read(2))[0]
        division = struct.unpack('>h', stream.read(2))[0]
        if division & (1 << 15) is not 0:
            raise Exception("SMPTE time not supported")
        self.ppqn = division
        
    def if_header(self, func):
        return func(self)

class MTrkChunk(Chunk):
    def __init__(self, type_name, contents):
        super(self.__class__, self).__init__(type_name, contents)
        self._parse(io.BytesIO(contents))
        
    def _parse(self, stream):
        pass
    
    def if_track(self, func):
        return func(self)
        
class MidiFileReader(object):
    def __init__(self, stream):
        self.stream = stream
    
    def __iter__(self):
        return self
    
    def next(self):
        type_name = self.stream.read(4)
        raw_length = self.stream.read(4)
        if 4 is len(raw_length):
            length = struct.unpack('>i', raw_length)[0]
            contents = self.stream.read(length)
            return Chunk.for_type(type_name, contents)
        raise StopIteration()

