"""
Quantum energy levels, electron shells & spectra.

Energy levels are equilateral geometries: level n holds n² unit triangles, gained/lost
in odd-number (2n−1) steps. Electron-shell mass-energy quanta scale as 12·n²
(12, 48, 108, 192, 300, 432, 588, 768 for n=1..8). Bound-electron energies follow the
familiar hydrogen ladder, and spectral lines follow Rydberg.

See ../../_KNOWLEDGE_Book1_QM.md §E, Part II.
"""

from __future__ import annotations

from . import constants as K
from .geometry import level_colour, units_in_triangle, units_in_row  # re-export

# Hydrogen ground-state energy (eV).  HIS value, verified on the plates:
#   * Book 3 p.75 "Hydrogen Ionisation Energies [/n²]": K-shell (n1) ground = 13.5 eV,
#     per-level eigenstates −13.525/n² (n2 −3.381, n3 −1.503, … exactly KEM/n²).
#   * The identity is Mv² = KEM = hv²; KEM ground = 13.525 eV (constants.KEM_EV).
# 13.6 eV is the rounded "free-electron" boundary / standard Rydberg form he restates —
# kept as HYDROGEN_IONIZATION_EV_STANDARD for explicit comparison only.
HYDROGEN_GROUND_EV = K.KEM_EV                  # 13.525 eV (his)
HYDROGEN_IONIZATION_EV = HYDROGEN_GROUND_EV    # primary alias -> his value
HYDROGEN_IONIZATION_EV_STANDARD = 13.6         # ⚠ standard/observed boundary, comparison only

# Rydberg constant (1/m).  HIS Tetryonic value (Book 2 p.118, boxed): R_H = c/27.49545417
# = 10,903,346.28 /m  -> Balmer-α = 660 nm.  The accurate/observed value (→656.5 nm) is kept
# as RYDBERG_OBSERVED for comparison.
RYDBERG = K.RYDBERG_TETRYONIC                  # his geometric R_H ≈ 1.0903e7
RYDBERG_OBSERVED = 1.0967758e7                 # ⚠ accurate/empirical, reproduces observed lines

# Spin <-> rotation angle (degrees) — leptons are geometrically spin-3 (120°).
SPIN_ROTATION = {0.5: 720, 1: 360, 2: 180, 3: 120}

# Shells K,L,M,N,O,P,Q,R = n1..n8
SHELL_NAMES = ["K", "L", "M", "N", "O", "P", "Q", "R"]


def level_quanta(n: int) -> int:
    """Cumulative mass-energy quanta at level n (square geometry) = n²."""
    return units_in_triangle(n)


def level_step(n: int) -> int:
    """Quanta added going from level n−1 to n (odd) = 2n−1."""
    return units_in_row(n)


def shell_quanta(n: int) -> int:
    """Electron-shell mass-energy quanta at principal level n = 12·n²."""
    return 12 * n * n


def shell_name(n: int) -> str:
    return SHELL_NAMES[n - 1] if 1 <= n <= len(SHELL_NAMES) else f"n{n}"


def hydrogen_energy(n: int) -> float:
    """Bound-electron energy of hydrogen level n (eV):  E = −13.525/n²  (his KEM, p.75)."""
    return -HYDROGEN_GROUND_EV / (n * n)


def ionization_energy(n: int = 1) -> float:
    """Energy (eV) to free an electron from level n = +13.525/n²  (his KEM ground)."""
    return HYDROGEN_GROUND_EV / (n * n)


# British-spelling alias (the elements module uses this spelling).
ionisation_energy = ionization_energy


def rydberg_wavelength(n_low: int, n_high: int, observed: bool = False) -> float:
    """Spectral-line wavelength (m):  1/λ = R·(1/n_low² − 1/n_high²).

    Uses Kelvin's Tetryonic Rydberg by default (Balmer-α = 660 nm). Pass observed=True
    for the empirical Rydberg that reproduces the measured 656.5 nm line."""
    if n_high <= n_low:
        raise ValueError("n_high must be greater than n_low")
    r = RYDBERG_OBSERVED if observed else RYDBERG
    inv = r * (1.0 / (n_low * n_low) - 1.0 / (n_high * n_high))
    return 1.0 / inv


def spin_rotation_angle(spin: float) -> int:
    """Rotation angle (degrees) for a given spin number."""
    return SPIN_ROTATION[spin]


def colour(n: int) -> str:
    """Chromatic energy-level colour (0..9 wrap)."""
    return level_colour(n)
