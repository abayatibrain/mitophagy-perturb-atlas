#!/usr/bin/env bash
# Idempotent dataset fetcher for mitophagy-perturb-atlas.
# Re-running this script with all hashes valid is a no-op (§2.6).
#
# Datasets pulled and their SHA256 hashes are documented in data/README.md.
set -euo pipefail

CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/mitophagy_perturb_atlas"
mkdir -p "$CACHE_DIR"

echo "→ Cache dir: $CACHE_DIR"
echo "→ See data/README.md for the dataset manifest."
echo
echo "TODO: implement per-dataset download + SHA256 verification in subsequent commits."
echo "      First implementation belongs to the data loader module that consumes it."
