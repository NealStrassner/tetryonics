"""
Thermodynamics & entropy — appears across Books 2 & 4 (blackbody, stellar, vacuum energy).

Tetryonics treats temperature/entropy statistically over the same Planck energy quanta.
The black-hole Bekenstein–Hawking entropy is included as the entropy of a GEM-pinch
horizon (Kelvin's pinch, not a singularity). Boltzmann's constant is statistical, not a
Tetryonic geometric constant.
"""

from __future__ import annotations

import math

from . import constants as K


def entropy_boltzmann(microstates: float) -> float:
    """Boltzmann entropy  S = k_B · ln(W)  (J/K)."""
    return K.BOLTZMANN * math.log(microstates)


def entropy_clausius(heat_j: float, temperature_k: float) -> float:
    """Clausius entropy change  ΔS = Q/T  (J/K)."""
    return heat_j / temperature_k


def ideal_gas_pressure(moles: float, temperature_k: float, volume_m3: float) -> float:
    """Ideal-gas law  P = nRT/V  (Pa)."""
    return moles * K.GAS_CONSTANT * temperature_k / volume_m3


def thermal_energy(temperature_k: float) -> float:
    """Characteristic thermal energy per degree of freedom  E = k_B·T  (J)."""
    return K.BOLTZMANN * temperature_k


def bekenstein_hawking_entropy(area_m2: float) -> float:
    """Horizon entropy  S = A·k_B·c³/(4·G·ħ)  (J/K) — the GEM-pinch horizon entropy."""
    h_bar = K.H / (2 * math.pi)
    return area_m2 * K.BOLTZMANN * K.C**3 / (4 * K.G * h_bar)


def ideal_gas_volume(moles: float, temperature_k: float, pressure_pa: float) -> float:
    """Ideal-gas volume  V = nRT/P  (m³)."""
    return moles * K.GAS_CONSTANT * temperature_k / pressure_pa


def ideal_gas_temperature(pressure_pa: float, volume_m3: float, moles: float) -> float:
    """Ideal-gas temperature  T = PV/(nR)  (K)."""
    return pressure_pa * volume_m3 / (moles * K.GAS_CONSTANT)


def ideal_gas_moles(pressure_pa: float, volume_m3: float, temperature_k: float) -> float:
    """Ideal-gas amount  n = PV/(RT)  (mol)."""
    return pressure_pa * volume_m3 / (K.GAS_CONSTANT * temperature_k)


def pressure_energy_density(energy_j: float, volume_m3: float) -> float:
    """Pressure as energy density  P = E/V  (Pa) — Book 4 p.91 (P = F/A = E/V)."""
    return energy_j / volume_m3


def internal_energy(moles: float, temperature_k: float, dof: int = 3) -> float:
    """Internal energy of an ideal gas  U = (dof/2)·nRT  (J)."""
    return (dof / 2.0) * moles * K.GAS_CONSTANT * temperature_k


def carnot_efficiency(t_hot: float, t_cold: float) -> float:
    """Maximum (Carnot) efficiency  η = 1 − T_cold/T_hot."""
    return 1.0 - t_cold / t_hot
