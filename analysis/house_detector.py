from music21 import stream, note, chord, meter, tempo, expressions

CMINOR_TRIAD = {60, 63, 67}  # MIDI numbers for C, E♭, G

def is_triadic(chord_or_notes):
    """
    Checks if all given pitches are members of the C minor triad.
    Accepts chords or lists of notes.
    """
    if isinstance(chord_or_notes, chord.Chord):
        pitch_set = set(p.midi for p in chord_or_notes.pitches)
    else:
        pitch_set = set(n.pitch.midi for n in chord_or_notes if isinstance(n, note.Note))
    return all(p in CMINOR_TRIAD for p in pitch_set)

def is_syncopated_pulse(measure):
    """
    Heuristic: look for repeated short-duration Gs (quarter notes, offset by 0.125)
    """
    pulse_notes = [n for n in measure.notes if n.pitch.name == 'G' and n.quarterLength == 0.25]
    return len(pulse_notes) >= 4 and all(n.offset % 0.5 != 0.0 for n in pulse_notes)

def detect_house_sections(score: stream.Score):
    house_measures = []
    for part in score.parts:
        for measure in part.getElementsByClass(stream.Measure):
            notes = measure.notes
            if is_syncopated_pulse(measure) and is_triadic(notes):
                house_measures.append((part.partName, measure.measureNumber))
    return house_measures
