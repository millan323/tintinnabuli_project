import os
import pandas as pd
from music21 import converter, interval, pitch, note

# === CONFIG ===
XML_FOLDER = "data/xml/"
OUTPUT_CSV = "stylefinder_features.csv"

CATEGORIES = {
    "Road_Orch.musicxml": "inward",
    "Reise_intro.musicxml": "minimalist",
    "Reise_excerpt5.musicxml": "excited",
    "Reise_excerpt4.musicxml": "planning",
    "Soteria.musicxml": "unclear",
    "Spiegel_Im_Spiegel_Cello__Piano_-_In_F_Major_-_D_Minor - Full score - 01 Spiegel Im Spiegel.musicxml": "tintinnabuli",
    "Fratres_for_Violin_and_Piano - Full score - 01 Fratres (1980).musicxml": "tintinnabuli",
    "Music_for_18_Musicians - Full score - 01 Untitled score.musicxml": "minimalist",
    "The_Deers_Cry - Full score - 01 The Deer's Cry.musicxml": "sacred",
    # add more as needed
}


def extract_features_from_score(file_path):
    try:
        score = converter.parse(file_path)
        all_notes = score.recurse().notes

        pitches = [n.pitch.midi for n in all_notes if isinstance(n, note.Note)]
        durations = [n.quarterLength for n in all_notes if isinstance(n, note.Note)]

        if not pitches:
            return None  # Skip empty files

        pitch_range = max(pitches) - min(pitches)
        avg_interval = (
            sum(abs(pitches[i] - pitches[i - 1]) for i in range(1, len(pitches)))
            / (len(pitches) - 1)
            if len(pitches) > 1
            else 0
        )

        key_analysis = score.analyze("key")
        features = {
            "filename": os.path.basename(file_path),
            "total_notes": len(pitches),
            "pitch_range": pitch_range,
            "avg_interval": avg_interval,
            "note_density": len(pitches) / score.duration.quarterLength,
            "avg_duration": sum(durations) / len(durations),
            "key": key_analysis.tonic.name,
            "mode": key_analysis.mode,
            "category": CATEGORIES.get(os.path.basename(file_path), "unspecified"),
        }
        return features

    except Exception as e:
        print(f"[ERROR] Skipping {file_path}: {e}")
        return None


def main():
    print("🎵 StyleFinder Dataset Extractor Starting...\n")
    all_features = []

    for filename in os.listdir(XML_FOLDER):
        if filename.endswith(".musicxml") or filename.endswith(".xml"):
            full_path = os.path.join(XML_FOLDER, filename)
            print(f"Processing: {filename}")
            feats = extract_features_from_score(full_path)
            if feats:
                all_features.append(feats)

    df = pd.DataFrame(all_features)
    print("\n✅ Extraction complete.\n")
    print(df)

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n📁 Features saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
