"""Tests for the canonical PINK1/Parkin pathway gene set."""

from __future__ import annotations

from mitophagy_perturb_atlas.pathway import (
    CANONICAL_MITOPHAGY_GENES,
    canonical_spine,
    extended_spine,
)


def test_canonical_spine_contains_pink1_parkin() -> None:
    spine = canonical_spine()
    assert "PINK1" in spine
    assert "PRKN" in spine
    assert "OPTN" in spine
    assert "BNIP3" in spine


def test_extended_spine_is_superset() -> None:
    base = set(canonical_spine())
    ext = set(extended_spine())
    assert base.issubset(ext)
    assert len(ext) > len(base)


def test_extended_spine_no_duplicates() -> None:
    ext = extended_spine()
    assert len(ext) == len(set(ext))


def test_spine_order_stable() -> None:
    # Plotting code depends on this ordering being deterministic.
    assert CANONICAL_MITOPHAGY_GENES[0] == "PINK1"
    assert CANONICAL_MITOPHAGY_GENES[1] == "PRKN"
