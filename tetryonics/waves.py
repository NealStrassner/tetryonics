"""
EM waves & photons — Book 2 (Electrodynamics).

Tetryonics keeps Planck's quanta ``v`` distinct from Einstein's frequency ``f``:
a photon = 2 bosons, so ``n·hv = E = hf`` and ``f = 2v``. EM waveforms are built from
ODD-π bosons (transverse) and EVEN-π photons (longitudinal); photon phase relationships
follow Euler's formula (each photon 90° out of phase with its neighbour).

    wavelength   λ = c/f
    wavenumber   k = 1/λ
    photon E     E = h·f = h·c/λ
    inverse-square law  I ∝ 1/r²
    Euler        e^{iθ} = cos θ + i·sin θ   (phase of the EM waveform)

See ../../_KNOWLEDGE_Book1_QM.md §D and Book 2 TOC pp.66–106.
"""

from __future__ import annotations

import cmath
import math

from . import constants as K


# --- wave geometry ------------------------------------------------------------
def wavelength(frequency_hz: float) -> float:
    """λ = c/f (m)."""
    return K.C / frequency_hz


def frequency(wavelength_m: float) -> float:
    """f = c/λ (Hz)."""
    return K.C / wavelength_m


def wavenumber(wavelength_m: float) -> float:
    """k = 1/λ (1/m)."""
    return 1.0 / wavelength_m


def angular_frequency(frequency_hz: float) -> float:
    """ω = 2πf."""
    return 2 * math.pi * frequency_hz


def wavelength_from_wavenumber(wavenumber: float) -> float:
    """λ = 1/k."""
    return 1.0 / wavenumber


def frequency_from_wavenumber(wavenumber: float) -> float:
    """f = c·k."""
    return K.C * wavenumber


def energy_from_wavenumber(wavenumber: float) -> float:
    """Photon energy from wavenumber  E = h·c·k."""
    return K.H * K.C * wavenumber


def wavenumber_from_energy(energy_j: float) -> float:
    """k = E/(h·c)."""
    return energy_j / (K.H * K.C)


def wavelength_from_energy(energy_j: float) -> float:
    """λ = h·c/E."""
    return K.H * K.C / energy_j


def frequency_from_energy(energy_j: float) -> float:
    """f = E/h."""
    return energy_j / K.H


# --- photon energy & momentum -------------------------------------------------
def photon_energy_from_frequency(frequency_hz: float) -> float:
    """E = h·f."""
    return K.H * frequency_hz


def photon_energy_from_wavelength(wavelength_m: float) -> float:
    """E = h·c/λ."""
    return K.H * K.C / wavelength_m


def photon_momentum(wavelength_m: float) -> float:
    """p = h/λ."""
    return K.H / wavelength_m


def boson_photon_energy(n: float, quanta_v: float) -> float:
    """EM-wave energy from n bosons:  E = n·h·v  (= h·f with f = 2v)."""
    return n * K.H * quanta_v


# --- propagation / phase ------------------------------------------------------
def inverse_square(intensity0: float, r: float) -> float:
    """Intensity at distance r under the inverse-square law:  I = I₀/r²."""
    return intensity0 / (r * r)


def euler_phase(theta_rad: float) -> complex:
    """e^{iθ} = cos θ + i sin θ — the phasor of an EM waveform component."""
    return cmath.exp(1j * theta_rad)


def photon_phase_offset(index: int) -> float:
    """Phase (radians) of the n-th photon in a wave — 90° apart from neighbours."""
    return index * math.pi / 2.0


# --- Compton scattering -------------------------------------------------------
def compton_frequency(mass_kg: float) -> float:
    """Compton frequency of a mass  f = m·c²/h  (Book 2 p.111)."""
    return mass_kg * K.C2 / K.H


def vacuum_energy_wavelength(base_wavelength_m: float, n: int) -> float:
    """Vacuum-energy wavelength ladder  λ_n = λ/(2·n²)  (Book 4 p.217)."""
    return base_wavelength_m / (2 * n * n)


def compton_shift(theta_rad: float, mass_kg: float = None) -> float:
    """Compton wavelength shift  Δλ = (h/mc)(1 − cos θ).

    Defaults to the electron mass (the usual Compton wavelength).
    """
    if mass_kg is None:
        mass_kg = K.N_ELECTRON * K.M_Q
    return (K.H / (mass_kg * K.C)) * (1 - math.cos(theta_rad))
