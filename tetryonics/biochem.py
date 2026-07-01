"""
Biochemistry — Book 3 (Chemistry), the organic / biological chapters.

Every biomolecule is just a sum of its atoms' charge-π topologies (the same rule as any
compound), so carbohydrates, amino acids and nucleotides all have an exact quanta count.
Condensation (peptide / glycosidic bonds) releases one water (768π) per bond formed.

Verified: glucose C₆H₁₂O₆ = 6·504 + 12·48 + 6·672 = 7632π (matches Book 3 p.408).
"""

from __future__ import annotations

from . import elements as el

WATER_QUANTA = 768          # H₂O = 768π (released per condensation bond)
CARBOHYDRATE_UNIT = 1272    # one C(H₂O) unit = 504 + 768

# The 20 standard amino acids (name -> molecular formula).
AMINO_ACIDS = {
    "glycine": "C2H5NO2", "alanine": "C3H7NO2", "serine": "C3H7NO3",
    "proline": "C5H9NO2", "valine": "C5H11NO2", "threonine": "C4H9NO3",
    "cysteine": "C3H7NO2S", "leucine": "C6H13NO2", "isoleucine": "C6H13NO2",
    "asparagine": "C4H8N2O3", "aspartate": "C4H7NO4", "glutamine": "C5H10N2O3",
    "lysine": "C6H14N2O2", "glutamate": "C5H9NO4", "methionine": "C5H11NO2S",
    "histidine": "C6H9N3O2", "phenylalanine": "C9H11NO2", "arginine": "C6H14N4O2",
    "tyrosine": "C9H11NO3", "tryptophan": "C11H12N2O2",
}

# Common sugars / building blocks.
SUGARS = {"glucose": "C6H12O6", "fructose": "C6H12O6", "ribose": "C5H10O5",
          "deoxyribose": "C5H10O4", "sucrose": "C12H22O11"}

# DNA/RNA nucleobases (name -> formula).
BASES = {"adenine": "C5H5N5", "guanine": "C5H5N5O", "cytosine": "C4H5N3O",
         "thymine": "C5H6N2O2", "uracil": "C4H4N2O2"}

# Functional-group quanta (Book 3 pp.392-428) = the ADDITIVE atomic-topology sum (C=504, H=48,
# N=588, O=672), the same rule as every compound. This keeps functional_group_quanta() consistent
# with molecule_quanta() and matches the plate-verified totals (glucose 7632 p408, TNT 9564 p402,
# the whole alkane series, p394 CH2=600, p408 CH=552/CH2=600). NOTE: his p389 lists an inconsistent
# CH=648/CH2=696/CH3=744 (and "CH3=744" is only *implied* there) — that outlier page is NOT used.
FUNCTIONAL_GROUPS = {"CH": 552, "CH2": 600, "CH3": 648, "OH": 720,
                     "NH2": 684, "NO2": 1932, "NO3": 2604, "COOH": None}


def molecule_quanta(formula: str) -> int:
    """Total charge-π quanta of any (bio)molecule = Σ atomic topologies."""
    return el.molecule_topology_pi(formula)


def molecule_mass(formula: str) -> float:
    """Rest mass (kg) of a biomolecule."""
    return el.molecule_mass(formula)


def amino_acid_quanta(name: str) -> int:
    return molecule_quanta(AMINO_ACIDS[name.lower()])


def sugar_quanta(name: str) -> int:
    return molecule_quanta(SUGARS[name.lower()])


def peptide_quanta(residues: list) -> int:
    """Quanta of a peptide built from a list of amino-acid names.

    Each peptide bond is a condensation that releases one water (768π), so for N residues
    forming a chain there are N−1 bonds:  Σ(residue quanta) − 768·(N−1).
    """
    total = sum(amino_acid_quanta(r) for r in residues)
    return total - WATER_QUANTA * (len(residues) - 1)


def polysaccharide_quanta(monomer: str, n: int) -> int:
    """Quanta of an n-unit polysaccharide: n monomers minus (n−1) condensation waters."""
    return n * sugar_quanta(monomer) - WATER_QUANTA * (n - 1)


def condensation_water(bonds: int) -> int:
    """Total water-quanta released forming ``bonds`` condensation bonds."""
    return WATER_QUANTA * bonds


def base_quanta(name: str) -> int:
    """Quanta of a DNA/RNA nucleobase."""
    return molecule_quanta(BASES[name.lower()])


# Complementary base pairs. In Tetryonics the strands are held together by CHARGE
# interaction between the bases' opposite field geometries — NOT hydrogen bonding
# (Book 3, the DNA/RNA plates). A↔T (DNA) / A↔U (RNA), G↔C.
DNA_PAIRS = {"adenine": "thymine", "thymine": "adenine",
             "guanine": "cytosine", "cytosine": "guanine"}
RNA_PAIRS = {"adenine": "uracil", "uracil": "adenine",
             "guanine": "cytosine", "cytosine": "guanine"}


def complementary_base(base: str, rna: bool = False) -> str:
    """The charge-complementary base: A→T (DNA) or A→U (RNA), G→C, etc."""
    pairs = RNA_PAIRS if rna else DNA_PAIRS
    return pairs[base.lower()]


def base_pair_quanta(base: str, rna: bool = False) -> int:
    """Combined charge-π of a base pair (A·T / A·U / G·C) — the two bases joined by
    charge interaction (Tetryonic pairing, not H-bonds)."""
    return base_quanta(base) + base_quanta(complementary_base(base, rna))


def nucleotide_quanta(base: str, deoxy: bool = False) -> int:
    """Quanta of a nucleotide = base + sugar (ribose/deoxyribose) + phosphate,
    minus two condensation waters (sugar–base and sugar–phosphate)."""
    sugar = "deoxyribose" if deoxy else "ribose"
    phosphate = molecule_quanta("H3PO4")
    return (base_quanta(base) + sugar_quanta(sugar) + phosphate
            - 2 * WATER_QUANTA)


def functional_group_quanta(group: str) -> int:
    """Quanta of a named functional group (CH2, OH, NO2 …)."""
    v = FUNCTIONAL_GROUPS[group]
    if v is None:
        return molecule_quanta(group)
    return v
