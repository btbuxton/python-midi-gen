import unittest

from midi_gen.note import Note

class NoteTest(unittest.TestCase):
    
    def testMiddleC(self):
        note = Note.middle_c()
        self.assertEqual(Note['C3'], note)

    def testNote(self):
        note = Note(60)
        self.assertEqual(60, note.value)
        self.assertEqual(Note['C3'], note)
        
    def testOctaveUp(self):
        note = Note(24)
        self.assertEqual(36, note.octave_up().value)
    
    def testOctaveDownFail(self):
        note = Note(11)
        self.assertRaises(ValueError, note.octave_down)
        
    def testName(self):
        note = Note(60)
        another = Note['C3']
        self.assertEqual(note, another)
        self.assertEqual('C3', note.name)
        self.assertEqual('C3', another.name)
        self.assertEqual('G8', Note(127).name)
        
    def testScale(self):
        root = Note['C2']
        notes = root.scale(Note.maj)
        scale = iter(notes)
        self.assertEqual(Note['C2'], next(scale))
        self.assertEqual(Note['D2'], next(scale))
        self.assertEqual(Note['E2'], next(scale))
        self.assertEqual(Note['F2'], next(scale))
        self.assertEqual(Note['G2'], next(scale))
        self.assertEqual(Note['A2'], next(scale))
        self.assertEqual(Note['B2'], next(scale))
        
if __name__ == "__main__":
    unittest.main()