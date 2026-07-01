"""
Tetryonic physics-units map (the 'PHYSICS UNITS' plate, Book 1 p.40).

A reference dictionary tying each quantity to its symbol, Tetryonic reading and SI units.
This is documentation-as-data: other tools can use it to label results consistently.
Every mechanical quantity in Tetryonics is "energy per spatial/temporal coordinate" —
i.e. a power of c applied to the mass-energy geometry.

Also records the two colour codes (see geometry.LEVEL_COLOURS / PROPERTY_COLOURS).
"""

from __future__ import annotations

# quantity -> (symbol, SI units, note)
UNITS = {
    "wavelength":          ("λ", "m", "spatial extent"),
    "velocity":            ("v", "m/s", "1D, vector"),
    "acceleration":        ("a", "m/s²", "Δv/Δt"),
    "frequency":           ("f", "1/s", "f = 2v (longitudinal cycles)"),
    "linear_momentum":     ("p", "kg·m/s", "p = mv"),
    "force":               ("F", "kg·m/s²", "F = ma = dp/dt"),
    "energy":              ("E", "kg·m²/s²", "E = mv² = hv²"),
    "qam":                 ("Ω", "m²/s", "quantised angular momentum (hidden constant)"),
    "planck_constant":     ("h", "kg·m²/s", "h = mΩ = quantum of action & of mass"),
    "em_mass":             ("m", "kg", "2D planar energy/second = E/c²"),
    "matter":              ("M", "kg", "3D tetrahedral topology = E/c⁴"),
    "charge":              ("q", "kg·s", "mass·QAM/second = Ω/c² per fascia"),
    "electric_constant":   ("ε₀", "F/m", "= 1/(μ₀c²)"),
    "magnetic_constant":   ("μ₀", "H/m", "= 1/(ε₀c²) = 4π×10⁻⁷"),
    "current":             ("I", "kg/s", "charged Matter in motion"),
    "celeritas_squared":   ("c²", "m²/s²", "proportionality constant between coordinate systems"),
}


def describe(quantity: str) -> str:
    sym, si, note = UNITS[quantity]
    return f"{quantity}: {sym} [{si}] — {note}"


def all_units() -> list[str]:
    return [describe(q) for q in UNITS]


# The two colour codes, surfaced here for convenience.
def colour_codes() -> dict:
    from .geometry import LEVEL_COLOURS, PROPERTY_COLOURS
    return {"energy_level": LEVEL_COLOURS, "physics_property": PROPERTY_COLOURS}
