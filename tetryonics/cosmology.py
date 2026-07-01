"""
Cosmology & gravitation — Book 4.

Tetryonic gravitation is **Newton's G + Special-Relativity EM fields**:
    G + SR = GR        and for light bending   4πG + 4πSR = 8πGR
Gravity is the convergent displacement of vacuum energies by Matter; the EM field around
Matter adds a divergent component ("dark energy") and a convergent component ("dark
matter"). There are no black holes — the centre of a galaxy is a GEM "pinch" singularity.

Newton's constant G is a *reduced* form of Coulomb's k (gravity = the geometric mean of
super-positioned EM mass-energies). Numerically the standard gravitational relations hold.
See ../../_KNOWLEDGE_Book1_QM.md Part I and Book 4 pp.108-176.
"""

from __future__ import annotations

import math

from . import constants as K

# Body masses (kg) and radii (m). Sun/Earth/Moon are Kelvin's worked-example values;
# planets included for completeness.
BODIES = {
    "sun":     {"mass": 1.98892e30, "radius": 6.9634e8},
    "mercury": {"mass": 3.3011e23,  "radius": 2.4397e6},
    "venus":   {"mass": 4.8675e24,  "radius": 6.0518e6},
    "earth":   {"mass": 5.9736e24,  "radius": 6.371e6},
    "moon":    {"mass": 7.3477e22,  "radius": 1.7374e6},
    "mars":    {"mass": 6.4171e23,  "radius": 3.3895e6},
    "jupiter": {"mass": 1.8982e27,  "radius": 6.9911e7},
    "saturn":  {"mass": 5.6834e26,  "radius": 5.8232e7},
    "uranus":  {"mass": 8.6810e25,  "radius": 2.5362e7},
    "neptune": {"mass": 1.02413e26, "radius": 2.4622e7},
}
LIGHT_SECOND_KM = 299_792.458   # one light-second in km


# --- Newtonian gravity (convergent G force) ----------------------------------
def gravity_force(m1: float, m2: float, r: float) -> float:
    """Newton's law of gravitation  F = G·m₁m₂/r²  (N)."""
    return K.G * m1 * m2 / (r * r)


def gravitational_acceleration(mass: float, r: float) -> float:
    """Surface/field gravitational acceleration  g = G·M/r²  (m/s²)."""
    return K.G * mass / (r * r)


def escape_velocity(mass: float, r: float) -> float:
    """Escape velocity  v = √(2GM/r)  (m/s)."""
    return math.sqrt(2.0 * K.G * mass / r)


def orbital_velocity(mass: float, r: float) -> float:
    """Circular orbital velocity  v = √(GM/r)  (m/s)."""
    return math.sqrt(K.G * mass / r)


def gravitational_potential_energy(m1: float, m2: float, r: float) -> float:
    """Gravitational PE  U = −G·m₁m₂/r  (J)."""
    return -K.G * m1 * m2 / r


def gravity_field_density(density: float) -> float:
    """Pressure-gradient gravity from mass-energy density  ∇φ = 4πG·ρ."""
    return 4.0 * math.pi * K.G * density


# --- the GEM identity (Newton + SR = GR) -------------------------------------
def gr_from_g_and_sr(newton_term: float, sr_term: float) -> float:
    """Full gravitational effect = convergent Newton + SR-EM term.

    For light bending Kelvin writes 4πG + 4πSR = 8πGR — i.e. the full GR value is the
    *sum* of the Newtonian convergent term and the Special-Relativity EM-refraction term.
    This helper just returns their sum (the two halves of GR).
    """
    return newton_term + sr_term


def vacuum_impedance() -> float:
    """Impedance of free space as Tetryonics frames it:  Z = ε₀μ₀ = 1/c²."""
    return K.EPSILON_0 * K.MU_0


def einstein_kappa() -> float:
    """Einstein's GR coupling constant  κ = 8πG/c⁴  (Gab = κ·Tab)."""
    return K.EINSTEIN_KAPPA


def em_to_gravity_ratio() -> float:
    """How much stronger the EM (Coulomb) coupling is than gravity:  k/G  (~10²⁰)."""
    return K.COULOMB_K / K.G


def cosmic_energy_budget() -> dict:
    """The mass-energy budget of the Universe (Book 4 p.218/220)."""
    return {"dark_energy": K.COSMIC_DARK_ENERGY,
            "dark_matter": K.COSMIC_DARK_MATTER,
            "baryonic": K.COSMIC_BARYONIC}


# --- orbital mechanics (Kepler) ----------------------------------------------
def kepler_period(semimajor_axis_m: float, central_mass_kg: float) -> float:
    """Orbital period from Kepler's 3rd law  T = 2π·√(a³/GM)  (s)."""
    return 2 * math.pi * math.sqrt(semimajor_axis_m**3 / (K.G * central_mass_kg))


def kepler_semimajor(period_s: float, central_mass_kg: float) -> float:
    """Semi-major axis from period:  a = (GM·T²/4π²)^(1/3)  (m)."""
    return (K.G * central_mass_kg * period_s**2 / (4 * math.pi**2)) ** (1.0 / 3.0)


# --- redshift (an EM effect in Tetryonics, not spacetime expansion) -----------
def redshift_doppler(velocity: float) -> float:
    """Relativistic Doppler redshift  z = √((1+β)/(1−β)) − 1  (β = v/c, receding)."""
    b = velocity / K.C
    return math.sqrt((1 + b) / (1 - b)) - 1.0


def redshift_energy_falloff(r: float, r0: float = 1.0) -> float:
    """Inverse-square energy diminution of radiant EM with distance:  (r0/r)²."""
    return (r0 / r) ** 2


# --- stellar energetics & the GEM pinch (Book 4 pp.135-151) ------------------
# Relative coupling strengths of the four interactions (Book 4 p.69).
FORCE_STRENGTHS = {"strong": 1e38, "electromagnetic": 1e36, "weak": 1e2, "gravity": 1.0}
# A GEM 'pinch' converts Matter to radiant energy at 100% efficiency; stellar fusion
# releases only this fraction of that total (Book 4 p.145/150).
FUSION_FRACTION = 1.0 / 3600.0


def annihilation_energy(mass_kg: float) -> float:
    """Radiant energy from a 100%-efficient Matter→energy GEM pinch  E = m·c²  (J).

    Stellar 'fusion' releases only ~1/3600 of this (see FUSION_FRACTION); the pinch
    converts the full 3D Matter topology to 2D radiant mass-energy."""
    return mass_kg * K.C2


def fusion_energy(mass_kg: float) -> float:
    """Energy a star releases by fusion ≈ FUSION_FRACTION × the full pinch energy."""
    return FUSION_FRACTION * annihilation_energy(mass_kg)


def light_deflection(mass: float, r: float) -> float:
    """Deflection of light grazing a mass  α = 4GM/(c²·r)  (radians).

    Tetryonics (Book 4 p.135): this is refraction of EM waves through the body's field, not
    spacetime curvature. Kelvin splits it into a Newtonian half (≈0.8725″) plus an equal
    field half, summing to the full ≈1.745″ at the Sun's limb — the total this returns."""
    return 4.0 * K.G * mass / (K.C2 * r)


def light_deflection_newtonian(mass: float, r: float) -> float:
    """The Newtonian half of the light deflection (≈0.8725″ at the Sun; Book 4 p.135)."""
    return 2.0 * K.G * mass / (K.C2 * r)


def gravitational_redshift(mass: float, r: float) -> float:
    """Gravitational redshift  z = 1/√(1 − 2GM/(rc²)) − 1  (an EM-field effect)."""
    return 1.0 / math.sqrt(1.0 - 2.0 * K.G * mass / (r * K.C2)) - 1.0


def gem_pinch_radius(mass: float) -> float:
    """The GEM-pinch scale  r = 2GM/c²  (the Schwarzschild radius — a pinch, not a
    black hole, in Tetryonics)."""
    return 2.0 * K.G * mass / K.C2


def force_strength(force: str) -> float:
    """Relative strength of one of the four interactions (gravity = 1)."""
    return FORCE_STRENGTHS[force]


def gravity_geometric_mean(m1: float, m2: float) -> float:
    """Kelvin's form of gravity as the convergent geometric mean of two masses √(m₁·m₂)
    (Book 4 p.77/109). The actual force is gravity_force(); this is the geometric core."""
    return math.sqrt(m1 * m2)


def mercury_precession() -> float:
    """Perihelion precession of Mercury = 43 arcsec/century (Book 4 p.171)."""
    return K.MERCURY_PRECESSION_ARCSEC_CENTURY


def pioneer_anomaly() -> float:
    """The Pioneer anomaly acceleration ≈ 8.74e-10 m/s² (Book 4 p.178)."""
    return K.PIONEER_ANOMALY


# --- stellar classification & solar-system data (Book 4 pp.139-157) ----------
# Spectral class lower mass bounds in solar masses (O hottest → M coolest).
STELLAR_CLASS_MIN_SOLAR_MASS = [
    ("O", 16.0), ("B", 2.1), ("A", 1.4), ("F", 1.04),
    ("G", 0.8), ("K", 0.45), ("M", 0.0),
]
# Sun's photospheric composition (fraction of atoms).
SOLAR_ABUNDANCE = {"H": 0.912, "He": 0.087, "O": 7.8e-4, "C": 3.3e-4, "N": 1.0e-4}
# Mean planet distance from the Sun, in light-seconds (Book 4 p.154).
PLANET_LIGHT_SECONDS = {
    "mercury": 192, "venus": 360, "earth": 499, "mars": 759, "jupiter": 2595,
    "saturn": 4759, "uranus": 9575, "neptune": 14976,
}
SUN_SURFACE_TEMPERATURE = 5772.0   # K


def stellar_class(mass_solar: float) -> str:
    """Morgan–Keenan spectral class from a star's mass (in solar masses)."""
    for cls, lo in STELLAR_CLASS_MIN_SOLAR_MASS:
        if mass_solar >= lo:
            return cls
    return "M"


def planet_distance_km(planet: str) -> float:
    """Mean Sun-distance of a planet in km (from its light-second value)."""
    return PLANET_LIGHT_SECONDS[planet.lower()] * LIGHT_SECOND_KM


# --- nuclear fission / Matter-energy release (Book 3 pp.444-447) -------------
def fission_quanta_release(parent_quanta: int, daughter_quanta: list) -> int:
    """Charge-π quanta released when a nucleus fissions = parent − Σ daughters.

    e.g. U(7728) → Ba(4704) + Kr(3024) releases the balance as radiant energy."""
    return parent_quanta - sum(daughter_quanta)


def quanta_to_energy(quanta: int) -> float:
    """Energy (J) of a number of charge-π quanta = quanta × m_q × c² = quanta × h."""
    return quanta * K.H


# --- 3D Matter ⇄ energy (E = Mc⁴ family, Book 4) -----------------------------
def matter_energy(matter_kg: float) -> float:
    """Energy of a 3D Matter topology  E = M·c⁴  (J)."""
    return matter_kg * K.C2 * K.C2


def matter_from_energy(energy_j: float) -> float:
    """3D Matter from energy  M = E/c⁴  (kg)."""
    return energy_j / (K.C2 * K.C2)


def matter_density(em_mass_density: float) -> float:
    """3D Matter density from 2D mass-energy density:  M = ρ/c⁴  (the same E=Mc⁴ relation
    applied to densities; Book 4 p.39/p.99)."""
    return em_mass_density / (K.C2 * K.C2)


# --- GEM Maxwell-analog field set (Book 4 p.15) ------------------------------
# Gravito-Electro-Magnetism: gravity written in Maxwell form, with G in the role of 1/(4πε₀).


def gem_field_equations() -> dict:
    """The four GEM (gravito-electromagnetic) field equations — gravity as a Maxwell-style
    field (Book 4 p.15).  E_g = gravito-electric (convergent) field, B_g = gravito-magnetic."""
    return {
        "gauss_gravity": "div E_g = -4*pi*G*rho",
        "no_gravimagnetic_monopole": "div B_g = 0",
        "faraday_gravity": "curl E_g = -dB_g/dt",
        "ampere_gravity": "curl B_g = -(4*pi*G/c^2)*J + (1/c^2)*dE_g/dt",
    }


def gem_gravity_field_divergence(density: float) -> float:
    """The gravito-electric field divergence  ∇·E_g = −4πGρ  (Book 4 p.15)."""
    return -4.0 * math.pi * K.G * density


# --- Galaxy rotation (Book 4 p.219) ------------------------------------------
def nett_convergent_force(grav_force: float, em_force: float) -> float:
    """The 'nett convergent force' that holds a galaxy together (Book 4 p.219) = gravity PLUS
    the EM (Lorentz) contribution.  Gravity alone is orders of magnitude too weak — what is
    attributed to 'dark matter' is really this EM force, not a missing substance."""
    return grav_force + em_force


def galaxy_rotation_velocity(enclosed_mass: float, r: float, em_force: float = 0.0,
                             orbiting_mass: float = 1.0) -> float:
    """Orbital speed of a star at radius r including the EM contribution (his p.219 model):
    centripetal balance  m·v²/r = F_grav + F_em  →  v = √(r·(F_grav+F_em)/m).  With
    em_force = 0 it reduces to the Newtonian √(GM/r) (which falls off too fast — the EM term
    is what flattens real rotation curves)."""
    f_grav = K.G * enclosed_mass * orbiting_mass / (r * r)
    return math.sqrt(r * (f_grav + em_force) / orbiting_mass)


# --- 'Dark' forces as vacuum momenta (Book 4 p.218-220) ----------------------
def dark_matter_momenta(frequency: float) -> float:
    """'Dark Matter' in Tetryonics = CONVERGENT vacuum momenta = h·f (Book 4 p.218/219) —
    a convergent KEM field, mistaken for missing mass."""
    return K.H * frequency


def dark_energy_momenta(mass: float, velocity: float) -> float:
    """'Dark Energy' = DIVERGENT vacuum momenta = 2·m·v² (Book 4 p.220) — a divergent KEM
    field (negative-pressure), mistaken for a substance."""
    return 2.0 * mass * velocity * velocity


# --- Stellar energy = Matter collapse, not fusion (Book 4 p.145-146) ----------
FUSION_VS_PINCH_RATIO = 3600   # standard 'fusion' estimate = 1/3600 of the real collapse


def stellar_collapse_energy(mass_kg: float) -> float:
    """The Sun's actual energy source (Book 4 p.145): Tetryonic Matter collapse = m·c²
    (the GEM pinch, 100% efficient) — NOT nuclear fusion.  Standard 'fusion' theory accounts
    for only 1/3600 of this (the P-P chain is 'completely erroneous')."""
    return mass_kg * K.C2


def fusion_efficiency(kind: str = "hot") -> float:
    """Energy efficiency of 'fusion' (Book 4 p.146): hot fusion = the stellar EM (GEM) pinch
    = 100%; cold fusion (e.g. Palladium) is really atomic fission ≈ 12-13%."""
    return {"hot": 1.0, "cold": 0.125}[kind.lower()]


# --- body-data accessors -----------------------------------------------------
def body_mass(name: str) -> float:
    return BODIES[name.lower()]["mass"]


def body_radius(name: str) -> float:
    return BODIES[name.lower()]["radius"]


# --- more gravitation --------------------------------------------------------
def gravitational_binding_energy(mass: float, radius: float) -> float:
    """Self-gravitational binding energy of a uniform sphere  U = 3GM²/(5R)  (J)."""
    return 3.0 * K.G * mass * mass / (5.0 * radius)


def roche_limit(primary_radius: float, primary_density: float,
                satellite_density: float) -> float:
    """Rigid Roche limit  d = R·(2·ρ_primary/ρ_satellite)^(1/3)."""
    return primary_radius * (2.0 * primary_density / satellite_density) ** (1.0 / 3.0)


def tidal_acceleration(mass: float, r: float, dr: float) -> float:
    """Tidal acceleration across a small span  a = 2GM·dr/r³."""
    return 2.0 * K.G * mass * dr / (r ** 3)


def gravitational_time_dilation(mass: float, r: float) -> float:
    """Clock-rate factor in a gravity well  √(1 − 2GM/(r·c²))."""
    return math.sqrt(1.0 - 2.0 * K.G * mass / (r * K.C2))


def poisson_newton(density: float) -> float:
    """Newtonian field equation  ∇²Φ = 4πG·ρ."""
    return 4.0 * math.pi * K.G * density


def poisson_einstein(density: float) -> float:
    """GR field equation source  8πG·ρ (the full GEM form vs 4πG Newtonian)."""
    return 8.0 * math.pi * K.G * density


def weight_force(mass: float, g: float = 9.80665) -> float:
    """Weight  w = m·g  (N)."""
    return mass * g


# --- helpers using the body table --------------------------------------------
def body_escape_velocity(name: str) -> float:
    b = BODIES[name.lower()]
    return escape_velocity(b["mass"], b["radius"])


def body_surface_gravity(name: str) -> float:
    b = BODIES[name.lower()]
    return gravitational_acceleration(b["mass"], b["radius"])
