import unittest

from midi_gen.midi.engine import Note
from test.test_support import get_attribute

class NoteTest(unittest.TestCase):

    def testNote(self):
        note = Note(24)
        self.assertEqual(24, note.number)
        self.assertEqual(note, get_attribute(Note, 'C2'))
        
    def testOctaveUp(self):
        note = Note(24)
        self.assertEqual(36, note.octave_up().number)
    
    def testOctaveDownFail(self):
        note = Note(11)
        self.assertRaises(Exception, note.octave_down)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()