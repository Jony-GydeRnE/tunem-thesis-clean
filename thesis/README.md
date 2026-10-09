# Thesis

[Read the condensed draft](thesis-draft.pdf) · [Original 166-page draft](thesis-original-166-pages.pdf) · [Source](thesis-draft.tex) · [Build](code/README.md)

The condensed working draft is 123 pages in 127 sections. It reconstructs tokamak design from physical requirements, rebuilds Freidberg's 2015 conventional reference and its two current-centred obstructions, tests the low-aspect-ratio branch against a published finite-A model, and quantifies the spherical-tokamak centre-stack trade. It is a working technical draft, not a completed degree thesis or a certified reactor design.

| Sections | Content |
|---|---|
| 1–50 | Components and variables, derived in the order the physics forces them |
| 51–101 | Freidberg's design calculation: baseline, four screens, four remedies, the high-field route |
| 102–111 | The low-aspect-ratio test and the qualified ST verdict |
| 112–127 | The centre stack: radial ledger, current-area test, the low-A boundary A_min |

## Layout

- `thesis-draft.tex` — the single source; `thesis-draft.pdf` combines the approved 18-page opening, the revised 17-page §§25–50 block, and the original pages 79–166.
- `thesis-original-166-pages.pdf` — the unchanged original PDF, preserved from revision `f9dfd38fa00a1d80e03c0c9fe9fc12922803a455`.
- `figures/final/` — the vector figures the source includes; `figures/source/` — their generators.
- `code/calculations/` — the Freidberg baseline chain and scan, and the centre-stack ledger.
- `code/` — document, figure and guide builders.

## Known limits

The proposal's commercialization and internationalization chapters remain to be written. The ST bootstrap/current-drive affordability comparison needs an independent check. Some later passages still need to be brought into agreement with the qualified §111 verdict. Scientific limitations stay in the text rather than in a changelog.

Rebuild into `.build/`, inspect, then deliberately replace the working PDF.

## Compression (October 2026)

Sections 1–24 occupy 18 pages and §§25–50 occupy 17 pages, replacing 78 original pages with 35. The current condensed PDF has 123 physical pages. The remaining 88 pages retain their original printed numbers (79–166), with link destinations remapped and PDF page labels reflecting that numbering. Sections 51 onward remain unchanged in the source. A fresh full-source build may reflow those later pages; the published PDF deliberately preserves them.

Keep the original 166-page PDF and one current condensed PDF in this directory. Replace the condensed PDF as approved blocks are integrated; intermediate editions remain available in Git history.
