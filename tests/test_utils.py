import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from melody_utils import mirror_melody
from harmony_utils import harmonize_melody
from utils import note_to_midi, midi_to_note


def test_harmonize():
    result = harmonize_melody("E4", key="C", mode="major", tintinnabuli_levels=[-1, -2], extra_m_intervals=[-9])
    print("Harmonize E4 result:")
    for k, v in result.items():
        print(f"{k}: {v}")

def test_mirror():
    melody = [(64, 0.5), (66, 0.5), (67, 1.0)]  # C4, D4, E4
    mirrored = mirror_melody(melody, axis_note="E4")
    print("\nMirrored melody:")
    for p, d in mirrored:
        print(f"MIDI: {p}, Duration: {d}")

if __name__ == "__main__":
    test_harmonize()
    test_mirror()
