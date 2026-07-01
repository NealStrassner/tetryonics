"""
The Tetryonic geometry core — the equilateral-triangle engine every other module sits on.

Founding identity:  "squared energies are equilateral geometries."
An equilateral triangle of side ``n`` subdivides into ``n**2`` unit triangles:
    * row r (from the apex) holds (2r-1) unit triangles  -> r up + (r-1) down
    * cumulative through row n = n**2   (since sum of first n odd numbers = n**2)
    * the right edge carries the square numbers 1,4,9,16,...
    * odd numbers = transverse levels (bosons);  even = longitudinal (photons)

Primitive type: a *fascia* = a subdividable equilateral triangle. Four fascia fold
into a *tetryon* (a tetrahedron) — the foundational quantum of Matter. See
../../_KNOWLEDGE_Book1_QM.md §A, §C2.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

SQRT3 = math.sqrt(3.0)

# --- Two distinct colour codes (see Part III of the knowledge doc) ------------
# 1) ENERGY-LEVEL chromatic code, index 0..9 (from the visible spectrum):
LEVEL_COLOURS = [
    "Brown", "Red", "Orange", "Yellow", "Green",
    "Aqua", "Blue", "Indigo", "Violet", "Black",
]

# 2) PHYSICS-PROPERTY colour code (Abraham's direct description, ABRAHAM.txt):
PROPERTY_COLOURS = {
    "momentum": "Pink",        # velocity / acceleration / linear momentum
    "positive": "Red",         # positive charge
    "neutral": "Blue",         # neutral charge
    "negative": "Black",       # negative charge
    "magnetic_north": "Green",
    "magnetic_south": "Blue",
    "charge_geometry": "Gold",
    "energy": "Maroon",
    "mass": "Blue",
}


def level_colour(level: int) -> str:
    """Chromatic colour for an energy/quantum level (wraps mod 10)."""
    return LEVEL_COLOURS[level % 10]


# --- Number-theory of the grid ------------------------------------------------
def units_in_triangle(n: int) -> int:
    """Total unit triangles in an equilateral triangle of side ``n`` -> n**2."""
    if n < 0:
        raise ValueError("side must be >= 0")
    return n * n


def units_in_row(r: int) -> int:
    """Unit triangles in row ``r`` (from apex, 1-based) -> 2r-1 (odd)."""
    if r < 1:
        raise ValueError("row index starts at 1")
    return 2 * r - 1


def up_down_in_row(r: int) -> tuple[int, int]:
    """(up-pointing, down-pointing) unit triangles in row ``r`` -> (r, r-1)."""
    return r, r - 1


def is_square(n: int) -> bool:
    """True if ``n`` is a perfect square (a completed equilateral energy level)."""
    if n < 0:
        return False
    root = math.isqrt(n)
    return root * root == n


def odd_sum_to_square(n: int) -> int:
    """Sum of the first ``n`` odd numbers = n**2 (the core visual identity)."""
    return sum(2 * r - 1 for r in range(1, n + 1))


def equilateral_area(base: float) -> float:
    """Area of an equilateral triangle of side ``base`` = (sqrt(3)/4) * base**2."""
    return (SQRT3 / 4.0) * base * base


# --- EM field quantum geometries (boson / photon) ----------------------------
# Energy is the SQUARE of a level: a triangular field at level n holds n² Planck
# quanta. The EM field quanta are FLAT (2D) tilings of those triangles:
#     boson  = ONE equilateral triangle              ->   n²  quanta (transverse, charged)
#     photon = a DIAMOND (rhombus) of TWO triangles  ->  2·n² quanta (neutral, planar, c)
# A photon is literally two opposite-handed bosons fused edge-to-edge — which is why
# f = 2v, and why Matter (a tetryon = FOUR triangles FOLDED into 3D) is 4·n² and is
# velocity-variant while the flat photon always travels at c. See Book 1 §C / Book 2.
def boson_quanta(n: int) -> int:
    """Planck quanta in a single-triangle boson at level n  = n²."""
    return units_in_triangle(n)


def photon_quanta(n: int) -> int:
    """Planck quanta in a photon — a flat diamond of TWO triangles — at level n = 2·n²."""
    return 2 * units_in_triangle(n)


def field_quanta(fascia: int, n: int) -> int:
    """General Tetryonic field count = (number of triangular fascia) · n².

    boson=1 (n²), photon=2 (2n²), tetryon/Matter=4 (4n²), lepton/quark shell=12 (12n²)."""
    return fascia * units_in_triangle(n)


# --- Fascia & tetryon ---------------------------------------------------------
@dataclass(frozen=True)
class Fascia:
    """One equilateral face of a tetryon at quantum ``level`` n.

    Holds ``level**2`` unit mass-energy triangles. ``sign`` is the charge/flux
    handedness: +1 = clockwise (positive), -1 = counter-clockwise (negative),
    0 = balanced/neutral. Physically a fascia is one shorted inductive loop.
    """

    level: int = 1
    sign: int = +1  # +1 clockwise/positive, -1 ccw/negative, 0 neutral

    @property
    def units(self) -> int:
        return units_in_triangle(self.level)

    @property
    def colour(self) -> str:
        return PROPERTY_COLOURS[
            {1: "positive", -1: "negative", 0: "neutral"}[self.sign]
        ]

    def area(self, base: float = 1.0) -> float:
        return equilateral_area(base)


@dataclass(frozen=True)
class Photon:
    """A photon = a planar DIAMOND (rhombus) of two opposite-handed fascia.

    Two triangles fused edge-to-edge: one up (+), one down (−), so it is net-neutral
    and FLAT (2D — never folded into 3D like Matter), which is why it always moves at c.
    Holds ``2·level²`` Planck mass-energy-momentum quanta (level n = the standing-wave
    harmonic). A photon = 2 bosons, hence its frequency f = 2v.
    """

    level: int = 1

    @property
    def quanta(self) -> int:
        """Planck quanta in the diamond = 2·n²."""
        return photon_quanta(self.level)

    @property
    def bosons(self) -> int:
        return 2

    @property
    def triangles(self) -> int:
        return 2

    @property
    def is_planar(self) -> bool:
        return True

    def vertices(self, size: float = 1.0):
        """The 4 corners of the flat diamond (a rhombus, two stacked equilateral
        triangles) in the XY plane — for the 2D/3D visualizer."""
        h = (SQRT3 / 2.0) * size
        return [(0.0, h, 0.0), (-size / 2, 0.0, 0.0),
                (0.0, -h, 0.0), (size / 2, 0.0, 0.0)]


@dataclass(frozen=True)
class Tetryon:
    """A tetrahedron = 4 fascia. The foundational quantum of Matter (4n geometry).

    ``charge`` is the [clockwise, counter-clockwise] quanta pair across the 4 fascia.
    Net charge quanta = cw - ccw. A charged tetryon is [4,0] or [0,4]; the neutral
    tetryon [2,2] is the gluon.
    """

    level: int = 1
    cw: int = 4   # clockwise / positive quanta
    ccw: int = 0  # counter-clockwise / negative quanta

    def __post_init__(self) -> None:
        if self.cw + self.ccw != 4:
            raise ValueError("a tetryon has exactly 4 fascia (cw + ccw must == 4)")

    @property
    def fascia(self) -> int:
        return 4

    @property
    def net_charge_quanta(self) -> int:
        return self.cw - self.ccw

    @property
    def is_neutral(self) -> bool:
        return self.net_charge_quanta == 0

    @property
    def units(self) -> int:
        """Total unit mass-energy triangles = 4 * level**2."""
        return 4 * units_in_triangle(self.level)


# Convenience constructors for the three tetryon charge states.
def positive_tetryon(level: int = 1) -> Tetryon:
    return Tetryon(level=level, cw=4, ccw=0)


def negative_tetryon(level: int = 1) -> Tetryon:
    return Tetryon(level=level, cw=0, ccw=4)


def neutral_tetryon(level: int = 1) -> Tetryon:
    """Also known as a gluon."""
    return Tetryon(level=level, cw=2, ccw=2)
