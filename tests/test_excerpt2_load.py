from music21 import converter

score2 = converter.parse("tests/stufen_excerpt2.musicxml")

for part in score2.parts:
    print(part.partName)
