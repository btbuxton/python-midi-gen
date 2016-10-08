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
        while True:
            delta_time = self._parse_var_len(stream)
            if delta_time is None:
                return
            event_type = struct.unpack('>B', stream.read(1))[0]
            if event_type is 0xF0:
                length = self._parse_var_len(stream)
                stream.read(length)
            elif event_type is 0xF7:
                length = self._parse_var_len(stream)
                stream.read(length)
            elif event_type is 0xFF:
                sub_type = struct.unpack('>B', stream.read(1))[0]
                length = self._parse_var_len(stream)
                stream.read(length)
            else:
                print "midi event ", hex(event_type)
                #TODO do something!
                print MidiEvent.parse(event_type, stream)
        
    def _parse_var_len(self, stream):
        result = 0
        while True:
            result = result << 8
            raw = stream.read(1)
            if len(raw) is 0:
                return None
            next_byte = struct.unpack('>B', raw)[0]
            if next_byte & 0x80 is 0:
                return result + next_byte
            result = result + (next_byte ^ 0x80)
    
    def if_track(self, func):
        return func(self)

class MidiEvent(object):
    @classmethod
    def parse(cls, type_byte, stream):
        parse_cls = cls.event_class_for(type_byte)
        if parse_cls is None:
            #TODO raise exception
            print "Unknown: ", hex(type_byte), bin(type_byte)
            return
        return parse_cls(type_byte, stream)
    
    @classmethod
    def event_class_for(cls, type_byte):
        for each in cls.__subclasses__():
            result = each.event_class_for(type_byte)
            if result is not None:
                return result
        return None

    def __init__(self, type_byte, stream):
        pass
    
class MidiChannelEvent(MidiEvent):
    def __init__(self, type_byte, stream):
        self.channel = type_byte & 0b1111
        
class ControlChange(MidiChannelEvent):
    @classmethod
    def event_class_for(cls, type_byte):
        if (0xB0 & type_byte) is 0xB0:
            return cls
        
    def __init__(self, type_byte, stream):
        super(self.__class__, self).__init__(type_byte, stream)
        stream.read(2)

class ProgramChange(MidiChannelEvent):
    @classmethod
    def event_class_for(cls, type_byte):
        if (0xC0 & type_byte) is 0xC0:
            return cls
        
    def __init__(self, type_byte, stream):
        super(self.__class__, self).__init__(type_byte, stream)
        stream.read(1)
        
class NoteOn(MidiChannelEvent):
    @classmethod
    def event_class_for(cls, type_byte):
        if (0x90 & type_byte) is 0x90:
            return cls
        
    def __init__(self, type_byte, stream):
        super(self.__class__, self).__init__(type_byte, stream)
        stream.read(2)

class NoteOff(MidiChannelEvent):
    @classmethod
    def event_class_for(cls, type_byte):
        if (0x80 & type_byte) is 0x80:
            return cls
        
    def __init__(self, type_byte, stream):
        super(self.__class__, self).__init__(type_byte, stream)
        stream.read(2)
    
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

