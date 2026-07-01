"""
Optics & photon–matter interactions — Book 2 (Electrodynamics).

In Tetryonics, refraction is a change in the velocity (and wavelength) of EM energy in a
medium at constant frequency; the photoelectric effect and pair production are energy
thresholds in n·hv quanta. Light "bending" near mass is refraction through the stellar EM
medium, not spacetime curvature (see cosmology). Standard relations hold numerically.
"""

from __future__ import annotations

import math

from . import constants as K

# rest energy of an electron (J) — the pair-production half-threshold.
ELECTRON_REST_ENERGY = K.N_ELECTRON * K.M_Q * K.C2   # ~8.19e-14 J ~ 0.511 MeV


def refractive_index(phase_velocity: float) -> float:
    """Refractive index  n = c/v  (v = phase velocity of light in the medium)."""
    return K.C / phase_velocity


def phase_velocity(refractive_index_n: float) -> float:
    """Phase velocity in a medium  v = c/n."""
    return K.C / refractive_index_n


def snell(n1: float, theta1_rad: float, n2: float) -> float:
    """Snell's law — refraction angle θ₂ from  n₁·sin θ₁ = n₂·sin θ₂."""
    return math.asin(n1 * math.sin(theta1_rad) / n2)


def photoelectric_ke(frequency_hz: float, work_function_j: float) -> float:
    """Photoelectron kinetic energy  KE = h·f − φ  (J); 0 below the threshold."""
    ke = K.H * frequency_hz - work_function_j
    return max(0.0, ke)


def photoelectric_threshold_frequency(work_function_j: float) -> float:
    """Cutoff frequency  f₀ = φ/h  below which no electrons are emitted."""
    return work_function_j / K.H


def pair_production_threshold() -> float:
    """Minimum photon energy to create an e⁺e⁻ pair = 2·m_e·c²  (J, ≈ 1.022 MeV)."""
    return 2.0 * ELECTRON_REST_ENERGY


# --- reflection / refraction (Book 2 pp.201-202; these are the only explicit laws) -
def reflection_angle(incidence_rad: float) -> float:
    """Law of reflection — angle of reflection equals angle of incidence."""
    return incidence_rad


def wavelength_in_medium(vacuum_wavelength_m: float, refractive_index_n: float) -> float:
    """In a medium the frequency is fixed and λ scales with velocity:  λ = λ_vac / n."""
    return vacuum_wavelength_m / refractive_index_n


def amplitude_from_intensity(intensity: float) -> float:
    """EM-wave amplitude is the square root of the wavefunction intensity (p.198)."""
    return math.sqrt(intensity)


def superpose(*amplitudes: float) -> float:
    """Linear superposition of wave amplitudes  F(ψ₁+ψ₂+…) = ΣF(ψᵢ)."""
    return sum(amplitudes)


def recoil_momentum(total_energy_j: float, rest_mass_kg: float) -> float:
    """Recoil-electron momentum  p = √(E² − (m·c²)²)/c  (Compton scattering, p.111)."""
    mc2 = rest_mass_kg * K.C2
    return math.sqrt(total_energy_j**2 - mc2**2) / K.C
