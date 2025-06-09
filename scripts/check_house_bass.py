from music21 import converter, interval, key, pitch

# Load the concert-pitch score
score = converter.parse("data/Road_Horn.musicxml")

# Define the key signatures at each House entry
house_keys = {
    9: 'C# minor',
    24: 'C# minor',
    38: 'C# minor',
    48: 'F minor',
    59: 'F minor',
    66: 'F minor',
    76: 'C# major',
    87: 'C# major'
}

# Define the House bars
house_bars = list(house_keys.keys())
results = []

# Locate parts
piano_part = None
horn_part = None
for p in score.parts:
    name = (p.partName or "").lower()
    if 'piano' in name:
        piano_part = p
    elif 'horn' in name:
        horn_part = p

if not piano_part:
    raise ValueError("Piano part not found.")

# Main analysis loop
for bar in house_bars:
    tonic, mode_type = house_keys[bar].split()
    current_key = key.Key(tonic, mode_type)
    
    m_note = None
    bass_note = None

    # Step 1: Find last M-note before House
    if bar == 9:
        # special case: intro M-line (bar 8), in treble clef piano
        for m in piano_part.measures(8, 9).getElementsByClass('Measure'):
            for n in m.recurse().notes:
                if n.offset < m.highestTime:
                    m_note = n
    else:
        if horn_part:
            for m in horn_part.measures(bar - 2, bar).getElementsByClass('Measure'):
                for n in m.recurse().notes:
                    if n.offset < m.highestTime:
                        m_note = n

    # Step 2: Find the lowest bass note in final bar of House (bar + 1)
    for m in piano_part.measures(bar + 1, bar + 2).getElementsByClass('Measure'):
        for n in m.recurse().notes:
            if n.offset < m.highestTime and n.pitch:
                if bass_note is None or n.pitch.midi < bass_note.pitch.midi:
                    bass_note = n

    # Step 3: Evaluate interval rule
    if m_note and bass_note:
        try:
            intvl = interval.Interval(noteStart=bass_note, noteEnd=m_note)
            rule_met = intvl.simpleName in ['m3', 'M3']
        except Exception:
            rule_met = False
    else:
        rule_met = False

    results.append((bar, m_note.nameWithOctave if m_note else None,
                    bass_note.nameWithOctave if bass_note else None,
                    rule_met))

# Output results
for r in results:
    print(f"House at bar {r[0]}: M-note={r[1]}, Bass={r[2]}, Rule Met={r[3]}")
