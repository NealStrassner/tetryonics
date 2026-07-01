"""
ElectroMagnetic fields & forces.

The EM constants are interdependent geometric properties of energy, not separate facts:
    c = 1/√(ε₀μ₀) ,   ε₀ = 1/(μ₀c²) ,   μ₀ = 1/(ε₀c²) ,   ε₀μ₀ = 1/c²

Field falloff in Tetryonics: Electric ∝ 1/r²  (monopole source),
Magnetic dipole ∝ 1/r³ (Biot–Savart). See ../../_KNOWLEDGE_Book1_QM.md Part I §C, §B.
"""

from __future__ import annotations

import math

from . import constants as K

PI = math.pi


# --- the interdependence of the EM constants ---------------------------------
def speed_of_light_from_constants() -> float:
    """c = 1/√(ε₀μ₀)."""
    return 1.0 / math.sqrt(K.EPSILON_0 * K.MU_0)


def epsilon0_from(mu0: float = K.MU_0, c: float = K.C) -> float:
    return 1.0 / (mu0 * c * c)


def mu0_from(eps0: float = K.EPSILON_0, c: float = K.C) -> float:
    return 1.0 / (eps0 * c * c)


# --- electrostatics (Coulomb / Gauss) ----------------------------------------
def coulomb_force(q1: float, q2: float, r: float) -> float:
    """Coulomb force  F = k·q₁q₂/r²  (N). Positive = repulsive (like charges)."""
    return K.COULOMB_K * q1 * q2 / (r * r)


def electric_field(q: float, r: float) -> float:
    """Radial E-field of a point charge  E = (1/4πε₀)·q/r²  (V/m)."""
    return q / (4 * PI * K.EPSILON_0 * r * r)


# --- magnetism ----------------------------------------------------------------
def biot_savart_point(current_a: float, length_m: float, r: float) -> float:
    """Magnitude of B from a current element (perpendicular):
    B = (μ₀/4π)·I·dl/r²  (T). Dipole fields fall as 1/r³."""
    return K.MU_0 * current_a * length_m / (4 * PI * r * r)


def magnetic_field_from_H(h_field: float) -> float:
    """B = μ₀·H."""
    return K.MU_0 * h_field


def ampere_force_per_length(i1: float, i2: float, d: float) -> float:
    """Force per length between two parallel wires  F/L = μ₀·I₁I₂/(2π·d)  (N/m)."""
    return K.MU_0 * i1 * i2 / (2 * PI * d)


# --- Lorentz force ------------------------------------------------------------
def lorentz_force(q: float, e_field: float = 0.0,
                  velocity: float = 0.0, b_field: float = 0.0) -> float:
    """Scalar Lorentz force  F = q(E + vB)  (perpendicular v,B)."""
    return q * (e_field + velocity * b_field)


# --- falloff helpers ----------------------------------------------------------
def electric_falloff(r: float) -> float:
    """Relative electric field strength ∝ 1/r²."""
    return 1.0 / (r * r)


def magnetic_dipole_falloff(r: float) -> float:
    """Relative magnetic dipole strength ∝ 1/r³."""
    return 1.0 / (r * r * r)


# --- Gauss / Poynting (Book 2 pp.8-22) ---------------------------------------
def gauss_flux(charge_c: float) -> float:
    """Total electric flux out of a closed surface  Φ = q/ε₀  (Gauss' law)."""
    return charge_c / K.EPSILON_0


def poynting(e_field: float, h_field: float) -> float:
    """Poynting energy-flux magnitude  S = E × H  (W/m²)."""
    return e_field * h_field


def coulomb_constant() -> float:
    """Coulomb constant  k = 1/(4πε₀)."""
    return 1.0 / (4 * PI * K.EPSILON_0)


# --- Fine-structure constant (the 'Hand of GOD', Book 2 pp.220-223) ----------
def fine_structure_constant(tetryonic: bool = True) -> float:
    """The fine-structure (EM coupling) constant.

    Tetryonics derives it geometrically as α = 2π·Ω ≈ 0.007539822 (inverse ≈ 132.63),
    sourced from Book 2 pp.220-223. Pass ``tetryonic=False`` for the empirical CODATA
    value (≈ 1/137.036).
    """
    return K.FINE_STRUCTURE if tetryonic else K.FINE_STRUCTURE_CODATA


# --- Magnetism: magnetons & charge-mass ratios (Book 1 pp.234-244) -----------
def bohr_magneton() -> float:
    """Bohr magneton  μ_B = e·ħ/(2·m_e)  (J/T)."""
    return K.BOHR_MAGNETON


def nuclear_magneton() -> float:
    """Nuclear magneton  μ_N = μ_B / 1875  (proton/electron mass ratio)."""
    return K.NUCLEAR_MAGNETON


def charge_mass_ratio(particle: str = "electron") -> float:
    """Charge-to-mass ratio q/m (C/kg). Electron ≈ 1.81e11, proton ≈ 9.65e7."""
    return K.CHARGE_MASS_RATIO_E if particle == "electron" else K.CHARGE_MASS_RATIO_P


def ampere_constant() -> float:
    """Ampère force constant  k_A = μ₀/(2π) = 2×10⁻⁷ N/A²."""
    return K.AMPERE_CONSTANT


def impedance_of_free_space() -> float:
    """Characteristic impedance of the vacuum  Z₀ = √(μ₀/ε₀) = μ₀·c ≈ 376.7 Ω."""
    return K.IMPEDANCE_FREE_SPACE


def magnetic_force_per_length(current_a: float, r: float) -> float:
    """Magnetic force per length of a single current  F = μ₀·I²/(2π·r)  (N/m)."""
    return K.MU_0 * current_a * current_a / (2 * PI * r)


def longitudinal_velocity() -> float:
    """Tetryonic longitudinal EM-energy velocity = (π/2)·c (Book 2 p.96)."""
    return K.LONGITUDINAL_VELOCITY
