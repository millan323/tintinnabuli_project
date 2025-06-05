from utils import note_to_midi, midi_to_note, get_scale_notes, get_triad, get_triad_note

def harmonize_melody(melody_note, key, mode, tintinnabuli_levels=None, extra_m_intervals=None):
    """
    Harmonizes a single melody note using:
    - M: the original melody note
    - M-9: a parallel voice a major sixth below (–9 semitones)
    - T voices: labeled as T[a|b|c][1|2|...], where:
        - T = tintinnabuli voice
        - a/b/c = track or behavioral variant
        - number = degree distance below the melody in the triad
    - M3: reserved for third above (optional future addition)

    Parameters:
        melody_note (str): The input melody note, e.g., "E4"
        key (str): Tonal center, e.g., "C"
        mode (str): 'major' or 'minor'
        tintinnabuli_levels (list): List of integers representing degrees below in triad (e.g., [-1, -2])
        extra_m_intervals (list): Optional list of fixed semitone intervals from melody (e.g., [-9])

    Returns:
        dict: A dictionary of harmonized note labels and pitch names
    """
    result = {}

    # Convert melody note to MIDI
    melody_midi = note_to_midi(melody_note)
    result["M"] = melody_note

    # Add additional melodic intervals (e.g., M-9)
    if extra_m_intervals:
        for interval in extra_m_intervals:
            label = f"M{interval}"  # e.g., M-9
            note = midi_to_note(melody_midi + interval)
            result[label] = note

    # Get scale and triad tones for tintinnabuli logic
    scale = get_scale_notes(key, mode)
    if not scale:
        raise ValueError(f"Unsupported key/mode combination: {key} {mode}")
    triad = get_triad(scale)

    # Extract pitch class without octave (e.g., 'E' from 'E4')
    melody_pitch_class = melody_note[:-1]

    # Determine base note for tintinnabuli: use nearest triad tone if melody not in triad
    if melody_pitch_class not in triad:
        closest = min(triad, key=lambda x: abs(scale.index(x) - scale.index(melody_pitch_class)))
        base_note = closest
    else:
        base_note = melody_pitch_class

    # Add tintinnabuli tones with structured labels: Ta1, Tb2, etc.
    if tintinnabuli_levels:
        for i, level in enumerate(tintinnabuli_levels):
            label = f"Ta{abs(level)}"  # Placeholder 'a' indicates first tintinnabuli track
            triad_note = get_triad_note(base_note, triad, abs(level), direction='below')
            result[label] = triad_note

    # TODO: Add support for multiple T tracks (a, b, c) with distinct rhythmic/tethering logic

    return result


