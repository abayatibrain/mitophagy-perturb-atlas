"""Replogle 2022 Perturb-Seq loader (real loader + synthetic fixture).

Per ADR-0003, both K562 and RPE1 spaces are headline-supported. The
real loader expects pseudobulk H5AD-derived TSVs from the Replogle et
al. (2022) deposit; download is gated behind ``scripts/download_data.sh``.

For testing without the real download, :func:`make_synthetic_perturbseq`
generates deterministic synthetic pseudobulk frames in the same canonical
schema.

Canonical schema (long-format):

* ``perturbation: str`` — the targeted gene (HGNC symbol).
* ``feature: str`` — the readout gene (HGNC symbol).
* ``z_score: float`` — pseudobulk perturbed-vs-control z-score on log-CPM.
* ``cell_line: str`` — one of ``"K562"``, ``"RPE1"``, or
  ``"synthetic-v1"``.
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

REPLOGLE_CELL_LINES: Final[tuple[str, ...]] = ("K562", "RPE1")
"""ADR-0003 pins these two."""


@dataclass(frozen=True)
class ReplogleMetadata:
    """Metadata about a loaded Replogle Perturb-Seq snapshot."""

    cell_line: str
    n_perturbations: int
    n_features: int
    source_path: str


def load_replogle_pseudobulk(
    path: Path | str, *, cell_line: str
) -> tuple[pl.DataFrame, ReplogleMetadata]:
    """Load a Replogle pseudobulk H5AD-derived TSV.

    Expected layout: a TSV with header ``perturbation\\tfeature\\tz_score``.
    """
    if cell_line not in REPLOGLE_CELL_LINES:
        raise ValueError(f"unknown cell line {cell_line!r}; expected one of {REPLOGLE_CELL_LINES}")
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Replogle snapshot not found at {path}")
    frame = pl.read_csv(path, separator="\t")
    required = {"perturbation", "feature", "z_score"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Replogle TSV at {path} missing required columns: {sorted(missing)}")
    frame = frame.select(["perturbation", "feature", "z_score"]).with_columns(
        pl.lit(cell_line).alias("cell_line"),
    )
    meta = ReplogleMetadata(
        cell_line=cell_line,
        n_perturbations=frame.get_column("perturbation").n_unique(),
        n_features=frame.get_column("feature").n_unique(),
        source_path=str(path),
    )
    return frame, meta


def make_synthetic_perturbseq(
    *,
    cell_line: str = "K562",
    n_features: int = 60,
    seed: int = 0xBEE5,
) -> tuple[pl.DataFrame, ReplogleMetadata]:
    """Synthetic perturbation x feature z-score matrix for tests.

    Perturbations cover the 18 canonical mitophagy genes (deterministic).
    Features are the canonical genes + ``n_features - 18`` background
    genes. PRKN and PINK1 are engineered to produce highly correlated
    perturbation signatures so the phenocopy detector finds them as the
    top hit pair.
    """
    rng = Generator(PCG64(seed))
    perturbations = list(CANONICAL_MITOPHAGY_GENES)
    background = [f"FG{i:04d}" for i in range(max(0, n_features - len(perturbations)))]
    features = list(CANONICAL_MITOPHAGY_GENES) + background

    matrix = rng.normal(0.0, 1.0, size=(len(perturbations), len(features)))
    if "PRKN" in perturbations and "PINK1" in perturbations:
        i_prkn = perturbations.index("PRKN")
        i_pink1 = perturbations.index("PINK1")
        shared = rng.normal(0.0, 1.0, size=len(features))
        matrix[i_prkn, :] = 0.5 * matrix[i_prkn, :] + 0.5 * shared
        matrix[i_pink1, :] = 0.4 * matrix[i_pink1, :] + 0.6 * shared

    rows: list[dict[str, object]] = []
    for p_idx, perturbation in enumerate(perturbations):
        for f_idx, feature in enumerate(features):
            rows.append(
                {
                    "perturbation": perturbation,
                    "feature": feature,
                    "z_score": float(matrix[p_idx, f_idx]),
                    "cell_line": cell_line,
                }
            )
    frame = pl.DataFrame(rows)
    meta = ReplogleMetadata(
        cell_line=cell_line,
        n_perturbations=len(perturbations),
        n_features=len(features),
        source_path="<synthetic>",
    )
    return frame, meta


def pivot_to_perturbation_matrix(
    long_frame: pl.DataFrame,
) -> tuple[np.ndarray, list[str], list[str]]:
    """Pivot to a ``(perturbation x feature)`` matrix with lexicographic axes."""
    pivoted = long_frame.pivot(
        index="perturbation",
        on="feature",
        values="z_score",
        aggregate_function="mean",
    ).sort("perturbation")
    perts = pivoted.get_column("perturbation").to_list()
    feat_cols = sorted([c for c in pivoted.columns if c != "perturbation"])
    pivoted = pivoted.select(["perturbation", *feat_cols])
    matrix = pivoted.drop("perturbation").to_numpy().astype(np.float64)
    return matrix, [str(p) for p in perts], feat_cols


__all__ = [
    "REPLOGLE_CELL_LINES",
    "ReplogleMetadata",
    "load_replogle_pseudobulk",
    "make_synthetic_perturbseq",
    "pivot_to_perturbation_matrix",
]
