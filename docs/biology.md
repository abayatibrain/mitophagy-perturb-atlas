# Biology primer for mitophagy-perturb-atlas

Audience: ML / engineering readers who need the biological context to read
this repo's README confidently. Skip if you already know the territory.

## Mitophagy in one paragraph
Mitophagy is the autophagic removal of mitochondria. The canonical
PINK1/Parkin pathway works like this: mitochondrial depolarization
stabilizes PINK1 on the outer mitochondrial membrane → PINK1 phosphorylates
ubiquitin and Parkin → activated Parkin ubiquitinates outer-membrane
substrates (MFN1/2, MIRO1, VDAC) → autophagy adaptors (OPTN, NDP52,
TAX1BP1) recognize the ubiquitin chains and recruit LC3 → an autophagosome
engulfs the damaged mitochondrion. **Reactome IDs of interest:**
R-HSA-5205685 (mitophagy, broadly) and R-HSA-5205647 (PINK1/Parkin
specifically).

Non-canonical mitophagy is also real and biologically distinct: BNIP3,
BNIP3L (NIX), and FUNDC1 are outer-membrane receptors that recruit LC3
directly without ubiquitin chains. This repo handles both, but is explicit
about which view it is showing.

## Why CRISPR screens matter here
A perturbation screen tells you, in an unbiased way, which genes have
similar consequences when knocked out (or knocked down, or activated).
For pathway biology, this is a directly relevant signal: a gene whose
loss phenocopies PRKN loss is, by definition, a candidate node in the
same functional module.

## A note on direction
Phenocopy correlation is signed. USP30 is a deubiquitinase that opposes
Parkin's action — its loss is expected to look *opposite* to PRKN loss.
The network view exposes signed correlation. Treating |correlation| as
"membership in the same pathway" without checking sign is a common
interpretation error this repo refuses to make.

## Authoritative sources
This primer was written from public, citable sources. Where a claim is made
about disease biology, the underlying source is one of:

- HGNC (https://www.genenames.org/) — gene symbols
- OpenTargets (https://platform.opentargets.org/) — target-disease associations
- Reactome (https://reactome.org/) — pathway definitions
- UniProt (https://www.uniprot.org/) — protein function
- Primary literature (cited in README §Method)

If you find a claim here that is not defensible from these sources, open
an issue — that is a defect.
