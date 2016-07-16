import unittest

from midi_gen.midi.engine import Note

class NoteTest(unittest.TestCase):

    def testNote(self):
        note = Note.C2
        self.assertEqual(24, note.number)
        
    def testOctaveUp(self):
        note = Note.C2
        self.assertEqual(36, note.octave_up().number)
    
    def testOctaveDownFail(self):
        note = Note(11)
        self.assertRaises(Exception, note.octave_down)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()