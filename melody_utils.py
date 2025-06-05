from utils import note_to_midi, midi_to_note


def mirror_melody(melody_midi, axis_note="Eb4"):
    axis_midi = note_to_midi(axis_note)
    return [(axis_midi - (p - axis_midi), d) for p, d in melody_midi]
