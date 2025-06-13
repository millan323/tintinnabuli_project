import unittest
from main import transpose_melody_diatonic


class TestTransposition(unittest.TestCase):

    def test_diatonic_up_two_degrees(self):
        melody = ["C4", "D4", "E4"]
        expected = ["E4", "F4", "G4"]
        result = transpose_melody_diatonic(melody, 2, key="C", mode="major")
        self.assertEqual(result, expected)

    def test_note_not_in_scale(self):
        melody = ["C4", "C#4", "E4"]
        expected = ["E4", None, "G4"]  # C#4 is not in C major
        result = transpose_melody_diatonic(melody, 2, key="C", mode="major")
        self.assertEqual(result, expected)

    def test_empty_melody(self):
        melody = []
        expected = []
        result = transpose_melody_diatonic(melody, 2, key="C", mode="major")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
