from utils import note_to_midi, midi_to_note, get_scale_notes
from music21 import note as m21_note, pitch as m21_pitch


def mirror_melody(melody_midi, axis_note="Eb4"):
    """
    Reflects a melody around a given axis note (in MIDI numbers).

    Parameters:
        melody_midi (list of tuples): [(midi_pitch, duration), ...]
        axis_note (str): Central pitch to mirror around (e.g., "Eb4")

    Returns:
        list of tuples: Mirrored melody
    """
    axis_midi = note_to_midi(axis_note)
    return [(axis_midi - (p - axis_midi), d) for p, d in melody_midi]


def transpose_note_by_semitones(note_str, semitones):
    """
    Transpose a note by a number of semitones.

    Parameters:
        note_str (str): Note in "C4", "Eb5", etc.
        semitones (int): Number of semitones to shift (positive or negative)

    Returns:
        str or None: Transposed note or None if invalid
    """
    try:
        n = m21_note.Note(note_str)
        n.transpose(semitones, inPlace=True)
        return n.nameWithOctave
    except Exception as e:
        print(f"[ERROR] transpose_note_by_semitones failed for '{note_str}': {e}")
        return None


def transpose_melody_diatonic(melody, degree_shift, key="C", mode="major"):
    """
    Transpose a melody diatonically by scale degree within a given key/mode.

    Parameters:
        melody (list of str): ["C4", "D4", "E4", ...]
        degree_shift (int): Number of scale degrees to shift
        key (str): Root key (e.g., "C", "Eb")
        mode (str): "major" or "minor"

    Returns:
        list of str or None: Transposed melody, with None where input notes are invalid
    """
    transposed = []

    try:
        scale = get_scale_notes(key, mode)
        if scale is None:
            raise ValueError(f"Unsupported key/mode combination: {key} {mode}")

        for note_str in melody:
            try:
                base = note_str[:-1]
                octave = int(note_str[-1])

                if base not in scale:
                    print(f"[WARN] Note '{note_str}' not in scale {key} {mode}")
                    transposed.append(None)
                    continue

                idx = scale.index(base)
                new_idx = idx + degree_shift
                octave_shift = new_idx // len(scale)
                new_idx = new_idx % len(scale)

                new_note = scale[new_idx] + str(octave + octave_shift)
                transposed.append(new_note)

            except Exception as e:
                print(f"[ERROR] Issue with note '{note_str}': {e}")
                transposed.append(None)

    except Exception as e:
        print(f"[ERROR] Failed to get scale: {e}")
        return [None] * len(melody)

    if not melody:
        print("[INFO] Empty melody provided.")
    elif all(n is None for n in transposed):
        print("[INFO] All notes failed to transpose.")

    return transposed
