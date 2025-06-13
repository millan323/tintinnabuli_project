# === Tintinnabuli Harmonizer ===

from melody_utils import mirror_melody
from harmony_utils import harmonize_melody

# --- Scale Definitions ---

from utils import (
    MAJOR_SCALES,
    MINOR_SCALES,
    NOTE_TO_SEMITONE,
    SEMITONE_TO_NOTE,
    note_to_midi,
    midi_to_note,
    get_scale_notes,
    get_triad,
    get_triad_note,
    get_parallel_interval,
)


# --- Melody Transposition (Diatonic) ---


def transpose_melody_diatonic(melody, degree_shift, key="C", mode="major"):
    transposed = []
    try:
        scale = get_scale_notes(key, mode)
        if scale is None:
            raise ValueError(f"Unsupported key/mode combination: {key} {mode}")
    except Exception as e:
        print(f"[ERROR] Failed to get scale: {e}")
        return [None] * len(melody)

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

        finally:
            if not melody:
                print("[INFO] Empty melody provided.")
            elif all(n is None for n in transposed):
                print("[INFO] All notes failed to transpose.")

    return transposed


from music21 import converter, note


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
            score = converter.parse(file_path)
            part = score.parts[0]
            melody_notes = []
            for el in part.flat.notes:
                if isinstance(el, note.Note):
                    melody_notes.append(el.nameWithOctave)
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


from music21 import stream, note, metadata, key as m21key


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

    # Add Key Signature
    p = stream.Part()
    ks = m21key.Key(key_sig, mode)
    p.append(ks)

    # Melody
    melody_part = stream.Part()
    for m_note in melody:
        n = note.Note(m_note) if m_note else note.Rest()
        melody_part.append(n)

    # T-Voice
    t_part = stream.Part()
    if t_voice:
        for t_note in t_voice:
            n = note.Note(t_note) if t_note else note.Rest()
            t_part.append(n)

    # Add both parts
    p.append(melody_part)
    if t_voice:
        p.append(t_part)

    s.insert(0, p)
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
    from music21 import stream, note, metadata, key as m21key

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
if __name__ == "__main__":
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

    if user_choice == "xml":
        print(
            "\n[INFO] Please ensure your MusicXML file contains ONLY ONE monophonic melody line (no chords or multiple instruments)."
        )
        print(
            "      Other info like dynamics, articulation, tempo will be preserved if present.\n"
        )

        try:
            from music21 import converter, stream, chord, key as key_module

            xml_path = input("Enter path to your MusicXML file: ").strip()
            score = converter.parse(xml_path)

            parts = score.parts
            if len(parts) != 1:
                raise ValueError(
                    "Too many parts in score. Expected one monophonic melody line."
                )

            melody_part = parts[0]
            measures = melody_part.getElementsByClass(stream.Measure)

            # Check for chords (only allow single-note events)
            for m in measures:
                for n in m.notesAndRests:
                    if isinstance(n, chord.Chord):
                        raise ValueError("Chord found in melody line.")

            # Extract melody note names and octaves
            for n in melody_part.flat.notes:
                melody.append(n.nameWithOctave)

            # Extract key signature and mode (fallback to C major if undetectable)
            ks = melody_part.analyze("key")
            key = ks.tonic.name
            mode = ks.mode
            print(f"[INFO] Detected key: {key} {mode}")

            # Extract time signature if available
            ts = melody_part.recurse().getElementsByClass("TimeSignature").first()
            if ts:
                print(f"[INFO] Detected time signature: {ts.ratioString}")
            else:
                print("[INFO] Time signature not found.")

        except Exception as e:
            print(
                f"\n[ERROR] Music in XML file is too complex for this script. Details: {e}"
            )
            sys.exit(1)

    elif user_choice == "manual":
        melody_str = input(
            "Enter melody notes separated by spaces (e.g., C4 D4 E4 F4 G4): "
        )
        melody = melody_str.strip().split()
        key = input("Enter key (e.g., C, D#, Bb): ").strip().capitalize()
        mode = input("Enter mode ('major' or 'minor'): ").strip().lower()

    else:
        print("Invalid choice. Please enter 'xml' or 'manual'.")
        sys.exit(1)

    print(f"\n[INFO] Melody loaded: {melody}")
    print(f"[INFO] Working in {key} {mode}\n")

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
            pattern = [True] * len(melody)

        t_level = int(input("Enter T-voice level (e.g., 1 for T-1): "))
        t_dir = input("Direction of T-voice? ('below' or 'above'): ").strip().lower()

        t_voice_output = apply_t_voice_with_pattern(
            melody,
            key=key,
            mode=mode,
            triad_level=t_level,
            direction=t_dir,
            bind_pattern=pattern,
        )

        print("\nMelody:     ", melody)
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
            build_score(
                melody=melody,
                t_voice=t_voice_output,
                key_signature=key,
                output_xml="harmonized_output.musicxml",
                output_midi="harmonized_output.mid",
            )
            print("[INFO] Export complete.")
        else:
            print("[INFO] Export skipped.")
    except Exception as e:
        print(f"[ERROR] Failed to export: {e}")
