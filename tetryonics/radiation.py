"""
Blackbody / thermal radiation — Book 2 (Electrodynamics) p.176.

In Tetryonics a blackbody spectrum is a distribution of n·hv Planck quanta across the
equilateral energy levels (per-level counts 1,4,9,…=n²). The classical laws — Planck's
radiation law, Wien's displacement, Stefan–Boltzmann — emerge from that distribution.
These use Boltzmann's constant (a statistical, not Tetryonic-geometric, quantity).
"""

from __future__ import annotations

import math

from . import constants as K

# Boltzmann constant (statistical mechanics; not a Tetryonic geometric constant).
K_B = 1.380649e-23          # J/K
# Wien displacement constant and Stefan-Boltzmann constant (derived).
WIEN_B = 2.897771955e-3     # m·K
STEFAN_BOLTZMANN = 5.670374419e-8   # W m^-2 K^-4


def planck_spectral_radiance(wavelength_m: float, temperature_k: float) -> float:
    """Planck's law — spectral radiance B(λ,T) (W·sr⁻¹·m⁻³).

    B = (2hc²/λ⁵) · 1/(exp(hc/λk_BT) − 1).  Uses the Tetryonics h.
    """
    h, c = K.H, K.C
    a = 2.0 * h * c * c / wavelength_m**5
    x = h * c / (wavelength_m * K_B * temperature_k)
    return a / (math.expm1(x))


def wien_peak_wavelength(temperature_k: float) -> float:
    """Wien's displacement law — peak wavelength  λ_max = b/T (m)."""
    return WIEN_B / temperature_k


def stefan_boltzmann_power(temperature_k: float, area_m2: float = 1.0,
                           emissivity: float = 1.0) -> float:
    """Total radiated power  P = εσA·T⁴ (W)."""
    return emissivity * STEFAN_BOLTZMANN * area_m2 * temperature_k**4


def photon_quanta_at_level(n: int) -> int:
    """Per-level Planck-quanta count in the equilateral distribution = n²."""
    return n * n


def stellar_luminosity(radius_m: float, temperature_k: float,
                       emissivity: float = 1.0) -> float:
    """Luminosity of a star (blackbody sphere)  L = 4π·R²·εσ·T⁴  (W)."""
    return stefan_boltzmann_power(temperature_k, 4 * math.pi * radius_m**2, emissivity)


def wien_peak_frequency(temperature_k: float) -> float:
    """Wien's law (frequency form)  f_max = 2.821439·k_B·T/h  (Hz)."""
    return 2.821439372 * K_B * temperature_k / K.H


def photon_flux(power_w: float, frequency_hz: float) -> float:
    """Photons per second from a beam  N = P/(h·f)."""
    return power_w / (K.H * frequency_hz)


def photon_intensity(power_w: float, area_m2: float) -> float:
    """Irradiance  I = P/A  (W/m²)."""
    return power_w / area_m2


def rayleigh_jeans(wavelength_m: float, temperature_k: float) -> float:
    """Classical Rayleigh–Jeans spectral radiance  B = 2c·k_B·T/λ⁴ (the UV-catastrophe form)."""
    return 2.0 * K.C * K_B * temperature_k / wavelength_m**4
