# === Tintinnabuli Harmonizer ===

# Core dependencies
from music21 import converter, stream, note, metadata, key as m21key

# Melody utilities
from melody_utils import (
    mirror_melody,
    transpose_note_by_semitones,
    transpose_melody_diatonic,
)

# Harmony utilities
from harmony_utils import harmonize_melody

# XML utilities
from xml_utils import extract_monophonic_melody_from_xml

# Structural logic
from structure_utils import prompt_structure_options, apply_structure

# Utility functions
from utils import (
    note_to_midi,
    midi_to_note,
    get_scale_notes,
    get_triad,
    get_triad_note,
    get_parallel_interval,
    MAJOR_SCALES,
    MINOR_SCALES,
    NOTE_TO_SEMITONE,
    SEMITONE_TO_NOTE,
)

# Optional or unused features (commented out for now)
# from utils import (
#     prompt_tintinnabuli_options,
#     generate_stepwise_transpositions,
#     build_tintinnabuli_score,
#     export_score_to_files,
# )


# --- Melody Transposition (Diatonic) ---


def transpose_melody_diatonic(melody, degree_shift, key="C", mode="major"):
    transposed = []

    try:
        scale = get_scale_notes(key, mode)
        if scale is None:
            raise ValueError(f"Unsupported key/mode combination: {key} {mode}")

        for note in melody:
            try:
                base = note[:-1]
                octave = int(note[-1])
                if base not in scale:
                    print(f"[WARN] Note '{note}' not in scale {key} {mode}")
                    transposed.append(None)
                    continue
                idx = scale.index(base)
                new_idx = idx + degree_shift
                octave_shift = new_idx // len(scale)
                new_idx = new_idx % len(scale)
                new_note = scale[new_idx] + str(octave + octave_shift)
                transposed.append(new_note)
            except Exception as e:
                print(f"[ERROR] Issue with note '{note}': {e}")
                transposed.append(None)

    except Exception as e:
        print(f"[ERROR] Failed to get scale: {e}")
        return [None] * len(melody)

    if not melody:
        print("[INFO] Empty melody provided.")
    elif all(n is None for n in transposed):
        print("[INFO] All notes failed to transpose.")

    return transposed


def get_user_melody():
    """
    Prompt the user to import a melody manually or from MusicXML.
    Returns a list of note names (e.g., ['E4', 'D4', 'C4']) or None if failed.
    """
    print("\n🎵 Melody Input:")
    print("1. Input melody manually (e.g., C4 D4 E4)")
    print("2. Import melody from MusicXML file")
    choice = input("Select option [1 or 2]: ").strip()

    if choice == "1":
        raw = input("Enter space-separated melody note names (e.g., C4 D4 E4): ")
        return raw.strip().split()

    elif choice == "2":
        file_path = input("Enter path to MusicXML file: ").strip()
        try:
            part, metadata = extract_monophonic_melody_from_xml(file_path)
            melody_notes = [n.nameWithOctave for n in part.notes]
            print(f"Imported {len(melody_notes)} notes.")
            return melody_notes
        except Exception as e:
            print(f"[ERROR] Failed to import melody from XML: {e}")
            return None

    else:
        print("Invalid choice. Returning None.")
        return None


# --- T-Voice Application with Pattern ---


def apply_t_voice_with_pattern(
    melody, key, mode, triad_level=1, direction="below", bind_pattern=None
):
    scale = get_scale_notes(key, mode)
    if not scale:
        raise ValueError(f"Unsupported key/mode: {key} {mode}")
    triad = get_triad(scale)

    t_voice = []
    for i, note in enumerate(melody):
        try:
            if bind_pattern and not bind_pattern[i % len(bind_pattern)]:
                t_voice.append(None)
                continue
            base = note[:-1]
            if base not in triad:
                t_voice.append(None)
                continue
            triad_note = get_triad_note(base, triad, triad_level, direction)
            if triad_note == base:
                t_voice.append(None)
            else:
                t_voice.append(triad_note + note[-1])
        except Exception as e:
            print(f"[ERROR] {e} on note {note}")
            t_voice.append(None)
    return t_voice


def build_tintinnabuli_score(
    melody,
    t_voice=None,
    key_sig="C",
    mode="major",
    title="Tintharm Example",
    composer="Anonymous",
):
    """
    Builds a music21 Score object from melody and optional T-voice.
    """
    s = stream.Score()
    s.insert(0, metadata.Metadata())
    s.metadata.title = title
    s.metadata.composer = composer

    # Melody Part
    melody_part = stream.Part()
    melody_part.id = "Melody"
    melody_part.append(m21key.Key(key_sig, mode))
    for m_note in melody:
        melody_part.append(note.Note(m_note) if m_note else note.Rest())

    # T-Voice Part (if exists)
    if t_voice:
        t_part = stream.Part()
        t_part.id = "T-Voice"
        t_part.append(m21key.Key(key_sig, mode))
        for t_note in t_voice:
            t_part.append(note.Note(t_note) if t_note else note.Rest())
        s.insert(0, t_part)

    s.insert(0, melody_part)
    return s


def export_score_to_files(score, filename_base="tintharm_output"):
    """
    Export a music21 score to MusicXML and MIDI formats.
    Useful for visual and audio verification.
    """
    try:
        score.write("musicxml", fp=f"{filename_base}.xml")
        score.write("midi", fp=f"{filename_base}.mid")
        print(f"[INFO] Exported score to {filename_base}.xml and {filename_base}.mid")
    except Exception as e:
        print(f"[ERROR] Failed to export files: {e}")


def build_score_and_export(
    melody, t_layers, key="C", mode="major", filename_prefix="tintharm_output"
):
    """
    Takes the melody and a dictionary of T-voice layers, constructs a Score,
    and exports it to MusicXML and MIDI.
    """

    s = stream.Score()
    s.insert(0, metadata.Metadata())
    s.metadata.title = filename_prefix
    s.metadata.composer = "Tintinnabuli AI"

    # Key Signature Part
    p = stream.Part()
    ks = m21key.Key(key, mode)
    p.append(ks)

    # Melody
    m_part = stream.Part()
    m_part.id = "Melody"
    for m_note in melody:
        n = note.Note(m_note) if m_note else note.Rest()
        m_part.append(n)
    s.insert(0, m_part)

    # T-Layers
    for label, voice in t_layers.items():
        t_part = stream.Part()
        t_part.id = label
        for t_note in voice:
            n = note.Note(t_note) if t_note else note.Rest()
            t_part.append(n)
        s.insert(0, t_part)

    # Export
    s.write("musicxml", fp=f"{filename_prefix}.xml")
    s.write("midi", fp=f"{filename_prefix}.mid")
    print(f"[INFO] Exported to {filename_prefix}.xml and {filename_prefix}.mid")


# === TEST CASE FUNCTIONS (optional debug or test code) ===
# test functions or manual runs (optional)


# === MAIN EXECUTION ===
def main():
    print("=== Tintinnabuli Harmonizer Tool ===\n")

    user_choice = (
        input(
            "Do you want to import a melody from a MusicXML file or input manually? (Enter 'xml' or 'manual'): "
        )
        .strip()
        .lower()
    )

    melody = []
    key = "C"
    mode = "major"
    rhythm = []

    if user_choice == "xml":
        print(
            "\n[INFO] Please ensure your MusicXML file contains ONLY ONE monophonic melody line (no chords or multiple instruments)."
        )
        print(
            "      Other info like dynamics, articulation, tempo will be preserved if present.\n"
        )

        file_path = input("Enter path to your MusicXML file: ").strip()
        result = extract_monophonic_melody_from_xml(file_path)

        if result is None:
            print("[ABORT] Could not load XML melody. Exiting.")
            sys.exit(1)

        melody_stream, meta = result
        melody = [n.nameWithOctave for n in melody_stream.notes]
        rhythm = [n.quarterLength for n in melody_stream.notes]
        key = meta["key"]
        mode = meta["mode"]

        print(f"[INFO] Detected key: {key} {mode}")
        if meta.get("time_signature"):
            print(f"[INFO] Detected time signature: {meta['time_signature']}")
        else:
            print("[INFO] Time signature not found.")

    elif user_choice == "manual":
        melody_str = input(
            "Enter melody notes separated by spaces (e.g., C4 D4 E4 F4 G4): "
        )
        melody = melody_str.strip().split()
        rhythm = [1.0] * len(melody)  # default to quarter notes
        key = input("Enter key (e.g., C, D#, Bb): ").strip().capitalize()
        mode = input("Enter mode ('major' or 'minor'): ").strip().lower()

    else:
        print("Invalid choice. Please enter 'xml' or 'manual'.")
        sys.exit(1)

    print(f"\n[INFO] Melody loaded: {melody}")
    print(f"[INFO] Working in {key} {mode}\n")
    print(f"[INFO] Rhythm values: {rhythm}")

    # === PROMPT: Melody structure ===
    print("\n[STRUCTURE] Choose a melodic structure or transformation:")
    print("1. AB - Original + Retrograde")
    print("2. AM - Original + Mirror (specify axis note)")
    print("3. ABM - Original + Mirror + Retrograde of both")
    print("4. Stepwise Transposition (up/down in 2nds, 3rds, 4ths, 5ths)")
    print("5. None (leave melody unchanged)")

    try:
        structure_choice = input("Enter structure number (1–5): ").strip()

        if structure_choice == "1":
            structure_cmd = ("retrograde",)
            axis_pitch = None

        elif structure_choice == "2":
            axis_pitch = input("Axis pitch for mirroring (e.g., C4): ").strip()
            structure_cmd = ("mirror",)

        elif structure_choice == "3":
            axis_pitch = input("Axis pitch for mirroring (e.g., C4): ").strip()
            structure_cmd = ("combo",)

        elif structure_choice == "4":
            direction = input("Step direction (up/down): ").lower().strip()
            interval = int(
                input("Step size in scale degrees (2, 3, 4, or 5): ").strip()
            )
            steps = int(
                input("How many steps before repeating original melody?: ").strip()
            )
            structure_cmd = ("transposition", direction, interval, steps)
            axis_pitch = None

        elif structure_choice == "5":
            structure_cmd = ("none",)
            axis_pitch = None

        else:
            print("[WARNING] Invalid choice. Defaulting to: None")
            structure_cmd = ("none",)
            axis_pitch = None

    except Exception as e:
        print(f"[ERROR] Invalid input in structure prompt. Details: {e}")
        print("[INFO] Defaulting to: None")
        structure_cmd = ("none",)
        axis_pitch = None

    # === Apply Structure ===
    structured_melody, rhythm = apply_structure(
        melody, rhythm, structure_cmd, key=key, mode=mode, axis_pitch=axis_pitch
    )
    print(f"[INFO] Structured melody length: {len(structured_melody)}")

    # === PROMPT: M-parallel lines ===
    print("\n=== M-parallel Line Options ===")
    add_parallel = (
        input("Do you want to add an M-parallel line? (y/n): ").strip().lower()
    )

    m_parallel_notes = []

    if add_parallel == "y":
        try:
            interval_input = input(
                "Enter parallel intervals in semitones (e.g., 3 for +3rd, -3 for down a 3rd). Separate with commas for multiple: "
            ).strip()
            intervals = [int(i.strip()) for i in interval_input.split(",") if i.strip()]
            print(f"[INFO] Intervals selected: {intervals}")

            # Apply all intervals and return a list of lists
            for interval in intervals:
                m_par = [
                    (
                        note_str
                        if note_str is None
                        else transpose_note_by_semitones(note_str, interval)
                    )
                    for note_str in structured_melody
                ]
                m_parallel_notes.append(m_par)

            print(f"[INFO] Generated {len(m_parallel_notes)} parallel lines.")
        except Exception as e:
            print(f"[ERROR] Failed to generate M-parallel lines: {e}")
            m_parallel_notes = []

    else:
        print("[INFO] Skipping M-parallel generation.")

    # === PROMPT: T-voice structure ===
    try:
        use_pattern = (
            input("Do you want to apply T-voices to every other note? (y/n): ")
            .strip()
            .lower()
        )
        if use_pattern == "y":
            pattern = [True, False]
        else:
            pattern = [True] * len(structured_melody)

        t_level = int(input("Enter T-voice level (e.g., 1 for T-1): "))
        t_dir = input("Direction of T-voice? ('below' or 'above'): ").strip().lower()

        t_voice_output = apply_t_voice_with_pattern(
            structured_melody,
            key,
            mode,
            triad_level=t_level,
            direction=t_dir,
            bind_pattern=pattern,
        )

        print("\nStructured Melody:     ", structured_melody)
        print("T-Voice out:", t_voice_output)

    except Exception as e:
        print(f"[ERROR] Could not generate T-voices: {e}")
        sys.exit(1)

    # === PROMPT: Export ===
    try:
        do_export = (
            input("\nDo you want to export the result to MusicXML and MIDI? (y/n): ")
            .strip()
            .lower()
        )
        if do_export == "y":
            score = build_tintinnabuli_score(
                melody=structured_melody, t_voice=t_voice_output, key_sig=key, mode=mode
            )

            export_score_to_files(score, filename_base="harmonized_output")

            print("[INFO] Export complete.")
        else:
            print("[INFO] Export skipped.")
    except Exception as e:
        print(f"[ERROR] Failed to export: {e}")

    # Optional: Show score in music21’s viewer
    # score.show()  # Uncomment if needed


if __name__ == "__main__":
    main()
