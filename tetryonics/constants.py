"""
Tetryonic physical constants.

All values are the *Tetryonics* figures as published by Kelvin Abraham (which differ
slightly from CODATA in places). They are internally self-consistent — the whole point
of the system is that they derive from one geometric quantum, not from measurement
fitting. See ../../_KNOWLEDGE_Book1_QM.md (Part II §E, Part III) for sources.

Key derivations (verified in tests/):
    m_q  = h / c**2                         (mass of one Planck energy quantum)
    q_q  = OMEGA / c**2                     (charge quantum = 1/12 of elementary charge)
    e    = 12 * q_q                         (elementary charge -> electron has 12 fascia)
"""

from __future__ import annotations

# --- The pivot constant -----------------------------------------------------
# Planck's constant (quantum of action AND quantum source of inertial mass).
H = 6.629432672e-34            # J*s   (Tetryonics value; CODATA ~6.62607015e-34)
H_EV = 4.137664546e-15         # eV*s  (= H/e; Kelvin's "exact value of Planck's constant" paper, title page)

# --- Light --------------------------------------------------------------------
# c = 299792458 m/s (the exact SI value). Verified: only this value makes
# m_q = h/c^2 and q = Omega/c^2 match Kelvin's published digits exactly.
C = 299_792_458.0              # m/s
C2 = C * C                     # m^2/s^2  = 8.987551787e16

# --- The quantum of mass-energy ----------------------------------------------
# One Planck energy quantum has this much mass-equivalent.  m_q = h / c^2.
M_Q = H / C2                   # kg    = 7.376238634e-51  (matches Kelvin exactly)

# --- Quantised Angular Momentum (QAM) ----------------------------------------
# The "hidden" geometric constant Omega.  Abraham's own figure (ABRAHAM.txt):
# Omega/c^2 = 1.335180e-20 = the charge quantum = 1/12 of the elementary charge.
OMEGA = 0.0012                 # m^2/s  (QAM)

# --- Charge -------------------------------------------------------------------
CHARGE_QUANTUM = OMEGA / C2    # C (kg*s)  = 1.335180067e-20  (one fascia's charge)
ELEMENTARY_CHARGE = 12 * CHARGE_QUANTUM   # C  = 1.602216e-19  (12 fascia = 1 e)

# --- EM field constants -------------------------------------------------------
EPSILON_0 = 8.85418785e-12     # F/m   electric constant   = 1/(mu0*c^2)
MU_0 = 1.25663706e-6           # H/m   magnetic constant    = 1/(eps0*c^2) = 4*pi*1e-7
EPS_MU = EPSILON_0 * MU_0      # s^2/m^2  ~ 1.112650056e-17 = 1/c^2
COULOMB_K = 1.0 / (4 * 3.141592653589793 * EPSILON_0)   # N*m^2/C^2 ~ 8.987e9

# --- Fine-structure constant (Tetryonics geometric value) --------------------
# Kelvin derives alpha as the geometry of QAM:  alpha = 2*pi*Omega.
# NOTE: this is his geometric figure (0.00754, inverse ~132.6), which differs from
# the empirical CODATA alpha = 1/137.036.  Kept distinct on purpose.
import math as _math
FINE_STRUCTURE = 2 * _math.pi * OMEGA      # ~0.007539822
FINE_STRUCTURE_INV = 1.0 / FINE_STRUCTURE  # ~132.629
FINE_STRUCTURE_CODATA = 7.2973525693e-3    # the empirical value, for comparison

# --- Bulk-matter references ---------------------------------------------------
AVOGADRO = 6.022141579e23      # 1/mol (Tetryonics value)

# --- Newtonian gravitation ----------------------------------------------------
G = 6.67384e-11                # m^3 kg^-1 s^-2  (Newton's constant, Kelvin's Book-4 value)
EINSTEIN_KAPPA = 8 * _math.pi * G / (C2 * C2)   # GR coupling  kappa = 8piG/c^4

# --- More EM / electrical constants (Books 2 & 4) ----------------------------
TAU = 2 * _math.pi                                  # full turn (360°) — photons = 2π
AMPERE_CONSTANT = MU_0 / (2 * _math.pi)             # = 2e-7 N/A²  (Ampère force constant)
IMPEDANCE_FREE_SPACE = (MU_0 / EPSILON_0) ** 0.5    # Z0 ~ 376.73 Ω  (= μ0·c)
ELECTRONS_PER_COULOMB = 1.0 / ELEMENTARY_CHARGE     # ~6.24e18 electrons per C
EV_KJ_PER_MOLE = ELEMENTARY_CHARGE * AVOGADRO / 1000.0   # 1 eV/particle in kJ/mol
# Tetryonic claim: longitudinal EM energy propagates at (π/2)·c (Book 2 p.96, Wheatstone).
LONGITUDINAL_VELOCITY = (_math.pi / 2) * C          # ~4.709e8 m/s
# Thermodynamics
BOLTZMANN = 1.380649e-23       # J/K
GAS_CONSTANT = 8.314462618     # J/(mol·K)
# Cosmology anomalies (Book 4)
MERCURY_PRECESSION_ARCSEC_CENTURY = 43.0
PIONEER_ANOMALY = 8.74e-10     # m/s²
# Tetryonic Rydberg divisor: per-series divisor = 27.49545417 · n_low²  (Book 2 p.128)
RYDBERG_DIVISOR = 27.49545417

# --- Geometry / golden ratio / named constants (Book 5) ----------------------
PHI = (1 + 5 ** 0.5) / 2       # golden ratio ~1.6180339887
E_EULER = _math.e              # Euler's number ~2.718281828
ZETA2 = _math.pi ** 2 / 6      # Basel sum Σ1/n² = π²/6 ~1.644934
KEPLER_BOUWKAMP = 0.1149420448 # nested-polygon inradius limit Π cos(π/n)
APOLLO_CONSTANT = 873825       # light:sound speed ratio (Book 5 p.130 prints "873,825"; was 873.825, a decimal-point typo)

# --- Particle rest energies in eV (Book 3 p.90) ------------------------------
BARYON_MEV = 930.947           # proton/neutron rest mass-energy (MeV)
ELECTRON_KEV = 496.519         # electron rest mass-energy (keV, Tetryonic)
KEM_EV = 13.525                # hydrogen KEM-field ground energy (eV)

# --- Chemistry / cosmology references ----------------------------------------
MAX_Z = 120                    # Tetryonic max periodic element (Book 3 p.27/69)
# Periodic per-shell electron caps (capped/mirrored, sum = 120) — Book 3 p.27/69.
PERIODIC_SHELL_CAPS = (2, 8, 18, 32, 32, 18, 8, 2)
# Cosmic mass-energy budget (Book 4 p.218/220).
COSMIC_DARK_ENERGY = 0.68
COSMIC_DARK_MATTER = 0.27
COSMIC_BARYONIC = 0.05

# --- Rydberg (Book 2 p.118/123/129) ------------------------------------------
# Kelvin's OWN geometric Rydberg R_H = c / 27.49545417 = 10,903,346.28 /m (Book 2 p.118,
# boxed) -> Balmer-α = 660 nm. This is the primary value used by levels/spectra.
RYDBERG_TETRYONIC = C / 27.49545417   # 1/m  = 10,903,346.28  (his)
# Accurate/empirical Rydberg (reproduces the *observed* lines, ~0.6% higher) — comparison ONLY.
# Named explicitly so a stray `from constants import RYDBERG` can't silently grab the observed
# value; the his-method default everywhere is RYDBERG_TETRYONIC (c/27.49545417 → Balmer-α 660 nm).
RYDBERG_OBSERVED = 1.0967758e7          # 1/m  (observed/CODATA, ~0.6% higher than his)

# --- Verified particle Planck-quanta numbers (rest mass-energy quanta) --------
# mass = N_planck * M_Q.  These reproduce the real particle masses (see tests).
# Sourced from Book 1 plates (electron 1.2e20; proton 2.25e23).
N_ELECTRON = 1.2e20            # -> 8.851486e-31 kg  (electron / positron)
N_PROTON = 2.25e23            # -> 1.659654e-27 kg  (proton)
N_NEUTRON = 2.25e23            # Tetryonics: proton & neutron have identical mass-Matter
N_HYDROGEN = N_PROTON + N_ELECTRON   # 2.2512e23 -> 1 amu

# Proton/electron mass ratio falls straight out: N_PROTON / N_ELECTRON = 1875.
PROTON_ELECTRON_RATIO = N_PROTON / N_ELECTRON

# --- Magnetism (Book 1 pp.234-244) — needs the particle quanta above ---------
H_BAR = H / (2 * _math.pi)                                          # reduced Planck constant
BOHR_MAGNETON = ELEMENTARY_CHARGE * H_BAR / (2 * N_ELECTRON * M_Q)  # J/T
NUCLEAR_MAGNETON = BOHR_MAGNETON / PROTON_ELECTRON_RATIO            # = mu_B / 1875
CHARGE_MASS_RATIO_E = ELEMENTARY_CHARGE / (N_ELECTRON * M_Q)        # ~1.81e11 C/kg
CHARGE_MASS_RATIO_P = ELEMENTARY_CHARGE / (N_PROTON * M_Q)          # ~9.65e7 C/kg


# --- MeV / amu conversions (for the nuclear energy-level mass model, Book 3) ---
MEV_J = 1.0e6 * ELEMENTARY_CHARGE        # 1 MeV in Joules  (Tetryonic e)
AMU_KG = N_HYDROGEN * M_Q                # 1 atomic mass unit in kg (Tetryonic: = hydrogen)
MEV_PER_AMU = BARYON_MEV + ELECTRON_KEV / 1000.0   # 931.443519 = Kelvin's printed Hydrogen rest-energy
                                                   # (proton 930.947 + electron 0.496519). Built from the SAME
                                                   # printed numbers as the element MeV totals, so per-element
                                                   # amu masses match his Book-3 pages exactly (H=1.0000, etc.).


def mass_from_quanta(n_planck: float) -> float:
    """Rest mass (kg) of a topology holding ``n_planck`` Planck energy quanta."""
    return n_planck * M_Q


def mass_from_mev(mev: float) -> float:
    """Rest mass (kg) equivalent of a mass-energy given in MeV  (m = E/c²)."""
    return mev * MEV_J / C2


def amu_from_mev(mev: float) -> float:
    """Convert a mass-energy in MeV to atomic mass units (Tetryonic, hydrogen = 1)."""
    return mev / MEV_PER_AMU


def summary() -> str:
    """One-screen dump of the constant set (handy for sanity checks)."""
    lines = [
        "Tetryonics constants",
        "--------------------",
        f"h              = {H:.10e} J*s",
        f"c              = {C:.0f} m/s",
        f"c^2            = {C2:.9e} m^2/s^2",
        f"m_q = h/c^2    = {M_Q:.9e} kg",
        f"Omega (QAM)    = {OMEGA} m^2/s",
        f"charge quantum = {CHARGE_QUANTUM:.9e} C  (= Omega/c^2)",
        f"e = 12*q_q     = {ELEMENTARY_CHARGE:.9e} C",
        f"Mp/Me ratio    = {PROTON_ELECTRON_RATIO:g}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
