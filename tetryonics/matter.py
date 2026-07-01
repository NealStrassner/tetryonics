"""
Matter assembly — building ALL Matter from the TETRYON, as a COMPOSITION TREE.

The tetryon (4 charged fascia folded into a tetra-deltahedron) is the quantum of Matter
(Book 1 p115). Everything is a tree of sub-assemblies down to tetryons:

    tetryon (1)                              4π    — the building block
      └ quark / lepton (3 tetryons)         12π   -> octa / dodeca-deltahedron
          └ meson (2 quarks = 6 tetryons)   24π   -> 14π
          └ baryon (3 quarks = 9 tetryons)  36π   -> 20π
              └ DEUTERIUM = proton + neutron + electron (21 tetryons)   84π
                  └ element Z>=2 = Z deuterium units (21·Z tetryons)    84·Z π
                  (Hydrogen = proton + electron = 12 tetryons, 48π — no neutron)

Charge, fascia and mass all SUM up the tree from the tetryons (Matter = 4nπ, Book 1 p114).
Deuterium is the building block of every element (the Planck-constant paper). Verified
against particles.py and elements.py (see tests/test_matter.py).
"""

from __future__ import annotations

from dataclasses import dataclass

from .geometry import Tetryon, positive_tetryon, negative_tetryon, neutral_tetryon
from .particles import Particle
from . import constants as K


# --- the fundamental unit: a tetryon (4 fascia) ------------------------------
def tetryon(cw: int, level: int = 1) -> Tetryon:
    """A tetryon: ``cw`` clockwise(+) fascia and ``4-cw`` counter-clockwise(-)."""
    if not 0 <= cw <= 4:
        raise ValueError("a tetryon has 4 fascia: cw must be 0..4")
    return Tetryon(level=level, cw=cw, ccw=4 - cw)


POSITIVE = positive_tetryon()      # [4·0]
NEGATIVE = negative_tetryon()      # [0·4]
GLUON = neutral_tetryon()          # [2·2]  (a neutral tetryon)


@dataclass(frozen=True)
class Assembly:
    """A piece of Matter as a tree of components (each a Tetryon or a sub-Assembly)."""
    name: str
    kind: str
    components: tuple                 # of Tetryon | Assembly
    topology: int | None = None      # external deltahedron faces (None for loose clusters)
    n_planck: float | None = None    # tabulated rest quanta (else summed from sub-parts)

    # --- flatten to tetryons -------------------------------------------------
    @property
    def tetryons(self) -> list:
        out = []
        for c in self.components:
            if isinstance(c, Tetryon):
                out.append(c)
            else:
                out.extend(c.tetryons)
        return out

    @property
    def tetryon_count(self) -> int:
        return len(self.tetryons)

    @property
    def subparticles(self) -> list:
        """Immediate components that are themselves Assemblies (the next level down)."""
        return [c for c in self.components if isinstance(c, Assembly)]

    # --- charge / fascia (sum from tetryons) ---------------------------------
    @property
    def cw(self) -> int:
        return sum(t.cw for t in self.tetryons)

    @property
    def ccw(self) -> int:
        return sum(t.ccw for t in self.tetryons)

    @property
    def fascia(self) -> int:
        """Total mass-energy fascia = 4·(tetryon count) = the 4nπ count (Book 1 p114)."""
        return 4 * self.tetryon_count

    mass_energy_pi = fascia

    @property
    def internalised_fascia(self) -> int:
        """Fascia folded INSIDE the topology ('antiMatter inside Matter') = 4n − topology."""
        return self.fascia - self.topology if self.topology is not None else 0

    @property
    def external_fascia(self) -> int:
        return self.topology if self.topology is not None else self.fascia

    @property
    def net_charge_quanta(self) -> int:
        return self.cw - self.ccw

    @property
    def charge_e(self) -> float:
        return self.net_charge_quanta / 12.0

    # --- mass (tabulated, else summed up the tree) ---------------------------
    @property
    def n_planck_total(self) -> float | None:
        if self.n_planck is not None:
            return self.n_planck
        subs = self.subparticles
        if subs and all(s.n_planck_total is not None for s in subs):
            return sum(s.n_planck_total for s in subs)
        return None

    @property
    def mass_kg(self) -> float | None:
        n = self.n_planck_total
        return None if n is None else n * K.M_Q

    @property
    def mass_amu(self) -> float | None:
        m = self.mass_kg
        return None if m is None else m / (K.N_HYDROGEN * K.M_Q)

    # --- display -------------------------------------------------------------
    def as_particle(self) -> Particle:
        return Particle(self.name, self.cw, self.ccw, self.fascia,
                        self.topology or self.fascia, self.n_planck_total, self.kind)

    def recipe(self) -> str:
        """One level of construction, e.g. 'proton = up + up + down' or
        'up = [4·0]+[4·0]+[2·2]'."""
        if self.subparticles:
            parts = " + ".join(c.name for c in self.components)
        else:
            parts = "+".join(f"[{t.cw}·{t.ccw}]" for t in self.components)
        return f"{self.name} = {parts}"

    def tree(self, indent: int = 0) -> str:
        """Full construction tree down to tetryons."""
        pad = "  " * indent
        line = (f"{pad}{self.name} [{self.cw}·{self.ccw}] "
                f"{self.tetryon_count} tetryons, {self.fascia}π"
                + (f" -> {self.topology}π topology" if self.topology else ""))
        if self.subparticles:
            kids = "\n".join(c.tree(indent + 1) for c in self.subparticles)
            return line + "\n" + kids
        return line


# --- recipes -----------------------------------------------------------------
QUARK_RECIPES = {
    "up":        [POSITIVE, POSITIVE, GLUON],     # [10·2]  +2/3
    "down":      [NEGATIVE, GLUON, GLUON],        # [4·8]   -1/3
    "anti-up":   [NEGATIVE, NEGATIVE, GLUON],     # [2·10]  -2/3
    "anti-down": [POSITIVE, GLUON, GLUON],        # [8·4]   +1/3
}
LEPTON_RECIPES = {
    "electron": [NEGATIVE, NEGATIVE, NEGATIVE],   # [0·12] -> -1
    "positron": [POSITIVE, POSITIVE, POSITIVE],   # [12·0] -> +1
    "neutrino": [GLUON, GLUON, GLUON],            # [6·6]  ->  0
}
MESON_RECIPES = {"pi+": ["up", "anti-down"], "pi-": ["anti-up", "down"], "pi0": ["up", "anti-up"]}
BARYON_RECIPES = {"proton": ["up", "up", "down"], "neutron": ["up", "down", "down"]}

_TOPOLOGY = {"quark": 8, "lepton": 12, "meson": 14, "baryon": 20}
_N = {"electron": K.N_ELECTRON, "positron": K.N_ELECTRON,
      "proton": K.N_PROTON, "neutron": K.N_NEUTRON}


# --- builders (assemble up the tree) -----------------------------------------
def build_tetryon(state: str = "positive") -> Assembly:
    t = {"positive": POSITIVE, "negative": NEGATIVE,
         "neutral": GLUON, "gluon": GLUON}[state]
    return Assembly(f"tetryon({state})", "tetryon", (t,), topology=4)


def build_quark(flavour: str) -> Assembly:
    return Assembly(flavour, "quark", tuple(QUARK_RECIPES[flavour]),
                    topology=_TOPOLOGY["quark"])


def build_lepton(name: str) -> Assembly:
    return Assembly(name, "lepton", tuple(LEPTON_RECIPES[name]),
                    topology=_TOPOLOGY["lepton"], n_planck=_N.get(name))


def build_meson(name: str) -> Assembly:
    quarks = tuple(build_quark(f) for f in MESON_RECIPES[name])
    return Assembly(name, "meson", quarks, topology=_TOPOLOGY["meson"])


def build_baryon(name: str) -> Assembly:
    quarks = tuple(build_quark(f) for f in BARYON_RECIPES[name])
    return Assembly(name, "baryon", quarks, topology=_TOPOLOGY["baryon"],
                    n_planck=_N.get(name))


def build_deuterium() -> Assembly:
    """Deuterium = proton + neutron + electron (21 tetryons, 84π). The building block of
    every element (Planck paper)."""
    return Assembly("deuterium", "nucleus+e",
                    (build_baryon("proton"), build_baryon("neutron"), build_lepton("electron")))


def build_hydrogen() -> Assembly:
    """Hydrogen = proton + electron (12 tetryons, 48π) — no neutron."""
    return Assembly("hydrogen", "atom",
                    (build_baryon("proton"), build_lepton("electron")))


def build_atom(z: int) -> Assembly:
    """A neutral atom built from its building blocks: Z deuterium units (Z>=2);
    Hydrogen (Z=1) = proton + electron."""
    from .elements import SYMBOLS
    if z == 1:
        return build_hydrogen()
    sym = SYMBOLS[z - 1] if z <= len(SYMBOLS) else f"Z{z}"
    return Assembly(sym, "atom", tuple(build_deuterium() for _ in range(z)))


def build(name: str) -> Assembly:
    """Build any standard particle/atom by name, from tetryons."""
    if name in QUARK_RECIPES:
        return build_quark(name)
    if name in LEPTON_RECIPES:
        return build_lepton(name)
    if name in MESON_RECIPES:
        return build_meson(name)
    if name in BARYON_RECIPES:
        return build_baryon(name)
    if name in ("deuterium", "hydrogen"):
        return build_deuterium() if name == "deuterium" else build_hydrogen()
    raise KeyError(f"unknown particle '{name}'")


def matter_pi(n_tetryons: int) -> int:
    """The mass-energy geometry of n tetryons = 4·n π (Book 1 p114: Matter = 4nπ)."""
    return 4 * n_tetryons


def tetryon_count(name: str) -> int:
    """How many tetryons make up a named particle/atom."""
    return build(name).tetryon_count
