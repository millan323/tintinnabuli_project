from music21 import converter, interval, key

# Load the concert-pitch version of the score
score = converter.parse("data/Road_Horn.musicxml")

# Define the key signature for each House entry
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

house_bars = list(house_keys.keys())
results = []

# Extract horn and piano parts
horn_part = [p for p in score.parts if "Horn" in p.partName][0]
piano_part = [p for p in score.parts if "Piano" in p.partName][0]

for bar in house_bars:
    current_key = key.Key(house_keys[bar])

    # Find the last M-note in the two bars preceding the House
    m_note = None
    for m in horn_part.measures(bar - 2, bar):
        for n in m.recurse().notes:
            if n.offset < m.highestTime:
                m_note = n

    # Find the lowest bass note in the final bar of the House (bar+1)
    bass_note = None
    for m in piano_part.measures(bar + 1, bar + 2):
        for n in m.recurse().notes:
            if n.offset < m.highestTime and n.pitch:
                if bass_note is None or n.pitch.midi < bass_note.pitch.midi:
                    bass_note = n

    # Determine if the bass note is a third below the M-note (within the key)
    if m_note and bass_note:
        intvl = interval.Interval(noteStart=bass_note, noteEnd=m_note)
        rule_met = intvl.simpleName in ['m3', 'M3']
        intvl_name = intvl.name
    else:
        rule_met = False
        intvl_name = "N/A"

    results.append((bar, m_note.nameWithOctave if m_note else None,
                    bass_note.nameWithOctave if bass_note else None,
                    intvl_name, rule_met))

# Output results
for r in results:
    print(f"House at bar {r[0]}: M-note={r[1]}, Bass={r[2]}, Interval={r[3]}, Rule Met={r[4]}")
