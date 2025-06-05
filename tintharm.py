# === Tintinnabuli Harmonizer ===


from melody_utils import mirror_melody
from harmony_utils import harmonize_melody

MAJOR_SCALES = {
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
    'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    'Eb': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']
}

MINOR_SCALES = {
    'C': ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'],
    'G': ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'],
    'D': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'],
    'A': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    'E': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
    'B': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
    'F#': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],
    'F': ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb']
}

NOTE_TO_SEMITONE = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11
}

SEMITONE_TO_NOTE = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E",
    5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A",
    10: "A#", 11: "B"
}

def note_to_midi(note):
    name = note[:-1]
    octave = int(note[-1])
    semitone = NOTE_TO_SEMITONE.get(name)
    if semitone is None:
        raise ValueError(f"Invalid note name: {note}")
    return 12 * (octave + 1) + semitone

def midi_to_note(midi):
    semitone = midi % 12
    octave = (midi // 12) - 1
    name = SEMITONE_TO_NOTE[semitone]
    return f"{name}{octave}"

def get_scale_notes(key: str, mode: str):
    key = key.capitalize()
    mode = mode.lower()
    if mode == 'major':
        return MAJOR_SCALES.get(key)
    elif mode == 'minor':
        return MINOR_SCALES.get(key)
    return None

def get_triad(scale):
    return [scale[0], scale[2], scale[4]]

def get_triad_note(note, triad, level, direction='below'):
    if note not in triad:
        return None
    index = triad.index(note)
    if direction == 'below':
        new_index = (index - level) % len(triad)
    else:
        new_index = (index + level) % len(triad)
    return triad[new_index]

def get_parallel_interval(note, scale, interval):
    try:
        idx = scale.index(note)
        return scale[(idx + interval) % len(scale)]
    except ValueError:
        return None


if __name__ == "__main__":
    test_note = "E4"
    print(f"Harmonizing note: {test_note}")
    result = harmonize_melody(
        melody_note=test_note,
        key="C",
        mode="major",
        tintinnabuli_levels=[-1, -2],
        extra_m_intervals=[-9]  # Major sixth below
    )
    for voice, note in result.items():
        print(f"{voice}: {note}")



# === TEST CASE FU
