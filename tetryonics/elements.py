"""
The element / periodic engine.

Tetryonic chemistry rule (Planck paper + the SketchUp model filenames):
  * Deuterium (84 charge-pi) is the foundational repeating unit of all elements.
  * Every element has equal numbers of protons = neutrons = electrons = Z
    (no "excess" neutrons) -- except Hydrogen (Z=1) which has no neutron.
  * Charge-pi topology = 36*(protons + neutrons) + 12*electrons
        Hydrogen = 48,  Deuterium = 84,  element Z>=2 = 84*Z
  * Rest mass = total Planck quanta * m_q
        quanta = protons*N_PROTON + neutrons*N_NEUTRON + electrons*N_ELECTRON

Verified: Hydrogen -> 1.6605e-27 kg (1 amu);  Helium -> ~6.64e-27 kg. See tests/.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import constants as K

# Symbols indexed by atomic number Z (1..118). Matches the 3D Elements (.skp) set.
SYMBOLS = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
    "Kl", "Ab",   # Z=119 Kelvinium, Z=120 Abrahamium — Kelvin's own naming (Book 3 p.350)
]


@dataclass(frozen=True)
class Atom:
    """A neutral atom (or named isotope) as a Tetryonic Matter topology."""

    z: int
    protons: int
    neutrons: int
    electrons: int
    name: str = ""

    @property
    def symbol(self) -> str:
        return SYMBOLS[self.z - 1] if 1 <= self.z <= len(SYMBOLS) else f"Z{self.z}"

    @property
    def topology_pi(self) -> int:
        """Charge-pi count: 36 per nucleon + 12 per electron."""
        return 36 * (self.protons + self.neutrons) + 12 * self.electrons

    @property
    def deuterium_units(self) -> float:
        """How many 84-pi deuterium units this topology equals."""
        return self.topology_pi / 84.0

    @property
    def planck_quanta(self) -> float:
        return (self.protons * K.N_PROTON
                + self.neutrons * K.N_NEUTRON
                + self.electrons * K.N_ELECTRON)

    @property
    def mass_kg(self) -> float:
        return K.mass_from_quanta(self.planck_quanta)

    @property
    def mass_amu(self) -> float:
        return self.mass_kg / K.mass_from_quanta(K.N_HYDROGEN)

    @property
    def net_charge_e(self) -> int:
        return self.protons - self.electrons   # neutral atom -> 0

    # --- Energy-level (nuclear-shell) mass, Kelvin's heavy-element method -----
    @property
    def shell_mass_amu(self) -> float:
        """Mass (amu) from the n-level Deuterium model — heavy-element-accurate."""
        return nuclear_mass_amu(self.z)

    @property
    def shell_mass_kg(self) -> float:
        return nuclear_mass_kg(self.z)

    @property
    def shell_mass_mev(self) -> float:
        return nuclear_mass_mev(self.z)

    def shells(self) -> "list[NuclearShell]":
        """The deuteron stack across energy levels K..R (see nuclear_shell_fill)."""
        return nuclear_shell_fill(self.z)

    def describe(self) -> str:
        nm = f" ({self.name})" if self.name else ""
        return (f"Z={self.z:<3} {self.symbol:<3}{nm:<12} "
                f"p={self.protons} n={self.neutrons} e={self.electrons}  "
                f"topology={self.topology_pi:>5}pi (={self.deuterium_units:g} D)  "
                f"mass={self.mass_kg:.6e} kg ({self.mass_amu:.4f} amu)")


def element(z: int) -> Atom:
    """The standard neutral atom for atomic number ``z`` (Tetryonic convention).

    Hydrogen (Z=1) has no neutron; every other element has protons=neutrons=electrons=Z.
    Tetryonics caps the periodic table at Z=120 (Book 3 p.27/69).
    """
    if z < 1:
        raise ValueError("atomic number must be >= 1")
    if z > K.MAX_Z:
        raise ValueError(f"Tetryonic periodic table caps at Z={K.MAX_Z}")
    neutrons = 0 if z == 1 else z
    return Atom(z=z, protons=z, neutrons=neutrons, electrons=z)


# --- Nuclear energy-level mass model (Book 3 p.83 & p.92) --------------------
# "All elements are comprised of n-level Deuterium nuclei" (p.92).  The Deuterium
# nuclei fill nuclear shells K..R (energy levels n=1..8) with the SAME capacities as
# the electron shells (2,8,18,32,32,18,8,2).  The mass-energy of a Deuteron CLIMBS
# with its level n — outer-shell nuclei are heavier purely because of their higher
# energy level, NOT because of extra particles.  Book 3 p.83 states the historical
# "excess neutrons" explanation of heavy-element mass "is not" correct: every element
# has equal protons = neutrons = electrons = Z.
#
# Per-shell Deuteron (proton+neutron) mass-energy in MeV.  A ground (K) Deuteron is
# exactly two baryon rest-masses; each higher level n carries more KEM, scaling as the
# square of its baryon quantum number d = 24+n  (p.92 labels the Deuteron levels 25..32
# for shells K..R, and the per-row formula is Z[[72·d·n²]+[12·n·v²]+[1.2e20]]).  So
#     MeV(n) = 2·BARYON · ((24+n)/25)²
# which reproduces the plate's published 1861.9, 2013.8, … 3050.6 MeV exactly, and the
# K value is 2·930.947 = 1861.894 MeV (a ground-state Deuteron, zero KEM).
SHELL_LETTERS = "KLMNOPQR"           # n = 1..8
ELECTRON_REST_MEV = K.ELECTRON_KEV / 1000.0   # 0.496519 MeV per bound electron (p.92)
DEUTERON_SHELL_MEV = {n: 2 * K.BARYON_MEV * ((24 + n) / 25.0) ** 2 for n in range(1, 9)}


@dataclass(frozen=True)
class NuclearShell:
    """One filled nuclear energy level (a row on the p.92 plate)."""

    n: int                  # principal energy level 1..8
    letter: str             # K..R
    deuterons: int          # how many Deuterium nuclei sit in this shell
    mev_each: float         # mass-energy of one Deuteron at this level
    capacity: int           # how many this shell can hold (2,8,18,32,32,18,8,2)

    @property
    def mev_total(self) -> float:
        return self.deuterons * self.mev_each


def nuclear_shell_fill(z: int) -> list[NuclearShell]:
    """Distribute ``z`` Deuterium nuclei across the K..R nuclear shells (Book 3 p.92).

    Each Deuterium unit is proton+neutron+**electron**, so the nucleus sits at its
    electron's energy level: the deuterons occupy the SAME shells as the electrons,
    filled in Aufbau/Madelung order.  The occupancy of principal level n therefore
    equals the number of electrons in shell n.  (This is the fix that makes the model
    reproduce Kelvin's own per-element masses — a naive 2,8,18,32 cap-cascade does not.)

    Returns one ``NuclearShell`` per occupied level, so you can SEE how a heavy element
    stacks its deuterons up the energy levels (this is what makes it heavy).
    """
    if z < 1:
        raise ValueError("atomic number must be >= 1")
    if z > K.MAX_Z:
        raise ValueError(f"Tetryonic periodic table caps at Z={K.MAX_Z}")
    per_n: dict[int, int] = {}
    for tok in electron_configuration(z).split():
        n = int(tok[0])
        per_n[n] = per_n.get(n, 0) + int(tok[2:])
    caps = K.PERIODIC_SHELL_CAPS
    return [NuclearShell(n=n, letter=SHELL_LETTERS[n - 1], deuterons=per_n[n],
                         mev_each=DEUTERON_SHELL_MEV[n],
                         capacity=caps[n - 1] if n <= len(caps) else 0)
            for n in sorted(per_n)]


def nuclear_mass_mev(z: int) -> float:
    """Total rest mass-energy (MeV) of element Z by Kelvin's energy-level method.

    = Σ over filled shells (deuterons · per-level Deuteron MeV)  +  Z bound electrons.
    Hydrogen (Z=1) is the lone exception: a single proton + electron, no neutron, so
    half a K-shell Deuteron's baryon energy.
    """
    if z == 1:
        return K.BARYON_MEV + ELECTRON_REST_MEV          # one proton + one electron
    baryon = sum(s.mev_total for s in nuclear_shell_fill(z))
    return baryon + z * ELECTRON_REST_MEV


def nuclear_mass_kg(z: int) -> float:
    """Energy-level rest mass (kg) of element Z (his method; no excess neutrons)."""
    return K.mass_from_mev(nuclear_mass_mev(z))


def nuclear_mass_amu(z: int) -> float:
    """Energy-level rest mass (amu) of element Z — reproduces Kelvin's per-element pages.

    This is the figure printed on each Book 3 element page (C=12.6493, Fe=58.9648,
    Au=195.0261, U=231.8998 — all matched to ~0.005 amu).  Unlike :func:`element`'s
    ``mass_amu`` (the flat ground-state floor with every Deuteron at level K, which by
    coincidence tracks mainstream amu for light elements), this lifts each Deuteron to
    its true Aufbau energy level, so mass grows the Tetryonic way: higher n, not extra
    neutrons.  His values deliberately differ from CODATA — heavier, by the KEM the
    higher levels carry.
    """
    return K.amu_from_mev(nuclear_mass_mev(z))


def nuclear_shell_report(z: int) -> str:
    """Human-readable breakdown of element Z's deuteron shell stack (p.92 style)."""
    atom = element(z)
    lines = [f"Z={z} {atom.symbol}  - n-level Deuterium nuclei (Book 3 p.92)"]
    if z == 1:
        # Hydrogen is the exception: 1 proton + 1 electron, NO neutron — not a full Deuteron.
        lines.append(f"  K (n=1):  1 proton (no neutron) x {K.BARYON_MEV:>7.1f} MeV "
                     f"= {K.BARYON_MEV:>10.1f} MeV")
    else:
        for s in nuclear_shell_fill(z):
            lines.append(f"  {s.letter} (n={s.n}): {s.deuterons:>2}/{s.capacity:<2} deuterons "
                         f"x {s.mev_each:>7.1f} MeV = {s.mev_total:>10.1f} MeV")
    lines.append(f"  + {z} electrons x {ELECTRON_REST_MEV*1000:.3f} keV")
    lines.append(f"  = {nuclear_mass_mev(z):,.1f} MeV  ->  {nuclear_mass_amu(z):.3f} amu "
                 f"(flat base model: {atom.mass_amu:.3f} amu)")
    return "\n".join(lines)


# --- Named light isotopes (the hydrogen family) ------------------------------
def hydrogen() -> Atom:
    return Atom(z=1, protons=1, neutrons=0, electrons=1, name="protium")


def deuterium() -> Atom:
    return Atom(z=1, protons=1, neutrons=1, electrons=1, name="deuterium")


def tritium() -> Atom:
    return Atom(z=1, protons=1, neutrons=2, electrons=1, name="tritium")


def isotope(z: int, mass_number: int, name: str = "") -> Atom:
    """An isotope with a given nucleon count (neutrons = A - Z)."""
    return Atom(z=z, protons=z, neutrons=mass_number - z, electrons=z, name=name)


def ion(z: int, charge: int, name: str = "") -> Atom:
    """A charged ion of element Z (charge = protons − electrons; e.g. Na⁺ → charge +1)."""
    neutrons = 0 if z == 1 else z
    return Atom(z=z, protons=z, neutrons=neutrons, electrons=z - charge,
                name=name or f"{SYMBOLS[z-1]}{charge:+d}")


# Common acids/bases registry (Book 3 p.378).
ACIDS = {
    "hydrochloric": "HCl", "nitric": "HNO3", "sulfuric": "H2SO4",
    "phosphoric": "H3PO4", "carbonic": "H2CO3", "acetic": "C2H4O2",
    "oxalic": "C2H2O4", "citric": "C6H8O7",
}
BASES = {"sodium_hydroxide": "NaOH", "potassium_hydroxide": "KOH",
         "ammonia": "NH3", "calcium_hydroxide": "CaO2H2"}


def acid(name: str) -> str:
    """Formula of a named acid."""
    return ACIDS[name.lower()]


def periodic_table(z_max: int = 20) -> list[Atom]:
    return [element(z) for z in range(1, z_max + 1)]


# --- Chemistry: shells, configuration, ionisation (Book 3) -------------------
SUBSHELL_CAPACITY = {"s": 2, "p": 6, "d": 10, "f": 14}

# Madelung (n+ℓ) filling order of subshells.
_MADELUNG = [
    (1, "s"), (2, "s"), (2, "p"), (3, "s"), (3, "p"), (4, "s"), (3, "d"),
    (4, "p"), (5, "s"), (4, "d"), (5, "p"), (6, "s"), (4, "f"), (5, "d"),
    (6, "p"), (7, "s"), (5, "f"), (6, "d"), (7, "p"),
]

_SYMBOL_TO_Z = {s: i + 1 for i, s in enumerate(SYMBOLS)}


def shell_capacity(n: int) -> int:
    """Electrons a principal shell can hold = 2·n²  (standard QM; Book 3 p.69)."""
    return 2 * n * n


def electron_configuration(z: int) -> str:
    """Ground-state electron configuration (Aufbau/Madelung order), e.g. '1s2 2s2 2p4'."""
    remaining = z
    parts = []
    for n, sub in _MADELUNG:
        if remaining <= 0:
            break
        cap = SUBSHELL_CAPACITY[sub]
        fill = min(cap, remaining)
        parts.append(f"{n}{sub}{fill}")
        remaining -= fill
    return " ".join(parts)


def ionisation_energy(z: int, n: int = 1) -> float:
    """Hydrogenic ionisation energy (eV)  E = 13.525·Z²/n²  (his KEM ground, Book 3 p.75).

    Uses Kelvin's KEM-field ground 13.525 eV (constants.KEM_EV) — the value his per-level
    eigenstate table is built on. (Book 3 p.79/80 also restates the standard 13.6·Z²/n²
    Rydberg form; that rounded figure is the free-electron boundary, not the eigenstate base.)"""
    return K.KEM_EV * z * z / (n * n)


# US-spelling alias.
ionization_energy = ionisation_energy


def periodic_shell_cap(level: int) -> int:
    """Electrons a periodic shell holds (capped/mirrored 2,8,18,32,32,18,8,2; Book 3 p.27/69)."""
    caps = K.PERIODIC_SHELL_CAPS
    return caps[level - 1] if 1 <= level <= len(caps) else 0


def valence_electrons(z: int) -> int:
    """Outer-shell electron count (highest principal level). Good for main-group valence."""
    cfg = electron_configuration(z)
    max_n = max(int(tok[0]) for tok in cfg.split())
    return sum(int(tok[2:]) for tok in cfg.split() if int(tok[0]) == max_n)


def valence(z: int) -> int:
    """Maximum valence / oxidation reach (Book 3 p.381 table: Sc=3, Ni=10, Au=11, Hg=2).

    Outer ns + np electrons, plus any *partially-filled* (n−1)d electrons (a filled d¹⁰
    sub-shell is a stable core and does not contribute)."""
    cfg = electron_configuration(z)
    toks = cfg.split()
    max_n = max(int(t[0]) for t in toks)
    v = sum(int(t[2:]) for t in toks if int(t[0]) == max_n)
    for t in toks:
        n, sub, cnt = int(t[0]), t[1], int(t[2:])
        if n == max_n - 1 and sub == "d" and cnt < 10:
            v += cnt
    return v


def element_quanta(z: int) -> int:
    """Integer charge-π quanta of a neutral atom (84·Z for Z≥2; H=48). The book's
    primary per-atom currency."""
    return element(z).topology_pi


def molar_mass(z: int) -> float:
    """Molar mass in g/mol (numerically the atomic mass in amu)."""
    return element(z).mass_amu


def element_block(z: int) -> str:
    """s / p / d / f block — the subshell of the last electron added (Aufbau order)."""
    return electron_configuration(z).split()[-1][1]


def element_family(z: int) -> str:
    """Coarse family from block + valence (main-group-accurate; Book 3 p.26/30)."""
    block = element_block(z)
    v = valence_electrons(z)
    if block == "f":
        return "Lanthanoid/Actinoid"
    if block == "d":
        return "Transition metal"
    if block == "s":
        return "Noble gas" if z == 2 else ("Alkali metal" if v == 1 else "Alkaline earth")
    # p-block
    if v == 8:
        return "Noble gas"
    if v == 7:
        return "Halogen"
    return "Non-metal / metalloid / post-transition"


def atoms_per_kg(z: int) -> float:
    """Number of atoms of element Z in 1 kg of its Matter  = 1/mass_kg."""
    return 1.0 / element(z).mass_kg


def period(z: int) -> int:
    """Period (table row) = highest occupied principal shell n  (Book 3 p.218)."""
    return max(int(tok[0]) for tok in electron_configuration(z).split())


def allotrope_topology_pi(z: int) -> int:
    """Allotropes share Z and topology-π (same charge geometry, different 3D form);
    so this just returns the element's topology-π (invariant across allotropes; p.355)."""
    return element(z).topology_pi


# --- Bonding (Book 3 pp.368-380) ---------------------------------------------
def bond_order(shared_electrons: int) -> int:
    """Bond order from shared electrons: 2→single, 4→double, 6→triple  (= e/2)."""
    return shared_electrons // 2


def sigma_pi_bonds(order: int) -> tuple[int, int]:
    """(σ, π) decomposition of a covalent bond: single=σ, double=σ+π, triple=σ+2π."""
    if order < 1:
        return (0, 0)
    return (1, order - 1)


def shared_electrons_for_bond(order: int) -> int:
    """Electrons shared for a given bond order: single=2, double=4, triple=6."""
    return 2 * order


def fascia_bond(order: int) -> str:
    """Kelvin's name for a bond by order (Book 3 p.370): "it is the electric field fascia
    of baryons that facilitates chemical bonds" — single/double/triple = 1/2/3 fascia bonds."""
    return {1: "single fascia bond", 2: "double fascia bonds",
            3: "triple fascia bonds"}.get(order, f"{order}-fascia bonds")


# --- Metal / non-metal classification (for bond-type, Book 3 p.380) ----------
# The periodic metal/non-metal divide Kelvin uses on the bonding plates.
_NONMETALS = frozenset({1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18,
                        34, 35, 36, 53, 54, 86, 118})   # H,He,C,N,O,F,Ne,P,S,Cl,Ar,Se,Br,Kr,I,Xe,Rn,Og
_METALLOIDS = frozenset({5, 14, 32, 33, 51, 52, 85})    # B,Si,Ge,As,Sb,Te,At
# Light metals whose small, highly-charged ion forms COVALENT (molecular) compounds rather
# than ionic — Beryllium (BeCl2 is covalent/linear on Kelvin's p.370 Lewis plate).
_COVALENT_FORMERS = frozenset({4})                      # Be


def is_metal(z: int) -> bool:
    """True if element Z is a metal (donates electrons → cations; Book 3 p.380)."""
    return z not in _NONMETALS and z not in _METALLOIDS


def is_nonmetal(z: int) -> bool:
    return z in _NONMETALS


def bond_type(sym_a: str, sym_b: str) -> str:
    """Classify a bond between two elements the Tetryonic way (charge transfer vs sharing,
    Book 3 p.371/380): metal+non-metal → ionic (one donates an electron), non-metal+non-metal
    → covalent (shared fascia), metal+metal → metallic. Valence-bond/MO theory is replaced by
    this charge-topology view."""
    za, zb = _z_of(sym_a), _z_of(sym_b)
    ma, mb = is_metal(za), is_metal(zb)
    if ma and mb:
        return "metallic"
    if ma != mb:                      # one metal, one non-metal/metalloid
        # Be (and other covalent-formers) make molecular, not ionic, compounds (p.370)
        if za in _COVALENT_FORMERS or zb in _COVALENT_FORMERS:
            return "covalent"
        return "ionic"
    return "covalent"


# --- Ionic bonding (Book 3 p.380) --------------------------------------------
# An electron carries 12 charge-quanta (= 1 e, the 12 electron fascia). So an ion that has
# given/taken k electrons carries ±12·k charge-quanta: Na⁺ = +12, Cl⁻ = −12, NaCl = neutral.
def ion_charge_quanta(charge_e: int) -> int:
    """Charge-quanta of an ion = 12 × its charge in e (Book 3 p.380: Na⁺ = +12, Cl⁻ = −12)."""
    return 12 * charge_e


def ionic_bond(cation: str, anion: str, n_cation: int = 1, n_anion: int = 1) -> dict:
    """Ionic compound from a metal cation + non-metal anion (Book 3 p.380, e.g. NaCl).

    Charge is balanced by electron transfer (group valence): the metal donates, the
    non-metal accepts; the compound is net-neutral (NaCl → Na⁺ +12 / Cl⁻ −12).
    ``topology_pi`` is the neutral-atom charge-π sum (Σ 84·Z, e.g. NaCl = 2352π — the
    engine's validated base count). NOTE: Kelvin's p.380 bonded-state diagram shows a
    slightly higher count (NaCl = 2424π = [1212·1212]) that includes the bond field-fascia;
    that bonded representation is recorded but not the engine's base topology."""
    zc, za = _z_of(cation), _z_of(anion)
    qc = group_valence(zc)                       # electrons the metal gives  (Na → +1)
    qa = group_valence(za) - 8                    # electrons the non-metal takes (Cl → −1)
    topo = element(zc).topology_pi * n_cation + element(za).topology_pi * n_anion
    return {
        "compound": f"{cation}{n_cation if n_cation>1 else ''}{anion}{n_anion if n_anion>1 else ''}",
        "cation": cation, "cation_charge_e": qc, "cation_charge_quanta": ion_charge_quanta(qc),
        "anion": anion, "anion_charge_e": qa, "anion_charge_quanta": ion_charge_quanta(qa),
        "net_charge_e": qc * n_cation + qa * n_anion,
        "topology_pi": topo, "type": "ionic",
    }


def group_valence(z: int) -> int:
    """Main-group 'combining' valence electrons (s+p of the outer shell), 1..8.
    Na→1, Mg→2, Cl→7, Ar→8.  (Transition metals use valence(z) instead.)"""
    return valence_electrons(z)


# --- Molecular geometry / VSEPR (Book 3 p.370 "Lewis Structures", p.384) ------
# Steric number = (bonding regions) + (lone pairs) on the central atom. Kelvin draws exactly
# these shapes on p.370: BeCl2 linear, BH3/BF3 trigonal planar, CH4 tetrahedral, NH3 pyramidal,
# H2O bent, HF/CO2 linear. Bond angles are the geometry's regular values.
_GEOMETRY = {
    (2, 0): ("linear", 180.0),
    (3, 0): ("trigonal planar", 120.0),
    (4, 0): ("tetrahedral", 109.5),
    (5, 0): ("trigonal bipyramidal", 90.0),
    (6, 0): ("octahedral", 90.0),
    (2, 1): ("bent", 119.0),
    (3, 1): ("trigonal pyramidal", 107.0),
    (2, 2): ("bent", 104.5),
    (4, 1): ("seesaw", 90.0),
    (3, 2): ("T-shaped", 90.0),
    (2, 3): ("linear", 180.0),
    (5, 1): ("square pyramidal", 90.0),
    (4, 2): ("square planar", 90.0),
}


def molecular_geometry(bonding_regions: int, lone_pairs: int = 0) -> dict:
    """Molecular shape from the steric number (bonding regions + lone pairs), Book 3 p.370.

    A 'bonding region' is one bonded atom (a double/triple bond still counts as ONE region).
    Returns {steric_number, shape, bond_angle_deg}."""
    steric = bonding_regions + lone_pairs
    shape, angle = _GEOMETRY.get((bonding_regions, lone_pairs), ("unknown", 0.0))
    return {"steric_number": steric, "shape": shape, "bond_angle_deg": angle,
            "bonding_regions": bonding_regions, "lone_pairs": lone_pairs}


def central_lone_pairs(central: str, n_bonded_atoms: int, charge: int = 0) -> int:
    """Lone pairs on a main-group central atom bonded to ``n_bonded_atoms`` (single-σ each):
    (valence − bonds − charge) // 2.  C in CH4 → 0, N in NH3 → 1, O in H2O → 2."""
    v = group_valence(_z_of(central)) - charge
    return max(0, (v - n_bonded_atoms) // 2)


# Named molecules straight off Kelvin's p.370 plate: (central, bonded atoms, lone pairs).
_MOLECULE_SHAPES = {
    "BeCl2": (2, 0), "BH3": (3, 0), "BF3": (3, 0), "CH4": (4, 0), "NH3": (3, 1),
    "H2O": (2, 2), "HF": (1, 0), "CO2": (2, 0), "HCHO": (3, 0), "CH2O": (3, 0),
    "C2H4": (3, 0), "C2H2": (2, 0), "PCl5": (5, 0), "SF6": (6, 0),
}


def molecule_shape(name: str) -> dict:
    """Geometry of a named molecule from Kelvin's p.370 set (e.g. 'H2O' → bent 104.5°).
    Diatomics are linear."""
    if name in _MOLECULE_SHAPES:
        b, lp = _MOLECULE_SHAPES[name]
        if b == 1:                    # diatomic
            return {"steric_number": 1, "shape": "linear", "bond_angle_deg": 180.0,
                    "bonding_regions": 1, "lone_pairs": lp}
        return molecular_geometry(b, lp)
    raise ValueError(f"no tabulated shape for {name!r}; use molecular_geometry(regions, lone_pairs)")


# --- Hydrogen / hydrogen bonding (Book 3 p.385) ------------------------------
def hydrogen_radical() -> dict:
    """The free hydrogen radical (Book 3 p.385): H = 48π `[24·24]` — proton[24·12] + electron[0·12].
    In Tetryonics a "hydrogen bond" is a CHARGE interaction (the H radical's field), not a
    shared-electron bond; H is the universal bonding agent ("free radical whose energy can be
    changed to facilitate chemical bonding", p.370)."""
    return {"species": "H", "topology_pi": 48, "cw": 24, "ccw": 24, "net_charge_e": 0,
            "role": "bonding agent / free radical"}


def hydrogen_bond_quanta(n_h: int = 1) -> int:
    """Charge-π of n hydrogen radicals participating as H-bonds (Book 3 p.385): 48 each
    (H₂ = 96π `[48·48]`)."""
    return 48 * n_h


# --- Polyatomic ions (Book 3 p.371/379/380) ----------------------------------
# Each is a molecular fragment carrying a net charge; its charge-π topology = Σ 84·Z of its
# atoms (the engine's validated count), and its charge = ±(electrons gained/lost) → ±12·k quanta.
POLYATOMIC_IONS = {
    "hydroxide": ("OH", -1), "hydronium": ("H3O", 1), "ammonium": ("NH4", 1),
    "nitrate": ("NO3", -1), "nitrite": ("NO2", -1), "bicarbonate": ("HCO3", -1),
    "carbonate": ("CO3", -2), "sulfate": ("SO4", -2), "sulfite": ("SO3", -2),
    "phosphate": ("PO4", -3), "cyanide": ("CN", -1), "acetate": ("C2H3O2", -1),
    "permanganate": ("MnO4", -1), "chromate": ("CrO4", -2), "peroxide": ("O2", -2),
}


def polyatomic_ion(name: str) -> dict:
    """A named polyatomic ion → {formula, charge_e, charge_quanta (±12·charge), topology_pi}.
    e.g. hydroxide OH⁻ = 720π, charge −1 (−12 quanta); nitrate NO₃⁻ = 2604π."""
    key = name.lower()
    if key not in POLYATOMIC_IONS:
        raise ValueError(f"unknown polyatomic ion: {name!r}")
    formula, charge = POLYATOMIC_IONS[key]
    return {"name": key, "formula": formula, "charge_e": charge,
            "charge_quanta": ion_charge_quanta(charge),
            "topology_pi": molecule_topology_pi(formula)}


# --- Lewis structure auto-derivation from a formula (Book 3 p.370) ------------
# Priority for picking the central atom of a simple molecule (least electronegative / most
# bonds): C/Si/B before N/P, then S, with O/H as terminals.
_CENTRAL_PRIORITY = {"C": 0, "Si": 1, "B": 2, "Al": 2, "P": 3, "N": 4, "S": 5, "O": 7, "H": 9}


def _central_atom(counts: dict) -> str | None:
    non_h = [s for s in counts if s != "H"]
    if not non_h:
        return "H" if counts.get("H") else None
    singles = [s for s in non_h if counts[s] == 1]
    pool = singles or non_h
    return min(pool, key=lambda s: _CENTRAL_PRIORITY.get(s, 6))


def lewis_structure(formula: str) -> dict:
    """Auto Lewis/VSEPR for a simple molecule (one central atom + terminal atoms), Book 3 p.370.

    Returns {central, terminals, bonding_regions, lone_pairs, shape, bond_angle_deg,
    valence_electrons, exact}. Uses Kelvin's tabulated p.370 shapes when available (exact);
    otherwise derives a best-effort shape from valence (``exact`` = False for molecules with
    multiple bonds it can't infer from the formula alone)."""
    counts = _parse_formula(formula)
    if not counts:
        raise ValueError(f"empty/invalid formula: {formula!r}")
    central = _central_atom(counts)
    terminals = {s: c for s, c in counts.items() if s != central}
    # a doubly-counted central (e.g. C2H4) — treat first central, terminals = the rest
    n_central = counts.get(central, 1)
    bonding_regions = sum(terminals.values()) if terminals else 0
    if n_central > 1:                       # e.g. C2H6: regions per central not from formula
        bonding_regions = max(1, bonding_regions // n_central + 1)
    if formula in _MOLECULE_SHAPES:         # Kelvin's exact p.370 geometry
        geo = molecule_shape(formula)
        geo.update({"central": central, "terminals": terminals,
                    "valence_electrons": _total_valence(counts), "exact": True})
        return geo
    lone = central_lone_pairs(central, bonding_regions)
    geo = (molecular_geometry(bonding_regions, lone) if bonding_regions >= 1
           else {"steric_number": 0, "shape": "monatomic", "bond_angle_deg": 0.0,
                 "bonding_regions": 0, "lone_pairs": lone})
    geo.update({"central": central, "terminals": terminals,
                "valence_electrons": _total_valence(counts), "exact": False})
    return geo


def _total_valence(counts: dict) -> int:
    return sum(group_valence(_z_of(s)) * c for s, c in counts.items())


# --- Atomic orbitals (Book 3 p.57-62) ----------------------------------------
# Each subshell of azimuthal number ℓ has (2ℓ+1) orbitals holding 2 electrons each →
# capacity 4ℓ+2.  Kelvin maps the blocks to families on p.59-62.
ORBITALS = {
    "s": {"l": 0, "orbitals": 1, "capacity": 2,  "shape": "spherical",
          "family": "Alkali metals & Alkaline earths"},
    "p": {"l": 1, "orbitals": 3, "capacity": 6,  "shape": "dumbbell (lobed)",
          "family": "Non-metals, Halogens & Noble gases"},
    "d": {"l": 2, "orbitals": 5, "capacity": 10, "shape": "cloverleaf",
          "family": "Transition & post-Transition metals"},
    "f": {"l": 3, "orbitals": 7, "capacity": 14, "shape": "complex (8-lobed)",
          "family": "Lanthanoids & Actinoids"},
}


def orbital(subshell: str) -> dict:
    """Geometry of an atomic orbital subshell (Book 3 p.59-62): s spherical (2e),
    p dumbbell (6e), d cloverleaf (10e), f complex (14e).  capacity = 4ℓ+2, orbitals = 2ℓ+1."""
    s = subshell.lower()
    if s not in ORBITALS:
        raise ValueError(f"unknown subshell: {subshell!r} (use s/p/d/f)")
    return {"subshell": s, **ORBITALS[s]}


def azimuthal_quantum_number(subshell: str) -> int:
    """Azimuthal (orbital angular momentum) quantum number ℓ: s=0, p=1, d=2, f=3."""
    return ORBITALS[subshell.lower()]["l"]


def subshell_capacity(subshell: str) -> int:
    """Electron capacity of a subshell = 4ℓ+2 (s=2, p=6, d=10, f=14)."""
    return ORBITALS[subshell.lower()]["capacity"]


def element_orbital(z: int) -> dict:
    """The orbital subshell the last (valence) electron of element Z occupies (Aufbau)."""
    return orbital(element_block(z))


# --- Bond geometry data (Book 3 p.369) ---------------------------------------
# Bond lengths / angles Kelvin gives on the Van der Waals plate (p.369); for other
# molecules the angle comes from the VSEPR shape (molecule_shape).
BOND_DATA = {
    "CO2": {"bond": "C=O", "bond_length_pm": 116.3, "shape": "linear", "bond_angle_deg": 180.0},
    "O3":  {"bond": "O-O", "bond_length_pm": 127.8, "shape": "bent",   "bond_angle_deg": 116.8},
}


def bond_geometry(name: str) -> dict:
    """Bond length/angle of a molecule — Kelvin's p.369 data where given (CO₂ 116.3 pm,
    O₃ 116.8°/127.8 pm), otherwise the VSEPR bond angle from :func:`molecule_shape`."""
    if name in BOND_DATA:
        return {"molecule": name, **BOND_DATA[name]}
    g = molecule_shape(name)
    return {"molecule": name, "shape": g["shape"], "bond_angle_deg": g["bond_angle_deg"]}


# --- Isotopes & isomers (Book 3) ---------------------------------------------
# Common isotopes by Z (mass numbers).  An isotope's charge-π topology follows straight
# from the Atom rule (36·A + 12·Z), so isotope(z, A).topology_pi already accounts for the
# extra neutrons (36π each) — Tetryonic "excess neutrons" are isotope variants, not the base.
COMMON_ISOTOPES = {1: [1, 2, 3], 2: [3, 4], 6: [12, 13, 14], 7: [14, 15], 8: [16, 17, 18],
                   17: [35, 37], 92: [234, 235, 238]}


def common_isotopes(z: int) -> list[int]:
    """Common isotope mass numbers of element Z (e.g. carbon → [12, 13, 14])."""
    return COMMON_ISOTOPES.get(z, [])


def isotope_notation(z: int, mass_number: int) -> str:
    """Isotope label, e.g. (6, 14) → 'C-14'."""
    return f"{SYMBOLS[z - 1]}-{mass_number}"


def neutron_number(z: int, mass_number: int) -> int:
    """Neutrons in an isotope = A − Z."""
    return mass_number - z


def molecular_formula(formula: str) -> str:
    """Canonical (Hill) molecular formula: C first, H second, then the rest alphabetically.
    e.g. 'OCH3CH3' → 'C2H6O'.  Two structures with the same molecular formula are isomers."""
    counts = dict(_parse_formula(formula))
    parts = []
    if "C" in counts:
        parts.append(("C", counts.pop("C")))
        if "H" in counts:
            parts.append(("H", counts.pop("H")))
    for s in sorted(counts):
        parts.append((s, counts[s]))
    return "".join(f"{s}{c if c > 1 else ''}" for s, c in parts)


def are_isomers(formula_a: str, formula_b: str) -> bool:
    """True if two distinct structural formulas share the same molecular formula
    (structural isomers, e.g. 'C2H6O' ethanol vs 'CH3OCH3' dimethyl ether)."""
    return formula_a != formula_b and molecular_formula(formula_a) == molecular_formula(formula_b)


# --- Molecules / compounds ----------------------------------------------------
def _parse_formula(formula: str) -> dict[str, int]:
    """Parse a chemical formula -> {symbol: count}, expanding parenthesised groups with
    multipliers (e.g. 'Ca(OH)2' -> {Ca:1, O:2, H:2}; 'Ca3(PO4)2' -> {Ca:3, P:2, O:8})."""
    import re

    def parse(s: str, i: int):
        local: dict[str, int] = {}
        while i < len(s):
            ch = s[i]
            if ch in "([{":
                sub, i = parse(s, i + 1)
                m = re.match(r"\d+", s[i:])
                mult = int(m.group()) if m else 1
                i += len(m.group()) if m else 0
                for k, v in sub.items():
                    local[k] = local.get(k, 0) + v * mult
            elif ch in ")]}":
                return local, i + 1
            else:
                m = re.match(r"([A-Z][a-z]?)(\d*)", s[i:])
                if m and m.group(1):
                    local[m.group(1)] = local.get(m.group(1), 0) + (int(m.group(2)) if m.group(2) else 1)
                    i += len(m.group(0))
                else:
                    i += 1
        return local, i

    return parse(formula, 0)[0]


def _z_of(sym: str) -> int:
    """Atomic number of an element symbol, with a clear error (not a bare KeyError)
    so a mistyped formula can't silently drop an atom and miscompute a mass."""
    z = _SYMBOL_TO_Z.get(sym)
    if z is None:
        raise ValueError(f"unknown element symbol: {sym!r}")
    return z


def molecule_topology_pi(formula: str) -> int:
    """Total charge-π of a compound = Σ atoms' topology π."""
    total = 0
    for sym, count in _parse_formula(formula).items():
        total += element(_z_of(sym)).topology_pi * count
    return total


def molecule_mass(formula: str) -> float:
    """Rest mass (kg) of a molecule = Σ constituent atom masses."""
    total = 0.0
    for sym, count in _parse_formula(formula).items():
        total += element(_z_of(sym)).mass_kg * count
    return total


def molecule_mass_amu(formula: str) -> float:
    return molecule_mass(formula) / K.mass_from_quanta(K.N_HYDROGEN)


# --- Chemical reactions: balancing & acid/base (Book 3 p.379, p.383) ---------
def balance_reaction(reactants: list[str], products: list[str]) -> dict:
    """Balance a chemical reaction by conserving every element (= conserving charge-π
    topology, since topology-π = Σ 84·Z; Book 3 p.383). Returns {formula: integer coeff}.

    e.g. balance_reaction(['CH4','O2'], ['CO2','H2O']) → {CH4:1, O2:2, CO2:1, H2O:2}."""
    from fractions import Fraction
    from math import gcd, lcm
    species = list(reactants) + list(products)
    n = len(species)
    signs = [1] * len(reactants) + [-1] * len(products)
    els = sorted({e for f in species for e in _parse_formula(f)})
    M = [[Fraction(signs[j] * _parse_formula(species[j]).get(e, 0)) for j in range(n)]
         for e in els]
    rows, cols = len(M), n
    pivots, r = [], 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in pivots]
    if len(free) != 1:
        raise ValueError(f"reaction not uniquely balanceable (free dimensions: {len(free)})")
    fcol = free[0]
    x = [Fraction(0)] * cols
    x[fcol] = Fraction(1)
    for i, pc in enumerate(pivots):
        x[pc] = -M[i][fcol]
    denom = 1
    for v in x:
        denom = lcm(denom, v.denominator)
    ints = [int(v * denom) for v in x]
    if all(v <= 0 for v in ints):
        ints = [-v for v in ints]
    if any(v <= 0 for v in ints):
        raise ValueError("reaction not balanceable with positive coefficients")
    g = 0
    for v in ints:
        g = gcd(g, v)
    if g > 1:
        ints = [v // g for v in ints]
    return {species[i]: ints[i] for i in range(n)}


def reaction_conserves_topology(reactants: list[str], products: list[str],
                                coeffs: dict | None = None) -> bool:
    """Verify a (balanced) reaction conserves total charge-π topology — the Tetryonic
    statement of mass conservation (atoms in = atoms out → Σ84·Z in = out)."""
    if coeffs is None:
        coeffs = balance_reaction(reactants, products)
    left = sum(coeffs[f] * molecule_topology_pi(f) for f in reactants)
    right = sum(coeffs[f] * molecule_topology_pi(f) for f in products)
    return left == right


# Common acid/base ion makeup for predicting neutralisation products.
_ACID_IONS = {"HCl": ("Cl", -1, 1), "HNO3": ("NO3", -1, 1), "H2SO4": ("SO4", -2, 2),
              "H3PO4": ("PO4", -3, 3), "H2CO3": ("CO3", -2, 2), "HF": ("F", -1, 1),
              "HBr": ("Br", -1, 1), "HI": ("I", -1, 1)}
_BASE_CATIONS = {"NaOH": ("Na", 1), "KOH": ("K", 1), "LiOH": ("Li", 1),
                 "CaO2H2": ("Ca", 2), "MgO2H2": ("Mg", 2)}   # Ca(OH)2 written CaO2H2


def neutralise(acid: str, base: str) -> dict:
    """Acid + hydroxide base → salt + water, balanced (Book 3 p.379).

    e.g. neutralise('H2SO4','NaOH') → {reaction: 'H2SO4 + 2 NaOH -> Na2SO4 + 2 H2O',
    salt: 'Na2SO4', coefficients: {...}}. The salt is the metal cation + acid anion
    (charges criss-crossed to neutral)."""
    acid = ACIDS.get(acid.lower(), acid)           # allow a name like 'sulfuric'
    if acid not in _ACID_IONS:
        raise ValueError(f"unsupported acid: {acid!r}")
    if base not in _BASE_CATIONS:
        raise ValueError(f"unsupported base: {base!r} (use e.g. NaOH, KOH, CaO2H2)")
    anion, qa, _ = _ACID_IONS[acid]
    cation, qc = _BASE_CATIONS[base]
    # criss-cross the charges to a neutral salt
    a, c = abs(qa), abs(qc)
    g = __import__("math").gcd(a, c)
    n_cat, n_an = a // g, c // g
    # build the salt's atom counts (expand the polyatomic anion) → a valid flat formula
    salt_counts: dict[str, int] = {cation: n_cat}
    for sym, ct in _parse_formula(anion).items():
        salt_counts[sym] = salt_counts.get(sym, 0) + ct * n_an
    salt_plain = "".join(f"{s}{salt_counts[s] if salt_counts[s] > 1 else ''}" for s in salt_counts)
    # pretty display: M(anion)n when the anion has >1 atom and appears >1 time
    salt = (f"{cation}{n_cat if n_cat>1 else ''}({anion}){n_an}"
            if n_an > 1 and len(_parse_formula(anion)) > 1 else salt_plain)
    coeffs = balance_reaction([acid, base], [salt_plain, "H2O"])
    def term(f):
        c = coeffs[f]
        return f"{c} {f}" if c > 1 else f
    sc = coeffs[salt_plain]
    salt_term = f"{sc} {salt}" if sc > 1 else salt
    rxn = (f"{term(acid)} + {term(base)} -> {salt_term} + {term('H2O')}")
    return {"reaction": rxn, "salt": salt, "coefficients": coeffs,
            "conserves_topology": reaction_conserves_topology([acid, base],
                                                              [salt_plain, "H2O"], coeffs)}


def molecule_nuclear_mass_amu(formula: str) -> float:
    """Energy-level (his Chemistry-book) mass of a compound (amu) = Σ atoms'
    :func:`nuclear_mass_amu`. Uses each atom's Aufbau-shell mass, so it matches the
    sum of Kelvin's per-element page masses rather than the flat ground-state floor."""
    return sum(nuclear_mass_amu(_z_of(sym)) * count
               for sym, count in _parse_formula(formula).items())


def molecule_composition(formula: str) -> list[dict]:
    """Per-element breakdown of a compound: [{symbol, z, count, topology_pi,
    mass_amu, shell_mass_amu}], handy for a molecule-builder UI."""
    rows = []
    for sym, count in _parse_formula(formula).items():
        z = _z_of(sym)
        a = element(z)
        rows.append({"symbol": sym, "z": z, "count": count,
                     "topology_pi": a.topology_pi, "mass_amu": a.mass_amu,
                     "shell_mass_amu": nuclear_mass_amu(z)})
    return rows


def divides_into_deuterium_units(formula: str) -> bool:
    """True if a compound's total topology-π is a whole number of 84π deuterium units.

    Book 3 (p.384) associates this with especially stable compounds, but it is NOT a
    complete stability predictor (e.g. H₂O = 768π is not divisible by 84 yet water is
    stable). Use as the Tetryonic deuterium-divisibility property, not a yes/no stability.
    """
    return molecule_topology_pi(formula) % 84 == 0


if __name__ == "__main__":
    for atom in periodic_table(12):
        print(atom.describe())
