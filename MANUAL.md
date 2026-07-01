# Tetryonics — Function Reference

The complete call list for the `tetryonics` engine. Every entry is a real
computation from Kelvin Abraham's Tetryonic theory. The **Python** names are shown
below; the **JavaScript** library (`tetryonics.js`) exposes the *same* functions in camelCase
(e.g. `nuclear_mass_amu` → `nuclearMassAmu`).

```python
import tetryonics as t
t.proton().charge_e            # 1.0
t.element(6).mass_amu          # carbon
t.fields.longitudinal_velocity()   # (pi/2)*c — longitudinal EM energy
```
```js
const T = require('./tetryonics.js');   // or window.Tetryonics in a browser
T.particles.proton().chargeE
T.fields.longitudinalVelocity()
```

## `constants`
> Tetryonic physical constants.

- `constants.AMPERE_CONSTANT` = `1.9999999977146666e-07`
- `constants.AMU_KG` = `1.6605388413096024e-27`
- `constants.APOLLO_CONSTANT` = `873825`
- `constants.AVOGADRO` = `6.022141579e+23`
- `constants.BARYON_MEV` = `930.947`
- `constants.BOHR_MAGNETON` = `9.549296585513719e-24`
- `constants.BOLTZMANN` = `1.380649e-23`
- `constants.C` = `299792458.0`
- `constants.C2` = `8.987551787368176e+16`
- `constants.CHARGE_MASS_RATIO_E` = `181010964191.29605`
- `constants.CHARGE_MASS_RATIO_P` = `96539180.90202455`
- `constants.CHARGE_QUANTUM` = `1.3351800672643421e-20`
- `constants.COSMIC_BARYONIC` = `0.05`
- `constants.COSMIC_DARK_ENERGY` = `0.68`
- `constants.COSMIC_DARK_MATTER` = `0.27`
- `constants.COULOMB_K` = `8987551754.500856`
- `constants.EINSTEIN_KAPPA` = `2.076504318049307e-43`
- `constants.ELECTRONS_PER_COULOMB` = `6.241355407894567e+18`
- `constants.ELECTRON_KEV` = `496.519`
- `constants.ELEMENTARY_CHARGE` = `1.6022160807172106e-19`
- `constants.EPSILON_0` = `8.85418785e-12`
- `constants.EPS_MU` = `1.112650058851172e-17`
- `constants.EV_KJ_PER_MOLE` = `96.48772078229534`
- `constants.E_EULER` = `2.718281828459045`
- `constants.FINE_STRUCTURE` = `0.0075398223686155025`
- `constants.FINE_STRUCTURE_CODATA` = `0.0072973525693`
- `constants.FINE_STRUCTURE_INV` = `132.62911924324612`
- `constants.G` = `6.67384e-11`
- `constants.GAS_CONSTANT` = `8.314462618`
- `constants.H` = `6.629432672e-34`
- `constants.H_BAR` = `1.0551069796437116e-34`
- `constants.H_EV` = `4.137664546e-15`
- `constants.IMPEDANCE_FREE_SPACE` = `376.730312557684`
- `constants.KEM_EV` = `13.525`
- `constants.KEPLER_BOUWKAMP` = `0.1149420448`
- `constants.LONGITUDINAL_VELOCITY` = `470912891.8272133`
- `constants.MAX_Z` = `120`
- `constants.MERCURY_PRECESSION_ARCSEC_CENTURY` = `43.0`
- `constants.MEV_J` = `1.6022160807172105e-13`
- `constants.MEV_PER_AMU` = `931.443519`
- `constants.MU_0` = `1.25663706e-06`
- `constants.M_Q` = `7.37623863410449e-51`
- `constants.NUCLEAR_MAGNETON` = `5.09295817894065e-27`
- `constants.N_ELECTRON` = `1.2e+20`
- `constants.N_HYDROGEN` = `2.2511999999999997e+23`
- `constants.N_NEUTRON` = `2.25e+23`
- `constants.N_PROTON` = `2.25e+23`
- `constants.OMEGA` = `0.0012`
- `constants.PERIODIC_SHELL_CAPS` = `(2, 8, 18, 32, 32, 18, 8, 2)`
- `constants.PHI` = `1.618033988749895`
- `constants.PIONEER_ANOMALY` = `8.74e-10`
- `constants.PROTON_ELECTRON_RATIO` = `1875.0`
- `constants.RYDBERG_DIVISOR` = `27.49545417`
- `constants.RYDBERG_OBSERVED` = `10967758.0`
- `constants.RYDBERG_TETRYONIC` = `10903346.28213199`
- `constants.TAU` = `6.283185307179586`
- `constants.ZETA2` = `1.6449340668482264`
- `constants.amu_from_mev(mev: 'float') -> 'float'` — Convert a mass-energy in MeV to atomic mass units (Tetryonic, hydrogen = 1).
- `constants.mass_from_mev(mev: 'float') -> 'float'` — Rest mass (kg) equivalent of a mass-energy given in MeV  (m = E/c²).
- `constants.mass_from_quanta(n_planck: 'float') -> 'float'` — Rest mass (kg) of a topology holding ``n_planck`` Planck energy quanta.
- `constants.summary() -> 'str'` — One-screen dump of the constant set (handy for sanity checks).

## `geometry`
> The Tetryonic geometry core — the equilateral-triangle engine every other module sits on.

- `class geometry.Fascia(level: 'int' = 1, sign: 'int' = 1) -> None` — One equilateral face of a tetryon at quantum ``level`` n.
- `class geometry.Photon(level: 'int' = 1) -> None` — A photon = a planar DIAMOND (rhombus) of two opposite-handed fascia.
- `class geometry.Tetryon(level: 'int' = 1, cw: 'int' = 4, ccw: 'int' = 0) -> None` — A tetrahedron = 4 fascia. The foundational quantum of Matter (4n geometry).
- `geometry.boson_quanta(n: 'int') -> 'int'` — Planck quanta in a single-triangle boson at level n  = n².
- `geometry.equilateral_area(base: 'float') -> 'float'` — Area of an equilateral triangle of side ``base`` = (sqrt(3)/4) * base**2.
- `geometry.field_quanta(fascia: 'int', n: 'int') -> 'int'` — General Tetryonic field count = (number of triangular fascia) · n².
- `geometry.is_square(n: 'int') -> 'bool'` — True if ``n`` is a perfect square (a completed equilateral energy level).
- `geometry.level_colour(level: 'int') -> 'str'` — Chromatic colour for an energy/quantum level (wraps mod 10).
- `geometry.negative_tetryon(level: 'int' = 1) -> 'Tetryon'` — 
- `geometry.neutral_tetryon(level: 'int' = 1) -> 'Tetryon'` — Also known as a gluon.
- `geometry.odd_sum_to_square(n: 'int') -> 'int'` — Sum of the first ``n`` odd numbers = n**2 (the core visual identity).
- `geometry.photon_quanta(n: 'int') -> 'int'` — Planck quanta in a photon — a flat diamond of TWO triangles — at level n = 2·n².
- `geometry.positive_tetryon(level: 'int' = 1) -> 'Tetryon'` — 
- `geometry.units_in_row(r: 'int') -> 'int'` — Unit triangles in row ``r`` (from apex, 1-based) -> 2r-1 (odd).
- `geometry.units_in_triangle(n: 'int') -> 'int'` — Total unit triangles in an equilateral triangle of side ``n`` -> n**2.
- `geometry.up_down_in_row(r: 'int') -> 'tuple[int, int]'` — (up-pointing, down-pointing) unit triangles in row ``r`` -> (r, r-1).

## `energy`
> Energy, mass, momentum & QAM — the core mechanics of Tetryonic Book 1.

- `energy.beta(velocity: 'float') -> 'float'` — β = v/c.
- `energy.boson_energy(quanta_v: 'float') -> 'float'` — Transverse boson energy  E = h·v  (v = transverse quanta count).
- `energy.boson_quanta_from_energy(energy_j: 'float') -> 'float'` — Inverse of boson_energy:  v = E/h.
- `energy.compton_wavelength(mass_kg: 'float') -> 'float'` — λ_c = h / (m c).
- `energy.de_broglie_wavelength(momentum_kg_m_s: 'float') -> 'float'` — λ = h / p.
- `energy.em_mass(energy_j: 'float') -> 'float'` — 2D ElectroMagnetic mass:  m = E / c²  (kg, planar 'energy per light-second').
- `energy.em_mass_from_matter(matter_kg: 'float') -> 'float'` — 3D Matter → 2D EM-mass bridge:  m = M·c².
- `energy.energy_from_em_mass(mass_kg: 'float') -> 'float'` — E = m c².
- `energy.energy_from_matter(matter_kg: 'float') -> 'float'` — E = M c⁴.
- `energy.energy_from_quanta(n_planck: 'float') -> 'float'` — Energy (J) of ``n_planck`` Planck quanta:  E = N·h.
- `energy.frequency_from_energy(energy_j: 'float') -> 'float'` — Inverse of photon_energy:  f = E/h.
- `energy.frequency_from_quanta(quanta_v: 'float') -> 'float'` — Einstein frequency from Planck quanta:  f = 2v   (since 2hv = hf).
- `energy.gamma(velocity: 'float') -> 'float'` — Lorentz factor γ = 1/√(1 − β²).
- `energy.kinetic_energy(mass_kg: 'float', velocity: 'float') -> 'float'` — ⚠ Standard ½mv² form — NOT Kelvin's primary energy. In Tetryonics the scalar
- `energy.length_contraction(rest_length: 'float', velocity: 'float') -> 'float'` — Contracted length  L = L₀·√(1 − v²/c²) = L₀/γ.
- `energy.mass_from_compton(wavelength_m: 'float') -> 'float'` — Inverse of compton_wavelength:  m = h/(λ·c).
- `energy.mass_from_energy_velocity(energy_j: 'float', velocity: 'float') -> 'float'` — Newton view:  m = E / v².
- `energy.mass_from_quanta(n_planck: 'float') -> 'float'` — Rest mass (kg) of ``n_planck`` Planck quanta:  m = N·m_q  (= N·h/c²).
- `energy.matter(energy_j: 'float') -> 'float'` — 3D Matter topology:  M = E / c⁴  (the 4nπ tetrahedral standing-wave form).
- `energy.matter_from_em_mass(em_mass_kg: 'float') -> 'float'` — 2D EM-mass → 3D Matter bridge:  M = m/c².
- `energy.momentum(mass_kg: 'float', velocity: 'float') -> 'float'` — Linear momentum  p = m v  (kg·m/s).
- `energy.momentum_from_de_broglie(wavelength_m: 'float') -> 'float'` — Inverse of de_broglie_wavelength:  p = h/λ.
- `energy.photon_energy(frequency_hz: 'float') -> 'float'` — Photon energy  E = h·f.
- `energy.qam() -> 'float'` — Quantised Angular Momentum Ω (m²/s) — the hidden geometric constant.
- `energy.quanta_from_energy(energy_j: 'float') -> 'float'` — Number of Planck quanta in an energy:  N = E/h.
- `energy.quanta_from_frequency(frequency_hz: 'float') -> 'float'` — Planck quanta from frequency:  v = f/2.
- `energy.quanta_from_mass(mass_kg: 'float') -> 'float'` — 
- `energy.relativistic_energy(momentum: 'float', rest_mass: 'float') -> 'float'` — Total energy  E = √((p·c)² + (m₀·c²)²)  (the energy–momentum relation).
- `energy.scalar_energy(mass_kg: 'float', velocity: 'float') -> 'float'` — Scalar mass-energy  E = m v²  (the mv² = hv² identity).
- `energy.scalar_energy_quantised(n: 'float', quanta_v: 'float') -> 'float'` — Scalar/square energy with the equilateral factor:  E = n·π·[h·v²]  (square quanta).
- `energy.tetryon_units(level: 'int') -> 'int'` — Unit mass-energy triangles in a tetryon at level n = 4·n²  (the 4nπ scaling).
- `energy.time_dilation(proper_time: 'float', velocity: 'float') -> 'float'` — Moving-frame time  t' = t/√(1 − v²/c²) = γ·t  (Book 2 p.209).
- `energy.transverse_energy(n: 'float', quanta_v: 'float') -> 'float'` — Transverse/boson energy with the equilateral factor:  E = n·π·[h·v]  (odd quanta).
- `energy.velocity_from_beta(beta_value: 'float') -> 'float'` — Inverse of beta():  v = β·c.

## `charge`
> Charge — the equilateral geometry of energy.

- `charge.charge_coulombs(cw: 'int', ccw: 'int') -> 'float'` — Net charge in coulombs = net_quanta × charge_quantum.
- `charge.charge_from_qam(qam: 'float' = 0.0012) -> 'float'` — Charge of a geometry from its quantised angular momentum:  q = QAM / c².
- `charge.charge_in_e(cw: 'int', ccw: 'int') -> 'float'` — Net charge in units of the elementary charge (e ↔ 12 quanta).
- `charge.is_fermion_charge(cw: 'int', ccw: 'int') -> 'bool'` — All Fermion charges are integer 1/3 multiples of e.
- `charge.net_quanta(cw: 'int', ccw: 'int') -> 'int'` — Net charge quanta = clockwise − counter-clockwise.
- `charge.time_as_charge(seconds: 'float') -> 'float'` — Abraham's identity: time *is* charge.

## `fields`
> ElectroMagnetic fields & forces.

- `fields.ampere_constant() -> 'float'` — Ampère force constant  k_A = μ₀/(2π) = 2×10⁻⁷ N/A².
- `fields.ampere_force_per_length(i1: 'float', i2: 'float', d: 'float') -> 'float'` — Force per length between two parallel wires  F/L = μ₀·I₁I₂/(2π·d)  (N/m).
- `fields.biot_savart_point(current_a: 'float', length_m: 'float', r: 'float') -> 'float'` — Magnitude of B from a current element (perpendicular):
- `fields.bohr_magneton() -> 'float'` — Bohr magneton  μ_B = e·ħ/(2·m_e)  (J/T).
- `fields.charge_mass_ratio(particle: 'str' = 'electron') -> 'float'` — Charge-to-mass ratio q/m (C/kg). Electron ≈ 1.81e11, proton ≈ 9.65e7.
- `fields.coulomb_constant() -> 'float'` — Coulomb constant  k = 1/(4πε₀).
- `fields.coulomb_force(q1: 'float', q2: 'float', r: 'float') -> 'float'` — Coulomb force  F = k·q₁q₂/r²  (N). Positive = repulsive (like charges).
- `fields.electric_falloff(r: 'float') -> 'float'` — Relative electric field strength ∝ 1/r².
- `fields.electric_field(q: 'float', r: 'float') -> 'float'` — Radial E-field of a point charge  E = (1/4πε₀)·q/r²  (V/m).
- `fields.epsilon0_from(mu0: 'float' = 1.25663706e-06, c: 'float' = 299792458.0) -> 'float'` — 
- `fields.fine_structure_constant(tetryonic: 'bool' = True) -> 'float'` — The fine-structure (EM coupling) constant.
- `fields.gauss_flux(charge_c: 'float') -> 'float'` — Total electric flux out of a closed surface  Φ = q/ε₀  (Gauss' law).
- `fields.impedance_of_free_space() -> 'float'` — Characteristic impedance of the vacuum  Z₀ = √(μ₀/ε₀) = μ₀·c ≈ 376.7 Ω.
- `fields.longitudinal_velocity() -> 'float'` — Tetryonic longitudinal EM-energy velocity = (π/2)·c (Book 2 p.96).
- `fields.lorentz_force(q: 'float', e_field: 'float' = 0.0, velocity: 'float' = 0.0, b_field: 'float' = 0.0) -> 'float'` — Scalar Lorentz force  F = q(E + vB)  (perpendicular v,B).
- `fields.magnetic_dipole_falloff(r: 'float') -> 'float'` — Relative magnetic dipole strength ∝ 1/r³.
- `fields.magnetic_field_from_H(h_field: 'float') -> 'float'` — B = μ₀·H.
- `fields.magnetic_force_per_length(current_a: 'float', r: 'float') -> 'float'` — Magnetic force per length of a single current  F = μ₀·I²/(2π·r)  (N/m).
- `fields.mu0_from(eps0: 'float' = 8.85418785e-12, c: 'float' = 299792458.0) -> 'float'` — 
- `fields.nuclear_magneton() -> 'float'` — Nuclear magneton  μ_N = μ_B / 1875  (proton/electron mass ratio).
- `fields.poynting(e_field: 'float', h_field: 'float') -> 'float'` — Poynting energy-flux magnitude  S = E × H  (W/m²).
- `fields.speed_of_light_from_constants() -> 'float'` — c = 1/√(ε₀μ₀).

## `levels`
> Quantum energy levels, electron shells & spectra.

- `levels.colour(n: 'int') -> 'str'` — Chromatic energy-level colour (0..9 wrap).
- `levels.hydrogen_energy(n: 'int') -> 'float'` — Bound-electron energy of hydrogen level n (eV):  E = −13.525/n²  (his KEM, p.75).
- `levels.ionisation_energy(n: 'int' = 1) -> 'float'` — Energy (eV) to free an electron from level n = +13.525/n²  (his KEM ground).
- `levels.ionization_energy(n: 'int' = 1) -> 'float'` — Energy (eV) to free an electron from level n = +13.525/n²  (his KEM ground).
- `levels.level_quanta(n: 'int') -> 'int'` — Cumulative mass-energy quanta at level n (square geometry) = n².
- `levels.level_step(n: 'int') -> 'int'` — Quanta added going from level n−1 to n (odd) = 2n−1.
- `levels.rydberg_wavelength(n_low: 'int', n_high: 'int', observed: 'bool' = False) -> 'float'` — Spectral-line wavelength (m):  1/λ = R·(1/n_low² − 1/n_high²).
- `levels.shell_name(n: 'int') -> 'str'` — 
- `levels.shell_quanta(n: 'int') -> 'int'` — Electron-shell mass-energy quanta at principal level n = 12·n².
- `levels.spin_rotation_angle(spin: 'float') -> 'int'` — Rotation angle (degrees) for a given spin number.

## `particles`
> The particle / quantum builder.

- `class particles.Particle(name: 'str', cw: 'int', ccw: 'int', fascia: 'int', topology: 'int', n_planck: 'float | None' = None, kind: 'str' = 'particle') -> None` — A built particle with its Tetryonic geometry, charge and (optional) mass.
- `particles.anti_proton() -> 'Particle'` — 
- `particles.baryon(flavours: 'list[str]', name: 'str | None' = None, n_planck: 'float | None' = None) -> 'Particle'` — Build an arbitrary tri-quark baryon from a flavour list (e.g. ['up','up','down']).
- `particles.electron() -> 'Particle'` — 
- `particles.from_quanta(cw: 'int', ccw: 'int', n_planck: 'float | None' = None, fascia: 'int | None' = None, name: 'str' = 'custom', kind: 'str' = 'particle') -> 'Particle'` — Build an arbitrary particle from a [cw·ccw] charge pair.
- `particles.meson(flavour1: 'str', flavour2: 'str', name: 'str | None' = None) -> 'Particle'` — A meson = quark + antiquark (24π geometry → 14π topology).
- `particles.neutrino() -> 'Particle'` — 
- `particles.neutron() -> 'Particle'` — 
- `particles.particle(name: 'str') -> 'Particle'` — Look up any standard particle by name (e.g. 'proton', 'up', 'electron').
- `particles.positron() -> 'Particle'` — 
- `particles.proton() -> 'Particle'` — 
- `particles.quark(flavour: 'str') -> 'Particle'` — 
- `particles.standard_particles() -> 'list[Particle]'` — The headline particles, ready for a table.

## `elements`
> The element / periodic engine.

- `class elements.Atom(z: 'int', protons: 'int', neutrons: 'int', electrons: 'int', name: 'str' = '') -> None` — A neutral atom (or named isotope) as a Tetryonic Matter topology.
- `class elements.NuclearShell(n: 'int', letter: 'str', deuterons: 'int', mev_each: 'float', capacity: 'int') -> None` — One filled nuclear energy level (a row on the p.92 plate).
- `elements.acid(name: 'str') -> 'str'` — Formula of a named acid.
- `elements.allotrope_topology_pi(z: 'int') -> 'int'` — Allotropes share Z and topology-π (same charge geometry, different 3D form);
- `elements.are_isomers(formula_a: 'str', formula_b: 'str') -> 'bool'` — True if two distinct structural formulas share the same molecular formula
- `elements.atoms_per_kg(z: 'int') -> 'float'` — Number of atoms of element Z in 1 kg of its Matter  = 1/mass_kg.
- `elements.azimuthal_quantum_number(subshell: 'str') -> 'int'` — Azimuthal (orbital angular momentum) quantum number ℓ: s=0, p=1, d=2, f=3.
- `elements.balance_reaction(reactants: 'list[str]', products: 'list[str]') -> 'dict'` — Balance a chemical reaction by conserving every element (= conserving charge-π
- `elements.bond_geometry(name: 'str') -> 'dict'` — Bond length/angle of a molecule — Kelvin's p.369 data where given (CO₂ 116.3 pm,
- `elements.bond_order(shared_electrons: 'int') -> 'int'` — Bond order from shared electrons: 2→single, 4→double, 6→triple  (= e/2).
- `elements.bond_type(sym_a: 'str', sym_b: 'str') -> 'str'` — Classify a bond between two elements the Tetryonic way (charge transfer vs sharing,
- `elements.central_lone_pairs(central: 'str', n_bonded_atoms: 'int', charge: 'int' = 0) -> 'int'` — Lone pairs on a main-group central atom bonded to ``n_bonded_atoms`` (single-σ each):
- `elements.common_isotopes(z: 'int') -> 'list[int]'` — Common isotope mass numbers of element Z (e.g. carbon → [12, 13, 14]).
- `elements.deuterium() -> 'Atom'` — 
- `elements.divides_into_deuterium_units(formula: 'str') -> 'bool'` — True if a compound's total topology-π is a whole number of 84π deuterium units.
- `elements.electron_configuration(z: 'int') -> 'str'` — Ground-state electron configuration (Aufbau/Madelung order), e.g. '1s2 2s2 2p4'.
- `elements.element(z: 'int') -> 'Atom'` — The standard neutral atom for atomic number ``z`` (Tetryonic convention).
- `elements.element_block(z: 'int') -> 'str'` — s / p / d / f block — the subshell of the last electron added (Aufbau order).
- `elements.element_family(z: 'int') -> 'str'` — Coarse family from block + valence (main-group-accurate; Book 3 p.26/30).
- `elements.element_orbital(z: 'int') -> 'dict'` — The orbital subshell the last (valence) electron of element Z occupies (Aufbau).
- `elements.element_quanta(z: 'int') -> 'int'` — Integer charge-π quanta of a neutral atom (84·Z for Z≥2; H=48). The book's
- `elements.fascia_bond(order: 'int') -> 'str'` — Kelvin's name for a bond by order (Book 3 p.370): "it is the electric field fascia
- `elements.group_valence(z: 'int') -> 'int'` — Main-group 'combining' valence electrons (s+p of the outer shell), 1..8.
- `elements.hydrogen() -> 'Atom'` — 
- `elements.hydrogen_bond_quanta(n_h: 'int' = 1) -> 'int'` — Charge-π of n hydrogen radicals participating as H-bonds (Book 3 p.385): 48 each
- `elements.hydrogen_radical() -> 'dict'` — The free hydrogen radical (Book 3 p.385): H = 48π `[24·24]` — proton[24·12] + electron[0·12].
- `elements.ion(z: 'int', charge: 'int', name: 'str' = '') -> 'Atom'` — A charged ion of element Z (charge = protons − electrons; e.g. Na⁺ → charge +1).
- `elements.ion_charge_quanta(charge_e: 'int') -> 'int'` — Charge-quanta of an ion = 12 × its charge in e (Book 3 p.380: Na⁺ = +12, Cl⁻ = −12).
- `elements.ionic_bond(cation: 'str', anion: 'str', n_cation: 'int' = 1, n_anion: 'int' = 1) -> 'dict'` — Ionic compound from a metal cation + non-metal anion (Book 3 p.380, e.g. NaCl).
- `elements.ionisation_energy(z: 'int', n: 'int' = 1) -> 'float'` — Hydrogenic ionisation energy (eV)  E = 13.525·Z²/n²  (his KEM ground, Book 3 p.75).
- `elements.ionization_energy(z: 'int', n: 'int' = 1) -> 'float'` — Hydrogenic ionisation energy (eV)  E = 13.525·Z²/n²  (his KEM ground, Book 3 p.75).
- `elements.is_metal(z: 'int') -> 'bool'` — True if element Z is a metal (donates electrons → cations; Book 3 p.380).
- `elements.is_nonmetal(z: 'int') -> 'bool'` — 
- `elements.isotope(z: 'int', mass_number: 'int', name: 'str' = '') -> 'Atom'` — An isotope with a given nucleon count (neutrons = A - Z).
- `elements.isotope_notation(z: 'int', mass_number: 'int') -> 'str'` — Isotope label, e.g. (6, 14) → 'C-14'.
- `elements.lewis_structure(formula: 'str') -> 'dict'` — Auto Lewis/VSEPR for a simple molecule (one central atom + terminal atoms), Book 3 p.370.
- `elements.molar_mass(z: 'int') -> 'float'` — Molar mass in g/mol (numerically the atomic mass in amu).
- `elements.molecular_formula(formula: 'str') -> 'str'` — Canonical (Hill) molecular formula: C first, H second, then the rest alphabetically.
- `elements.molecular_geometry(bonding_regions: 'int', lone_pairs: 'int' = 0) -> 'dict'` — Molecular shape from the steric number (bonding regions + lone pairs), Book 3 p.370.
- `elements.molecule_composition(formula: 'str') -> 'list[dict]'` — Per-element breakdown of a compound: [{symbol, z, count, topology_pi,
- `elements.molecule_mass(formula: 'str') -> 'float'` — Rest mass (kg) of a molecule = Σ constituent atom masses.
- `elements.molecule_mass_amu(formula: 'str') -> 'float'` — 
- `elements.molecule_nuclear_mass_amu(formula: 'str') -> 'float'` — Energy-level (his Chemistry-book) mass of a compound (amu) = Σ atoms'
- `elements.molecule_shape(name: 'str') -> 'dict'` — Geometry of a named molecule from Kelvin's p.370 set (e.g. 'H2O' → bent 104.5°).
- `elements.molecule_topology_pi(formula: 'str') -> 'int'` — Total charge-π of a compound = Σ atoms' topology π.
- `elements.neutralise(acid: 'str', base: 'str') -> 'dict'` — Acid + hydroxide base → salt + water, balanced (Book 3 p.379).
- `elements.neutron_number(z: 'int', mass_number: 'int') -> 'int'` — Neutrons in an isotope = A − Z.
- `elements.nuclear_mass_amu(z: 'int') -> 'float'` — Energy-level rest mass (amu) of element Z — reproduces Kelvin's per-element pages.
- `elements.nuclear_mass_kg(z: 'int') -> 'float'` — Energy-level rest mass (kg) of element Z (his method; no excess neutrons).
- `elements.nuclear_mass_mev(z: 'int') -> 'float'` — Total rest mass-energy (MeV) of element Z by Kelvin's energy-level method.
- `elements.nuclear_shell_fill(z: 'int') -> 'list[NuclearShell]'` — Distribute ``z`` Deuterium nuclei across the K..R nuclear shells (Book 3 p.92).
- `elements.nuclear_shell_report(z: 'int') -> 'str'` — Human-readable breakdown of element Z's deuteron shell stack (p.92 style).
- `elements.orbital(subshell: 'str') -> 'dict'` — Geometry of an atomic orbital subshell (Book 3 p.59-62): s spherical (2e),
- `elements.period(z: 'int') -> 'int'` — Period (table row) = highest occupied principal shell n  (Book 3 p.218).
- `elements.periodic_shell_cap(level: 'int') -> 'int'` — Electrons a periodic shell holds (capped/mirrored 2,8,18,32,32,18,8,2; Book 3 p.27/69).
- `elements.periodic_table(z_max: 'int' = 20) -> 'list[Atom]'` — 
- `elements.polyatomic_ion(name: 'str') -> 'dict'` — A named polyatomic ion → {formula, charge_e, charge_quanta (±12·charge), topology_pi}.
- `elements.reaction_conserves_topology(reactants: 'list[str]', products: 'list[str]', coeffs: 'dict | None' = None) -> 'bool'` — Verify a (balanced) reaction conserves total charge-π topology — the Tetryonic
- `elements.shared_electrons_for_bond(order: 'int') -> 'int'` — Electrons shared for a given bond order: single=2, double=4, triple=6.
- `elements.shell_capacity(n: 'int') -> 'int'` — Electrons a principal shell can hold = 2·n²  (standard QM; Book 3 p.69).
- `elements.sigma_pi_bonds(order: 'int') -> 'tuple[int, int]'` — (σ, π) decomposition of a covalent bond: single=σ, double=σ+π, triple=σ+2π.
- `elements.subshell_capacity(subshell: 'str') -> 'int'` — Electron capacity of a subshell = 4ℓ+2 (s=2, p=6, d=10, f=14).
- `elements.tritium() -> 'Atom'` — 
- `elements.valence(z: 'int') -> 'int'` — Maximum valence / oxidation reach (Book 3 p.381 table: Sc=3, Ni=10, Au=11, Hg=2).
- `elements.valence_electrons(z: 'int') -> 'int'` — Outer-shell electron count (highest principal level). Good for main-group valence.

## `biochem`
> Biochemistry — Book 3 (Chemistry), the organic / biological chapters.

- `biochem.amino_acid_quanta(name: 'str') -> 'int'` — 
- `biochem.base_pair_quanta(base: 'str', rna: 'bool' = False) -> 'int'` — Combined charge-π of a base pair (A·T / A·U / G·C) — the two bases joined by
- `biochem.base_quanta(name: 'str') -> 'int'` — Quanta of a DNA/RNA nucleobase.
- `biochem.complementary_base(base: 'str', rna: 'bool' = False) -> 'str'` — The charge-complementary base: A→T (DNA) or A→U (RNA), G→C, etc.
- `biochem.condensation_water(bonds: 'int') -> 'int'` — Total water-quanta released forming ``bonds`` condensation bonds.
- `biochem.functional_group_quanta(group: 'str') -> 'int'` — Quanta of a named functional group (CH2, OH, NO2 …).
- `biochem.molecule_mass(formula: 'str') -> 'float'` — Rest mass (kg) of a biomolecule.
- `biochem.molecule_quanta(formula: 'str') -> 'int'` — Total charge-π quanta of any (bio)molecule = Σ atomic topologies.
- `biochem.nucleotide_quanta(base: 'str', deoxy: 'bool' = False) -> 'int'` — Quanta of a nucleotide = base + sugar (ribose/deoxyribose) + phosphate,
- `biochem.peptide_quanta(residues: 'list') -> 'int'` — Quanta of a peptide built from a list of amino-acid names.
- `biochem.polysaccharide_quanta(monomer: 'str', n: 'int') -> 'int'` — Quanta of an n-unit polysaccharide: n monomers minus (n−1) condensation waters.
- `biochem.sugar_quanta(name: 'str') -> 'int'` — 

## `units`
> Tetryonic physics-units map (the 'PHYSICS UNITS' plate, Book 1 p.40).

- `units.all_units() -> 'list[str]'` — 
- `units.colour_codes() -> 'dict'` — 
- `units.describe(quantity: 'str') -> 'str'` — 

## `electrical`
> Electricity — Book 2 (Electrodynamics).

- `electrical.capacitance_from_charge(charge_c: 'float', voltage_v: 'float') -> 'float'` — C = Q/V (farads).
- `electrical.capacitor_charge(capacitance_f: 'float', voltage_v: 'float') -> 'float'` — Q = C·V.
- `electrical.capacitor_energy(capacitance_f: 'float', voltage_v: 'float') -> 'float'` — E = ½·C·V².
- `electrical.current(voltage_v: 'float', resistance_ohm: 'float') -> 'float'` — I = V/R.
- `electrical.displacement_current(d_e_flux: 'float', dt: 'float') -> 'float'` — Maxwell's displacement current  I_D = ε₀·dΦ_E/dt  (A).
- `electrical.drift_velocity(current_a: 'float', number_density: 'float', area_m2: 'float', charge_c: 'float' = 1.6022160807172106e-19) -> 'float'` — Electron drift velocity  v_d = I/(n·q·A)  (m/s).
- `electrical.electrical_work(charge_c: 'float', voltage_v: 'float') -> 'float'` — Energy moved by pushing charge through a potential:  W = q·V (J).
- `electrical.electron_volt_to_joules(ev: 'float') -> 'float'` — 1 eV = e joules.
- `electrical.ev_to_kj_per_mole(ev: 'float') -> 'float'` — Convert eV/particle to kJ/mol  (1 eV ≈ 96.5 kJ/mol).
- `electrical.faraday_emf(d_flux: 'float', dt: 'float', turns: 'int' = 1) -> 'float'` — Induced EMF  ε = −N·dΦ/dt  (V).
- `electrical.impedance(resistance_ohm: 'float', x_l: 'float' = 0.0, x_c: 'float' = 0.0) -> 'float'` — Series RLC impedance  Z = √(R² + (X_L − X_C)²)  (Ω).
- `electrical.inductor_emf(inductance_h: 'float', d_current: 'float', dt: 'float') -> 'float'` — Self-induced EMF across an inductor  v = −L·di/dt  (V).
- `electrical.inductor_energy(inductance_h: 'float', current_a: 'float') -> 'float'` — E = ½·L·I².
- `electrical.joules_to_electron_volt(joules: 'float') -> 'float'` — 
- `electrical.kj_per_mole_to_ev(kj_mol: 'float') -> 'float'` — Convert kJ/mol to eV/particle.
- `electrical.lc_resonance(inductance_h: 'float', capacitance_f: 'float') -> 'float'` — LC tank resonant frequency  f = 1/(2π√(LC)).
- `electrical.lr_time_constant(inductance_h: 'float', resistance_ohm: 'float') -> 'float'` — L/R time constant  τ = L/R  (s).
- `electrical.parallel_plate_capacitance(area_m2: 'float', separation_m: 'float', rel_permittivity: 'float' = 1.0) -> 'float'` — Parallel-plate capacitance  C = ε·A/d  (F).
- `electrical.power_i2r(current_a: 'float', resistance_ohm: 'float') -> 'float'` — P = I²·R.
- `electrical.power_v2r(voltage_v: 'float', resistance_ohm: 'float') -> 'float'` — P = V²/R.
- `electrical.power_vi(voltage_v: 'float', current_a: 'float') -> 'float'` — P = V·I (watts).
- `electrical.rc_time_constant(resistance_ohm: 'float', capacitance_f: 'float') -> 'float'` — RC time constant  τ = R·C  (s).
- `electrical.reactance_capacitive(frequency_hz: 'float', capacitance_f: 'float') -> 'float'` — Capacitive reactance  X_C = 1/(2π·f·C)  (Ω).
- `electrical.reactance_inductive(frequency_hz: 'float', inductance_h: 'float') -> 'float'` — Inductive reactance  X_L = 2π·f·L  (Ω).
- `electrical.resistance(voltage_v: 'float', current_a: 'float') -> 'float'` — R = V/I.
- `electrical.resistivity_field(resistivity: 'float', current_density: 'float') -> 'float'` — Microscopic Ohm's law  E = ρ·J  (V/m).
- `electrical.voltage(current_a: 'float', resistance_ohm: 'float') -> 'float'` — V = I·R.

## `waves`
> EM waves & photons — Book 2 (Electrodynamics).

- `waves.angular_frequency(frequency_hz: 'float') -> 'float'` — ω = 2πf.
- `waves.boson_photon_energy(n: 'float', quanta_v: 'float') -> 'float'` — EM-wave energy from n bosons:  E = n·h·v  (= h·f with f = 2v).
- `waves.compton_frequency(mass_kg: 'float') -> 'float'` — Compton frequency of a mass  f = m·c²/h  (Book 2 p.111).
- `waves.compton_shift(theta_rad: 'float', mass_kg: 'float' = None) -> 'float'` — Compton wavelength shift  Δλ = (h/mc)(1 − cos θ).
- `waves.energy_from_wavenumber(wavenumber: 'float') -> 'float'` — Photon energy from wavenumber  E = h·c·k.
- `waves.euler_phase(theta_rad: 'float') -> 'complex'` — e^{iθ} = cos θ + i sin θ — the phasor of an EM waveform component.
- `waves.frequency(wavelength_m: 'float') -> 'float'` — f = c/λ (Hz).
- `waves.frequency_from_energy(energy_j: 'float') -> 'float'` — f = E/h.
- `waves.frequency_from_wavenumber(wavenumber: 'float') -> 'float'` — f = c·k.
- `waves.inverse_square(intensity0: 'float', r: 'float') -> 'float'` — Intensity at distance r under the inverse-square law:  I = I₀/r².
- `waves.photon_energy_from_frequency(frequency_hz: 'float') -> 'float'` — E = h·f.
- `waves.photon_energy_from_wavelength(wavelength_m: 'float') -> 'float'` — E = h·c/λ.
- `waves.photon_momentum(wavelength_m: 'float') -> 'float'` — p = h/λ.
- `waves.photon_phase_offset(index: 'int') -> 'float'` — Phase (radians) of the n-th photon in a wave — 90° apart from neighbours.
- `waves.vacuum_energy_wavelength(base_wavelength_m: 'float', n: 'int') -> 'float'` — Vacuum-energy wavelength ladder  λ_n = λ/(2·n²)  (Book 4 p.217).
- `waves.wavelength(frequency_hz: 'float') -> 'float'` — λ = c/f (m).
- `waves.wavelength_from_energy(energy_j: 'float') -> 'float'` — λ = h·c/E.
- `waves.wavelength_from_wavenumber(wavenumber: 'float') -> 'float'` — λ = 1/k.
- `waves.wavenumber(wavelength_m: 'float') -> 'float'` — k = 1/λ (1/m).
- `waves.wavenumber_from_energy(energy_j: 'float') -> 'float'` — k = E/(h·c).

## `spectra`
> Atomic spectra — the named hydrogen spectral series (Book 2, pp.117–167).

- `spectra.all_series() -> 'list[str]'` — 
- `spectra.line_energy_ev(series: 'str', n_high: 'int') -> 'float'` — Photon energy (eV) of the transition = |E(n_low) − E(n_high)|.
- `spectra.line_wavelength(series: 'str', n_high: 'int') -> 'float'` — Wavelength (m) of the transition n_high → series lower level.
- `spectra.quanta_differential(n: 'int') -> 'int'` — Mass-energy quanta of the n-th level step = 12·(2n−1).
- `spectra.rydberg_factor(n_low: 'int', n_high: 'int') -> 'float'` — The Rydberg/KEM fraction  (1/n_low² − 1/n_high²) for a transition.
- `spectra.series_lines(series: 'str', count: 'int' = 4) -> 'list[dict]'` — First ``count`` lines of a series, as dicts of (n_high, wavelength_nm, energy_eV).
- `spectra.series_lower_level(series: 'str') -> 'int'` — 
- `spectra.series_rydberg_divisor(series: 'str') -> 'float'` — Tetryonic per-series Rydberg divisor = 27.49545417 · n_low²  (Book 2 p.128).
- `spectra.series_shell_quanta(series: 'str') -> 'int'` — Mass-energy quanta of a series' lower shell = 12·n_low²  (Book 2 p.119).

## `radiation`
> Blackbody / thermal radiation — Book 2 (Electrodynamics) p.176.

- `radiation.photon_flux(power_w: 'float', frequency_hz: 'float') -> 'float'` — Photons per second from a beam  N = P/(h·f).
- `radiation.photon_intensity(power_w: 'float', area_m2: 'float') -> 'float'` — Irradiance  I = P/A  (W/m²).
- `radiation.photon_quanta_at_level(n: 'int') -> 'int'` — Per-level Planck-quanta count in the equilateral distribution = n².
- `radiation.planck_spectral_radiance(wavelength_m: 'float', temperature_k: 'float') -> 'float'` — Planck's law — spectral radiance B(λ,T) (W·sr⁻¹·m⁻³).
- `radiation.rayleigh_jeans(wavelength_m: 'float', temperature_k: 'float') -> 'float'` — Classical Rayleigh–Jeans spectral radiance  B = 2c·k_B·T/λ⁴ (the UV-catastrophe form).
- `radiation.stefan_boltzmann_power(temperature_k: 'float', area_m2: 'float' = 1.0, emissivity: 'float' = 1.0) -> 'float'` — Total radiated power  P = εσA·T⁴ (W).
- `radiation.stellar_luminosity(radius_m: 'float', temperature_k: 'float', emissivity: 'float' = 1.0) -> 'float'` — Luminosity of a star (blackbody sphere)  L = 4π·R²·εσ·T⁴  (W).
- `radiation.wien_peak_frequency(temperature_k: 'float') -> 'float'` — Wien's law (frequency form)  f_max = 2.821439·k_B·T/h  (Hz).
- `radiation.wien_peak_wavelength(temperature_k: 'float') -> 'float'` — Wien's displacement law — peak wavelength  λ_max = b/T (m).

## `optics`
> Optics & photon–matter interactions — Book 2 (Electrodynamics).

- `optics.amplitude_from_intensity(intensity: 'float') -> 'float'` — EM-wave amplitude is the square root of the wavefunction intensity (p.198).
- `optics.pair_production_threshold() -> 'float'` — Minimum photon energy to create an e⁺e⁻ pair = 2·m_e·c²  (J, ≈ 1.022 MeV).
- `optics.phase_velocity(refractive_index_n: 'float') -> 'float'` — Phase velocity in a medium  v = c/n.
- `optics.photoelectric_ke(frequency_hz: 'float', work_function_j: 'float') -> 'float'` — Photoelectron kinetic energy  KE = h·f − φ  (J); 0 below the threshold.
- `optics.photoelectric_threshold_frequency(work_function_j: 'float') -> 'float'` — Cutoff frequency  f₀ = φ/h  below which no electrons are emitted.
- `optics.recoil_momentum(total_energy_j: 'float', rest_mass_kg: 'float') -> 'float'` — Recoil-electron momentum  p = √(E² − (m·c²)²)/c  (Compton scattering, p.111).
- `optics.reflection_angle(incidence_rad: 'float') -> 'float'` — Law of reflection — angle of reflection equals angle of incidence.
- `optics.refractive_index(phase_velocity: 'float') -> 'float'` — Refractive index  n = c/v  (v = phase velocity of light in the medium).
- `optics.snell(n1: 'float', theta1_rad: 'float', n2: 'float') -> 'float'` — Snell's law — refraction angle θ₂ from  n₁·sin θ₁ = n₂·sin θ₂.
- `optics.superpose(*amplitudes: 'float') -> 'float'` — Linear superposition of wave amplitudes  F(ψ₁+ψ₂+…) = ΣF(ψᵢ).
- `optics.wavelength_in_medium(vacuum_wavelength_m: 'float', refractive_index_n: 'float') -> 'float'` — In a medium the frequency is fixed and λ scales with velocity:  λ = λ_vac / n.

## `cosmology`
> Cosmology & gravitation — Book 4.

- `cosmology.annihilation_energy(mass_kg: 'float') -> 'float'` — Radiant energy from a 100%-efficient Matter→energy GEM pinch  E = m·c²  (J).
- `cosmology.body_escape_velocity(name: 'str') -> 'float'` — 
- `cosmology.body_mass(name: 'str') -> 'float'` — 
- `cosmology.body_radius(name: 'str') -> 'float'` — 
- `cosmology.body_surface_gravity(name: 'str') -> 'float'` — 
- `cosmology.cosmic_energy_budget() -> 'dict'` — The mass-energy budget of the Universe (Book 4 p.218/220).
- `cosmology.dark_energy_momenta(mass: 'float', velocity: 'float') -> 'float'` — 'Dark Energy' = DIVERGENT vacuum momenta = 2·m·v² (Book 4 p.220) — a divergent KEM
- `cosmology.dark_matter_momenta(frequency: 'float') -> 'float'` — 'Dark Matter' in Tetryonics = CONVERGENT vacuum momenta = h·f (Book 4 p.218/219) —
- `cosmology.einstein_kappa() -> 'float'` — Einstein's GR coupling constant  κ = 8πG/c⁴  (Gab = κ·Tab).
- `cosmology.em_to_gravity_ratio() -> 'float'` — How much stronger the EM (Coulomb) coupling is than gravity:  k/G  (~10²⁰).
- `cosmology.escape_velocity(mass: 'float', r: 'float') -> 'float'` — Escape velocity  v = √(2GM/r)  (m/s).
- `cosmology.fission_quanta_release(parent_quanta: 'int', daughter_quanta: 'list') -> 'int'` — Charge-π quanta released when a nucleus fissions = parent − Σ daughters.
- `cosmology.force_strength(force: 'str') -> 'float'` — Relative strength of one of the four interactions (gravity = 1).
- `cosmology.fusion_efficiency(kind: 'str' = 'hot') -> 'float'` — Energy efficiency of 'fusion' (Book 4 p.146): hot fusion = the stellar EM (GEM) pinch
- `cosmology.fusion_energy(mass_kg: 'float') -> 'float'` — Energy a star releases by fusion ≈ FUSION_FRACTION × the full pinch energy.
- `cosmology.galaxy_rotation_velocity(enclosed_mass: 'float', r: 'float', em_force: 'float' = 0.0, orbiting_mass: 'float' = 1.0) -> 'float'` — Orbital speed of a star at radius r including the EM contribution (his p.219 model):
- `cosmology.gem_field_equations() -> 'dict'` — The four GEM (gravito-electromagnetic) field equations — gravity as a Maxwell-style
- `cosmology.gem_gravity_field_divergence(density: 'float') -> 'float'` — The gravito-electric field divergence  ∇·E_g = −4πGρ  (Book 4 p.15).
- `cosmology.gem_pinch_radius(mass: 'float') -> 'float'` — The GEM-pinch scale  r = 2GM/c²  (the Schwarzschild radius — a pinch, not a
- `cosmology.gr_from_g_and_sr(newton_term: 'float', sr_term: 'float') -> 'float'` — Full gravitational effect = convergent Newton + SR-EM term.
- `cosmology.gravitational_acceleration(mass: 'float', r: 'float') -> 'float'` — Surface/field gravitational acceleration  g = G·M/r²  (m/s²).
- `cosmology.gravitational_binding_energy(mass: 'float', radius: 'float') -> 'float'` — Self-gravitational binding energy of a uniform sphere  U = 3GM²/(5R)  (J).
- `cosmology.gravitational_potential_energy(m1: 'float', m2: 'float', r: 'float') -> 'float'` — Gravitational PE  U = −G·m₁m₂/r  (J).
- `cosmology.gravitational_redshift(mass: 'float', r: 'float') -> 'float'` — Gravitational redshift  z = 1/√(1 − 2GM/(rc²)) − 1  (an EM-field effect).
- `cosmology.gravitational_time_dilation(mass: 'float', r: 'float') -> 'float'` — Clock-rate factor in a gravity well  √(1 − 2GM/(r·c²)).
- `cosmology.gravity_field_density(density: 'float') -> 'float'` — Pressure-gradient gravity from mass-energy density  ∇φ = 4πG·ρ.
- `cosmology.gravity_force(m1: 'float', m2: 'float', r: 'float') -> 'float'` — Newton's law of gravitation  F = G·m₁m₂/r²  (N).
- `cosmology.gravity_geometric_mean(m1: 'float', m2: 'float') -> 'float'` — Kelvin's form of gravity as the convergent geometric mean of two masses √(m₁·m₂)
- `cosmology.kepler_period(semimajor_axis_m: 'float', central_mass_kg: 'float') -> 'float'` — Orbital period from Kepler's 3rd law  T = 2π·√(a³/GM)  (s).
- `cosmology.kepler_semimajor(period_s: 'float', central_mass_kg: 'float') -> 'float'` — Semi-major axis from period:  a = (GM·T²/4π²)^(1/3)  (m).
- `cosmology.light_deflection(mass: 'float', r: 'float') -> 'float'` — Deflection of light grazing a mass  α = 4GM/(c²·r)  (radians).
- `cosmology.light_deflection_newtonian(mass: 'float', r: 'float') -> 'float'` — The Newtonian half of the light deflection (≈0.8725″ at the Sun; Book 4 p.135).
- `cosmology.matter_density(em_mass_density: 'float') -> 'float'` — 3D Matter density from 2D mass-energy density:  M = ρ/c⁴  (the same E=Mc⁴ relation
- `cosmology.matter_energy(matter_kg: 'float') -> 'float'` — Energy of a 3D Matter topology  E = M·c⁴  (J).
- `cosmology.matter_from_energy(energy_j: 'float') -> 'float'` — 3D Matter from energy  M = E/c⁴  (kg).
- `cosmology.mercury_precession() -> 'float'` — Perihelion precession of Mercury = 43 arcsec/century (Book 4 p.171).
- `cosmology.nett_convergent_force(grav_force: 'float', em_force: 'float') -> 'float'` — The 'nett convergent force' that holds a galaxy together (Book 4 p.219) = gravity PLUS
- `cosmology.orbital_velocity(mass: 'float', r: 'float') -> 'float'` — Circular orbital velocity  v = √(GM/r)  (m/s).
- `cosmology.pioneer_anomaly() -> 'float'` — The Pioneer anomaly acceleration ≈ 8.74e-10 m/s² (Book 4 p.178).
- `cosmology.planet_distance_km(planet: 'str') -> 'float'` — Mean Sun-distance of a planet in km (from its light-second value).
- `cosmology.poisson_einstein(density: 'float') -> 'float'` — GR field equation source  8πG·ρ (the full GEM form vs 4πG Newtonian).
- `cosmology.poisson_newton(density: 'float') -> 'float'` — Newtonian field equation  ∇²Φ = 4πG·ρ.
- `cosmology.quanta_to_energy(quanta: 'int') -> 'float'` — Energy (J) of a number of charge-π quanta = quanta × m_q × c² = quanta × h.
- `cosmology.redshift_doppler(velocity: 'float') -> 'float'` — Relativistic Doppler redshift  z = √((1+β)/(1−β)) − 1  (β = v/c, receding).
- `cosmology.redshift_energy_falloff(r: 'float', r0: 'float' = 1.0) -> 'float'` — Inverse-square energy diminution of radiant EM with distance:  (r0/r)².
- `cosmology.roche_limit(primary_radius: 'float', primary_density: 'float', satellite_density: 'float') -> 'float'` — Rigid Roche limit  d = R·(2·ρ_primary/ρ_satellite)^(1/3).
- `cosmology.stellar_class(mass_solar: 'float') -> 'str'` — Morgan–Keenan spectral class from a star's mass (in solar masses).
- `cosmology.stellar_collapse_energy(mass_kg: 'float') -> 'float'` — The Sun's actual energy source (Book 4 p.145): Tetryonic Matter collapse = m·c²
- `cosmology.tidal_acceleration(mass: 'float', r: 'float', dr: 'float') -> 'float'` — Tidal acceleration across a small span  a = 2GM·dr/r³.
- `cosmology.vacuum_impedance() -> 'float'` — Impedance of free space as Tetryonics frames it:  Z = ε₀μ₀ = 1/c².
- `cosmology.weight_force(mass: 'float', g: 'float' = 9.80665) -> 'float'` — Weight  w = m·g  (N).

## `geometrics`
> Geometrics — Book 5: the pure equilateral-triangle maths underpinning everything.

- `geometrics.apothem(n: 'int', side: 'float') -> 'float'` — Apothem (inradius) of a regular n-gon  = s/(2·tan(π/n)).
- `geometrics.area_perimeter_ratio() -> 'float'` — Equilateral A/P² ratio = 1/(12√3) ≈ 0.04811.
- `geometrics.basel_sum(terms: 'int') -> 'float'` — Partial Basel sum Σ 1/n² (converges to π²/6).
- `geometrics.binomial(n: 'int', k: 'int') -> 'int'` — Binomial coefficient C(n,k) — the entries of Pascal's triangle (Book 5 p.48).
- `geometrics.c_power_ladder(n: 'int') -> 'float'` — The cⁿ dimensional ladder: c¹ (1D velocity) … c⁴ (quaternion volume) (Book 5 p.141).
- `geometrics.cartesian_to_polar(x: 'float', y: 'float') -> 'tuple'` — (x, y) → (r, θ°).
- `geometrics.circumcircle_area(side: 'float') -> 'float'` — Area of the circumscribed circle  π·R² = (π/3)·s².
- `geometrics.circumradius(side: 'float') -> 'float'` — Circumscribed-circle radius R = s/√3.  (R = 2·r — the 1:2 ratio.)
- `geometrics.cos_deg(angle_deg: 'float') -> 'float'` — 
- `geometrics.deltahedron_metrics(solid: 'str', edge: 'float' = 1.0) -> 'dict'` — Surface area & volume of a Tetryonic deltahedron.
- `geometrics.dihedral_angle(solid: 'str') -> 'float'` — Dihedral angle (degrees) between adjacent faces of a Platonic solid.
- `geometrics.equilateral_area(side: 'float') -> 'float'` — Area = (√3/4)·s².
- `geometrics.equilateral_distribution(n: 'int') -> 'list[int]'` — Kelvin's quantum probability distribution (Book 5 p.152): the equilateral row
- `geometrics.equilateral_height(side: 'float') -> 'float'` — Height = (√3/2)·s.
- `geometrics.euler_characteristic(solid: 'str') -> 'int'` — F − E + V (should be 2 for every convex polyhedron). Accepts Platonic or deltahedron names.
- `geometrics.euler_identity() -> 'complex'` — Euler's identity value  e^(iπ) + 1  (= 0).
- `geometrics.euler_inequality_ok(circumradius_R: 'float', inradius_r: 'float') -> 'bool'` — Euler's inequality for a triangle:  R ≥ 2r (equality only for equilateral).
- `geometrics.eutrigon_c2(a: 'float', b: 'float') -> 'float'` — Third side² of a 60°-apex triangle: c² = a² + b² − a·b  (cos60 = ½).
- `geometrics.eutrigon_identity(a: 'float', b: 'float', c: 'float') -> 'float'` — Tetryonic eutrigon relation  a·b = a² + b² − c²  (returns LHS−RHS, ~0 if 60°).
- `geometrics.fourth_power(n: 'int') -> 'int'` — n⁴ = (n²)² — fourth powers are squares of squares (Book 5 p.42).
- `geometrics.geometric_mean(a: 'float', b: 'float') -> 'float'` — Geometric mean √(a·b) — Kelvin's form for the convergent gravity of two fields.
- `geometrics.geometric_series_sum(ratio: 'float', terms: 'int' = None) -> 'float'` — Sum of a geometric series. With ``terms`` → finite Σ₀^{n-1} rⁿ; else the
- `geometrics.golden_power(n: 'int') -> 'float'` — φⁿ via Binet:  φⁿ = (φⁿ).
- `geometrics.golden_ratio() -> 'float'` — The golden ratio φ = (1+√5)/2 ≈ 1.618 (Book 5 pp.182-184).
- `geometrics.golden_rhombus(short_diagonal: 'float' = 1.0) -> 'dict'` — Kelvin's KE energy 'diamond' is a golden rhombus (Book 5 p.183): a rhombus
- `geometrics.hexagon_area(side: 'float') -> 'float'` — Regular hexagon area  (3√3/2)·s²  (= 6 equilateral triangles).
- `geometrics.i_power(n: 'int') -> 'tuple[int, int]'` — i^n as a point on the unit circle (Book 5 p.55), returned as (real, imag):
- `geometrics.imaginary_rotation(x: 'float', y: 'float', quarter_turns: 'int' = 1) -> 'tuple[float, float]'` — √−1 is the quarter-turn operator (Book 5 p.55): multiplying a 2D vector — a complex
- `geometrics.incircle_area(side: 'float') -> 'float'` — Area of the inscribed circle  π·r² = (π/12)·s².
- `geometrics.incircle_to_triangle_ratio() -> 'float'` — Ratio of inscribed-circle area to equilateral-triangle area = π/(3√3) ≈ 0.6046.
- `geometrics.infinities_exist() -> 'bool'` — Renormalisation — the Tetryonic answer (Book 5 p.144): infinities do NOT exist. A
- `geometrics.inradius(side: 'float') -> 'float'` — Inscribed-circle radius r = s/(2√3).
- `geometrics.kepler_bouwkamp(terms: 'int' = 1000) -> 'float'` — Partial product Π_{n=3}^{N} cos(π/n) → the Kepler–Bouwkamp constant ≈ 0.1149.
- `geometrics.law_of_cosines(a: 'float', b: 'float', angle_c_deg: 'float') -> 'float'` — General law of cosines  c = √(a² + b² − 2ab·cos C).  (C=60° → the eutrigon.)
- `geometrics.mass_energy_pi(level: 'int') -> 'int'` — The 4nπ mass-energy scaling of a tetryon at level n  = 4·n  (π multiples).
- `geometrics.nth_even(n: 'int') -> 'int'` — The n-th even number = 2n (photon levels).
- `geometrics.nth_odd(n: 'int') -> 'int'` — The n-th odd number = 2n−1 (boson levels).
- `geometrics.odd_as_square_difference(n: 'int') -> 'int'` — The geometric odd-number identity (Book 5 p.86): n² − (n−1)² = 2n−1 — each odd number
- `geometrics.odom_golden_ratio() -> 'float'` — The golden ratio φ measured from George Odom's construction (Book 5 p.182):
- `geometrics.particle_solid_metrics(particle: 'str', edge: 'float' = 1.0) -> 'dict'` — Full geometry of a particle's 3D deltahedron: faces/edges/vertices + area + volume.
- `geometrics.pascal_row(n: 'int') -> 'list'` — Row n of Pascal's triangle (0-indexed).
- `geometrics.pentagonal_number(n: 'int') -> 'int'` — n-th pentagonal number  = n(3n−1)/2.
- `geometrics.perimeter(side: 'float') -> 'float'` — Equilateral perimeter  p = 3·s.
- `geometrics.pi_content(shape: 'str') -> 'float'` — π-radian content of a planar shape (in radians).
- `geometrics.platonic_metrics(solid: 'str', edge: 'float' = 1.0) -> 'dict'` — Surface area & volume of a classical Platonic solid (the p19 comparison).
- `geometrics.polar_to_cartesian(r: 'float', theta_deg: 'float') -> 'tuple'` — (r, θ°) → (x, y).
- `geometrics.polygon_exterior_angle(n: 'int') -> 'float'` — Exterior angle of a regular n-gon (degrees)  = 360/n.
- `geometrics.polygon_interior_angle(n: 'int') -> 'float'` — Interior angle of a regular n-gon (degrees)  = (n−2)·180/n.
- `geometrics.probability_from_amplitude(amplitude: 'float') -> 'float'` — Born rule as geometry (Book 5 p.157): probability = |amplitude|² — the square (an
- `geometrics.regular_polygon_area(n: 'int', side: 'float') -> 'float'` — Area of a regular n-gon  A = (1/4)·n·s²·cot(π/n).
- `geometrics.regular_polygon_metrics(n: 'int', side: 'float') -> 'dict'` — Bundle of regular-n-gon metrics: perimeter, apothem, area, interior/exterior angle.
- `geometrics.regular_polygon_perimeter(n: 'int', side: 'float') -> 'float'` — Perimeter of a regular n-gon  = n·s.
- `geometrics.side_from_area(area: 'float') -> 'float'` — Invert the equilateral area: side = √(4·A/√3).
- `geometrics.sin_deg(angle_deg: 'float') -> 'float'` — Sine of an angle in degrees.
- `geometrics.solid_for_particle(particle: 'str') -> 'dict'` — The particle's Tetryonic DELTAHEDRON: {solid, faces, edges, vertices,
- `geometrics.square_from_odds(n: 'int') -> 'int'` — Sum of the first n odd numbers = n² (the tessellation identity).
- `geometrics.square_pyramidal_number(n: 'int') -> 'int'` — n-th square-pyramidal number  = n(n+1)(2n+1)/6 (= Σ k²).
- `geometrics.sum_of_cubes(n: 'int') -> 'int'` — Σk³ = (Σk)² = T(n)²  (cubes sum to a square triangular number; Book 5 p.41).
- `geometrics.tan_deg(angle_deg: 'float') -> 'float'` — 
- `geometrics.taylor_cos(x: 'float', terms: 'int' = 10) -> 'float'` — Maclaurin series for cos x  = Σ (−1)ⁿ x^(2n)/(2n)!.
- `geometrics.taylor_exp(x: 'float', terms: 'int' = 12) -> 'float'` — Maclaurin series for eˣ  = Σ xⁿ/n!  (Book 5 p.55).
- `geometrics.taylor_sin(x: 'float', terms: 'int' = 10) -> 'float'` — Maclaurin series for sin x  = Σ (−1)ⁿ x^(2n+1)/(2n+1)!.
- `geometrics.tetrahedral_number(n: 'int') -> 'int'` — n-th tetrahedral number  = n(n+1)(n+2)/6.
- `geometrics.triangular_number(n: 'int') -> 'int'` — n-th triangular number  T = n(n+1)/2.
- `geometrics.twin_triangular_square(n: 'int') -> 'int'` — Consecutive triangular numbers sum to a square: T(n) + T(n−1) = n² (p.40).
- `geometrics.viviani_distance_sum(side: 'float') -> 'float'` — Viviani's theorem: sum of perpendiculars from any interior point of an equilateral

## `numbertheory`
> Number theory — Book 5 (Geometrics).

- `numbertheory.digital_root(n: 'int') -> 'int'` — Digital root (repeated digit sum) = 1 + (n−1) mod 9 for n>0 (base-9 cycle).
- `numbertheory.fibonacci(n: 'int') -> 'int'` — The n-th Fibonacci number (0-indexed: 0,1,1,2,3,5,…).
- `numbertheory.fibonacci_ratio(n: 'int') -> 'float'` — F(n+1)/F(n) — converges to the golden ratio φ.
- `numbertheory.goldbach_pair(even_n: 'int') -> 'tuple'` — A pair of primes summing to an even number > 2 (Goldbach).
- `numbertheory.is_mersenne_prime(n: 'int') -> 'bool'` — Whether 2ⁿ − 1 is prime (n itself must be prime).
- `numbertheory.is_perfect_number(n: 'int') -> 'bool'` — Whether n equals the sum of its proper divisors (6, 28, 496, …).
- `numbertheory.is_prime(n: 'int') -> 'bool'` — Primality test.
- `numbertheory.is_twin_prime_form(n: 'int') -> 'bool'` — Whether n has the 6k±1 form that all primes >3 take.
- `numbertheory.lucas(n: 'int') -> 'int'` — The n-th Lucas number (2,1,3,4,7,11,…); ratio also converges to φ.
- `numbertheory.mersenne(n: 'int') -> 'int'` — The n-th Mersenne number  Mₙ = 2ⁿ − 1.
- `numbertheory.prime_as_square_difference(n: 'int') -> 'tuple'` — Every odd number 2k−1 = k² − (k−1)²; returns (k, k−1) for odd n.
- `numbertheory.primes_up_to(limit: 'int') -> 'list'` — All primes ≤ limit (sieve).

## `music`
> Music & harmonics — Book 5 (Geometrics).

- `music.circle_of_fifths() -> 'list'` — The 12 notes ordered by ascending perfect fifths (×3:2, mod octave).
- `music.equal_tempered_frequency(midi_note: 'int') -> 'float'` — 12-TET frequency (Hz) of a MIDI note number  f = 440·2^((n−69)/12)  (A4=440).
- `music.interval_from_frequencies(f_low: 'float', f_high: 'float') -> 'float'` — Frequency ratio between two pitches.
- `music.interval_ratio(name: 'str') -> 'float'` — Just-intonation frequency ratio of a named interval (e.g. 'fifth' → 1.5).
- `music.note_frequency(note: 'str', octave: 'int' = 4) -> 'float'` — 12-TET frequency (Hz) of a named note + octave, e.g. note_frequency('A',4)=440.
- `music.note_index(note: 'str') -> 'int'` — Chromatic index 0..11 of a note name (C=0 … B=11).
- `music.note_to_phase(note: 'str') -> 'float'` — Phase angle (degrees) of a note on the chromatic circle  = semitone × 30°.
- `music.scale_ratios(scale: 'str' = 'major') -> 'list'` — Just-intonation frequency ratios of a scale's degrees (relative to the tonic).
- `music.semitones_to_ratio(semitones: 'int') -> 'float'` — Equal-tempered frequency ratio for an interval of n semitones = 2^(n/12).

## `thermodynamics`
> Thermodynamics & entropy — appears across Books 2 & 4 (blackbody, stellar, vacuum energy).

- `thermodynamics.bekenstein_hawking_entropy(area_m2: 'float') -> 'float'` — Horizon entropy  S = A·k_B·c³/(4·G·ħ)  (J/K) — the GEM-pinch horizon entropy.
- `thermodynamics.carnot_efficiency(t_hot: 'float', t_cold: 'float') -> 'float'` — Maximum (Carnot) efficiency  η = 1 − T_cold/T_hot.
- `thermodynamics.entropy_boltzmann(microstates: 'float') -> 'float'` — Boltzmann entropy  S = k_B · ln(W)  (J/K).
- `thermodynamics.entropy_clausius(heat_j: 'float', temperature_k: 'float') -> 'float'` — Clausius entropy change  ΔS = Q/T  (J/K).
- `thermodynamics.ideal_gas_moles(pressure_pa: 'float', volume_m3: 'float', temperature_k: 'float') -> 'float'` — Ideal-gas amount  n = PV/(RT)  (mol).
- `thermodynamics.ideal_gas_pressure(moles: 'float', temperature_k: 'float', volume_m3: 'float') -> 'float'` — Ideal-gas law  P = nRT/V  (Pa).
- `thermodynamics.ideal_gas_temperature(pressure_pa: 'float', volume_m3: 'float', moles: 'float') -> 'float'` — Ideal-gas temperature  T = PV/(nR)  (K).
- `thermodynamics.ideal_gas_volume(moles: 'float', temperature_k: 'float', pressure_pa: 'float') -> 'float'` — Ideal-gas volume  V = nRT/P  (m³).
- `thermodynamics.internal_energy(moles: 'float', temperature_k: 'float', dof: 'int' = 3) -> 'float'` — Internal energy of an ideal gas  U = (dof/2)·nRT  (J).
- `thermodynamics.pressure_energy_density(energy_j: 'float', volume_m3: 'float') -> 'float'` — Pressure as energy density  P = E/V  (Pa) — Book 4 p.91 (P = F/A = E/V).
- `thermodynamics.thermal_energy(temperature_k: 'float') -> 'float'` — Characteristic thermal energy per degree of freedom  E = k_B·T  (J).

## `statistics`
> Statistics & quantum probability — Books 1 & 2 (EM-wavefunction distributions, uncertainty).

- `statistics.binomial_probability(n: 'int', k: 'int', p: 'float') -> 'float'` — Binomial probability  C(n,k)·pᵏ·(1−p)ⁿ⁻ᵏ.
- `statistics.born_rule(amplitude: 'float') -> 'float'` — Probability/intensity = |amplitude|²  (the EM wavefunction Born rule).
- `statistics.gaussian(x: 'float', mu: 'float' = 0.0, sigma: 'float' = 1.0) -> 'float'` — Normal distribution  P(x) = 1/(σ√2π)·exp(−(x−μ)²/2σ²).
- `statistics.heisenberg_min_energy(delta_t: 'float') -> 'float'` — Minimum energy spread from time spread  ΔE ≥ ħ/(2·Δt).
- `statistics.heisenberg_min_momentum(delta_x: 'float') -> 'float'` — Minimum momentum spread from position spread  Δp ≥ ħ/(2·Δx).
- `statistics.normal_empirical_rule() -> 'tuple'` — The 68–95–99.7 rule: fraction of a normal distribution within 1, 2, 3 σ.
- `statistics.shannon_entropy(probabilities) -> 'float'` — Shannon information entropy  H = −Σ pᵢ·log₂(pᵢ)  (bits).
- `statistics.standard_deviation(values) -> 'float'` — Population standard deviation σ = √(Σ(x−μ)²/N).
- `statistics.z_score(x: 'float', mu: 'float', sigma: 'float') -> 'float'` — Standard score  z = (x − μ)/σ.

## `kinematics`
> Kinematics & classical mechanics — recurring across all books (v=Δx/Δt, F=ma, SHM).

- `kinematics.acceleration(delta_v: 'float', time: 'float') -> 'float'` — a = Δv/Δt.
- `kinematics.centripetal_acceleration(vel: 'float', radius: 'float') -> 'float'` — a_c = v²/r.
- `kinematics.force(mass: 'float', accel: 'float') -> 'float'` — Newton's 2nd law  F = m·a.
- `kinematics.impulse(force_n: 'float', time: 'float') -> 'float'` — Impulse  J = F·Δt = Δp.
- `kinematics.kinetic_energy(mass: 'float', vel: 'float') -> 'float'` — ⚠ Classical ½·m·v² — NOT Kelvin's primary form. His scalar mass-energy is
- `kinematics.momentum(mass: 'float', vel: 'float') -> 'float'` — p = m·v.
- `kinematics.power(work_j: 'float', time: 'float') -> 'float'` — Power  P = W/t.
- `kinematics.shm_frequency(mass: 'float', spring_constant: 'float') -> 'float'` — SHM frequency  f = 1/T.
- `kinematics.shm_period(mass: 'float', spring_constant: 'float') -> 'float'` — SHM period  T = 2π·√(m/k).
- `kinematics.shm_restoring_force(spring_constant: 'float', displacement: 'float') -> 'float'` — Hooke's law / SHM restoring force  F = −k·x.
- `kinematics.velocity(displacement: 'float', time: 'float') -> 'float'` — v = Δx/Δt.
- `kinematics.work(force_n: 'float', distance: 'float') -> 'float'` — Work  W = F·d.

## `dynamics`
> Dynamics — the INTERACTIONS of Tetryonics as computable state-transitions.

- `class dynamics.Interaction(kind: 'str', direction: 'str', force_n: 'float' = 0.0, detail: 'dict' = <factory>) -> None` — A force interaction between two charged geometries.
- `class dynamics.Transition(kind: 'str', before: 'str' = '', after: 'str' = '', quanta: 'float' = 0.0, energy_j: 'float' = 0.0, energy_ev: 'float' = 0.0, wavelength_m: 'float' = 0.0, detail: 'dict' = <factory>) -> None` — A computed state-transition (a process happening to energy/charge/Matter).
- `dynamics.absorb_photon(n_low: 'int', photon_energy_ev: 'float', max_level: 'int' = 50) -> 'Transition'` — A bound electron at n_low absorbs a photon and climbs to a higher level.
- `dynamics.charge_interaction(p1, p2, r: 'float') -> 'Interaction'` — EM force between two particles (his Coulomb k). Opposites attract, similars repel.
- `dynamics.emit_photon(n_high: 'int', n_low: 'int') -> 'Transition'` — An electron drops from n_high to n_low, emitting a photon (a diamond).
- `dynamics.fusion(mass_kg: 'float') -> 'Transition'` — Stellar p-p 'fusion' release = only 1/3600 of the full pinch energy.
- `dynamics.level_energy_ev(n: 'int') -> 'float'` — Bound KEM-field energy of level n (eV) = −KEM/n²  (his ladder, KEM=13.525).
- `dynamics.pair_creation(photon_energy_j: 'float') -> 'Transition'` — Energy -> Matter: a photon above 2·m_e·c² creates an electron-positron pair.
- `dynamics.pinch(mass_kg: 'float') -> 'Transition'` — Collapse a 3D Matter topology to 2D radiant mass-energy — 100% efficient (E = m·c²).
- `dynamics.seek_equilibrium(*particles) -> 'dict'` — Combine charged geometries; their net charge moves toward equilibrium (neutrality).
- `dynamics.shell_quanta(n: 'int') -> 'int'` — Mass-energy quanta of shell n = 12·n².
- `dynamics.spectral_emission(series: 'str', n_high: 'int') -> 'Transition'` — Emit the photon of a named series transition (lyman..abraham).
- `dynamics.strong_interaction(fascia_sign_a: 'int', fascia_sign_b: 'int') -> 'Interaction'` — Strong force = the interaction of two Matter fascia.

## `matter`
> Matter assembly — building ALL Matter from the TETRYON, as a COMPOSITION TREE.

- `class matter.Assembly(name: 'str', kind: 'str', components: 'tuple', topology: 'int | None' = None, n_planck: 'float | None' = None) -> None` — A piece of Matter as a tree of components (each a Tetryon or a sub-Assembly).
- `matter.build(name: 'str') -> 'Assembly'` — Build any standard particle/atom by name, from tetryons.
- `matter.build_atom(z: 'int') -> 'Assembly'` — A neutral atom built from its building blocks: Z deuterium units (Z>=2);
- `matter.build_baryon(name: 'str') -> 'Assembly'` — 
- `matter.build_deuterium() -> 'Assembly'` — Deuterium = proton + neutron + electron (21 tetryons, 84π). The building block of
- `matter.build_hydrogen() -> 'Assembly'` — Hydrogen = proton + electron (12 tetryons, 48π) — no neutron.
- `matter.build_lepton(name: 'str') -> 'Assembly'` — 
- `matter.build_meson(name: 'str') -> 'Assembly'` — 
- `matter.build_quark(flavour: 'str') -> 'Assembly'` — 
- `matter.build_tetryon(state: 'str' = 'positive') -> 'Assembly'` — 
- `matter.matter_pi(n_tetryons: 'int') -> 'int'` — The mass-energy geometry of n tetryons = 4·n π (Book 1 p114: Matter = 4nπ).
- `matter.tetryon(cw: 'int', level: 'int' = 1) -> 'Tetryon'` — A tetryon: ``cw`` clockwise(+) fascia and ``4-cw`` counter-clockwise(-).
- `matter.tetryon_count(name: 'str') -> 'int'` — How many tetryons make up a named particle/atom.

---

*448 functions and 9 classes across 24 modules. Generated from the engine's own docstrings.*