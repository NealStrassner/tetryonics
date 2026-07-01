"""
Book 3 — Chemistry (elements, shells, bonding, molecular geometry, isotopes,
biochemistry, periodic position, nuclear energy-level masses).
Run:  python tests/test_book3_chemistry.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tetryonics as t
from tetryonics import (constants as K, elements as el, biochem, geometrics as geo,
                        cosmology as cos)


def close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel)


# ===== from test_mining2.py (Book 3 subset) ==================================

# --- biochemistry (Book 3) ---------------------------------------------------
def test_biochem_quanta():
    assert biochem.molecule_quanta("H2O") == 768
    assert biochem.sugar_quanta("glucose") == 7632          # 6*504+12*48+6*672
    assert biochem.CARBOHYDRATE_UNIT == 1272
    # dipeptide of two glycines releases one water
    di = biochem.peptide_quanta(["glycine", "glycine"])
    assert di == 2 * biochem.amino_acid_quanta("glycine") - 768
    assert biochem.condensation_water(3) == 2304


# --- elements 119/120 & fission ----------------------------------------------
def test_kelvinium_abrahamium():
    assert el.element(119).symbol == "Kl"      # Kelvinium
    assert el.element(120).symbol == "Ab"      # Abrahamium
    assert el.element(120).topology_pi == 84 * 120


# ===== from test_books345.py (Book 3 subset) =================================

# --- chemistry (Book 3) ------------------------------------------------------
def test_shell_capacity_2n2():
    assert [el.shell_capacity(n) for n in range(1, 5)] == [2, 8, 18, 32]


def test_electron_configuration():
    assert el.electron_configuration(1) == "1s1"
    assert el.electron_configuration(2) == "1s2"
    assert el.electron_configuration(6).startswith("1s2 2s2 2p2")
    assert el.electron_configuration(10) == "1s2 2s2 2p6"


def test_ionisation_energy_hydrogen():
    # His KEM ground 13.525 eV (Book 3 p.75), not the rounded standard 13.6.
    assert close(el.ionisation_energy(1, 1), 13.525)
    assert close(el.ionisation_energy(2, 1), 54.1)   # He+ = 13.525*4


def test_water_topology_and_mass():
    # H2O = 48 + 48 + 672 = 768 pi
    assert el.molecule_topology_pi("H2O") == 768
    # mass ~ 2*H + O ~ 2.988e-26 kg (~18 amu)
    assert close(el.molecule_mass("H2O"), 2.988e-26, rel=2e-3)
    assert close(el.molecule_mass_amu("H2O"), 18.0, rel=1e-2)


def test_bond_type_classification():
    # His charge-topology view (Book 3 p.371/380): metal+non-metal=ionic, non-metal pair=covalent.
    assert el.bond_type("Na", "Cl") == "ionic"
    assert el.bond_type("H", "O") == "covalent"
    assert el.bond_type("C", "O") == "covalent"
    assert el.bond_type("Fe", "Cu") == "metallic"
    assert el.bond_type("Be", "Cl") == "covalent"   # BeCl2 is covalent/linear (p.370), not ionic


def test_formula_parser_expands_parentheses():
    # Ca(OH)2, Ca3(PO4)2 must expand the group multipliers, not drop them.
    assert el._parse_formula("Ca(OH)2") == {"Ca": 1, "O": 2, "H": 2}
    assert el._parse_formula("Ca3(PO4)2") == {"Ca": 3, "P": 2, "O": 8}
    assert el.molecule_topology_pi("Ca3(PO4)2") == 12936
    # neutralise emits Ca(NO3)2 — it must re-parse correctly
    assert el.molecule_topology_pi("Ca(NO3)2") == el.molecule_topology_pi("CaN2O6")


def test_molecular_geometry_matches_p370():
    # The shapes Kelvin draws on the Lewis-structures plate (p.370).
    cases = {"BeCl2": "linear", "BH3": "trigonal planar", "CH4": "tetrahedral",
             "NH3": "trigonal pyramidal", "H2O": "bent", "CO2": "linear", "HF": "linear"}
    for mol, shape in cases.items():
        assert el.molecule_shape(mol)["shape"] == shape, mol
    assert el.molecule_shape("CH4")["bond_angle_deg"] == 109.5
    assert el.molecule_shape("H2O")["bond_angle_deg"] == 104.5
    # lone pairs drive the bend: O→2, N→1, C→0
    assert el.central_lone_pairs("O", 2) == 2
    assert el.central_lone_pairs("N", 3) == 1
    assert el.central_lone_pairs("C", 4) == 0


def test_orbitals():
    # s/p/d/f: capacity 4ℓ+2, orbitals 2ℓ+1 (Book 3 p.59-62).
    assert [el.subshell_capacity(s) for s in "spdf"] == [2, 6, 10, 14]
    assert [el.orbital(s)["orbitals"] for s in "spdf"] == [1, 3, 5, 7]
    assert el.azimuthal_quantum_number("d") == 2
    assert el.orbital("s")["shape"] == "spherical"
    assert el.element_orbital(79)["subshell"] == "d"     # gold is a d-block element


def test_bond_geometry_p369():
    assert el.bond_geometry("CO2")["bond_length_pm"] == 116.3
    assert el.bond_geometry("O3")["bond_angle_deg"] == 116.8
    assert el.bond_geometry("H2O")["bond_angle_deg"] == 104.5   # VSEPR fallback


def test_isotopes_and_isomers():
    assert el.common_isotopes(6) == [12, 13, 14]
    assert el.neutron_number(6, 14) == 8
    assert el.isotope(6, 14).topology_pi == 576                 # 36·14 + 12·6
    assert el.isotope_notation(92, 235) == "U-235"
    assert el.molecular_formula("OCH3CH3") == "C2H6O"
    assert el.are_isomers("C2H6O", "CH3OCH3") is True
    assert el.are_isomers("H2O", "H2O") is False


def test_base_pairing():
    from tetryonics import biochem as bc
    assert bc.complementary_base("adenine") == "thymine"        # DNA
    assert bc.complementary_base("adenine", rna=True) == "uracil"
    assert bc.complementary_base("guanine") == "cytosine"
    assert bc.base_pair_quanta("guanine") == bc.base_quanta("guanine") + bc.base_quanta("cytosine")


def test_functional_groups_match_additive_topology():
    # A functional group's quanta must equal the additive atomic-topology sum (the same rule as
    # any compound), so functional_group_quanta() agrees with molecule_quanta() for every group.
    from tetryonics import biochem as bc
    for g in ("CH", "CH2", "CH3", "OH", "NH2", "NO2", "NO3"):
        assert bc.functional_group_quanta(g) == bc.molecule_quanta(g), g
    # plate-anchored values (glucose p408 / TNT p402 sub-units)
    assert bc.functional_group_quanta("CH3") == 648   # C+3H = 504+144
    assert bc.functional_group_quanta("OH") == 720     # O+H  = 672+48
    assert bc.molecule_quanta("C6H12O6") == 7632       # glucose unchanged


def test_balance_reaction():
    # Conserving atoms = conserving charge-π topology (Book 3 p.383).
    assert el.balance_reaction(["H2", "O2"], ["H2O"]) == {"H2": 2, "O2": 1, "H2O": 2}
    assert el.balance_reaction(["CH4", "O2"], ["CO2", "H2O"]) == {"CH4": 1, "O2": 2, "CO2": 1, "H2O": 2}
    assert el.balance_reaction(["Fe", "O2"], ["Fe2O3"]) == {"Fe": 4, "O2": 3, "Fe2O3": 2}
    assert el.reaction_conserves_topology(["CH4", "O2"], ["CO2", "H2O"])


def test_neutralisation():
    # Acid + hydroxide base → salt + water, balanced (Book 3 p.379).
    hcl = el.neutralise("HCl", "NaOH")
    assert hcl["salt"] == "NaCl" and hcl["conserves_topology"]
    h2so4 = el.neutralise("H2SO4", "NaOH")
    assert h2so4["coefficients"]["NaOH"] == 2 and h2so4["salt"] == "Na2SO4"
    cano3 = el.neutralise("HNO3", "CaO2H2")          # → Ca(NO3)2
    assert cano3["coefficients"]["HNO3"] == 2 and cano3["conserves_topology"]


def test_hydrogen_radical_and_bond_quanta():
    # Book 3 p.385: H = 48π [24·24]; H₂ = 96π.
    h = el.hydrogen_radical()
    assert h["topology_pi"] == 48 and h["cw"] == 24 and h["ccw"] == 24 and h["net_charge_e"] == 0
    assert el.hydrogen_bond_quanta(2) == 96
    assert el.molecule_topology_pi("H2") == 96      # consistency with the molecule engine


def test_polyatomic_ions():
    oh = el.polyatomic_ion("hydroxide")
    assert oh["formula"] == "OH" and oh["charge_e"] == -1 and oh["charge_quanta"] == -12
    assert oh["topology_pi"] == el.molecule_topology_pi("OH")   # = 720π
    assert el.polyatomic_ion("phosphate")["charge_quanta"] == -36   # PO₄³⁻ = 3×(−12)
    assert el.polyatomic_ion("ammonium")["charge_e"] == 1


def test_lewis_from_formula():
    # Kelvin's tabulated p.370 shapes come back exact; hydrides auto-derive correctly.
    assert el.lewis_structure("H2O")["shape"] == "bent" and el.lewis_structure("H2O")["exact"]
    assert el.lewis_structure("CH4")["shape"] == "tetrahedral"
    assert el.lewis_structure("CO2")["shape"] == "linear"
    ph3 = el.lewis_structure("PH3")
    assert ph3["central"] == "P" and ph3["shape"] == "trigonal pyramidal"


def test_ionic_bond_charge_transfer():
    # Book 3 p.380: Na donates 1 e (→ +12 charge-quanta), Cl accepts 1 (→ −12); NaCl neutral.
    nacl = el.ionic_bond("Na", "Cl")
    assert nacl["cation_charge_e"] == 1 and nacl["cation_charge_quanta"] == 12
    assert nacl["anion_charge_e"] == -1 and nacl["anion_charge_quanta"] == -12
    assert nacl["net_charge_e"] == 0
    assert el.ion_charge_quanta(2) == 24          # an electron = 12 charge-quanta


def test_co2_topology():
    # CO2 = 504 + 2*672 = 1848
    assert el.molecule_topology_pi("CO2") == 1848


# --- Nuclear energy-level mass model (Book 3 p.83 & p.92) --------------------
def test_nuclear_shells_follow_electron_aufbau():
    # Deuterons occupy the SAME shells as the electrons (Aufbau/Madelung), NOT a
    # naive cap-cascade. Uranium: K2 L8 M18 N32 O22 P8 Q2 (= its electron shells).
    shells = el.nuclear_shell_fill(92)
    assert {s.letter: s.deuterons for s in shells} == {
        "K": 2, "L": 8, "M": 18, "N": 32, "O": 22, "P": 8, "Q": 2}
    assert sum(s.deuterons for s in shells) == 92


def test_k_shell_deuteron_is_two_baryons():
    # A ground-level (K) Deuteron = proton + neutron = 2 baryon rest energies.
    assert close(el.DEUTERON_SHELL_MEV[1], 2 * K.BARYON_MEV, rel=1e-4)
    # Outer (R) Deuteron scales as ((24+8)/25)^2 -> the plate's 3050.6 MeV.
    assert close(el.DEUTERON_SHELL_MEV[8], 3050.6, rel=1e-3)


def test_shell_mass_reproduces_kelvins_element_pages():
    # The energy-level mass must match the figure printed on each Book 3 element page.
    # 13 elements spanning every block (s/p/d/f), noble gases, lanthanide & actinides —
    # all read directly off Kelvin's pages; locks the Madelung shell-filling edge cases.
    his_pages = {
        6: 12.6493, 8: 16.9744, 10: 21.2996, 18: 39.9563, 26: 58.9648, 36: 83.3412,
        47: 111.2937, 60: 145.7335, 74: 181.5746, 79: 195.0261, 82: 203.4744,
        90: 226.5192, 92: 231.8998,
    }
    for z, his in his_pages.items():
        assert close(el.nuclear_mass_amu(z), his, rel=2e-4), (z, el.nuclear_mass_amu(z), his)


def test_shell_mass_beats_flat_for_heavy_elements():
    # The flat ground-state floor undershoots his published heavy masses; the
    # energy-level model lands on them (via higher n, NOT extra neutrons).
    flat = el.element(92).mass_amu          # ~184 (all deuterons at K)
    shell = el.nuclear_mass_amu(92)         # ~231.9 (his page value)
    assert flat < 190
    assert abs(shell - 231.8998) < abs(flat - 231.8998)


def test_atom_exposes_shell_mass():
    au = el.element(79)
    assert close(au.shell_mass_amu, el.nuclear_mass_amu(79))
    assert au.shell_mass_amu > au.mass_amu     # outer deuterons are heavier


def test_molecule_energy_level_mass_and_composition():
    # A compound's energy-level mass = Σ its atoms' his-book masses.
    assert close(el.molecule_nuclear_mass_amu("H2O"),
                 2 * el.nuclear_mass_amu(1) + el.nuclear_mass_amu(8))
    assert el.molecule_topology_pi("C6H12O6") == 7632          # glucose
    assert close(el.molecule_nuclear_mass_amu("C6H12O6"),
                 6 * el.nuclear_mass_amu(6) + 12 * el.nuclear_mass_amu(1)
                 + 6 * el.nuclear_mass_amu(8))
    comp = el.molecule_composition("H2O")
    assert {r["symbol"]: r["count"] for r in comp} == {"H": 2, "O": 1}
    assert all("shell_mass_amu" in r and "topology_pi" in r for r in comp)


# ===== from test_coverage2.py (Book 3 subset) ================================

# --- Book 3 bonding & periodic position --------------------------------------
def test_period():
    assert el.period(1) == 1 and el.period(2) == 1   # H, He -> shell 1
    assert el.period(3) == 2                          # Li -> shell 2
    assert el.period(11) == 3                         # Na -> shell 3


def test_bond_order_and_sigma_pi():
    assert el.bond_order(2) == 1 and el.bond_order(4) == 2 and el.bond_order(6) == 3
    assert el.sigma_pi_bonds(1) == (1, 0)
    assert el.sigma_pi_bonds(2) == (1, 1)
    assert el.sigma_pi_bonds(3) == (1, 2)
    assert el.shared_electrons_for_bond(3) == 6


def test_allotrope_invariant():
    assert el.allotrope_topology_pi(6) == 504    # carbon, any allotrope


# ===== from test_api.py (Book 3 subset) ======================================

# --- chemistry / biochem -----------------------------------------------------
def test_chem_api():
    assert el.valence(79) == 11 and el.valence(80) == 2     # Au, Hg
    assert el.element_quanta(8) == 672
    assert el.ion(11, 1).net_charge_e == 1                  # Na+
    assert el.acid("sulfuric") == "H2SO4"
    assert close(el.molar_mass(6), el.element(6).mass_amu)
    assert el.ionization_energy(1) == el.ionisation_energy(1)
    assert biochem.base_quanta("adenine") == biochem.molecule_quanta("C5H5N5")
    assert biochem.nucleotide_quanta("adenine", deoxy=True) > 0


# ===== from test_audit.py (Book 3 subset) ====================================

# --- Book 3 chemistry additions ----------------------------------------------
def test_periodic_caps_and_max_z():
    assert el.periodic_shell_cap(4) == 32 and el.periodic_shell_cap(5) == 32
    try:
        el.element(121)
        assert False, "should cap at Z=120"
    except ValueError:
        pass


def test_valence_block_family():
    assert el.valence_electrons(8) == 6          # oxygen
    assert el.valence_electrons(11) == 1         # sodium
    assert el.element_block(26) == "d"           # iron, d-block
    assert el.element_family(2) == "Noble gas"   # helium
    assert el.element_family(9) == "Halogen"     # fluorine


def test_atoms_per_kg_and_deuterium_div():
    assert close(el.atoms_per_kg(1), 1 / el.element(1).mass_kg)
    assert el.divides_into_deuterium_units("CO2") is True    # 1848 = 22*84
    assert el.divides_into_deuterium_units("H2O") is False   # 768 not /84


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
