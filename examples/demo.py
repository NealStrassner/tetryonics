"""Demo: print the particle table, the element rule, and the headline proofs."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tetryonics as t
from tetryonics import constants as K


def main() -> None:
    print(K.summary())

    print("\nStandard particles")
    print("-" * 18)
    for p in t.standard_particles():
        print(p.describe())

    print("\nElements (deuterium stacking)")
    print("-" * 29)
    for atom in t.periodic_table(10):
        print(atom.describe())
    print(t.deuterium().describe())
    print(t.tritium().describe())

    print("\nHeadline proofs (computed, not typed in)")
    print("-" * 40)
    print(f"electron mass     {t.electron().mass_kg:.6e} kg")
    print(f"proton mass       {t.proton().mass_kg:.6e} kg")
    print(f"Mp/Me ratio       {t.proton().mass_kg / t.electron().mass_kg:.0f}")
    print(f"hydrogen mass     {t.hydrogen().mass_kg:.6e} kg  ({t.hydrogen().mass_amu:.4f} amu)")
    print(f"up quark charge   {t.quark('up').charge_e:+.4f} e")
    print(f"down quark charge {t.quark('down').charge_e:+.4f} e")
    print(f"proton charge     {t.proton().charge_e:+.0f} e   {t.proton().topology_charge}")
    print(f"neutron charge    {t.neutron().charge_e:+.0f} e   {t.neutron().topology_charge}")
    print(f"elementary charge {K.ELEMENTARY_CHARGE:.6e} C (= 12 x {K.CHARGE_QUANTUM:.4e})")

    print("\nEngine mechanics (calling the modules)")
    print("-" * 38)
    print(f"mass of 1 Planck quantum   E/c^2 = {t.energy.em_mass(K.H):.4e} kg")
    print(f"3D Matter of that quantum  E/c^4 = {t.energy.matter(K.H):.4e} kg/m^3")
    print(f"Lorentz gamma at 0.8c            = {t.energy.gamma(0.8 * K.C):.4f}")
    print(f"c from 1/sqrt(eps0*mu0)          = {t.fields.speed_of_light_from_constants():.0f} m/s")
    print(f"Coulomb force e-e at 1 angstrom  = {t.fields.coulomb_force(K.ELEMENTARY_CHARGE, K.ELEMENTARY_CHARGE, 1e-10):.4e} N")
    print(f"H-alpha line (Rydberg n3->n2)    = {t.levels.rydberg_wavelength(2, 3) * 1e9:.1f} nm")
    print("hydrogen levels (eV):           ",
          [round(t.levels.hydrogen_energy(n), 3) for n in range(1, 6)])
    print("electron-shell quanta 12*n^2:   ",
          [t.levels.shell_quanta(n) for n in range(1, 9)])

    print("\nBooks 2-5 engine (electricity, spectra, chemistry, cosmology, geometry)")
    print("-" * 70)
    print(f"Ohm: 12V/4ohm -> {t.electrical.current(12, 4)} A, "
          f"power V^2/R = {t.electrical.power_v2r(12, 4)} W")
    print("Balmer visible lines (nm):      ",
          [round(t.spectra.line_wavelength('balmer', n) * 1e9, 1) for n in (3, 4, 5)])
    print(f"fine-structure alpha (2pi*Omega) = {t.fields.fine_structure_constant():.7f} "
          f"(1/{1/t.fields.fine_structure_constant():.3f})")
    print(f"water H2O: {t.elements.molecule_topology_pi('H2O')}pi, "
          f"{t.elements.molecule_mass_amu('H2O'):.2f} amu; "
          f"carbon config {t.elements.electron_configuration(6)}")
    print(f"Earth: g = {t.cosmology.body_surface_gravity('earth'):.2f} m/s^2, "
          f"escape = {t.cosmology.body_escape_velocity('earth'):.0f} m/s")
    print("particle solids:                ",
          {p: t.geometrics.solid_for_particle(p)['solid']
           for p in ('tetryon', 'quark', 'lepton', 'baryon')})


if __name__ == "__main__":
    main()
