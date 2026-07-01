"""
Kinematics & classical mechanics — recurring across all books (v=Δx/Δt, F=ma, SHM).

Tetryonics keeps the classical relations exactly (it reinterprets their geometry, not
their algebra). Note the Tetryonic energy convention is E = m·v² (not ½mv²); kinetic
energy is ½mv² as usual — both are provided.
"""

from __future__ import annotations

import math


def velocity(displacement: float, time: float) -> float:
    """v = Δx/Δt."""
    return displacement / time


def acceleration(delta_v: float, time: float) -> float:
    """a = Δv/Δt."""
    return delta_v / time


def force(mass: float, accel: float) -> float:
    """Newton's 2nd law  F = m·a."""
    return mass * accel


def momentum(mass: float, vel: float) -> float:
    """p = m·v."""
    return mass * vel


def impulse(force_n: float, time: float) -> float:
    """Impulse  J = F·Δt = Δp."""
    return force_n * time


def work(force_n: float, distance: float) -> float:
    """Work  W = F·d."""
    return force_n * distance


def power(work_j: float, time: float) -> float:
    """Power  P = W/t."""
    return work_j / time


def kinetic_energy(mass: float, vel: float) -> float:
    """⚠ Classical ½·m·v² — NOT Kelvin's primary form. His scalar mass-energy is
    E = m·v² (energy.scalar_energy); ½mv² is only the KEM-field-in-motion energy.
    Kept for classical comparison."""
    return 0.5 * mass * vel * vel


def centripetal_acceleration(vel: float, radius: float) -> float:
    """a_c = v²/r."""
    return vel * vel / radius


# --- simple harmonic motion (Book 5 p.227, F = -kx) --------------------------
def shm_restoring_force(spring_constant: float, displacement: float) -> float:
    """Hooke's law / SHM restoring force  F = −k·x."""
    return -spring_constant * displacement


def shm_period(mass: float, spring_constant: float) -> float:
    """SHM period  T = 2π·√(m/k)."""
    return 2 * math.pi * math.sqrt(mass / spring_constant)


def shm_frequency(mass: float, spring_constant: float) -> float:
    """SHM frequency  f = 1/T."""
    return 1.0 / shm_period(mass, spring_constant)
