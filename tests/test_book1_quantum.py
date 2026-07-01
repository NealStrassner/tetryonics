"""
Book 1 — Quantum (core geometry, matter/tetryon assembly, foundation locks,
dynamics/process layer, engine energy/charge/fields/levels/units, statistics,
plus the Book-1 API and audit coverage tests).
Run:  python tests/test_book1_quantum.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tetryonics as t
from tetryonics import (constants as K, geometry, energy, charge, fields, levels,
                        waves, spectra, radiation, optics, cosmology as cos,
                        thermodynamics as thermo, statistics as st, geometrics as geo,
                        numbertheory as nt, music, kinematics as kin, particles as P,
                        matter as m, dynamics as dyn, units, biochem, elements as el)


def close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel)


# ===== from test_core.py =====================================================

# --- constants: the geometric identities -------------------------------------
def test_mass_quantum_is_h_over_c2():
    assert close(K.M_Q, K.H / K.C2, rel=1e-12)
    assert close(K.M_Q, 7.376238634e-51, rel=1e-6)


def test_charge_quantum_and_elementary_charge():
    # Abraham's derivation: Omega/c^2 = charge quantum = 1/12 of e.
    assert close(K.CHARGE_QUANTUM, 1.335180067e-20, rel=1e-6)
    assert close(K.ELEMENTARY_CHARGE, 12 * K.CHARGE_QUANTUM, rel=1e-12)
    # ...and that matches the real elementary charge to ~3 sig figs.
    assert close(K.ELEMENTARY_CHARGE, 1.602176634e-19, rel=1e-3)


# --- masses: real particle masses from quanta --------------------------------
def test_electron_mass():
    assert close(t.electron().mass_kg, 8.851486e-31, rel=1e-4)


def test_proton_mass():
    assert close(t.proton().mass_kg, 1.659654e-27, rel=1e-4)


def test_proton_electron_ratio_is_1875():
    assert close(t.proton().mass_kg / t.electron().mass_kg, 1875.0, rel=1e-6)


def test_hydrogen_is_one_amu():
    # 1 amu ~ 1.660539e-27 kg
    assert close(t.hydrogen().mass_kg, 1.660539e-27, rel=1e-4)
    assert close(t.hydrogen().mass_amu, 1.0, rel=1e-9)


# --- charges: fractional + integer charges from assembly ---------------------
def test_quark_fractional_charges():
    assert close(t.quark("up").charge_e, 2 / 3)
    assert close(t.quark("down").charge_e, -1 / 3)
    assert close(t.quark("anti-up").charge_e, -2 / 3)
    assert close(t.quark("anti-down").charge_e, 1 / 3)


def test_proton_charge_plus_one_from_uud():
    p = t.proton()
    assert (p.cw, p.ccw) == (24, 12)      # [24·12]
    assert p.charge_e == 1.0


def test_neutron_is_neutral_from_udd():
    n = t.neutron()
    assert (n.cw, n.ccw) == (18, 18)      # [18·18]
    assert n.charge_e == 0.0


def test_topology_counts():
    assert t.quark("up").fascia == 12 and t.quark("up").topology == 8
    assert t.electron().fascia == 12 and t.electron().topology == 12
    assert t.proton().fascia == 36 and t.proton().topology == 20


# --- geometry: the triangle identities ---------------------------------------
def test_square_numbers_and_odd_rows():
    assert t.units_in_triangle(8) == 64
    assert [t.units_in_row(r) for r in range(1, 6)] == [1, 3, 5, 7, 9]
    assert t.geometry.odd_sum_to_square(8) == 64
    assert all(t.is_square(n * n) for n in range(1, 20))


def test_equilateral_area():
    assert close(t.equilateral_area(2.0), math.sqrt(3))   # (sqrt3/4)*4


# --- elements: deuterium stacking --------------------------------------------
def test_element_topology_numbers_match_skp_files():
    assert t.element(1).topology_pi == 48     # Hydrogen
    assert t.deuterium().topology_pi == 84    # Deuterium
    assert t.element(2).topology_pi == 168    # Helium = 2*84
    assert t.element(3).topology_pi == 252    # Lithium = 3*84
    assert t.element(6).topology_pi == 504    # Carbon = 6*84


def test_element_z_ge_2_is_84z():
    for z in range(2, 30):
        assert t.element(z).topology_pi == 84 * z


def test_helium_mass():
    assert close(t.element(2).mass_kg, 6.64e-27, rel=2e-3)


def test_neutral_atom_charge_zero():
    for z in (1, 2, 6, 26, 92):
        assert t.element(z).net_charge_e == 0


# ===== from test_matter.py ===================================================

# --- the tetryon: the fundamental 4-fascia unit ------------------------------
def test_tetryon_has_4_fascia():
    for state in ("positive", "negative", "neutral"):
        a = m.build_tetryon(state)
        assert a.tetryon_count == 1 and a.fascia == 4
    assert m.build_tetryon("positive").cw == 4
    assert m.build_tetryon("negative").ccw == 4
    assert m.build_tetryon("gluon").net_charge_quanta == 0   # neutral tetryon


def test_tetryon_constructor():
    assert (m.tetryon(3).cw, m.tetryon(3).ccw) == (3, 1)


# --- particle counts: how many tetryons -------------------------------------
def test_tetryon_counts():
    assert m.tetryon_count("up") == 3          # quark = 3 tetryons
    assert m.tetryon_count("electron") == 3    # lepton = 3 tetryons
    assert m.tetryon_count("proton") == 9      # baryon = 3 quarks = 9 tetryons
    assert m.build("up").fascia == 12
    assert m.build("proton").fascia == 36


# --- assembled charges reproduce the plate values ---------------------------
def test_quark_assembly_charges():
    assert (m.build("up").cw, m.build("up").ccw) == (10, 2)         # [10·2]
    assert (m.build("down").cw, m.build("down").ccw) == (4, 8)      # [4·8]
    assert (m.build("anti-up").cw, m.build("anti-up").ccw) == (2, 10)
    assert (m.build("anti-down").cw, m.build("anti-down").ccw) == (8, 4)
    assert abs(m.build("up").charge_e - 2/3) < 1e-9
    assert abs(m.build("down").charge_e + 1/3) < 1e-9


def test_lepton_assembly_charges():
    assert (m.build("electron").cw, m.build("electron").ccw) == (0, 12)
    assert (m.build("positron").cw, m.build("positron").ccw) == (12, 0)
    assert (m.build("neutrino").cw, m.build("neutrino").ccw) == (6, 6)
    assert m.build("electron").charge_e == -1.0


def test_baryon_assembly_charges():
    # proton = u+u+d assembled from 9 tetryons -> [24·12] -> +1
    assert (m.build("proton").cw, m.build("proton").ccw) == (24, 12)
    assert (m.build("neutron").cw, m.build("neutron").ccw) == (18, 18)
    assert m.build("proton").charge_e == 1.0 and m.build("neutron").charge_e == 0.0


# --- consistency: assembled == directly-defined (particles.py) --------------
def test_assembly_matches_particles_module():
    pairs = [("up", P.quark("up")), ("down", P.quark("down")),
             ("electron", P.electron()), ("positron", P.positron()),
             ("neutrino", P.neutrino()), ("proton", P.proton()), ("neutron", P.neutron())]
    for name, ref in pairs:
        a = m.build(name)
        assert a.cw == ref.cw and a.ccw == ref.ccw, name
        assert a.fascia == ref.fascia, name
        assert a.topology == ref.topology, name
        # mass (where tabulated)
        if ref.mass_kg is not None:
            assert abs(a.mass_kg - ref.mass_kg) < 1e-40, name


def test_as_particle_roundtrip():
    p = m.build("proton").as_particle()
    assert p.charge_e == 1.0 and p.fascia == 36 and p.topology == 20


def test_recipe_strings():
    assert m.build("up").recipe().startswith("up = [4·0]+[4·0]+[2·2]")
    # a neutrino is literally three gluons
    assert m.build("neutrino").recipe().startswith("neutrino = [2·2]+[2·2]+[2·2]")


# --- the 4nπ formula (Book 1 p114): Matter = 4·(tetryon count) π --------------
def test_4n_pi_formula():
    assert m.matter_pi(1) == 4      # tetryon
    assert m.matter_pi(3) == 12     # quark / lepton
    assert m.matter_pi(9) == 36     # baryon
    assert m.build("up").mass_energy_pi == 12
    assert m.build("proton").mass_energy_pi == 36


# --- internalised ('antimatter inside') fascia (Book 1 p145 / ABRAHAM.txt) ----
def test_internalised_fascia():
    # internal = mass-energy pi - topology pi
    assert m.build("up").internalised_fascia == 4          # 12 - 8 (quark)
    assert m.build("electron").internalised_fascia == 0    # 12 - 12 (lepton, repulsive)
    assert m.build("proton").internalised_fascia == 16     # 36 - 20 (baryon)
    assert m.build("up").external_fascia == 8              # = topology


# --- mesons = quark + antiquark (6 tetryons, 24π → 14π) ----------------------
def test_meson_assembly():
    pi_plus = m.build("pi+")    # u + anti-d
    assert pi_plus.tetryon_count == 6 and pi_plus.fascia == 24
    assert pi_plus.topology == 14 and pi_plus.internalised_fascia == 10
    assert pi_plus.charge_e == 1.0
    assert m.build("pi-").charge_e == -1.0
    assert m.build("pi0").charge_e == 0.0


# --- DEUTERIUM = the building block of elements (proton + neutron + electron) -
def test_deuterium_build():
    d = m.build_deuterium()
    # immediate components: proton, neutron, electron
    assert [c.name for c in d.subparticles] == ["proton", "neutron", "electron"]
    # 21 tetryons = 9 (p) + 9 (n) + 3 (e); 84π
    assert d.tetryon_count == 21 and d.fascia == 84
    assert d.cw == 42 and d.ccw == 42 and d.charge_e == 0.0   # neutral
    assert abs(d.mass_amu - 2.0) < 1e-2                       # ~2 amu


def test_hydrogen_build():
    h = m.build_hydrogen()
    assert [c.name for c in h.subparticles] == ["proton", "electron"]
    assert h.tetryon_count == 12 and h.fascia == 48           # no neutron
    assert abs(h.mass_amu - 1.0) < 1e-3


def test_atom_build_from_deuterium_units():
    import tetryonics as t
    for z in (2, 6, 8):
        a = m.build_atom(z)
        assert len(a.subparticles) == z                       # Z deuterium units
        assert all(s.name == "deuterium" for s in a.subparticles)
        assert a.fascia == 84 * z                             # 84·Z π
        assert a.tetryon_count == 21 * z
        # mass matches the elements engine (summed up the tetryon tree)
        assert abs(a.mass_amu - t.element(z).mass_amu) < 1e-6


def test_construction_tree_string():
    tree = m.build_deuterium().tree()
    assert "deuterium" in tree and "proton" in tree and "electron" in tree and "up" in tree


# --- mass still sums right from the assembly --------------------------------
def test_assembled_masses():
    assert abs(m.build("electron").mass_kg - 8.851486e-31) < 1e-36
    assert abs(m.build("proton").mass_kg - 1.659654e-27) < 1e-32


# ===== from test_foundation.py ===============================================

# --- particle -> Tetryonic DELTAHEDRON (Book 5 p20 / Book 1 p130) -------------
def test_particle_solid_mapping():
    assert geo.PARTICLE_SOLID["tetryon"] == ("tetra-deltahedron", 4, 4)
    assert geo.PARTICLE_SOLID["quark"] == ("octa-deltahedron", 8, 12)
    assert geo.PARTICLE_SOLID["lepton"] == ("dodeca-deltahedron", 12, 12)
    assert geo.PARTICLE_SOLID["baryon"] == ("icoso-deltahedron", 20, 36)
    # face counts = the topology pi (= external charge fascia)
    assert geo.solid_for_particle("baryon")["faces"] == 20
    assert geo.solid_for_particle("lepton")["faces"] == 12


def test_lepton_is_dodeca_DELTAHEDRON_not_platonic_dodecahedron():
    # THE CORRECTION: lepton = 12 TRIANGULAR faces, 18 edges, 8 vertices (a hexagonal
    # bipyramid / snub disphenoid) — NOT the Platonic dodecahedron (12 pentagons, 30 E, 20 V).
    info = geo.solid_for_particle("lepton")
    assert info["solid"] == "dodeca-deltahedron"
    assert (info["faces"], info["edges"], info["vertices"]) == (12, 18, 8)
    # the Platonic dodecahedron (kept only for the p19 comparison) has different E,V
    assert geo.PLATONIC["dodecahedron"] == (12, 30, 20)


def test_all_solids_are_valid_manifolds():
    # Euler F-E+V = 2 for every Tetryonic deltahedron
    for solid in ("tetra-deltahedron", "octa-deltahedron", "dodeca-deltahedron",
                  "icoso-deltahedron"):
        assert geo.euler_characteristic(solid) == 2
    # deltahedra have all-equilateral-triangle faces: surface area = F * (sqrt3/4) s^2
    assert close(geo.deltahedron_metrics("icoso-deltahedron", 1.0)["area"],
                 20 * geo.equilateral_area(1.0))


# --- charge topologies [cw·ccw] (Book 1 p142/p151, plate-verified) -----------
def test_quark_charge_topologies():
    assert P.QUARKS["up"] == (10, 2)        # 8 [10·2] -> +2/3
    assert P.QUARKS["down"] == (4, 8)       # 4 [4·8]  -> -1/3
    assert P.QUARKS["anti-up"] == (2, 10)   # 8 [2·10] -> -2/3
    assert P.QUARKS["anti-down"] == (8, 4)  # 4 [8·4]  -> +1/3
    assert close(P.quark("up").charge_e, 2 / 3)
    assert close(P.quark("down").charge_e, -1 / 3)


def test_lepton_charge_topologies():
    assert (P.electron().cw, P.electron().ccw) == (0, 12)   # 12 [0·12] -> -1
    assert (P.positron().cw, P.positron().ccw) == (12, 0)   # 12 [12·0] -> +1
    assert (P.neutrino().cw, P.neutrino().ccw) == (6, 6)    # 0  [6·6]  ->  0


def test_baryon_charge_topologies():
    assert (P.proton().cw, P.proton().ccw) == (24, 12)      # 12 [24·12] -> +1
    assert (P.neutron().cw, P.neutron().ccw) == (18, 18)    # 0  [18·18] ->  0
    assert P.proton().charge_e == 1.0 and P.neutron().charge_e == 0.0


def test_baryon_assemblies_match_plate_p208():
    d = dyn.seek_equilibrium(P.proton(), P.neutron())       # deuteron
    assert (d["cw"], d["ccw"], d["net_quanta"]) == (42, 30, 12)
    nn = dyn.seek_equilibrium(P.neutron(), P.neutron())     # neutronium
    assert (nn["cw"], nn["ccw"], nn["net_quanta"]) == (36, 36, 0)


# --- the core constants (verified to match Kelvin's published digits) --------
def test_foundation_constants():
    assert K.C == 299792458.0
    assert close(K.M_Q, 7.376238634e-51, rel=1e-9)          # = h/c^2
    assert close(K.CHARGE_QUANTUM, 1.335180067e-20, rel=1e-9)  # = Omega/c^2
    assert close(K.ELEMENTARY_CHARGE, 12 * K.CHARGE_QUANTUM)   # e = 12 fascia
    assert K.N_PROTON / K.N_ELECTRON == 1875.0


def test_element_rule():
    # Hydrogen=48, Deuterium=84, every element Z>=2 = 84*Z (matches the .skp models)
    assert t.element(1).topology_pi == 48
    assert t.deuterium().topology_pi == 84
    assert all(t.element(z).topology_pi == 84 * z for z in range(2, 30))


def test_photon_is_a_diamond_of_two_triangles():
    # Energy is the square: a boson (1 triangle) = n²; a photon (a flat DIAMOND of
    # 2 triangles) = 2n². A photon is exactly two bosons fused edge-to-edge.
    from tetryonics import geometry as g
    assert [g.boson_quanta(n) for n in range(1, 5)] == [1, 4, 9, 16]
    assert [g.photon_quanta(n) for n in range(1, 5)] == [2, 8, 18, 32]   # 2n²
    assert all(g.photon_quanta(n) == 2 * g.boson_quanta(n) for n in range(1, 9))
    # general field rule: fascia·n² (boson1, photon2, tetryon/Matter4, lepton/quark12)
    assert g.field_quanta(4, 3) == 4 * 9 and g.field_quanta(12, 2) == 12 * 4
    # the diamond is planar (2D) with 2 triangular fascia and 4 corners
    ph = g.Photon(level=3)
    assert ph.quanta == 18 and ph.triangles == 2 and ph.is_planar
    assert len(ph.vertices()) == 4


# ===== from test_dynamics.py =================================================

# --- emission ----------------------------------------------------------------
def test_emit_photon_balmer_alpha():
    tr = dyn.emit_photon(3, 2)
    assert tr.kind == "emission"
    # his KEM ladder: 13.525*(1/4 - 1/9) ~ 1.879 eV
    assert close(tr.energy_ev, K.KEM_EV * (1/4 - 1/9), rel=1e-9)
    # quanta out = 12*(9-4) = 60
    assert tr.quanta == 12 * (9 - 4)
    assert tr.wavelength_m > 0
    assert "diamond" in tr.detail["photon"]


def test_emit_requires_drop():
    try:
        dyn.emit_photon(2, 3)
        assert False
    except ValueError:
        pass


# --- absorption (inverse of emission) ----------------------------------------
def test_absorb_is_inverse_of_emit():
    emitted = dyn.emit_photon(4, 1)
    absorbed = dyn.absorb_photon(1, emitted.energy_ev)
    assert absorbed.detail["reached_level"] == 4
    assert absorbed.quanta == emitted.quanta


def test_absorb_ionises_above_binding():
    # a photon with more than the n1 binding energy frees the electron
    tr = dyn.absorb_photon(1, 20.0)   # > 13.525 eV
    assert tr.detail["ionised"] is True


# --- pinch / fusion / pair creation ------------------------------------------
def test_pinch_is_100_percent_mc2():
    tr = dyn.pinch(1e-3)
    assert close(tr.energy_j, 1e-3 * K.C2)
    assert tr.detail["efficiency"] == 1.0


def test_fusion_is_one_3600th_of_pinch():
    assert close(dyn.fusion(1.0).energy_j, dyn.pinch(1.0).energy_j / 3600)


def test_pair_creation_threshold():
    thresh = 2 * K.N_ELECTRON * K.M_Q * K.C2
    assert dyn.pair_creation(thresh * 1.1).detail["creates_pair"] is True
    assert dyn.pair_creation(thresh * 0.5).detail["creates_pair"] is False


# --- force interactions ------------------------------------------------------
def test_charge_interaction_attract_repel():
    assert dyn.charge_interaction(P.proton(), P.electron(), 1e-10).direction == "attract"
    assert dyn.charge_interaction(P.proton(), P.proton(), 1e-10).direction == "repel"
    assert dyn.charge_interaction(P.neutron(), P.proton(), 1e-10).direction == "neutral"
    # force magnitude is positive and inverse-square
    f1 = dyn.charge_interaction(P.proton(), P.electron(), 1e-10).force_n
    f2 = dyn.charge_interaction(P.proton(), P.electron(), 2e-10).force_n
    assert close(f1 / f2, 4.0)


def test_strong_interaction():
    assert dyn.strong_interaction(1, -1).direction == "attract"   # opposite fascia bind
    assert dyn.strong_interaction(1, 1).direction == "repel"      # like fascia -> leptons
    assert dyn.strong_interaction(0, 1).direction == "neutral"


def test_seek_equilibrium():
    # u + u + d should assemble to a proton: net +1, [24,12]
    eq = dyn.seek_equilibrium(P.quark("up"), P.quark("up"), P.quark("down"))
    assert eq["cw"] == 24 and eq["ccw"] == 12 and eq["net_charge_e"] == 1.0
    # electron + positron -> neutral
    eq2 = dyn.seek_equilibrium(P.electron(), P.positron())
    assert eq2["neutral"] is True


def test_spectral_emission_helper():
    tr = dyn.spectral_emission("balmer", 3)
    assert tr.kind == "emission" and tr.quanta == 12 * (9 - 4)


def test_transition_describe():
    s = dyn.emit_photon(3, 2).describe()
    assert "emission" in s and "nm" in s


# ===== from test_engine.py (Book 1 subset) ===================================

# --- energy / mass / momentum -------------------------------------------------
def test_quanta_energy_mass_consistency():
    # one Planck quantum: energy h, mass h/c^2
    assert close(energy.energy_from_quanta(1), K.H)
    assert close(energy.mass_from_quanta(1), K.M_Q)
    # E/c^2 == mass for the same quantum
    assert close(energy.em_mass(K.H), K.M_Q)


def test_round_trips():
    assert close(energy.quanta_from_energy(energy.energy_from_quanta(1e23)), 1e23)
    assert close(energy.quanta_from_mass(energy.mass_from_quanta(5e20)), 5e20)
    assert close(energy.energy_from_em_mass(energy.em_mass(123.0)), 123.0)
    assert close(energy.energy_from_matter(energy.matter(123.0)), 123.0)


def test_matter_is_energy_over_c4():
    assert close(energy.matter(K.H), K.H / (K.C2 * K.C2))


def test_momentum_and_kinetic():
    m, v = 2.0, 3.0
    assert close(energy.momentum(m, v), 6.0)
    assert close(energy.scalar_energy(m, v), 18.0)        # mv^2
    assert close(energy.kinetic_energy(m, v), 9.0)        # 1/2 mv^2
    assert close(energy.mass_from_energy_velocity(18.0, 3.0), 2.0)


def test_frequency_quanta_relation():
    # 2hv = hf  ->  f = 2v
    assert close(energy.frequency_from_quanta(50.0), 100.0)
    assert close(energy.quanta_from_frequency(100.0), 50.0)
    assert close(energy.photon_energy(100.0), 2 * energy.boson_energy(50.0))


def test_lorentz():
    assert close(energy.beta(K.C / 2), 0.5)
    assert close(energy.gamma(0.0), 1.0)
    assert energy.gamma(0.8 * K.C) > 1.6


# --- charge -------------------------------------------------------------------
def test_charge_from_topology():
    assert charge.charge_in_e(24, 12) == 1.0          # proton
    assert charge.charge_in_e(18, 18) == 0.0          # neutron
    assert close(charge.charge_in_e(10, 2), 2 / 3)    # up quark
    assert close(charge.charge_coulombs(12, 0), 12 * K.CHARGE_QUANTUM)


def test_fermion_charge_rule():
    assert charge.is_fermion_charge(10, 2)   # 8 quanta = 2/3 e
    assert charge.is_fermion_charge(4, 8)    # -4 quanta = -1/3 e


# --- fields -------------------------------------------------------------------
def test_em_constants_interdependence():
    # c = 1/sqrt(eps0 mu0) within ~1e-3 (Tetryonics rounded values)
    assert close(fields.speed_of_light_from_constants(), K.C, rel=1e-3)


def test_coulomb_force_repulsive_for_like_charges():
    f = fields.coulomb_force(K.ELEMENTARY_CHARGE, K.ELEMENTARY_CHARGE, 1e-10)
    assert f > 0
    # inverse-square: doubling r quarters the force
    f2 = fields.coulomb_force(K.ELEMENTARY_CHARGE, K.ELEMENTARY_CHARGE, 2e-10)
    assert close(f / f2, 4.0, rel=1e-9)


def test_field_falloff():
    assert close(fields.electric_falloff(2.0), 0.25)
    assert close(fields.magnetic_dipole_falloff(2.0), 0.125)


# --- levels -------------------------------------------------------------------
def test_level_and_shell_quanta():
    assert levels.level_quanta(8) == 64
    assert [levels.level_step(n) for n in range(1, 6)] == [1, 3, 5, 7, 9]
    assert [levels.shell_quanta(n) for n in range(1, 9)] == \
        [12, 48, 108, 192, 300, 432, 588, 768]


def test_spin_angles_and_colour():
    assert levels.spin_rotation_angle(0.5) == 720
    assert levels.spin_rotation_angle(3) == 120
    assert levels.colour(1) == "Red" and levels.colour(8) == "Violet"


# --- units --------------------------------------------------------------------
def test_units_map():
    assert "Ω" in units.describe("qam")
    cc = units.colour_codes()
    assert cc["energy_level"][1] == "Red"
    assert cc["physics_property"]["positive"] == "Red"


# ===== from test_mining.py (Book 1 subset) ===================================

# --- statistics --------------------------------------------------------------
def test_statistics():
    assert close(st.born_rule(3), 9)
    assert close(st.gaussian(0), 1 / math.sqrt(2 * math.pi))   # peak of standard normal
    assert close(st.binomial_probability(4, 2, 0.5), 6 * 0.0625)
    assert st.heisenberg_min_momentum(1e-10) > 0
    assert close(st.shannon_entropy([0.5, 0.5]), 1.0)          # 1 bit


# ===== from test_api.py (Book 1 subset) ======================================

# --- inverse conversions (round-trips) ---------------------------------------
def test_energy_wave_round_trips():
    assert close(energy.frequency_from_energy(energy.photon_energy(5e14)), 5e14)
    assert close(energy.momentum_from_de_broglie(energy.de_broglie_wavelength(3.0)), 3.0)
    assert close(energy.mass_from_compton(energy.compton_wavelength(9e-31)), 9e-31)
    assert close(energy.velocity_from_beta(energy.beta(1e8)), 1e8)
    assert close(energy.em_mass_from_matter(energy.matter_from_em_mass(2.0)), 2.0)
    lam = 5e-7
    assert close(waves.wavelength_from_energy(waves.energy_from_wavenumber(1 / lam)), lam)
    assert close(waves.frequency_from_wavenumber(1 / lam), K.C / lam)


# --- particle accessors & lookup ---------------------------------------------
def test_particle_api():
    p = t.particle("proton")
    assert p.charge_e == 1.0 and p.charge_pair == (24, 12)
    assert close(p.planck_quanta, K.N_PROTON)
    assert close(p.mass_energy_mev, p.mass_energy_ev / 1e6)
    assert t.particle("electron").magnetic_moment() == K.BOHR_MAGNETON
    assert t.particle("proton").magnetic_moment() == K.NUCLEAR_MAGNETON
    assert t.particle("electron").compton() > 0
    custom = t.from_quanta(10, 2, name="x")
    assert custom.charge_e == 2 / 3
    assert t.meson("up", "anti-down").fascia == 24


# --- kinematics --------------------------------------------------------------
def test_kinematics():
    assert kin.velocity(10, 2) == 5
    assert kin.acceleration(6, 3) == 2
    assert kin.force(2, 3) == 6 and kin.momentum(2, 3) == 6
    assert kin.kinetic_energy(2, 3) == 9
    assert kin.shm_restoring_force(5, 2) == -10
    assert close(kin.shm_period(1, (2 * math.pi) ** 2), 1.0)


# --- previously-untested functions (audit §5) --------------------------------
def test_previously_untested_api():
    assert t.positive_tetryon().net_charge_quanta == 4
    assert t.negative_tetryon().net_charge_quanta == -4
    assert t.neutral_tetryon().is_neutral
    assert charge.net_quanta(24, 12) == 12
    assert fields.lorentz_force(1, 2, 3, 4) == 14           # 1*(2+3*4)
    assert fields.poynting(2, 3) == 6
    assert levels.shell_name(1) == "K"
    assert t.anti_proton().charge_e == -1
    assert el.periodic_table(3)[2].symbol == "Li"
    assert cos.gravity_force(1, 1, 1) == K.G
    assert geo.perimeter(3) == 9


# ===== from test_audit.py (Book 1 subset) ====================================

# --- the c-correction: constants now match Kelvin's published digits ----------
def test_c_is_exact_si_value():
    assert K.C == 299792458.0
    assert close(K.C2, 8.987551787e16, rel=1e-9)
    assert close(K.M_Q, 7.376238634e-51, rel=1e-9)
    assert close(K.CHARGE_QUANTUM, 1.335180067e-20, rel=1e-9)


# --- magnetism (Book 1) -------------------------------------------------------
def test_magnetons_and_ratios():
    assert fields.nuclear_magneton() == fields.bohr_magneton() / 1875
    assert close(fields.charge_mass_ratio("electron"), 1.810109642e11, rel=1e-3)
    assert fields.charge_mass_ratio("proton") < fields.charge_mass_ratio("electron")


# --- quantised energy forms & tetryon units (Book 1) -------------------------
def test_quantised_energy_and_tetryon_units():
    assert close(energy.transverse_energy(1, 1), math.pi * K.H)
    assert close(energy.scalar_energy_quantised(2, 3), 2 * math.pi * K.H * 9)
    assert energy.tetryon_units(3) == 36          # 4 * 3^2


# --- charge fix ---------------------------------------------------------------
def test_charge_from_qam_gives_charge_quantum():
    assert close(charge.charge_from_qam(), K.CHARGE_QUANTUM)


# --- previously-untested functions (internal audit) --------------------------
def test_previously_untested_audit():
    assert close(energy.de_broglie_wavelength(K.H), 1.0)
    assert close(energy.compton_wavelength(K.N_ELECTRON * K.M_Q), K.H / (K.N_ELECTRON * K.M_Q * K.C))
    assert fields.electric_field(K.ELEMENTARY_CHARGE, 1e-10) > 0
    assert fields.gauss_flux(K.ELEMENTARY_CHARGE) > 0
    assert close(fields.coulomb_constant(), 1 / (4 * math.pi * K.EPSILON_0))
    assert t.geometry.up_down_in_row(4) == (4, 3)
    assert t.particles.positron().charge_e == 1.0
    assert t.particles.neutrino().charge_e == 0.0
    assert len(t.particles.standard_particles()) == 10
    assert t.elements.tritium().neutrons == 2
    assert close(t.waves.angular_frequency(1), 2 * math.pi)


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
