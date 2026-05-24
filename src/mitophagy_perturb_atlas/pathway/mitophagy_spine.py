"""Canonical PINK1/Parkin mitophagy gene set.

Per ADR-0005, the headline pathway annotation uses Reactome's "Mitophagy"
hierarchy (Reactome R-HSA-5205647 + child terms). This module hard-codes
the *spine* of that pathway — the most central genes that any analysis
of PRKN-loss phenocopy must report on — so that downstream code has a
single source of truth even before the Reactome client is wired up.

The spine is drawn from:

* Reactome R-HSA-5205647 "Mitophagy" (canonical pathway)
* Pickrell & Youle (2015) *Neuron* 85:257-273 — canonical mitophagy
  review whose Figure 1 informs which genes count as "central."
* Lazarou et al. (2015) *Nature* 524:309-314 — receptor-mediated
  mitophagy via NDP52 / OPTN.

Genes are HGNC-symbol-normalized; aliases handled at the loader boundary.
"""

from __future__ import annotations

from typing import Final

CANONICAL_MITOPHAGY_GENES: Final[tuple[str, ...]] = (
    # Kinase + ligase axis (the PINK1/Parkin step).
    "PINK1",
    "PRKN",  # = Parkin
    "PARK7",  # = DJ-1
    # Ubiquitin signal readers.
    "OPTN",
    "NBR1",
    "CALCOCO2",  # = NDP52
    "TAX1BP1",
    "SQSTM1",  # = p62
    # Mitochondrial fission / dynamics directly required for mitophagy.
    "DNM1L",  # = DRP1
    "FIS1",
    "MFF",
    # Receptors / outer-membrane.
    "BNIP3",
    "BNIP3L",  # = NIX
    "FUNDC1",
    # Downstream autophagy machinery (a curated subset).
    "ATG7",
    "ATG5",
    "MAP1LC3B",
    "GABARAPL1",
)
"""Eighteen canonical mitophagy genes. Order is significant: kept stable so
downstream plots have a deterministic axis order."""


def canonical_spine() -> tuple[str, ...]:
    """Return the canonical 18-gene spine."""
    return CANONICAL_MITOPHAGY_GENES


def extended_spine() -> tuple[str, ...]:
    """Spine + a curated mitochondrial-QC adjuncy set.

    Adds genes that aren't strictly mitophagy executors but whose loss
    phenocopies a mitophagy defect strongly enough to belong on the
    "things to look at" list per Pickrell & Youle Table 1.
    """
    extras: tuple[str, ...] = (
        "HTRA2",
        "VPS13C",
        "MUL1",
        "TOMM7",
        "TOMM20",
        "MIRO1",  # RHOT1
        "MIRO2",  # RHOT2
    )
    seen: set[str] = set()
    out: list[str] = []
    for g in (*CANONICAL_MITOPHAGY_GENES, *extras):
        if g not in seen:
            seen.add(g)
            out.append(g)
    return tuple(out)


__all__ = [
    "CANONICAL_MITOPHAGY_GENES",
    "canonical_spine",
    "extended_spine",
]
