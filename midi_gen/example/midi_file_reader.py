'''
Created on Oct 4, 2016

@author: btbuxton
'''

from midi_gen.midi_file import MidiFileReader

def main():
    with open('../../data/RunningLate-DanWheeler.mid','rb') as stream:
        for chunk in MidiFileReader(stream):
            print chunk
            def do_track(track):
                for event in track:
                    print event
            chunk.if_track(do_track)
    
if __name__ == '__main__':
    main()