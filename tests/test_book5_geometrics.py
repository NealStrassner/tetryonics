"""
Book 5 — Geometrics (number theory, music, trig/polar, Platonic solids,
eutrigons, triangular/square numbers, Pascal/binomial, series, dihedral angles,
golden ratio, named constants).
Run:  python tests/test_book5_geometrics.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tetryonics as t
from tetryonics import (constants as K, geometrics as geo, numbertheory as nt, music,
                        statistics as st)


def close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel)


# ===== from test_mining2.py (Book 5 subset) ==================================

# --- number theory (Book 5) --------------------------------------------------
def test_digital_root_and_primes():
    assert nt.digital_root(157) == 4
    assert nt.digital_root(9) == 9 and nt.digital_root(18) == 9
    assert nt.is_prime(97) and not nt.is_prime(91)
    assert nt.primes_up_to(10) == [2, 3, 5, 7]
    assert nt.is_twin_prime_form(11) and nt.is_twin_prime_form(13)


def test_mersenne_goldbach_perfect():
    assert nt.mersenne(7) == 127 and nt.is_mersenne_prime(7)
    p, q = nt.goldbach_pair(28)
    assert nt.is_prime(p) and nt.is_prime(q) and p + q == 28
    assert nt.is_perfect_number(28) and nt.is_perfect_number(6)
    assert nt.prime_as_square_difference(7) == (4, 3)   # 16-9=7


def test_fibonacci_converges_to_phi():
    assert [nt.fibonacci(n) for n in range(7)] == [0, 1, 1, 2, 3, 5, 8]
    assert close(nt.fibonacci_ratio(20), K.PHI, rel=1e-6)


# --- music (Book 5) ----------------------------------------------------------
def test_music_phase_and_intervals():
    assert music.note_to_phase("C") == 0
    assert music.note_to_phase("G") == 210      # 7 semitones * 30
    assert music.note_to_phase("B") == 330
    assert close(music.interval_ratio("fifth"), 1.5)
    assert close(music.interval_ratio("octave"), 2.0)
    assert close(music.equal_tempered_frequency(69), 440.0)   # A4
    assert close(music.semitones_to_ratio(12), 2.0)
    assert music.circle_of_fifths()[0] == "C" and music.circle_of_fifths()[1] == "G"


# --- geometrics extras (Book 5) ----------------------------------------------
def test_geometrics_trig_polar():
    assert close(geo.sin_deg(60), math.sqrt(3) / 2)
    assert close(geo.cos_deg(60), 0.5)
    assert close(geo.tan_deg(60), math.sqrt(3))
    r, th = geo.cartesian_to_polar(3, 4)
    assert close(r, 5.0) and close(th, 53.13, rel=1e-3)
    x, y = geo.polar_to_cartesian(5, 53.13010235)
    assert close(x, 3.0, rel=1e-4) and close(y, 4.0, rel=1e-4)
    assert close(geo.side_from_area(geo.equilateral_area(2)), 2.0)
    assert geo.euler_inequality_ok(2.0, 1.0)
    assert close(geo.basel_sum(100000), K.ZETA2, rel=1e-4)


def test_named_constants():
    assert close(K.E_EULER, math.e)
    assert close(K.ZETA2, math.pi**2 / 6)


# ===== from test_books345.py (Book 5 subset) =================================

# --- geometrics (Book 5) -----------------------------------------------------
def test_euler_characteristic_all_solids():
    for solid in geo.PLATONIC:
        assert geo.euler_characteristic(solid) == 2


def test_particle_solid_map():
    assert geo.solid_for_particle("tetryon")["faces"] == 4
    assert geo.solid_for_particle("quark")["solid"] == "octa-deltahedron"
    assert geo.solid_for_particle("lepton")["faces"] == 12
    assert geo.solid_for_particle("baryon")["faces"] == 20


def test_eutrigon_60_degree():
    # equilateral a=b=c=2 -> identity ~0
    assert close(geo.eutrigon_identity(2, 2, 2) + 1, 1, rel=1e-9)  # ~0
    assert geo.eutrigon_c2(2, 2) == 4   # 4+4-4


def test_triangular_and_square():
    assert [geo.triangular_number(n) for n in range(1, 6)] == [1, 3, 6, 10, 15]
    assert geo.square_from_odds(8) == 64


def test_math_as_geometry():
    # √−1 = the 90° quarter-turn operator (Book 5 p.55).
    assert geo.imaginary_rotation(1, 0, 1) == (0, 1)
    assert geo.imaginary_rotation(1, 0, 2) == (-1, 0)
    assert geo.i_power(2) == (-1, 0) and geo.i_power(4) == (1, 0)
    # odd numbers as square-difference gnomons (p.86): n²−(n−1)² = 2n−1.
    assert [geo.odd_as_square_difference(n) for n in range(1, 6)] == [1, 3, 5, 7, 9]
    # equilateral quantum-probability distribution (p.152): 1..n..1, sum = n².
    assert geo.equilateral_distribution(4) == [1, 2, 3, 4, 3, 2, 1]
    assert sum(geo.equilateral_distribution(7)) == 49
    assert close(geo.probability_from_amplitude(0.6), 0.36)
    assert geo.infinities_exist() is False     # renormalisation: no infinities (p.144)


def test_equilateral_metrics():
    assert close(geo.equilateral_area(2), math.sqrt(3))
    assert close(geo.equilateral_height(2), math.sqrt(3))
    assert close(geo.circumradius(2), 2 * geo.inradius(2))   # 1:2 ratio


# ===== from test_coverage2.py (Book 5 subset) ================================

# --- Book 5 geometry extras --------------------------------------------------
def test_fourth_power_and_twin_triangular():
    assert geo.fourth_power(3) == 81
    assert all(geo.twin_triangular_square(n) == n * n for n in range(2, 12))


def test_pascal_and_binomial():
    assert geo.binomial(5, 2) == 10
    assert geo.pascal_row(4) == [1, 4, 6, 4, 1]


def test_law_of_cosines_reduces_to_eutrigon():
    # C=60 -> c^2 = a^2+b^2-ab
    c = geo.law_of_cosines(2, 3, 60)
    assert close(c * c, geo.eutrigon_c2(2, 3))
    # C=90 -> pythagoras
    assert close(geo.law_of_cosines(3, 4, 90), 5.0)


def test_geometric_series():
    assert close(geo.geometric_series_sum(0.5), 2.0)        # sum 1/2^n from 0
    assert close(geo.geometric_series_sum(0.25), 4 / 3)
    assert close(geo.geometric_series_sum(0.5, terms=3), 1.75)


def test_dihedral_angles():
    assert close(geo.dihedral_angle("cube"), 90.0)
    assert close(geo.dihedral_angle("tetrahedron"), 70.5288, rel=1e-4)
    assert close(geo.dihedral_angle("octahedron"), 109.4712, rel=1e-4)


# ===== from test_api.py (Book 5 subset) ======================================

# --- geometrics / number / music extras --------------------------------------
def test_geometrics_extras():
    assert close(geo.apothem(4, 2), 1.0)                    # square apothem = s/2
    assert close(geo.viviani_distance_sum(2), geo.equilateral_height(2))
    assert geo.pentagonal_number(5) == 35
    assert geo.tetrahedral_number(4) == 20
    assert geo.square_pyramidal_number(3) == 14
    assert close(geo.taylor_exp(1, 20), math.e)
    assert close(geo.taylor_cos(0), 1.0)
    assert abs(geo.euler_identity()) < 1e-12
    assert close(geo.kepler_bouwkamp(2000), K.KEPLER_BOUWKAMP, rel=3e-2)  # slow convergence
    assert geo.nth_odd(5) == 9 and geo.nth_even(5) == 10


def test_number_music_stats():
    assert nt.lucas(5) == 11
    assert close(nt.lucas(20) / nt.lucas(19), K.PHI, rel=1e-3)
    assert close(music.note_frequency("A", 4), 440.0)
    assert len(music.scale_ratios("major")) == 8
    assert st.normal_empirical_rule()[0] == 0.6827
    assert close(st.standard_deviation([2, 4, 4, 4, 5, 5, 7, 9]), 2.0)


# ===== from test_audit.py (Book 5 subset) ====================================

# --- Book 5 geometrics additions ---------------------------------------------
def test_platonic_metrics():
    assert close(geo.platonic_metrics("cube", 2)["volume"], 8.0)
    assert close(geo.platonic_metrics("tetrahedron", 1)["area"], math.sqrt(3))
    assert close(geo.platonic_metrics("octahedron", 1)["volume"], math.sqrt(2) / 3)


def test_golden_ratio_and_polygons():
    assert close(geo.golden_ratio(), 1.6180339887)
    assert close(geo.golden_ratio() ** 2, geo.golden_ratio() + 1)   # phi^2 = phi+1
    assert geo.polygon_interior_angle(6) == 120
    assert geo.polygon_exterior_angle(4) == 90
    assert close(geo.hexagon_area(1), 3 * math.sqrt(3) / 2)


def test_number_geometry_extras():
    assert geo.sum_of_cubes(3) == 36             # (1+2+3)^2
    assert close(geo.geometric_mean(4, 9), 6.0)
    assert close(geo.incircle_area(1) * 4, geo.circumcircle_area(1))   # R=2r -> areas 1:4


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
