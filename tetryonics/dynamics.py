"""
Dynamics — the INTERACTIONS of Tetryonics as computable state-transitions.

Built strictly from ../_CORE_MECHANICS.md §4 (HIS METHOD ONLY): emission, absorption,
the GEM pinch, and the geometric force interactions. Each process returns a structured
``Transition`` describing the before/after state and the energy / quanta exchanged.

His-method rules used here (NOT standard physics):
  * Energy levels are squared geometries; shell mass-energy quanta = 12·n².
  * A photon is a DIAMOND (2 bosons, EVEN quanta, neutral, bidirectional).
  * KEM-field ladder energy  E_n = −KEM/n²  (KEM = 13.525 eV).  Photon = the differential.
  * The GEM pinch converts 3D Matter → 2D radiant mass-energy at 100% (E = m·c²);
    stellar "fusion" releases only 1/3600 of that.
  * Charge: opposites attract, similars repel; all charge seeks equilibrium.
  * Strong force = attraction between opposite-charged fascia (repulsion between like).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import constants as K
from . import particles as P

KEM_EV = K.KEM_EV          # 13.525 eV — his KEM-field ground energy
FUSION_FRACTION = 1.0 / 3600.0


@dataclass
class Transition:
    """A computed state-transition (a process happening to energy/charge/Matter)."""
    kind: str
    before: str = ""
    after: str = ""
    quanta: float = 0.0            # mass-energy quanta exchanged (his 12·n² currency)
    energy_j: float = 0.0          # energy exchanged (J)
    energy_ev: float = 0.0         # energy exchanged (eV)
    wavelength_m: float = 0.0      # photon wavelength if radiant (m)
    detail: dict = field(default_factory=dict)

    def describe(self) -> str:
        ev = f"{self.energy_ev:.4g} eV" if self.energy_ev else "—"
        nm = f"{self.wavelength_m*1e9:.1f} nm" if self.wavelength_m else "—"
        return (f"[{self.kind}] {self.before} -> {self.after} | "
                f"{self.quanta:g} quanta | {ev} | {nm}")


# --- helpers (his-method energies) -------------------------------------------
def level_energy_ev(n: int) -> float:
    """Bound KEM-field energy of level n (eV) = −KEM/n²  (his ladder, KEM=13.525)."""
    return -KEM_EV / (n * n)


def shell_quanta(n: int) -> int:
    """Mass-energy quanta of shell n = 12·n²."""
    return 12 * n * n


# --- §4.1 EMISSION: Matter -> radiant energy (photon out) --------------------
def emit_photon(n_high: int, n_low: int) -> Transition:
    """An electron drops from n_high to n_low, emitting a photon (a diamond).

    Energy out = the KEM level differential; quanta out = 12·(n_high² − n_low²)."""
    if n_high <= n_low:
        raise ValueError("emission requires n_high > n_low")
    e_ev = abs(level_energy_ev(n_high) - level_energy_ev(n_low))
    e_j = e_ev * K.ELEMENTARY_CHARGE
    lam = K.H * K.C / e_j
    q = shell_quanta(n_high) - shell_quanta(n_low)
    return Transition("emission", f"electron n{n_high}", f"electron n{n_low} + photon",
                      quanta=q, energy_j=e_j, energy_ev=e_ev, wavelength_m=lam,
                      detail={"photon": "diamond (even quanta, neutral)",
                              "even_quanta": q})


# --- §4.2 ABSORPTION: energy -> Matter (energy in) --------------------------
def absorb_photon(n_low: int, photon_energy_ev: float, max_level: int = 50) -> Transition:
    """A bound electron at n_low absorbs a photon and climbs to a higher level.

    Returns the nearest level reachable with that energy (its inverse is emit_photon)."""
    best, best_err = None, 1e9
    for n in range(n_low + 1, max_level + 1):
        e = abs(level_energy_ev(n) - level_energy_ev(n_low))
        if abs(e - photon_energy_ev) < best_err:
            best, best_err = n, abs(e - photon_energy_ev)
    ionised = photon_energy_ev >= abs(level_energy_ev(n_low))
    after = "free electron (ionised)" if ionised else f"electron n{best}"
    q = (shell_quanta(best) - shell_quanta(n_low)) if best else 0
    return Transition("absorption", f"electron n{n_low} + photon", after,
                      quanta=q, energy_ev=photon_energy_ev,
                      energy_j=photon_energy_ev * K.ELEMENTARY_CHARGE,
                      detail={"reached_level": best, "ionised": ionised})


# --- §4.1 GEM PINCH: 3D Matter -> 2D radiant energy (100%) -------------------
def pinch(mass_kg: float) -> Transition:
    """Collapse a 3D Matter topology to 2D radiant mass-energy — 100% efficient (E = m·c²)."""
    e_j = mass_kg * K.C2
    return Transition("pinch", f"Matter {mass_kg:.3e} kg", "radiant 2D EM mass-energy",
                      energy_j=e_j, energy_ev=e_j / K.ELEMENTARY_CHARGE,
                      detail={"efficiency": 1.0, "note": "Matter -> light+heat (stellar core)"})


def fusion(mass_kg: float) -> Transition:
    """Stellar p-p 'fusion' release = only 1/3600 of the full pinch energy."""
    e_j = FUSION_FRACTION * mass_kg * K.C2
    return Transition("fusion", f"Matter {mass_kg:.3e} kg", "radiant energy (partial)",
                      energy_j=e_j, energy_ev=e_j / K.ELEMENTARY_CHARGE,
                      detail={"efficiency": FUSION_FRACTION})


def pair_creation(photon_energy_j: float) -> Transition:
    """Energy -> Matter: a photon above 2·m_e·c² creates an electron-positron pair."""
    threshold = 2 * K.N_ELECTRON * K.M_Q * K.C2
    makes_pair = photon_energy_j >= threshold
    return Transition("pair_creation", "photon",
                      "e- + e+ pair" if makes_pair else "photon (below threshold)",
                      energy_j=photon_energy_j, energy_ev=photon_energy_j / K.ELEMENTARY_CHARGE,
                      detail={"threshold_j": threshold, "creates_pair": makes_pair})


# --- §4.3/4.4 FORCE INTERACTIONS (geometric) --------------------------------
@dataclass
class Interaction:
    """A force interaction between two charged geometries."""
    kind: str
    direction: str        # "attract" | "repel" | "neutral"
    force_n: float = 0.0
    detail: dict = field(default_factory=dict)

    def describe(self) -> str:
        return f"[{self.kind}] {self.direction}  F={self.force_n:.3e} N"


def charge_interaction(p1, p2, r: float) -> Interaction:
    """EM force between two particles (his Coulomb k). Opposites attract, similars repel."""
    q1 = p1.charge_e * K.ELEMENTARY_CHARGE if hasattr(p1, "charge_e") else p1
    q2 = p2.charge_e * K.ELEMENTARY_CHARGE if hasattr(p2, "charge_e") else p2
    f = K.COULOMB_K * q1 * q2 / (r * r)
    if q1 == 0 or q2 == 0:
        direction = "neutral"
    elif (q1 > 0) == (q2 > 0):
        direction = "repel"
    else:
        direction = "attract"
    return Interaction("electromagnetic", direction, abs(f),
                       detail={"q1": q1, "q2": q2, "seeks": "equilibrium"})


def strong_interaction(fascia_sign_a: int, fascia_sign_b: int) -> Interaction:
    """Strong force = the interaction of two Matter fascia.

    Opposite-charged fascia ATTRACT (bind quarks → baryons); like-charged fascia REPEL
    (→ charged leptons). Sign: +1, −1, or 0."""
    if fascia_sign_a == 0 or fascia_sign_b == 0:
        d = "neutral"
    elif fascia_sign_a == fascia_sign_b:
        d = "repel"
    else:
        d = "attract"
    return Interaction("strong", d, detail={"fascia": (fascia_sign_a, fascia_sign_b)})


def seek_equilibrium(*particles) -> dict:
    """Combine charged geometries; their net charge moves toward equilibrium (neutrality).

    Returns the net [cw·ccw] and net charge of the assembly."""
    cw = sum(p.cw for p in particles)
    ccw = sum(p.ccw for p in particles)
    return {"cw": cw, "ccw": ccw, "net_quanta": cw - ccw,
            "net_charge_e": (cw - ccw) / 12.0,
            "neutral": cw == ccw}


# --- convenience: a full hydrogen-line emission as a process ----------------
def spectral_emission(series: str, n_high: int) -> Transition:
    """Emit the photon of a named series transition (lyman..abraham)."""
    from .spectra import series_lower_level
    return emit_photon(n_high, series_lower_level(series))
