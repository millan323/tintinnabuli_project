# === xml_utils.py ===

from music21 import converter, key, meter, note, stream


def extract_monophonic_melody_from_xml(path):
    """
    Load a monophonic melody line from a MusicXML file and extract metadata.
    Returns:
        - melody_stream: music21 stream containing the melody
        - metadata: dict with key, mode, time signature
    Raises:
        - ValueError if the file contains polyphonic or multi-part music
    """
    try:
        score = converter.parse(path)
        parts = score.parts
        if len(parts) != 1:
            raise ValueError("MusicXML must contain only one part.")

        notes = [n for n in parts[0].flat.notes if isinstance(n, note.Note)]
        if len(notes) != len(parts[0].flat.notes):
            raise ValueError("Only monophonic melodies without chords are supported.")

        key_sig = parts[0].analyze("key")
        ts = parts[0].recurse().getElementsByClass(meter.TimeSignature).first()
        metadata = {
            "key": key_sig.tonic.name,
            "mode": key_sig.mode,
            "time_signature": str(ts) if ts else "4/4",
        }

        return stream.Part(notes), metadata
    except Exception as e:
        raise ValueError(f"Error parsing XML file: {e}")
