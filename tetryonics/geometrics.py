"""
Geometrics — Book 5: the pure equilateral-triangle maths underpinning everything.

Covers the Tetryonic-SOLID topologies that 2D mass-energy folds into, the equilateral
metrics, the Tetryonic 'eutrigon' (the 60° law of cosines), triangular numbers, and the
π-radian content of shapes.

IMPORTANT (Book 5 p20 "Tetryonic Solids" + Book 1 p130): the particle solids are
**deltahedra** — polyhedra with ALL equilateral-triangle faces, built from 4n² Planck
mass-energy triangles. They MATCH the Euler numbers of Platonic solids but are NOT the
Platonic solids. The number (4/8/12/20) = the count of external charge fascia = faces:
    tetryon → tetra-deltahedron  (4 triangular faces)  = tetrahedron
    quark   → octa-deltahedron   (8 faces)             = octahedron
    lepton  → dodeca-deltahedron (12 TRIANGULAR faces) ≠ Platonic dodecahedron (12 pentagons)!
    baryon  → icoso-deltahedron  (20 faces)            = icosahedron
The tetra/octa/icoso cases coincide with Platonic solids (those ARE deltahedra); the
**lepton's dodeca-deltahedron is a 12-equilateral-TRIANGLE solid: 12 F, 18 E, 8 V (Euler 2)**
— Kelvin's word is "dodecadeltahedral" (Book 1 p130, Book 5 p20), the "6-loop rotator", built
from 12 charged fascia. He does not name a textbook solid; the canonical all-equilateral
realization of (12 F, 18 E, 8 V) is the snub disphenoid (J84). (A hexagonal bipyramid shares
the 12/18/8 counts but cannot be all-equilateral, so it is only a rough schematic.)
The PLATONIC dict below is kept only for the classical comparison Kelvin draws on p19.
"""

from __future__ import annotations

import math

from . import constants as K

SQRT3 = math.sqrt(3.0)
SQRT2 = math.sqrt(2.0)
SQRT5 = math.sqrt(5.0)
PI = math.pi
PHI = K.PHI   # golden ratio

# Classical Platonic solids (faces, edges, vertices) — kept for the p19 comparison only.
PLATONIC = {
    "tetrahedron":  (4, 6, 4),
    "cube":         (6, 12, 8),
    "octahedron":   (8, 12, 6),
    "dodecahedron": (12, 30, 20),
    "icosahedron":  (20, 30, 12),
}

# Kelvin's actual particle solids: regular DELTAHEDRA (all equilateral-triangle faces).
# (faces, edges, vertices) — Euler F−E+V = 2 for each.  faces = external charge fascia.
DELTAHEDRA = {
    "tetra-deltahedron":  (4, 6, 4),    # = tetrahedron
    "octa-deltahedron":   (8, 12, 6),   # = octahedron
    "dodeca-deltahedron": (12, 18, 8),  # 12-triangle deltahedron (snub disphenoid J84, all-equilateral)
    "icoso-deltahedron":  (20, 30, 12), # = icosahedron
}

# particle -> (deltahedron, topology pi = faces, mass-energy pi)
PARTICLE_SOLID = {
    "tetryon": ("tetra-deltahedron", 4, 4),
    "quark":   ("octa-deltahedron", 8, 12),
    "lepton":  ("dodeca-deltahedron", 12, 12),
    "baryon":  ("icoso-deltahedron", 20, 36),
}

# π-radian content of planar shapes (an equilateral triangle spans π = 180°).
PI_CONTENT = {"triangle": 1, "square": 2, "hexagon": 4, "circle": 2}  # multiples of π


# --- equilateral metrics ------------------------------------------------------
def equilateral_area(side: float) -> float:
    """Area = (√3/4)·s²."""
    return (SQRT3 / 4.0) * side * side


def equilateral_height(side: float) -> float:
    """Height = (√3/2)·s."""
    return (SQRT3 / 2.0) * side


def inradius(side: float) -> float:
    """Inscribed-circle radius r = s/(2√3)."""
    return side / (2.0 * SQRT3)


def circumradius(side: float) -> float:
    """Circumscribed-circle radius R = s/√3.  (R = 2·r — the 1:2 ratio.)"""
    return side / SQRT3


def perimeter(side: float) -> float:
    """Equilateral perimeter  p = 3·s."""
    return 3.0 * side


def incircle_area(side: float) -> float:
    """Area of the inscribed circle  π·r² = (π/12)·s²."""
    return PI * inradius(side) ** 2


def circumcircle_area(side: float) -> float:
    """Area of the circumscribed circle  π·R² = (π/3)·s²."""
    return PI * circumradius(side) ** 2


def hexagon_area(side: float) -> float:
    """Regular hexagon area  (3√3/2)·s²  (= 6 equilateral triangles)."""
    return (3 * SQRT3 / 2.0) * side * side


def regular_polygon_area(n: int, side: float) -> float:
    """Area of a regular n-gon  A = (1/4)·n·s²·cot(π/n)."""
    return 0.25 * n * side * side / math.tan(PI / n)


def polygon_interior_angle(n: int) -> float:
    """Interior angle of a regular n-gon (degrees)  = (n−2)·180/n."""
    return (n - 2) * 180.0 / n


def polygon_exterior_angle(n: int) -> float:
    """Exterior angle of a regular n-gon (degrees)  = 360/n."""
    return 360.0 / n


def apothem(n: int, side: float) -> float:
    """Apothem (inradius) of a regular n-gon  = s/(2·tan(π/n))."""
    return side / (2.0 * math.tan(PI / n))


def regular_polygon_perimeter(n: int, side: float) -> float:
    """Perimeter of a regular n-gon  = n·s."""
    return n * side


def regular_polygon_metrics(n: int, side: float) -> dict:
    """Bundle of regular-n-gon metrics: perimeter, apothem, area, interior/exterior angle."""
    return {"perimeter": regular_polygon_perimeter(n, side),
            "apothem": apothem(n, side),
            "area": regular_polygon_area(n, side),
            "interior_angle": polygon_interior_angle(n),
            "exterior_angle": polygon_exterior_angle(n)}


def viviani_distance_sum(side: float) -> float:
    """Viviani's theorem: sum of perpendiculars from any interior point of an equilateral
    triangle = the altitude  (√3/2)·s."""
    return equilateral_height(side)


def incircle_to_triangle_ratio() -> float:
    """Ratio of inscribed-circle area to equilateral-triangle area = π/(3√3) ≈ 0.6046."""
    return PI / (3 * SQRT3)


def area_perimeter_ratio() -> float:
    """Equilateral A/P² ratio = 1/(12√3) ≈ 0.04811."""
    return 1.0 / (12 * SQRT3)


# --- the eutrigon / 60° law of cosines ---------------------------------------
def eutrigon_c2(a: float, b: float) -> float:
    """Third side² of a 60°-apex triangle: c² = a² + b² − a·b  (cos60 = ½)."""
    return a * a + b * b - a * b


def eutrigon_identity(a: float, b: float, c: float) -> float:
    """Tetryonic eutrigon relation  a·b = a² + b² − c²  (returns LHS−RHS, ~0 if 60°)."""
    return (a * b) - (a * a + b * b - c * c)


# --- number geometry ----------------------------------------------------------
def triangular_number(n: int) -> int:
    """n-th triangular number  T = n(n+1)/2."""
    return n * (n + 1) // 2


def square_from_odds(n: int) -> int:
    """Sum of the first n odd numbers = n² (the tessellation identity)."""
    return sum(2 * r - 1 for r in range(1, n + 1))


def sum_of_cubes(n: int) -> int:
    """Σk³ = (Σk)² = T(n)²  (cubes sum to a square triangular number; Book 5 p.41)."""
    t = triangular_number(n)
    return t * t


def geometric_mean(a: float, b: float) -> float:
    """Geometric mean √(a·b) — Kelvin's form for the convergent gravity of two fields."""
    return math.sqrt(a * b)


def nth_odd(n: int) -> int:
    """The n-th odd number = 2n−1 (boson levels)."""
    return 2 * n - 1


def nth_even(n: int) -> int:
    """The n-th even number = 2n (photon levels)."""
    return 2 * n


def pentagonal_number(n: int) -> int:
    """n-th pentagonal number  = n(3n−1)/2."""
    return n * (3 * n - 1) // 2


def tetrahedral_number(n: int) -> int:
    """n-th tetrahedral number  = n(n+1)(n+2)/6."""
    return n * (n + 1) * (n + 2) // 6


def square_pyramidal_number(n: int) -> int:
    """n-th square-pyramidal number  = n(n+1)(2n+1)/6 (= Σ k²)."""
    return n * (n + 1) * (2 * n + 1) // 6


def golden_power(n: int) -> float:
    """φⁿ via Binet:  φⁿ = (φⁿ)."""
    return PHI ** n


def taylor_exp(x: float, terms: int = 12) -> float:
    """Maclaurin series for eˣ  = Σ xⁿ/n!  (Book 5 p.55)."""
    return sum(x**k / math.factorial(k) for k in range(terms))


def taylor_sin(x: float, terms: int = 10) -> float:
    """Maclaurin series for sin x  = Σ (−1)ⁿ x^(2n+1)/(2n+1)!."""
    return sum((-1)**k * x**(2*k+1) / math.factorial(2*k+1) for k in range(terms))


def taylor_cos(x: float, terms: int = 10) -> float:
    """Maclaurin series for cos x  = Σ (−1)ⁿ x^(2n)/(2n)!."""
    return sum((-1)**k * x**(2*k) / math.factorial(2*k) for k in range(terms))


def euler_identity() -> complex:
    """Euler's identity value  e^(iπ) + 1  (= 0)."""
    import cmath
    return cmath.exp(1j * PI) + 1


def c_power_ladder(n: int) -> float:
    """The cⁿ dimensional ladder: c¹ (1D velocity) … c⁴ (quaternion volume) (Book 5 p.141)."""
    from . import constants as K
    return K.C ** n


def kepler_bouwkamp(terms: int = 1000) -> float:
    """Partial product Π_{n=3}^{N} cos(π/n) → the Kepler–Bouwkamp constant ≈ 0.1149."""
    p = 1.0
    for n in range(3, terms + 1):
        p *= math.cos(PI / n)
    return p


def golden_ratio() -> float:
    """The golden ratio φ = (1+√5)/2 ≈ 1.618 (Book 5 pp.182-184)."""
    return PHI


def odom_golden_ratio() -> float:
    """The golden ratio φ measured from George Odom's construction (Book 5 p.182):
    an equilateral triangle inscribed in a circle. Take the midpoints P, Q of two
    sides and extend PQ to meet the circle at R; then PQ : QR = φ. Computed straight
    from the geometry — returns φ ≈ 1.618."""
    a, b, c = (0.0, 1.0), (-math.sqrt(3) / 2, -0.5), (math.sqrt(3) / 2, -0.5)  # equilateral in unit circle
    p = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)        # midpoint of AB
    q = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)        # midpoint of AC
    x_r = math.sqrt(1.0 - q[1] ** 2)                  # PQ extended (the line y=1/4) meets the unit circle here
    return (q[0] - p[0]) / (x_r - q[0])               # PQ / QR = φ


def golden_rhombus(short_diagonal: float = 1.0) -> dict:
    """Kelvin's KE energy 'diamond' is a golden rhombus (Book 5 p.183): a rhombus
    whose diagonals are in the golden ratio (long : short = φ : 1). Returns its
    geometry for the given short diagonal (acute angle ≈ 63.43°)."""
    short_d = float(short_diagonal)
    long_d = PHI * short_d
    side = math.hypot(long_d / 2, short_d / 2)
    acute = 2 * math.degrees(math.atan2(short_d / 2, long_d / 2))   # vertices on the long diagonal
    return {"short_diagonal": short_d, "long_diagonal": long_d, "diagonal_ratio": PHI,
            "side": side, "acute_angle_deg": acute, "obtuse_angle_deg": 180.0 - acute,
            "area": long_d * short_d / 2}


def fourth_power(n: int) -> int:
    """n⁴ = (n²)² — fourth powers are squares of squares (Book 5 p.42)."""
    return n ** 4


def twin_triangular_square(n: int) -> int:
    """Consecutive triangular numbers sum to a square: T(n) + T(n−1) = n² (p.40)."""
    return triangular_number(n) + triangular_number(n - 1)


def binomial(n: int, k: int) -> int:
    """Binomial coefficient C(n,k) — the entries of Pascal's triangle (Book 5 p.48)."""
    return math.comb(n, k)


def pascal_row(n: int) -> list:
    """Row n of Pascal's triangle (0-indexed)."""
    return [math.comb(n, k) for k in range(n + 1)]


def law_of_cosines(a: float, b: float, angle_c_deg: float) -> float:
    """General law of cosines  c = √(a² + b² − 2ab·cos C).  (C=60° → the eutrigon.)"""
    return math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(angle_c_deg)))


def geometric_series_sum(ratio: float, terms: int = None) -> float:
    """Sum of a geometric series. With ``terms`` → finite Σ₀^{n-1} rⁿ; else the
    infinite sum 1/(1−r) for |r|<1 (e.g. Σ(1/2)ⁿ = 2, Σ(1/4)ⁿ = 4/3)."""
    if terms is None:
        if abs(ratio) >= 1:
            raise ValueError("infinite geometric series needs |ratio| < 1")
        return 1.0 / (1.0 - ratio)
    return (1.0 - ratio ** terms) / (1.0 - ratio)


def sin_deg(angle_deg: float) -> float:
    """Sine of an angle in degrees."""
    return math.sin(math.radians(angle_deg))


def cos_deg(angle_deg: float) -> float:
    return math.cos(math.radians(angle_deg))


def tan_deg(angle_deg: float) -> float:
    return math.tan(math.radians(angle_deg))


def cartesian_to_polar(x: float, y: float) -> tuple:
    """(x, y) → (r, θ°)."""
    return (math.hypot(x, y), math.degrees(math.atan2(y, x)))


def polar_to_cartesian(r: float, theta_deg: float) -> tuple:
    """(r, θ°) → (x, y)."""
    t = math.radians(theta_deg)
    return (r * math.cos(t), r * math.sin(t))


def side_from_area(area: float) -> float:
    """Invert the equilateral area: side = √(4·A/√3)."""
    return math.sqrt(4 * area / SQRT3)


def euler_inequality_ok(circumradius_R: float, inradius_r: float) -> bool:
    """Euler's inequality for a triangle:  R ≥ 2r (equality only for equilateral)."""
    return circumradius_R >= 2 * inradius_r - 1e-12


def basel_sum(terms: int) -> float:
    """Partial Basel sum Σ 1/n² (converges to π²/6)."""
    return sum(1.0 / (n * n) for n in range(1, terms + 1))


def dihedral_angle(solid: str) -> float:
    """Dihedral angle (degrees) between adjacent faces of a Platonic solid."""
    angles = {"tetrahedron": math.degrees(math.acos(1 / 3)),       # ~70.53
              "cube": 90.0,
              "octahedron": math.degrees(math.acos(-1 / 3)),       # ~109.47
              "dodecahedron": math.degrees(math.acos(-1 / SQRT5)), # ~116.57
              "icosahedron": math.degrees(math.acos(-SQRT5 / 3))}  # ~138.19
    return angles[solid]


def pi_content(shape: str) -> float:
    """π-radian content of a planar shape (in radians)."""
    return PI_CONTENT[shape] * PI


# --- solids (Platonic for the classical comparison, deltahedra for particles) -
def _fev(solid: str) -> tuple:
    """(faces, edges, vertices) for a solid — checks deltahedra then Platonic."""
    return DELTAHEDRA[solid] if solid in DELTAHEDRA else PLATONIC[solid]


def euler_characteristic(solid: str) -> int:
    """F − E + V (should be 2 for every convex polyhedron). Accepts Platonic or deltahedron names."""
    f, e, v = _fev(solid)
    return f - e + v


def solid_for_particle(particle: str) -> dict:
    """The particle's Tetryonic DELTAHEDRON: {solid, faces, edges, vertices,
    topology_pi, mass_energy_pi}.  (lepton → dodeca-deltahedron, NOT Platonic dodecahedron)."""
    solid, topo, me = PARTICLE_SOLID[particle]
    f, e, v = DELTAHEDRA[solid]
    return {"solid": solid, "faces": f, "edges": e, "vertices": v,
            "topology_pi": topo, "mass_energy_pi": me}


# Closed-form surface area & volume of each classical Platonic solid (edge = a).
_AREA = {
    "tetrahedron":  lambda a: SQRT3 * a * a,
    "cube":         lambda a: 6.0 * a * a,
    "octahedron":   lambda a: 2.0 * SQRT3 * a * a,
    "dodecahedron": lambda a: 3.0 * math.sqrt(25 + 10 * SQRT5) * a * a,
    "icosahedron":  lambda a: 5.0 * SQRT3 * a * a,
}
_VOLUME = {
    "tetrahedron":  lambda a: a**3 / (6 * SQRT2),
    "cube":         lambda a: a**3,
    "octahedron":   lambda a: (SQRT2 / 3.0) * a**3,
    "dodecahedron": lambda a: (15 + 7 * SQRT5) / 4.0 * a**3,
    "icosahedron":  lambda a: 5.0 * (3 + SQRT5) / 12.0 * a**3,
}
# Volume of each particle DELTAHEDRON (edge = a). tetra/octa/icoso coincide with the
# Platonic solids; the dodeca-deltahedron is the snub disphenoid (12-face convex deltahedron).
_DELTA_VOLUME = {
    "tetra-deltahedron":  lambda a: a**3 / (6 * SQRT2),
    "octa-deltahedron":   lambda a: (SQRT2 / 3.0) * a**3,
    "dodeca-deltahedron": lambda a: 0.859493 * a**3,   # snub disphenoid (J84)
    "icoso-deltahedron":  lambda a: 5.0 * (3 + SQRT5) / 12.0 * a**3,
}


def platonic_metrics(solid: str, edge: float = 1.0) -> dict:
    """Surface area & volume of a classical Platonic solid (the p19 comparison)."""
    return {"area": _AREA[solid](edge), "volume": _VOLUME[solid](edge)}


def deltahedron_metrics(solid: str, edge: float = 1.0) -> dict:
    """Surface area & volume of a Tetryonic deltahedron.
    Surface area = faces × equilateral-triangle area (all faces are equilateral triangles)."""
    f, _, _ = DELTAHEDRA[solid]
    return {"area": f * equilateral_area(edge), "volume": _DELTA_VOLUME[solid](edge)}


def particle_solid_metrics(particle: str, edge: float = 1.0) -> dict:
    """Full geometry of a particle's 3D deltahedron: faces/edges/vertices + area + volume."""
    info = solid_for_particle(particle)
    info.update(deltahedron_metrics(info["solid"], edge))
    return info


def mass_energy_pi(level: int) -> int:
    """The 4nπ mass-energy scaling of a tetryon at level n  = 4·n  (π multiples)."""
    return 4 * level


# --- Math-of-physics drawn as geometry (Book 5 pp.55, 86, 144, 152) ----------
def imaginary_rotation(x: float, y: float, quarter_turns: int = 1) -> tuple[float, float]:
    """√−1 is the quarter-turn operator (Book 5 p.55): multiplying a 2D vector — a complex
    number x+iy — by i rotates it 90°.  i·(x+iy) = −y + i·x.  ``quarter_turns`` = the power
    of i applied.  This is what makes the imaginary unit a *geometry*, not a mystery."""
    for _ in range(quarter_turns % 4):
        x, y = -y, x
    return (x, y)


def i_power(n: int) -> tuple[int, int]:
    """i^n as a point on the unit circle (Book 5 p.55), returned as (real, imag):
    i⁰=1, i¹=i, i²=−1, i³=−i — a 4-fold rotation cycle."""
    return [(1, 0), (0, 1), (-1, 0), (0, -1)][n % 4]


def odd_as_square_difference(n: int) -> int:
    """The geometric odd-number identity (Book 5 p.86): n² − (n−1)² = 2n−1 — each odd number
    is the L-shaped gnomon that grows one square to the next."""
    return n * n - (n - 1) * (n - 1)


def equilateral_distribution(n: int) -> list[int]:
    """Kelvin's quantum probability distribution (Book 5 p.152): the equilateral row
    1,2,…,n,…,2,1 (length 2n−1, peak n, sum = n²).  This triangular distribution of quantised
    energy-momenta is the geometric basis of every normal (Gaussian) distribution in QM,
    thermodynamics and information entropy."""
    if n < 1:
        return []
    return list(range(1, n + 1)) + list(range(n - 1, 0, -1))


def probability_from_amplitude(amplitude: float) -> float:
    """Born rule as geometry (Book 5 p.157): probability = |amplitude|² — the square (an
    equilateral area) of the wave amplitude."""
    return abs(amplitude) ** 2


def infinities_exist() -> bool:
    """Renormalisation — the Tetryonic answer (Book 5 p.144): infinities do NOT exist. A
    charged particle's EM self-energy is FINITE because Matter is a finite equilateral geometry,
    not a zero-radius point; QED must cancel infinities, Tetryonics never produces them."""
    return False
