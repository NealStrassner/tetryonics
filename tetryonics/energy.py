"""
Energy, mass, momentum & QAM — the core mechanics of Tetryonic Book 1.

Everything here flows from one quantum: a single Planck energy quantum carries energy
``h`` (joules) and mass ``m_q = h/c²`` (kg). So a system of ``N`` Planck quanta has
energy ``N·h`` and mass ``N·m_q`` — masses are just quanta counts.

The signature Tetryonic identities (see ../../_KNOWLEDGE_Book1_QM.md §D):
    mv² = E = hv²            (scalar mass-energy = Planck quanta squared)
    m = E/v²,  h = E/v²      (Newton view / Planck view of the same triangle)
    p = mv = E/v             (linear momentum)
    E = mc²  (2D EM mass) ,  E = Mc⁴  (3D Matter topology)
    2hv = hf  (so f = 2v) ,  photon E = hf = 2 bosons
"""

from __future__ import annotations

import math

from . import constants as K

PI = math.pi


# --- The Tetryonic energy equations (the nπ geometric forms) ------------------
def transverse_energy(n: float, quanta_v: float) -> float:
    """Transverse/boson energy with the equilateral factor:  E = n·π·[h·v]  (odd quanta)."""
    return n * PI * K.H * quanta_v


def scalar_energy_quantised(n: float, quanta_v: float) -> float:
    """Scalar/square energy with the equilateral factor:  E = n·π·[h·v²]  (square quanta)."""
    return n * PI * K.H * quanta_v * quanta_v


def tetryon_units(level: int) -> int:
    """Unit mass-energy triangles in a tetryon at level n = 4·n²  (the 4nπ scaling)."""
    return 4 * level * level


# --- Quanta <-> energy / mass -------------------------------------------------
def energy_from_quanta(n_planck: float) -> float:
    """Energy (J) of ``n_planck`` Planck quanta:  E = N·h."""
    return n_planck * K.H


def quanta_from_energy(energy_j: float) -> float:
    """Number of Planck quanta in an energy:  N = E/h."""
    return energy_j / K.H


def mass_from_quanta(n_planck: float) -> float:
    """Rest mass (kg) of ``n_planck`` Planck quanta:  m = N·m_q  (= N·h/c²)."""
    return n_planck * K.M_Q


def quanta_from_mass(mass_kg: float) -> float:
    return mass_kg / K.M_Q


# --- mass-ENERGY-Matter equivalence ------------------------------------------
def em_mass(energy_j: float) -> float:
    """2D ElectroMagnetic mass:  m = E / c²  (kg, planar 'energy per light-second')."""
    return energy_j / K.C2


def energy_from_em_mass(mass_kg: float) -> float:
    """E = m c²."""
    return mass_kg * K.C2


def matter(energy_j: float) -> float:
    """3D Matter topology:  M = E / c⁴  (the 4nπ tetrahedral standing-wave form)."""
    return energy_j / (K.C2 * K.C2)


def energy_from_matter(matter_kg: float) -> float:
    """E = M c⁴."""
    return matter_kg * K.C2 * K.C2


# --- momentum & kinetic energy -----------------------------------------------
def momentum(mass_kg: float, velocity: float) -> float:
    """Linear momentum  p = m v  (kg·m/s)."""
    return mass_kg * velocity


def scalar_energy(mass_kg: float, velocity: float) -> float:
    """Scalar mass-energy  E = m v²  (the mv² = hv² identity)."""
    return mass_kg * velocity * velocity


def mass_from_energy_velocity(energy_j: float, velocity: float) -> float:
    """Newton view:  m = E / v²."""
    return energy_j / (velocity * velocity)


def kinetic_energy(mass_kg: float, velocity: float) -> float:
    """⚠ Standard ½mv² form — NOT Kelvin's primary energy. In Tetryonics the scalar
    mass-energy is E = m·v² (see :func:`scalar_energy`); the ½ only appears as the
    KEM-field-in-motion energy ½·M·v² (M = E/c⁴). Kept for classical comparison only."""
    return 0.5 * mass_kg * velocity * velocity


# --- bosons, photons, frequency ----------------------------------------------
def boson_energy(quanta_v: float) -> float:
    """Transverse boson energy  E = h·v  (v = transverse quanta count)."""
    return K.H * quanta_v


def photon_energy(frequency_hz: float) -> float:
    """Photon energy  E = h·f."""
    return K.H * frequency_hz


def frequency_from_energy(energy_j: float) -> float:
    """Inverse of photon_energy:  f = E/h."""
    return energy_j / K.H


def boson_quanta_from_energy(energy_j: float) -> float:
    """Inverse of boson_energy:  v = E/h."""
    return energy_j / K.H


def frequency_from_quanta(quanta_v: float) -> float:
    """Einstein frequency from Planck quanta:  f = 2v   (since 2hv = hf)."""
    return 2.0 * quanta_v


def quanta_from_frequency(frequency_hz: float) -> float:
    """Planck quanta from frequency:  v = f/2."""
    return frequency_hz / 2.0


# --- relativity (Lorentz) -----------------------------------------------------
def beta(velocity: float) -> float:
    """β = v/c."""
    return velocity / K.C


def gamma(velocity: float) -> float:
    """Lorentz factor γ = 1/√(1 − β²)."""
    b = beta(velocity)
    return 1.0 / math.sqrt(1.0 - b * b)


def time_dilation(proper_time: float, velocity: float) -> float:
    """Moving-frame time  t' = t/√(1 − v²/c²) = γ·t  (Book 2 p.209)."""
    return proper_time * gamma(velocity)


def length_contraction(rest_length: float, velocity: float) -> float:
    """Contracted length  L = L₀·√(1 − v²/c²) = L₀/γ."""
    return rest_length / gamma(velocity)


def relativistic_energy(momentum: float, rest_mass: float) -> float:
    """Total energy  E = √((p·c)² + (m₀·c²)²)  (the energy–momentum relation)."""
    pc = momentum * K.C
    mc2 = rest_mass * K.C2
    return math.sqrt(pc * pc + mc2 * mc2)


# --- wave/particle wavelengths -----------------------------------------------
def de_broglie_wavelength(momentum_kg_m_s: float) -> float:
    """λ = h / p."""
    return K.H / momentum_kg_m_s


def momentum_from_de_broglie(wavelength_m: float) -> float:
    """Inverse of de_broglie_wavelength:  p = h/λ."""
    return K.H / wavelength_m


def compton_wavelength(mass_kg: float) -> float:
    """λ_c = h / (m c)."""
    return K.H / (mass_kg * K.C)


def mass_from_compton(wavelength_m: float) -> float:
    """Inverse of compton_wavelength:  m = h/(λ·c)."""
    return K.H / (wavelength_m * K.C)


def velocity_from_beta(beta_value: float) -> float:
    """Inverse of beta():  v = β·c."""
    return beta_value * K.C


def matter_from_em_mass(em_mass_kg: float) -> float:
    """2D EM-mass → 3D Matter bridge:  M = m/c²."""
    return em_mass_kg / K.C2


def em_mass_from_matter(matter_kg: float) -> float:
    """3D Matter → 2D EM-mass bridge:  m = M·c²."""
    return matter_kg * K.C2


# --- QAM ----------------------------------------------------------------------
def qam() -> float:
    """Quantised Angular Momentum Ω (m²/s) — the hidden geometric constant."""
    return K.OMEGA
