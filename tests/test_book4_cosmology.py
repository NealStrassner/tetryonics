"""
Book 4 — Cosmology (stellar classes, planetary data, GEM gravity, gravitation,
E=Mc⁴ pinch/fusion, stellar energetics, light deflection, redshift, fission).
Run:  python tests/test_book4_cosmology.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tetryonics as t
from tetryonics import (constants as K, cosmology as cos, radiation, elements as el,
                        thermodynamics as thermo)


def close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel)


# ===== from test_mining.py (Book 4 subset) ===================================

# --- cosmology data ----------------------------------------------------------
def test_stellar_class():
    assert cos.stellar_class(20) == "O"
    assert cos.stellar_class(1.0) == "G"     # Sun-like
    assert cos.stellar_class(0.2) == "M"


def test_planet_distance_and_geometric_gravity():
    # Earth ~ 499 light-seconds ~ 1.496e8 km
    assert close(cos.planet_distance_km("earth"), 499 * cos.LIGHT_SECOND_KM)
    assert close(cos.gravity_geometric_mean(4, 9), 6.0)
    assert cos.mercury_precession() == 43.0
    assert cos.pioneer_anomaly() > 0


# --- thermodynamics ----------------------------------------------------------
def test_thermodynamics():
    assert close(thermo.entropy_boltzmann(math.e), K.BOLTZMANN)   # ln(e)=1
    assert close(thermo.entropy_clausius(100, 50), 2.0)
    assert close(thermo.ideal_gas_pressure(1, 273.15, 0.0224136), 101325, rel=1e-2)
    assert close(thermo.thermal_energy(300), K.BOLTZMANN * 300)
    assert thermo.bekenstein_hawking_entropy(1.0) > 0


# ===== from test_mining2.py (Book 4 subset) ==================================

def test_fission_release():
    # U(7728) -> Ba(4704) + Kr(3024) balances exactly (a clean split)
    u = el.element(92).topology_pi
    ba, kr = el.element(56).topology_pi, el.element(36).topology_pi
    assert cos.fission_quanta_release(u, [ba, kr]) == u - ba - kr
    assert cos.quanta_to_energy(1000) == 1000 * K.H


# ===== from test_books345.py (Book 4 subset) =================================

# --- cosmology (Book 4) ------------------------------------------------------
def test_earth_surface_gravity():
    assert close(cos.body_surface_gravity("earth"), 9.82, rel=2e-2)


def test_earth_escape_velocity():
    # ~11.2 km/s
    assert close(cos.body_escape_velocity("earth"), 11186, rel=1e-2)


def test_orbital_lt_escape():
    m, r = cos.BODIES["earth"]["mass"], cos.BODIES["earth"]["radius"]
    assert cos.orbital_velocity(m, r) < cos.escape_velocity(m, r)


def test_gem_field_and_galaxy_rotation():
    # GEM gravity field divergence = -4πGρ (Book 4 p.15).
    assert close(cos.gem_gravity_field_divergence(1.0), -4 * math.pi * K.G)
    assert "div E_g" in cos.gem_field_equations()["gauss_gravity"]
    # Galaxy rotation (p.219): the EM term raises v above the Newtonian sqrt(GM/r).
    v_newton = cos.galaxy_rotation_velocity(1e41, 3e20)
    v_em = cos.galaxy_rotation_velocity(1e41, 3e20, em_force=1e-9)
    assert v_em > v_newton
    assert close(v_newton, math.sqrt(K.G * 1e41 / 3e20))     # reduces to Newton when em=0


def test_stellar_collapse_and_dark_forces():
    # Sun's energy = Matter collapse m·c² (Book 4 p.145), NOT fusion (which is 1/3600 of it).
    assert close(cos.stellar_collapse_energy(1.0), K.C2)
    assert cos.FUSION_VS_PINCH_RATIO == 3600
    assert cos.fusion_efficiency("hot") == 1.0 and cos.fusion_efficiency("cold") == 0.125
    # 'Dark' forces as vacuum momenta: matter = h·f (convergent), energy = 2mv² (divergent).
    assert close(cos.dark_matter_momenta(1e15), K.H * 1e15)
    assert close(cos.dark_energy_momenta(1.0, 100.0), 2 * 100.0 ** 2)


def test_all_planets_present():
    for p in ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]:
        assert cos.body_mass(p) > 0 and cos.body_radius(p) > 0


def test_gem_identity():
    # 4piG + 4piSR = 8piGR  -> the two halves sum to the whole
    assert close(cos.gr_from_g_and_sr(4.0, 4.0), 8.0)


def test_vacuum_impedance_is_inverse_c2():
    assert close(cos.vacuum_impedance(), 1.0 / K.C2, rel=1e-3)


# ===== from test_coverage2.py (Book 4 subset) ================================

# --- Book 4 stellar / GEM ----------------------------------------------------
def test_stellar_luminosity_sun():
    # Sun: R=6.96e8 m, T=5772 K -> L ~ 3.8e26 W
    L = radiation.stellar_luminosity(6.9634e8, 5772)
    assert close(L, 3.83e26, rel=3e-2)


def test_light_deflection_sun_is_1_75_arcsec():
    M, R = cos.BODIES["sun"]["mass"], cos.BODIES["sun"]["radius"]
    arcsec = math.degrees(cos.light_deflection(M, R)) * 3600
    assert close(arcsec, 1.75, rel=2e-2)


def test_pinch_vs_fusion():
    e_pinch = cos.annihilation_energy(1.0)
    assert close(e_pinch, K.C2)
    assert close(cos.fusion_energy(1.0), e_pinch / 3600)


def test_gravitational_redshift_and_pinch_radius():
    M, R = cos.BODIES["sun"]["mass"], cos.BODIES["sun"]["radius"]
    assert cos.gravitational_redshift(M, R) > 0
    assert close(cos.gem_pinch_radius(M), 2 * K.G * M / K.C2)   # ~2.95 km


def test_force_strengths():
    assert cos.force_strength("gravity") == 1.0
    assert cos.force_strength("strong") > cos.force_strength("electromagnetic")


# ===== from test_api.py (Book 4 subset) ======================================

# --- cosmology E=Mc⁴ + bodies + gravitation ----------------------------------
def test_cosmology_api():
    assert close(cos.matter_energy(1.0), K.C2 * K.C2)
    assert close(cos.matter_from_energy(cos.matter_energy(3.0)), 3.0)
    assert cos.body_mass("jupiter") > cos.body_mass("earth")
    assert cos.gravitational_binding_energy(cos.body_mass("earth"), cos.body_radius("earth")) > 0
    assert 0 < cos.gravitational_time_dilation(cos.body_mass("sun"), cos.body_radius("sun")) < 1
    assert close(cos.poisson_einstein(1.0), 2 * cos.poisson_newton(1.0))
    assert close(cos.weight_force(10, 9.8), 98)


# ===== from test_audit.py (Book 4 subset) ====================================

# --- Book 4 cosmology additions ----------------------------------------------
def test_kepler_earth_year():
    # a = 1 AU, central mass = Sun -> ~365 days
    T = cos.kepler_period(1.496e11, cos.BODIES["sun"]["mass"])
    assert close(T / 86400, 365.25, rel=2e-2)
    # round-trip
    a = cos.kepler_semimajor(T, cos.BODIES["sun"]["mass"])
    assert close(a, 1.496e11, rel=1e-6)


def test_cosmic_budget_and_kappa():
    b = cos.cosmic_energy_budget()
    assert close(b["dark_energy"] + b["dark_matter"] + b["baryonic"], 1.0)
    assert cos.einstein_kappa() > 0
    assert cos.em_to_gravity_ratio() > 1e19      # EM ~10^20 x gravity


def test_redshift():
    assert cos.redshift_doppler(0.0) == 0.0
    assert cos.redshift_doppler(0.5 * K.C) > 0
    assert close(cos.redshift_energy_falloff(2.0), 0.25)


if __name__ == "__main__":
    funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in funcs:
        try:
            fn(); print(f"PASS  {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1; print(f"FAIL  {fn.__name__}: {exc}")
    print(f"\n{len(funcs) - failed}/{len(funcs)} passed")
    sys.exit(1 if failed else 0)
