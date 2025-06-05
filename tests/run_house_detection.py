import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from music21 import converter
from analysis.house_detector import detect_house_sections

# Load your musicXML score
score = converter.parse("tests/stufen_excerpt.musicxml")

# Run detection
house_hits = detect_house_sections(score)

# Print results
if house_hits:
    print("🔍 Detected potential HOUSE sections:")
    for part, measure in house_hits:
        print(f" - {part}, Measure {measure}")
else:
    print("❌ No house candidates found.")
