"""
Book 2 — Electrodynamics (electrical, waves, spectra, relativity, radiation,
fine-structure, induction/optics, hydrogen/Rydberg spectral lines, EM constants).
NOTE: in this file the alias `el` means `electrical` (Book 2's convention).
Run:  python tests/test_book2_electrodynamics.py
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tetryonics as t
from tetryonics import (constants as K, electrical, waves, spectra, energy, fields,
                        levels, radiation, optics, thermodynamics as thermo,
                        cosmology as cos, kinematics as kin)
el = electrical


def close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel)


# ===== from test_book2.py ====================================================

# --- electrical ---------------------------------------------------------------
def test_ohms_law():
    assert close(el.voltage(2, 5), 10)
    assert close(el.current(10, 5), 2)
    assert close(el.resistance(10, 2), 5)


def test_power_three_ways_agree():
    v, i, r = 12.0, 3.0, 4.0   # consistent V=IR
    assert close(el.power_vi(v, i), 36)
    assert close(el.power_i2r(i, r), 36)
    assert close(el.power_v2r(v, r), 36)


def test_electron_volt():
    assert close(el.electron_volt_to_joules(1.0), K.ELEMENTARY_CHARGE)
    assert close(el.joules_to_electron_volt(K.ELEMENTARY_CHARGE), 1.0)


def test_capacitor_inductor_energy():
    assert close(el.capacitor_charge(2, 3), 6)
    assert close(el.capacitor_energy(2, 3), 9)      # 1/2 * 2 * 9
    assert close(el.inductor_energy(2, 3), 9)       # 1/2 * 2 * 9
    assert el.lc_resonance(1e-3, 1e-6) > 0


# --- waves --------------------------------------------------------------------
def test_wave_relations():
    f = 5e14
    lam = waves.wavelength(f)
    assert close(waves.frequency(lam), f)
    assert close(waves.wavenumber(lam), 1 / lam)
    assert close(waves.photon_energy_from_frequency(f),
                 waves.photon_energy_from_wavelength(lam))


def test_inverse_square():
    assert close(waves.inverse_square(100, 2), 25)


def test_euler_phase():
    z = waves.euler_phase(math.pi)
    assert close(z.real, -1.0, rel=1e-9) and abs(z.imag) < 1e-9
    assert close(waves.photon_phase_offset(1), math.pi / 2)


def test_compton_shift_electron():
    # max shift at 180 deg = 2 * Compton wavelength ~ 4.85e-12 m
    dl = waves.compton_shift(math.pi)
    assert close(dl, 2 * K.H / ((K.N_ELECTRON * K.M_Q) * K.C))


# --- spectra ------------------------------------------------------------------
def test_series_lower_levels():
    assert spectra.series_lower_level("lyman") == 1
    assert spectra.series_lower_level("balmer") == 2
    assert spectra.series_lower_level("abraham") == 7


def test_balmer_alpha_his_660nm():
    # His Tetryonic Rydberg gives Balmer-α = 660 nm (observed = 656.5; ~0.6% Tetryonic offset).
    lam = spectra.line_wavelength("balmer", 3)   # H-alpha
    assert close(lam * 1e9, 660.35, rel=1e-3)


def test_lyman_alpha_his_122nm():
    lam = spectra.line_wavelength("lyman", 2)
    assert close(lam * 1e9, 122.29, rel=2e-3)


def test_quanta_differential():
    assert [spectra.quanta_differential(n) for n in range(1, 6)] == [12, 36, 60, 84, 108]


def test_series_lines_shape():
    lines = spectra.series_lines("balmer", 3)
    assert len(lines) == 3 and "wavelength_nm" in lines[0]


# ===== from test_engine.py (Book 2 subset) ===================================

def test_hydrogen_energies():
    # His KEM ground 13.525 eV (Book 3 p.75 eigenstates −13.525/n²), NOT standard 13.6.
    assert close(levels.hydrogen_energy(1), -13.525)
    assert close(levels.hydrogen_energy(2), -13.525 / 4)
    assert close(levels.ionization_energy(1), 13.525)


def test_rydberg_balmer_alpha():
    # His Tetryonic Rydberg (R_H = c/27.49545, Book 2 p.118) -> Balmer-α = 660 nm.
    assert close(levels.rydberg_wavelength(2, 3), 660.35e-9, rel=1e-3)
    # The empirical/observed Rydberg reproduces the measured 656.5 nm (comparison).
    assert close(levels.rydberg_wavelength(2, 3, observed=True), 656.5e-9, rel=1e-3)


# ===== from test_mining.py (Book 2 subset) ===================================

# --- new EM constants --------------------------------------------------------
def test_em_constants():
    assert close(fields.ampere_constant(), 2e-7)
    assert close(fields.impedance_of_free_space(), 376.73, rel=1e-3)
    assert close(K.ELECTRONS_PER_COULOMB, 1 / K.ELEMENTARY_CHARGE)
    assert close(K.EV_KJ_PER_MOLE, 96.5, rel=2e-2)
    assert close(fields.longitudinal_velocity(), (math.pi / 2) * K.C)
    assert close(K.TAU, 2 * math.pi)


# --- waves / optics ----------------------------------------------------------
def test_compton_frequency_and_recoil():
    m = K.N_ELECTRON * K.M_Q
    assert close(waves.compton_frequency(m), m * K.C2 / K.H)
    assert close(waves.vacuum_energy_wavelength(1.0, 2), 1.0 / 8)   # λ/(2·4)
    # recoil: total energy = rest energy -> zero momentum
    assert close(optics.recoil_momentum(m * K.C2 * 2, m), math.sqrt(3) * m * K.C, rel=1e-9)


# --- spectra: Tetryonic per-series divisors ----------------------------------
def test_series_rydberg_divisors():
    assert close(spectra.series_rydberg_divisor("lyman"), 27.49545417)
    assert close(spectra.series_rydberg_divisor("balmer"), 27.49545417 * 4)
    assert close(spectra.series_rydberg_divisor("paschen"), 27.49545417 * 9)
    assert spectra.series_shell_quanta("balmer") == 48     # 12 * 2^2
    assert close(spectra.rydberg_factor(2, 3), 1 / 4 - 1 / 9)


# ===== from test_books345.py (Book 2 subset) =================================

# --- relativity (Book 2 additions) -------------------------------------------
def test_time_dilation_and_length_contraction():
    v = 0.8 * K.C
    assert close(energy.time_dilation(1.0, v), 1.0 / 0.6)     # gamma = 1.6667
    assert close(energy.length_contraction(1.0, v), 0.6)


def test_relativistic_energy_reduces_to_rest():
    m = 9.11e-31
    assert close(energy.relativistic_energy(0.0, m), m * K.C2)


# --- fine-structure constant -------------------------------------------------
def test_fine_structure_tetryonic_is_2pi_omega():
    assert close(fields.fine_structure_constant(), 2 * math.pi * K.OMEGA)
    assert close(fields.fine_structure_constant(), 0.007539822, rel=1e-6)
    assert close(1 / fields.fine_structure_constant(), 132.629, rel=1e-4)
    # the empirical value is available too
    assert close(fields.fine_structure_constant(tetryonic=False), 1 / 137.036, rel=1e-3)


# --- radiation ----------------------------------------------------------------
def test_wien_peak_sun():
    # Sun ~5772 K peaks ~502 nm
    assert close(radiation.wien_peak_wavelength(5772) * 1e9, 502, rel=1e-2)


def test_stefan_boltzmann_scales_as_t4():
    p1 = radiation.stefan_boltzmann_power(300)
    p2 = radiation.stefan_boltzmann_power(600)
    assert close(p2 / p1, 16.0)


def test_planck_radiance_positive():
    assert radiation.planck_spectral_radiance(500e-9, 5000) > 0


# ===== from test_coverage2.py (Book 2 subset) ================================

# --- Book 2 optics (faithful: only what's on the plates) ---------------------
def test_reflection_and_refraction():
    assert optics.reflection_angle(0.4) == 0.4
    assert close(optics.wavelength_in_medium(600e-9, 1.5), 400e-9)
    assert close(optics.amplitude_from_intensity(9.0), 3.0)
    assert close(optics.superpose(1, 2, -0.5), 2.5)


# ===== from test_api.py (Book 2 subset) ======================================

# --- electrical reactances ---------------------------------------------------
def test_reactance_impedance():
    xl = electrical.reactance_inductive(60, 0.1)
    xc = electrical.reactance_capacitive(60, 1e-4)
    assert close(xl, 2 * math.pi * 60 * 0.1)
    assert electrical.impedance(3, 4, 0) == 5.0
    assert electrical.rc_time_constant(1000, 1e-6) == 1e-3
    assert close(electrical.ev_to_kj_per_mole(1), K.EV_KJ_PER_MOLE)


# --- radiation / thermo extras ----------------------------------------------
def test_radiation_thermo():
    assert radiation.wien_peak_frequency(5772) > 0
    assert radiation.photon_flux(1.0, 5e14) > 0
    assert close(thermo.carnot_efficiency(400, 300), 0.25)
    assert close(thermo.ideal_gas_volume(1, 273.15, 101325), 0.0224, rel=1e-2)
    assert close(thermo.pressure_energy_density(100, 4), 25)


# ===== from test_audit.py (Book 2 subset) ====================================

# --- Book 2 induction / capacitance / optics ---------------------------------
def test_induction_and_capacitance():
    assert close(electrical.faraday_emf(2.0, 0.5, turns=10), -40.0)
    assert close(electrical.inductor_emf(2.0, 3.0, 1.5), -4.0)
    assert close(electrical.capacitance_from_charge(6.0, 3.0), 2.0)
    assert electrical.parallel_plate_capacitance(1.0, 1e-3) > 0


def test_optics():
    assert close(optics.refractive_index(optics.phase_velocity(1.5)), 1.5)
    # snell: light entering denser medium bends toward normal
    assert optics.snell(1.0, math.radians(30), 1.5) < math.radians(30)
    assert close(optics.photoelectric_ke(1e15, 0.0), K.H * 1e15)
    assert optics.photoelectric_ke(1e10, 1e-18) == 0.0   # below threshold
    assert optics.pair_production_threshold() > 0


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
