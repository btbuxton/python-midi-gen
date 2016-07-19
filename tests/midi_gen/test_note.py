import unittest

from midi_gen.note import Note

class NoteTest(unittest.TestCase):

    def testNote(self):
        note = Note(24)
        self.assertEqual(24, note.value)
        self.assertEqual(note, Note['C2'])
        
    def testOctaveUp(self):
        note = Note(24)
        self.assertEqual(36, note.octave_up().value)
    
    def testOctaveDownFail(self):
        note = Note(11)
        self.assertRaises(ValueError, note.octave_down)
        
    def testName(self):
        note = Note(24)
        another = Note['C2']
        self.assertEqual(note, another)
        self.assertEqual('C2', note.name)
        self.assertEqual('C2', another.name)
        self.assertEqual('G10', Note(127).name)
        
    def testScale(self):
        root = Note['C2']
        notes = root.scale(Note.maj)
        scale = iter(notes)
        self.assertEqual(Note['C2'], scale.next())
        self.assertEqual(Note['D2'], scale.next())
        self.assertEqual(Note['E2'], scale.next())
        self.assertEqual(Note['F2'], scale.next())
        self.assertEqual(Note['G2'], scale.next())
        self.assertEqual(Note['A2'], scale.next())
        self.assertEqual(Note['B2'], scale.next())
        
if __name__ == "__main__":
    unittest.main()