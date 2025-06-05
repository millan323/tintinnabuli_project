from music21 import converter

# Load your MusicXML file
score = converter.parse("Stufen_excerpt.musicxml")

# Print all part names
print("Parts in score:")
for part in score.parts:
    print("-", part.partName)

# Select one part (e.g., the first one)
part = score.parts[0]

# Show contents of that part in text format
print("\nText representation of first part:")
part.show('text')
