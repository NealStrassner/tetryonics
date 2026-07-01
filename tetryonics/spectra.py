"""
Atomic spectra — the named hydrogen spectral series (Book 2, pp.117–167).

Each series is the set of photon emissions/absorptions for electron transitions down to
(or up from) a fixed lower level n_low, via Rydberg's formula. Tetryonics names a 7th
series after the author:

    Lyman = 1, Balmer = 2, Paschen = 3, Brackett = 4, Pfund = 5, Humphreys = 6, Abraham = 7

The per-transition quanta differential is 12·(2n−1) (the odd-number level steps), and the
cumulative shell quanta is 12·n² (see levels.shell_quanta). 1/λ = R·(1/n_low² − 1/n_high²).
"""

from __future__ import annotations

from .levels import rydberg_wavelength, hydrogen_energy

SERIES = {
    "lyman": 1,
    "balmer": 2,
    "paschen": 3,
    "brackett": 4,
    "pfund": 5,
    "humphreys": 6,
    "abraham": 7,   # Kelvin Abraham's own named series
}


def series_lower_level(series: str) -> int:
    return SERIES[series.lower()]


def line_wavelength(series: str, n_high: int) -> float:
    """Wavelength (m) of the transition n_high → series lower level."""
    n_low = series_lower_level(series)
    if n_high <= n_low:
        raise ValueError("n_high must be above the series lower level")
    return rydberg_wavelength(n_low, n_high)


def line_energy_ev(series: str, n_high: int) -> float:
    """Photon energy (eV) of the transition = |E(n_low) − E(n_high)|."""
    n_low = series_lower_level(series)
    return abs(hydrogen_energy(n_high) - hydrogen_energy(n_low))


def quanta_differential(n: int) -> int:
    """Mass-energy quanta of the n-th level step = 12·(2n−1)."""
    return 12 * (2 * n - 1)


def rydberg_factor(n_low: int, n_high: int) -> float:
    """The Rydberg/KEM fraction  (1/n_low² − 1/n_high²) for a transition."""
    return 1.0 / (n_low * n_low) - 1.0 / (n_high * n_high)


def series_rydberg_divisor(series: str) -> float:
    """Tetryonic per-series Rydberg divisor = 27.49545417 · n_low²  (Book 2 p.128).

    R_series = c / divisor. Lyman 27.50, Balmer 110.0, Paschen 247.5 …
    """
    from . import constants as K
    return K.RYDBERG_DIVISOR * series_lower_level(series) ** 2


def series_shell_quanta(series: str) -> int:
    """Mass-energy quanta of a series' lower shell = 12·n_low²  (Book 2 p.119)."""
    return 12 * series_lower_level(series) ** 2


def series_lines(series: str, count: int = 4) -> list[dict]:
    """First ``count`` lines of a series, as dicts of (n_high, wavelength_nm, energy_eV)."""
    n_low = series_lower_level(series)
    out = []
    for n_high in range(n_low + 1, n_low + 1 + count):
        out.append({
            "transition": f"n{n_high}->n{n_low}",
            "wavelength_nm": line_wavelength(series, n_high) * 1e9,
            "energy_ev": line_energy_ev(series, n_high),
        })
    return out


def all_series() -> list[str]:
    return list(SERIES.keys())
