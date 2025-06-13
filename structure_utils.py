# structure_utils.py

from melody_utils import mirror_melody

# generate_stepwise_transpositions is currently not implemented


def apply_structure(
    melody, rhythm, structure_command, key="C", mode="major", axis_pitch=None
):
    """
    Applies structural transformation to melody and rhythm.
    Only retrograde modifies rhythm.
    Mirror uses an axis pitch.
    """
    if structure_command[0] == "retrograde":
        return list(reversed(melody)), list(reversed(rhythm))

    elif structure_command[0] == "mirror":
        mirrored = mirror_melody(melody, axis_pitch)
        return melody + mirrored, rhythm * 2

    elif structure_command[0] == "combo":
        mirrored = mirror_melody(melody, axis_pitch)
        retro_mirror = list(reversed(mirrored))
        retro_original = list(reversed(melody))
        return melody + mirrored + retro_mirror + retro_original, rhythm * 4

    elif structure_command[0] == "transposition":
        direction, step, count = (
            structure_command[1],
            structure_command[2],
            structure_command[3],
        )
        transposed = generate_stepwise_transpositions(
            melody, direction, step, count, key, mode
        )
        return melody + transposed, rhythm * (1 + count)

    # Default: return unchanged
    return melody, rhythm


def prompt_structure_options():
    print("\n--- Structure Options ---")
    print("Choose a structure form:")
    print("1. AB (Original, Retrograde)")
    print("2. AM (Original, Mirror over axis)")
    print("3. ABM (Original, Retrograde, Mirror)")
    print("4. Transposition sequence (e.g. stepwise up/down in 2nds/3rds/5ths)")
    choice = input("Enter your choice (1-4): ")

    if choice == "4":
        direction = input("Step direction (up/down): ").lower()
        interval = int(input("Step size in scale degrees (2, 3, 4, or 5): "))
        steps = int(input("How many steps before return?: "))
        return ("transposition", direction, interval, steps)
    elif choice == "1":
        return ("retrograde",)
    elif choice == "2":
        axis_note = input("Enter axis pitch for mirroring (e.g., C4): ")
        return ("mirror", axis_note)
    elif choice == "3":
        axis_note = input("Enter axis pitch for mirroring (e.g., C4): ")
        return ("combo", axis_note)
    else:
        print("Invalid choice. Defaulting to AB.")
        return ("retrograde",)
