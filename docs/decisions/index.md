# Decision log

Every non-trivial decision in this repo lives here as an Architecture
Decision Record (ADR). Reading these in order should let you reconstruct
every meaningful judgment call that shaped the code, without reading the
code itself.

The ADR template lives at [`templates/adr.md`](../templates/adr.md).

## Index — current ADRs

| ADR | Title | Status |
|-----|-----------------------------------------------------------|--------|
| [0001](0001.md) | Keep DepMap and Perturb-Seq in separate similarity spaces | Proposed |
| [0002](0002.md) | DepMap release pinning | Proposed |
| [0003](0003.md) | Replogle 2022 cell-line subset (K562 + RPE1) | Proposed |
| [0004](0004.md) | Similarity metric (cosine + Pearson + Spearman) | Proposed |
| [0005](0005.md) | Pathway-definition scope (Reactome primary, KEGG/GO cross-check) | Proposed |
| [0006](0006.md) | Phenocopy FDR methodology (empirical null per modality) | Proposed |

All six ADRs are in **Proposed — awaiting Armin sign-off** status.
Implementation work waits until the relevant ADR ratifies.

## Dependency graph

```
ADR-0001 (separate spaces)
   ├── ADR-0002 (DepMap release; per-modality version)
   ├── ADR-0003 (Replogle subsets; multiple lines as sub-modalities)
   ├── ADR-0004 (similarity metric; computed per modality)
   │     └── ADR-0006 (empirical null built on the metric)
   └── ADR-0005 (pathway scope; orthogonal to similarity)
```

## How to read these ADRs

ADR-0001 is the architecture-shaping choice — separate-spaces framing
ripples into every other decision.

ADR-0006 (FDR) is the most consequential for the README's headline claim
("X phenocopies PRKN at FDR < 0.05") and should be reviewed by anyone
sceptical of the atlas's statistical claims.

ADR-0004 (similarity metric) is where to push back if you want a
different mathematical foundation.
