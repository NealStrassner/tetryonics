"""
Electricity — Book 2 (Electrodynamics).

In Tetryonics: charge is mass·QAM/second (kg·s), current is charged Matter in motion
(kg/s), and voltage is the net energy-momenta of a charge geometry (the potential to do
work). The numeric relationships are the familiar ones — Tetryonic geometry agrees with
the established electrical math, it just gives them a physical (triangle) picture.

    Ohm's law      V = I·R
    Power          P = V·I = I²·R = V²/R
    Work/energy    W = q·V              (E = charge × voltage)
    Capacitor      Q = C·V ,  E = ½C·V²
    Inductor       E = ½L·I²
    electron-volt  1 eV = e × 1 V
"""

from __future__ import annotations

from . import constants as K


# --- Ohm's law ----------------------------------------------------------------
def voltage(current_a: float, resistance_ohm: float) -> float:
    """V = I·R."""
    return current_a * resistance_ohm


def current(voltage_v: float, resistance_ohm: float) -> float:
    """I = V/R."""
    return voltage_v / resistance_ohm


def resistance(voltage_v: float, current_a: float) -> float:
    """R = V/I."""
    return voltage_v / current_a


# --- power --------------------------------------------------------------------
def power_vi(voltage_v: float, current_a: float) -> float:
    """P = V·I (watts)."""
    return voltage_v * current_a


def power_i2r(current_a: float, resistance_ohm: float) -> float:
    """P = I²·R."""
    return current_a * current_a * resistance_ohm


def power_v2r(voltage_v: float, resistance_ohm: float) -> float:
    """P = V²/R."""
    return voltage_v * voltage_v / resistance_ohm


# --- work / energy ------------------------------------------------------------
def electrical_work(charge_c: float, voltage_v: float) -> float:
    """Energy moved by pushing charge through a potential:  W = q·V (J)."""
    return charge_c * voltage_v


def electron_volt_to_joules(ev: float) -> float:
    """1 eV = e joules."""
    return ev * K.ELEMENTARY_CHARGE


def joules_to_electron_volt(joules: float) -> float:
    return joules / K.ELEMENTARY_CHARGE


# --- capacitance / inductance -------------------------------------------------
def capacitor_charge(capacitance_f: float, voltage_v: float) -> float:
    """Q = C·V."""
    return capacitance_f * voltage_v


def capacitor_energy(capacitance_f: float, voltage_v: float) -> float:
    """E = ½·C·V²."""
    return 0.5 * capacitance_f * voltage_v * voltage_v


def inductor_energy(inductance_h: float, current_a: float) -> float:
    """E = ½·L·I²."""
    return 0.5 * inductance_h * current_a * current_a


def lc_resonance(inductance_h: float, capacitance_f: float) -> float:
    """LC tank resonant frequency  f = 1/(2π√(LC))."""
    import math
    return 1.0 / (2 * math.pi * math.sqrt(inductance_h * capacitance_f))


def capacitance_from_charge(charge_c: float, voltage_v: float) -> float:
    """C = Q/V (farads)."""
    return charge_c / voltage_v


def parallel_plate_capacitance(area_m2: float, separation_m: float,
                               rel_permittivity: float = 1.0) -> float:
    """Parallel-plate capacitance  C = ε·A/d  (F)."""
    return rel_permittivity * K.EPSILON_0 * area_m2 / separation_m


# --- Electromagnetic induction (Faraday / Henry) -----------------------------
def faraday_emf(d_flux: float, dt: float, turns: int = 1) -> float:
    """Induced EMF  ε = −N·dΦ/dt  (V)."""
    return -turns * d_flux / dt


def inductor_emf(inductance_h: float, d_current: float, dt: float) -> float:
    """Self-induced EMF across an inductor  v = −L·di/dt  (V)."""
    return -inductance_h * d_current / dt


def displacement_current(d_e_flux: float, dt: float) -> float:
    """Maxwell's displacement current  I_D = ε₀·dΦ_E/dt  (A)."""
    return K.EPSILON_0 * d_e_flux / dt


# --- AC reactance & impedance ------------------------------------------------
def reactance_capacitive(frequency_hz: float, capacitance_f: float) -> float:
    """Capacitive reactance  X_C = 1/(2π·f·C)  (Ω)."""
    import math
    return 1.0 / (2 * math.pi * frequency_hz * capacitance_f)


def reactance_inductive(frequency_hz: float, inductance_h: float) -> float:
    """Inductive reactance  X_L = 2π·f·L  (Ω)."""
    import math
    return 2 * math.pi * frequency_hz * inductance_h


def impedance(resistance_ohm: float, x_l: float = 0.0, x_c: float = 0.0) -> float:
    """Series RLC impedance  Z = √(R² + (X_L − X_C)²)  (Ω)."""
    import math
    return math.sqrt(resistance_ohm**2 + (x_l - x_c) ** 2)


def rc_time_constant(resistance_ohm: float, capacitance_f: float) -> float:
    """RC time constant  τ = R·C  (s)."""
    return resistance_ohm * capacitance_f


def lr_time_constant(inductance_h: float, resistance_ohm: float) -> float:
    """L/R time constant  τ = L/R  (s)."""
    return inductance_h / resistance_ohm


def resistivity_field(resistivity: float, current_density: float) -> float:
    """Microscopic Ohm's law  E = ρ·J  (V/m)."""
    return resistivity * current_density


def drift_velocity(current_a: float, number_density: float, area_m2: float,
                   charge_c: float = K.ELEMENTARY_CHARGE) -> float:
    """Electron drift velocity  v_d = I/(n·q·A)  (m/s)."""
    return current_a / (number_density * charge_c * area_m2)


def ev_to_kj_per_mole(ev: float) -> float:
    """Convert eV/particle to kJ/mol  (1 eV ≈ 96.5 kJ/mol)."""
    return ev * K.EV_KJ_PER_MOLE


def kj_per_mole_to_ev(kj_mol: float) -> float:
    """Convert kJ/mol to eV/particle."""
    return kj_mol / K.EV_KJ_PER_MOLE
