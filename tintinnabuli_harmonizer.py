# tintinnabuli_harmonizer.py

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

def get_scale_notes(key: str, mode: str):
    if mode == 'major':
        return MAJOR_SCALES.get(key)
    elif mode == 'minor':
        return MINOR_SCALES.get(key)
    return None

def get_note_index(note, scale):
    try:
        return scale.index(note)
    except ValueError:
        return -1

def get_parallel_interval(note, scale, interval):
    idx = get_note_index(note, scale)
    if idx == -1:
        return None
    return scale[(idx + interval) % len(scale)]

def get_triad(scale):
    return [scale[0], scale[2], scale[4]]

def get_triad_note(note, triad, scale, level, direction='below'):
    melody_idx = get_note_index(note, scale)
    triad_indices = [get_note_index(t, scale) for t in triad if get_note_index(t, scale) != -1]
    if melody_idx == -1 or not triad_indices:
        return None
    if direction == 'below':
        candidates = [i for i in triad_indices if i < melody_idx]
        while len(candidates) < level:
            candidates = triad_indices[::-1] + candidates
        chosen_idx = candidates[-level % len(triad_indices)]
    else:
        candidates = [i for i in triad_indices if i > melody_idx]
        while len(candidates) < level:
            candidates += triad_indices
        chosen_idx = candidates[(level - 1) % len(triad_indices)]
    return scale[chosen_idx]

def harmonize_melody(melody_note, key='C', mode='major', tintinnabuli_levels=[-1]):
    scale = get_scale_notes(key, mode)
    if not scale:
        return {"Error": f"Unsupported key or mode: {key} {mode}"}
    triad = get_triad(scale)
    result = {
        'M': melody_note,
        'M-6': get_parallel_interval(melody_note, scale, -5),
        'M-10': get_parallel_interval(melody_note, scale, -6),
        'M+6': get_parallel_interval(melody_note, scale, +5),
        'M+3': get_parallel_interval(melody_note, scale, +2),
    }
    for level in tintinnabuli_levels:
        if level < 0:
            tn = get_triad_note(melody_note, triad, scale, abs(level), direction='below')
            if tn:
                result[f'T{level}'] = tn
        else:
            tn = get_triad_note(melody_note, triad, scale, level, direction='above')
            if tn:
                result[f'T{level}'] = tn
    return result

if __name__ == "__main__":
    melody_note = input("Enter melody note (e.g., C, D, E): ").strip()
    key = input("Enter key (e.g., C, G, A): ").strip()
    mode = input("Enter mode (major or minor): ").strip().lower()
    levels_input = input("Enter Tintinnabuli levels (e.g., -1,2 or -1,-2): ")
    try:
        levels = [int(x.strip()) for x in levels_input.split(",")]
    except:
        print("Invalid Tintinnabuli levels format.")
        levels = []

    if melody_note and key and mode and levels:
        result = harmonize_melody(melody_note, key, mode, levels)
        for label, note in result.items():
            print(f"{label}: {note}")
    else:
        print("Missing input. Please enter all required values correctly.")
