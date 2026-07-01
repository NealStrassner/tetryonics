"""
Charge — the equilateral geometry of energy.

In Tetryonics charge is "a measure of mass·QAM per second" and is bookkept as a
``[cw, ccw]`` pair: clockwise(+) vs counter-clockwise(−) energy-flux quanta. The
elementary charge corresponds to 12 charge quanta (one lepton's worth of fascia),
so any net charge is ``(cw − ccw)/12`` elementary charges.

    charge quantum   q = Ω/c²            (one fascia's charge ~ 1.335e-20 C)
    elementary charge e = 12·q           (electron has 12 fascia)

The charge of any geometry is its quantised-angular-momentum (QAM) per c²: a topology
holding QAM Ω carries charge Ω/c². The per-fascia QAM is Ω, giving the charge quantum.

See ../../_KNOWLEDGE_Book1_QM.md §B, Part III.
"""

from __future__ import annotations

from . import constants as K


def net_quanta(cw: int, ccw: int) -> int:
    """Net charge quanta = clockwise − counter-clockwise."""
    return cw - ccw


def charge_in_e(cw: int, ccw: int) -> float:
    """Net charge in units of the elementary charge (e ↔ 12 quanta)."""
    return net_quanta(cw, ccw) / 12.0


def charge_coulombs(cw: int, ccw: int) -> float:
    """Net charge in coulombs = net_quanta × charge_quantum."""
    return net_quanta(cw, ccw) * K.CHARGE_QUANTUM


def charge_from_qam(qam: float = K.OMEGA) -> float:
    """Charge of a geometry from its quantised angular momentum:  q = QAM / c².

    With the per-fascia QAM Ω this returns the charge quantum (1.335e-20 C).
    """
    return qam / K.C2


def time_as_charge(seconds: float) -> float:
    """Abraham's identity: time *is* charge.

    ``time = QAM/second = [m²/s]·[s²/m²] = seconds``; ±seconds = ±charge.
    Returns the equivalent charge (in charge-quanta units) for a span of seconds.
    """
    return seconds * K.C2 / K.OMEGA   # inverse of q = Ω/c² per second


def is_fermion_charge(cw: int, ccw: int) -> bool:
    """All Fermion charges are integer 1/3 multiples of e."""
    n = net_quanta(cw, ccw)
    return n % 4 == 0   # 4 quanta = 1/3 e
