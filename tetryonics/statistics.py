"""
Statistics & quantum probability — Books 1 & 2 (EM-wavefunction distributions, uncertainty).

In Tetryonics the "probabilities" of QM are the geometric distribution of Planck quanta
across the equilateral energy levels (the Born rule P = |amplitude|², Gaussian and binomial
distributions, Heisenberg's relations). These are exact, not fuzzy — the spread is the
real distribution of energy momenta in a waveform.
"""

from __future__ import annotations

import math

from . import constants as K

H_BAR = K.H / (2 * math.pi)


def born_rule(amplitude: float) -> float:
    """Probability/intensity = |amplitude|²  (the EM wavefunction Born rule)."""
    return abs(amplitude) ** 2


def gaussian(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal distribution  P(x) = 1/(σ√2π)·exp(−(x−μ)²/2σ²)."""
    return (1.0 / (sigma * math.sqrt(2 * math.pi))
            * math.exp(-((x - mu) ** 2) / (2 * sigma * sigma)))


def binomial_probability(n: int, k: int, p: float) -> float:
    """Binomial probability  C(n,k)·pᵏ·(1−p)ⁿ⁻ᵏ."""
    return math.comb(n, k) * p**k * (1 - p) ** (n - k)


def heisenberg_min_momentum(delta_x: float) -> float:
    """Minimum momentum spread from position spread  Δp ≥ ħ/(2·Δx)."""
    return H_BAR / (2 * delta_x)


def heisenberg_min_energy(delta_t: float) -> float:
    """Minimum energy spread from time spread  ΔE ≥ ħ/(2·Δt)."""
    return H_BAR / (2 * delta_t)


def shannon_entropy(probabilities) -> float:
    """Shannon information entropy  H = −Σ pᵢ·log₂(pᵢ)  (bits)."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def normal_empirical_rule() -> tuple:
    """The 68–95–99.7 rule: fraction of a normal distribution within 1, 2, 3 σ."""
    return (0.6827, 0.9545, 0.9973)


def standard_deviation(values) -> float:
    """Population standard deviation σ = √(Σ(x−μ)²/N)."""
    n = len(values)
    mu = sum(values) / n
    return math.sqrt(sum((x - mu) ** 2 for x in values) / n)


def z_score(x: float, mu: float, sigma: float) -> float:
    """Standard score  z = (x − μ)/σ."""
    return (x - mu) / sigma
