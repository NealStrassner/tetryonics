"""
Music & harmonics — Book 5 (Geometrics).

Tetryonics maps the 12 chromatic notes onto the equilateral/hexagonal phase circle:
one semitone = 30°, so the 12 tones tile a full 360° turn. Intervals are the simple
whole-number frequency ratios (2:1 octave, 3:2 fifth, …) — the same ratios that build
the equilateral energy levels. Equal-temperament frequencies use the 2^(1/12) step.
"""

from __future__ import annotations

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SEMITONE_DEGREES = 30.0     # one semitone = 30° on the phase circle (12 × 30 = 360)

# Just-intonation interval ratios (Book 5 p.120).
JUST_INTERVALS = {
    "unison": (1, 1), "minor_third": (6, 5), "major_third": (5, 4),
    "fourth": (4, 3), "fifth": (3, 2), "major_sixth": (5, 3),
    "octave": (2, 1),
}


def note_index(note: str) -> int:
    """Chromatic index 0..11 of a note name (C=0 … B=11)."""
    return NOTES.index(note.upper().replace("B#", "C"))


def note_to_phase(note: str) -> float:
    """Phase angle (degrees) of a note on the chromatic circle  = semitone × 30°."""
    return note_index(note) * SEMITONE_DEGREES


def interval_ratio(name: str) -> float:
    """Just-intonation frequency ratio of a named interval (e.g. 'fifth' → 1.5)."""
    a, b = JUST_INTERVALS[name]
    return a / b


def interval_from_frequencies(f_low: float, f_high: float) -> float:
    """Frequency ratio between two pitches."""
    return f_high / f_low


def equal_tempered_frequency(midi_note: int) -> float:
    """12-TET frequency (Hz) of a MIDI note number  f = 440·2^((n−69)/12)  (A4=440)."""
    return 440.0 * 2.0 ** ((midi_note - 69) / 12.0)


def note_frequency(note: str, octave: int = 4) -> float:
    """12-TET frequency (Hz) of a named note + octave, e.g. note_frequency('A',4)=440."""
    midi = 12 * (octave + 1) + note_index(note)
    return equal_tempered_frequency(midi)


def scale_ratios(scale: str = "major") -> list:
    """Just-intonation frequency ratios of a scale's degrees (relative to the tonic)."""
    scales = {
        "major": [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2],
        "pentatonic": [1, 9/8, 5/4, 3/2, 5/3, 2],
        "chromatic": [2 ** (i / 12) for i in range(13)],
    }
    return scales[scale.lower()]


def semitones_to_ratio(semitones: int) -> float:
    """Equal-tempered frequency ratio for an interval of n semitones = 2^(n/12)."""
    return 2.0 ** (semitones / 12.0)


def circle_of_fifths() -> list:
    """The 12 notes ordered by ascending perfect fifths (×3:2, mod octave)."""
    order, idx = [], 0
    for _ in range(12):
        order.append(NOTES[idx % 12])
        idx += 7   # a perfect fifth = 7 semitones
    return order
