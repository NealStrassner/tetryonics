"""
Tetryonics — a computational engine for Kelvin Abraham's Tetryonic geometry.

Build physics out of equilateral triangles: particles, charges, masses, fields,
energy levels and elements all derive from one geometric quantum.

This package is intended as a reusable *engine* — other tools and apps can import it
and call into the core mechanics rather than re-deriving them.

Submodules
----------
    constants  -- the verified Tetryonics constant set
    geometry   -- the equilateral-triangle / fascia / tetryon engine
    energy     -- mass / energy / momentum / QAM mechanics
    charge     -- charge geometry & topology bookkeeping
    fields     -- ElectroMagnetic fields & forces (Coulomb, Biot-Savart, Lorentz)
    levels     -- quantum energy levels, electron shells, spectra
    electrical -- electricity (Ohm, power, capacitance, inductance) [Book 2]
    waves      -- EM waves & photons (λ/f, wavenumber, Euler phase, Compton) [Book 2]
    spectra    -- named hydrogen spectral series (Lyman..Abraham) [Book 2]
    radiation  -- blackbody / thermal radiation (Planck, Wien, Stefan-Boltzmann) [Book 2]
    particles  -- the particle/quantum builder (quarks, leptons, baryons)
    elements   -- the element / periodic engine + chemistry (shells, compounds) [Book 3]
    cosmology  -- gravitation & GEM fields (G+SR=GR, orbits, escape velocity) [Book 4]
    geometrics -- Platonic-solid topologies & equilateral maths [Book 5]
    units      -- the Tetryonic physics-units map + colour codes

Quick start
-----------
    >>> import tetryonics as t
    >>> t.proton().charge_e
    1.0
    >>> t.energy.em_mass(t.constants.H)        # mass of one Planck quantum
    7.376e-51
    >>> t.element(6).mass_amu                  # carbon
    11.99...
"""

from __future__ import annotations

from . import (
    constants, geometry, energy, charge, fields, levels,
    particles, elements, units, electrical, waves, spectra,
    radiation, cosmology, geometrics, optics, thermodynamics, statistics,
    numbertheory, music, biochem, kinematics, dynamics, matter,
)

# Re-export the most-used builders / helpers at the top level.
from .geometry import (
    Fascia, Tetryon,
    positive_tetryon, negative_tetryon, neutral_tetryon,
    units_in_triangle, units_in_row, is_square, equilateral_area, level_colour,
)
from .particles import (
    Particle, quark, electron, positron, neutrino,
    proton, neutron, anti_proton, baryon, standard_particles,
    particle, from_quanta, meson,
)
from .elements import (
    Atom, element, hydrogen, deuterium, tritium, isotope, periodic_table,
)

__version__ = "0.13.0"
__author__ = "Built on the Tetryonic geometry of Kelvin Abraham (used with permission)"

__all__ = [
    # submodules
    "constants", "geometry", "energy", "charge", "fields", "levels",
    "particles", "elements", "units", "electrical", "waves", "spectra",
    "radiation", "cosmology", "geometrics", "optics", "thermodynamics", "statistics",
    "numbertheory", "music", "biochem", "kinematics", "dynamics", "matter",
    # geometry
    "Fascia", "Tetryon", "positive_tetryon", "negative_tetryon", "neutral_tetryon",
    "units_in_triangle", "units_in_row", "is_square", "equilateral_area", "level_colour",
    # particles
    "Particle", "quark", "electron", "positron", "neutrino",
    "proton", "neutron", "anti_proton", "baryon", "standard_particles",
    # elements
    "Atom", "element", "hydrogen", "deuterium", "tritium", "isotope", "periodic_table",
]
