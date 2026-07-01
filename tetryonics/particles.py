"""
The particle / quantum builder.

Particles are assemblies of charged fascia. The charge bookkeeping ``[cw, ccw]``
(clockwise/positive vs counter-clockwise/negative quanta) is *fully computed* from
the assembly — the fractional quark charges and integer hadron charges fall straight
out as ``(cw - ccw) / 12`` in units of the elementary charge.

  * elementary charge e  <->  12 charge quanta
  * up quark   = [10, 2]  -> +8/12 = +2/3
  * down quark = [4,  8]  -> -4/12 = -1/3
  * proton (uud) = u+u+d  = [24,12] -> +1
  * neutron (udd)= u+d+d  = [18,18] ->  0

Masses use the verified Planck-quanta numbers from constants.py
(mass = N_planck * m_q). See ../../_KNOWLEDGE_Book1_QM.md Part II §A,§B.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import constants as K


@dataclass(frozen=True)
class Particle:
    """A built particle with its Tetryonic geometry, charge and (optional) mass."""

    name: str
    cw: int                 # clockwise / positive charge quanta
    ccw: int                # counter-clockwise / negative charge quanta
    fascia: int             # 2D charged mass-energy geometry count (the "pi" count)
    topology: int           # 3D Matter topology count (octa=8, dodeca=12, etc.)
    n_planck: float | None = None   # rest mass-energy quanta (None if not tabulated)
    kind: str = "particle"

    # --- charge -------------------------------------------------------------
    @property
    def net_charge_quanta(self) -> int:
        return self.cw - self.ccw

    @property
    def charge_e(self) -> float:
        """Net charge in units of the elementary charge (e <-> 12 quanta)."""
        return self.net_charge_quanta / 12.0

    @property
    def charge_coulombs(self) -> float:
        return self.net_charge_quanta * K.CHARGE_QUANTUM

    # --- mass ---------------------------------------------------------------
    @property
    def mass_kg(self) -> float | None:
        if self.n_planck is None:
            return None
        return K.mass_from_quanta(self.n_planck)

    @property
    def mass_energy_j(self) -> float | None:
        """Rest mass-energy E = m c^2 (J)."""
        m = self.mass_kg
        return None if m is None else m * K.C2

    @property
    def mass_energy_ev(self) -> float | None:
        """Rest mass-energy in electron-volts."""
        e = self.mass_energy_j
        return None if e is None else e / K.ELEMENTARY_CHARGE

    @property
    def mass_energy_mev(self) -> float | None:
        """Rest mass-energy in MeV."""
        ev = self.mass_energy_ev
        return None if ev is None else ev / 1e6

    @property
    def planck_quanta(self) -> float | None:
        """Rest mass-energy quanta count (alias for n_planck)."""
        return self.n_planck

    @property
    def charge_pair(self) -> tuple:
        """The raw [cw, ccw] charge-quanta pair."""
        return (self.cw, self.ccw)

    def de_broglie(self, velocity: float) -> float | None:
        """de Broglie wavelength λ = h/(m·v) for this particle at ``velocity``."""
        m = self.mass_kg
        return None if m is None else K.H / (m * velocity)

    def compton(self) -> float | None:
        """Compton wavelength λ_c = h/(m·c) for this particle."""
        m = self.mass_kg
        return None if m is None else K.H / (m * K.C)

    def magnetic_moment(self) -> float | None:
        """Spin magnetic moment: Bohr magneton for leptons, nuclear for baryons."""
        if self.kind == "lepton":
            return K.BOHR_MAGNETON
        if self.kind == "baryon":
            return K.NUCLEAR_MAGNETON
        return None

    # --- display ------------------------------------------------------------
    @property
    def topology_charge(self) -> str:
        return f"[{self.cw}·{self.ccw}]"   # e.g. [24·12]

    def describe(self) -> str:
        q = self.charge_e
        qs = f"{q:+.4g} e" if q else "0 e"
        mass = self.mass_kg
        ms = "n/a" if mass is None else f"{mass:.6e} kg"
        return (f"{self.name:<12} {self.kind:<8} fascia={self.fascia:>3} "
                f"topology={self.topology:>3}  charge={self.topology_charge:>9} "
                f"= {qs:<8}  mass={ms}")


# --- Quarks (12 fascia mass-energy geometry -> 8pi octahedral topology) -------
# [cw, ccw] charge splits that yield the observed fractional charges.
QUARKS: dict[str, tuple[int, int]] = {
    "up":        (10, 2),   # +2/3
    "down":      (4, 8),    # -1/3
    "anti-up":   (2, 10),   # -2/3
    "anti-down": (8, 4),    # +1/3
}


def quark(flavour: str) -> Particle:
    cw, ccw = QUARKS[flavour]
    return Particle(name=flavour, cw=cw, ccw=ccw, fascia=12, topology=8, kind="quark")


# --- Leptons (12 fascia -> 12pi dodecahedral topology) ------------------------
def electron() -> Particle:
    return Particle("electron", cw=0, ccw=12, fascia=12, topology=12,
                    n_planck=K.N_ELECTRON, kind="lepton")


def positron() -> Particle:
    return Particle("positron", cw=12, ccw=0, fascia=12, topology=12,
                    n_planck=K.N_ELECTRON, kind="lepton")


def neutrino() -> Particle:
    return Particle("neutrino", cw=6, ccw=6, fascia=12, topology=12,
                    n_planck=None, kind="lepton")


# --- Baryons (3 quarks = 36 fascia -> 20pi topology) --------------------------
def _compose(name: str, flavours: list[str], n_planck: float | None,
             kind: str = "baryon") -> Particle:
    cw = sum(QUARKS[f][0] for f in flavours)
    ccw = sum(QUARKS[f][1] for f in flavours)
    return Particle(name=name, cw=cw, ccw=ccw, fascia=12 * len(flavours),
                    topology=20 if len(flavours) == 3 else 8 * len(flavours),
                    n_planck=n_planck, kind=kind)


def proton() -> Particle:
    # uud  -> [24,12] -> +1
    return _compose("proton", ["up", "up", "down"], K.N_PROTON)


def neutron() -> Particle:
    # udd  -> [18,18] -> 0
    return _compose("neutron", ["up", "down", "down"], K.N_NEUTRON)


def anti_proton() -> Particle:
    return _compose("anti-proton", ["anti-up", "anti-up", "anti-down"], K.N_PROTON)


def baryon(flavours: list[str], name: str | None = None,
           n_planck: float | None = None) -> Particle:
    """Build an arbitrary tri-quark baryon from a flavour list (e.g. ['up','up','down'])."""
    if name is None:
        name = "".join(f[0] for f in flavours)
    return _compose(name, flavours, n_planck)


# --- registry -----------------------------------------------------------------
def from_quanta(cw: int, ccw: int, n_planck: float | None = None,
                fascia: int | None = None, name: str = "custom",
                kind: str = "particle") -> Particle:
    """Build an arbitrary particle from a [cw·ccw] charge pair."""
    if fascia is None:
        fascia = cw + ccw
    return Particle(name=name, cw=cw, ccw=ccw, fascia=fascia,
                    topology=fascia, n_planck=n_planck, kind=kind)


def meson(flavour1: str, flavour2: str, name: str | None = None) -> Particle:
    """A meson = quark + antiquark (24π geometry → 14π topology)."""
    cw = QUARKS[flavour1][0] + QUARKS[flavour2][0]
    ccw = QUARKS[flavour1][1] + QUARKS[flavour2][1]
    return Particle(name=name or f"{flavour1}-{flavour2}", cw=cw, ccw=ccw,
                    fascia=24, topology=14, n_planck=None, kind="meson")


# Name → builder registry for lookup.
_REGISTRY = {
    "up": lambda: quark("up"), "down": lambda: quark("down"),
    "anti-up": lambda: quark("anti-up"), "anti-down": lambda: quark("anti-down"),
    "electron": electron, "positron": positron, "neutrino": neutrino,
    "proton": proton, "neutron": neutron, "anti-proton": anti_proton,
}


def particle(name: str) -> Particle:
    """Look up any standard particle by name (e.g. 'proton', 'up', 'electron')."""
    return _REGISTRY[name.lower()]()


def standard_particles() -> list[Particle]:
    """The headline particles, ready for a table."""
    return [
        quark("up"), quark("down"), quark("anti-up"), quark("anti-down"),
        electron(), positron(), neutrino(),
        proton(), neutron(), anti_proton(),
    ]


if __name__ == "__main__":
    for p in standard_particles():
        print(p.describe())
