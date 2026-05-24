"""DepMap CRISPR fitness loader (real loader + synthetic fixture).

Per ADR-0002, the real loader pins DepMap release 24Q2. The actual download
is large (~150 MB) and lives behind ``scripts/download_data.sh``; this
module exposes two surfaces:

* :func:`load_depmap_essentiality` — parse a downloaded DepMap CSV into a
  long-format Polars DataFrame in the canonical schema (one row per
  ``(cell_line, gene)``).
* :func:`make_synthetic_depmap` — generate a deterministic synthetic
  fitness matrix that has the same shape as the real one but small enough
  to ship in the test suite.

Canonical schema (long-format):

* ``cell_line: str`` — DepMap ID (e.g. ``ACH-000001``).
* ``gene: str`` — HGNC symbol.
* ``effect: float`` — Chronos / CERES effect score. More-negative = more
  essential (loss reduces fitness).
* ``release: str`` — DepMap release tag (e.g. ``"24Q2"`` or
  ``"synthetic-v1"``).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

import numpy as np
import polars as pl
from numpy.random import PCG64, Generator

from mitophagy_perturb_atlas.pathway.mitophagy_spine import (
    CANONICAL_MITOPHAGY_GENES,
)

DEPMAP_PINNED_RELEASE: Final[str] = "24Q2"
"""ADR-0002 commits to this release."""


@dataclass(frozen=True)
class DepMapMetadata:
    """Metadata about a loaded DepMap snapshot."""

    release: str
    n_cell_lines: int
    n_genes: int
    source_path: str


def load_depmap_essentiality(
    path: Path | str, *, release: str | None = None
) -> tuple[pl.DataFrame, DepMapMetadata]:
    """Load DepMap CRISPR-screen effect scores from a downloaded CSV.

    Expected CSV layout: the public ``CRISPRGeneEffect.csv`` shape — first
    column is ``ModelID`` (DepMap cell-line ID); remaining columns are
    gene symbols in ``SYMBOL (ENTREZ_ID)`` format.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"DepMap snapshot not found at {path}")
    raw = pl.read_csv(path)
    if "ModelID" not in raw.columns:
        raise ValueError(
            f"DepMap CSV at {path} does not look like CRISPRGeneEffect: "
            f"missing 'ModelID' column. Got: {raw.columns[:5]}..."
        )

    gene_cols = [c for c in raw.columns if c != "ModelID"]

    long = raw.unpivot(
        index=["ModelID"],
        on=gene_cols,
        variable_name="gene_raw",
        value_name="effect",
    )
    long = (
        long.with_columns(
            pl.col("gene_raw").str.replace(r"\s*\(.+\)\s*$", "").alias("gene"),
        )
        .rename({"ModelID": "cell_line"})
        .drop("gene_raw")
    )

    long = long.with_columns(pl.lit(release or DEPMAP_PINNED_RELEASE).alias("release"))
    long = long.select(["cell_line", "gene", "effect", "release"])
    long = long.drop_nulls(subset=["effect"])

    meta = DepMapMetadata(
        release=release or DEPMAP_PINNED_RELEASE,
        n_cell_lines=long.get_column("cell_line").n_unique(),
        n_genes=long.get_column("gene").n_unique(),
        source_path=str(path),
    )
    return long, meta


def make_synthetic_depmap(
    *,
    n_cell_lines: int = 24,
    extra_genes: tuple[str, ...] = (),
    seed: int = 0xDE9A,
) -> tuple[pl.DataFrame, DepMapMetadata]:
    """Deterministic synthetic DepMap-shape fitness matrix.

    Covers the 18 canonical mitophagy genes + any ``extra_genes`` + 50
    background genes (random labels ``BG0000`` ... ``BG0049``). Two
    canonical genes (PRKN and PINK1) are deliberately correlated across
    cell lines (r ~ 0.7) so the phenocopy detector should rank PINK1 as
    the top hit when queried for PRKN.
    """
    rng = Generator(PCG64(seed))
    cell_lines = [f"ACH-SYN-{i:04d}" for i in range(n_cell_lines)]
    genes_canonical = list(CANONICAL_MITOPHAGY_GENES)
    background = [f"BG{i:04d}" for i in range(50)]
    seen: set[str] = set()
    genes: list[str] = []
    for g in (*genes_canonical, *extra_genes, *background):
        if g not in seen:
            seen.add(g)
            genes.append(g)

    n_g = len(genes)
    matrix = np.zeros((n_cell_lines, n_g), dtype=np.float64)

    for g_idx, gene in enumerate(genes):
        mean = -0.4 if gene in genes_canonical else 0.0
        matrix[:, g_idx] = rng.normal(mean, 0.25, size=n_cell_lines)

    # Engineer the PRKN <-> PINK1 phenocopy correlation.
    if "PRKN" in genes and "PINK1" in genes:
        prkn_idx = genes.index("PRKN")
        pink1_idx = genes.index("PINK1")
        shared = rng.normal(-0.4, 0.20, size=n_cell_lines)
        matrix[:, prkn_idx] = 0.5 * matrix[:, prkn_idx] + 0.5 * shared
        matrix[:, pink1_idx] = 0.6 * matrix[:, pink1_idx] + 0.4 * shared

    rows: list[dict[str, object]] = []
    for c_idx, cell in enumerate(cell_lines):
        for g_idx, gene in enumerate(genes):
            rows.append(
                {
                    "cell_line": cell,
                    "gene": gene,
                    "effect": float(matrix[c_idx, g_idx]),
                    "release": "synthetic-v1",
                }
            )
    frame = pl.DataFrame(rows)
    meta = DepMapMetadata(
        release="synthetic-v1",
        n_cell_lines=n_cell_lines,
        n_genes=n_g,
        source_path="<synthetic>",
    )
    return frame, meta


def pivot_to_gene_matrix(
    long_frame: pl.DataFrame,
) -> tuple[np.ndarray, list[str], list[str]]:
    """Pivot a long-format DepMap frame to a ``(cell_line x gene)`` matrix.

    Returns ``(matrix, cell_line_ids, gene_ids)``. Order is stable for a
    given input (lexicographic). Missing ``(cell, gene)`` pairs filled NaN.
    """
    pivoted = long_frame.pivot(
        index="cell_line", on="gene", values="effect", aggregate_function="mean"
    ).sort("cell_line")
    cell_lines = pivoted.get_column("cell_line").to_list()
    gene_cols = sorted([c for c in pivoted.columns if c != "cell_line"])
    pivoted = pivoted.select(["cell_line", *gene_cols])
    matrix = pivoted.drop("cell_line").to_numpy().astype(np.float64)
    return matrix, [str(c) for c in cell_lines], gene_cols


__all__ = [
    "DEPMAP_PINNED_RELEASE",
    "DepMapMetadata",
    "load_depmap_essentiality",
    "make_synthetic_depmap",
    "pivot_to_gene_matrix",
]
