import unittest

from midi_gen.midi.engine import Note

class NoteTest(unittest.TestCase):

    def testNote(self):
        note = Note(24)
        self.assertEqual(24, note.value)
        self.assertEqual(note, getattr(Note, 'C2'))
        
    def testOctaveUp(self):
        note = Note(24)
        self.assertEqual(36, note.octave_up().value)
    
    def testOctaveDownFail(self):
        note = Note(11)
        self.assertRaises(ValueError, note.octave_down)

if __name__ == "__main__":
    unittest.main()