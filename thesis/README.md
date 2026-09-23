# Thesis

[Read the draft](thesis-draft.pdf) · [Source](thesis-draft.tex) · [Build](code/README.md)

The working draft is 166 pages in 127 sections. It reconstructs tokamak design from physical requirements, rebuilds Freidberg's 2015 conventional reference and its two current-centred obstructions, tests the low-aspect-ratio branch against a published finite-A model, and quantifies the spherical-tokamak centre-stack trade. It is a working technical draft, not a completed degree thesis or a certified reactor design.

| Sections | Content |
|---|---|
| 1–50 | Components and variables, derived in the order the physics forces them |
| 51–101 | Freidberg's design calculation: baseline, four screens, four remedies, the high-field route |
| 102–111 | The low-aspect-ratio test and the qualified ST verdict |
| 112–127 | The centre stack: radial ledger, current-area test, the low-A boundary A_min |

## Layout

- `thesis-draft.tex` — the single source; `thesis-draft.pdf` is its current build.
- `figures/final/` — the vector figures the source includes; `figures/source/` — their generators.
- `code/calculations/` — the Freidberg baseline chain and scan, and the centre-stack ledger.
- `code/` — document, figure and guide builders.

## Known limits

The proposal's commercialization and internationalization chapters remain to be written. The ST bootstrap/current-drive affordability comparison needs an independent check. Some later passages still need to be brought into agreement with the qualified §111 verdict. Scientific limitations stay in the text rather than in a changelog.

Rebuild into `.build/`, inspect, then deliberately replace the working PDF.
