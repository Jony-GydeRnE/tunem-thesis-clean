# Thesis

[Read the condensed draft](thesis-draft.pdf) · [Original 166-page draft](thesis-original-166-pages.pdf) · [Source](thesis-draft.tex) · [Build](code/README.md)

The condensed working draft is 76 pages in 127 sections. It reconstructs tokamak design from physical requirements, rebuilds Freidberg's 2015 conventional reference and its two current-centred obstructions, tests the low-aspect-ratio branch against a published finite-A model, and quantifies the spherical-tokamak centre-stack trade. It is a working technical draft, not a completed degree thesis or a certified reactor design.

| Sections | Content |
|---|---|
| 1–50 | Components and variables, derived in the order the physics forces them |
| 51–101 | Freidberg's design calculation: baseline, four screens, four remedies, the high-field route |
| 102–111 | The low-aspect-ratio test and the qualified ST verdict |
| 112–127 | The centre stack: radial ledger, current-area test, the low-A boundary A_min |

## Layout

- `thesis-draft.tex` — the single editable source for the complete 76-page `thesis-draft.pdf`, including the approved final §§102–127 block. The full PDF is built from this source; no original pages are spliced in.
- `thesis-original-166-pages.pdf` — the unchanged original PDF, preserved from revision `f9dfd38fa00a1d80e03c0c9fe9fc12922803a455`.
- `figures/final/` — the vector figures the source includes; `figures/source/` — their generators.
- `code/calculations/` — the Freidberg baseline chain and scan, and the centre-stack ledger.
- `code/` — document, figure and guide builders.

## Known limits

The proposal's commercialization and internationalization chapters remain to be written. The ST bootstrap/current-drive affordability comparison needs an independent check. The final block retains the qualified §111 verdict and the independent external-drive affordability condition. SUNIST-2 remains outside this core, for a separate later add-on/appendix decision. Scientific limitations stay in the text rather than in a changelog.

Rebuild into `.build/`, inspect, then deliberately replace the working PDF.

## Compression (October 2026)

The assembled core has 76 physical pages with continuous printed numbering. Sections 1–101 occupy pages 1–62; the approved final §§102–127 block occupies pages 63–76. The final block was reconstructed from the approved 14-page comparison PDF using the existing LaTeX equations and figure inputs, with the requested §110 clarification and assembly cleanup.

Equations run continuously from 1 to 198 after removing the unused 50–52 gap; the reference final block’s equations 177–201 therefore become 174–198. Figures run from 1 to 30 and tables from 1 to 12. Model/scope headings and cross-references are unified, review-only title wording is removed, and the entire PDF is rebuilt from source. The original 166-page PDF remains unchanged.

Reproduce with `python3 thesis/code/build.py thesis --latexmk`; the output is `.build/documents/thesis/thesis-draft.pdf`. Reproduce the numerical checks with `st_drive_affordability.py`, `centre_stack_ledger.py`, `freidberg_chain.py`, and `freidberg_baseline_scan.py` in `code/calculations/`.

Accessibility standard: write for an undergraduate physics reader. Introduce the physical question before the symbol, explain each causal step, and identify where empirical evidence or a model closure enters. Main prose uses rounded physical thresholds; tables, captions, footnotes and code retain the numerical audit trail.

Keep the original 166-page PDF and one current condensed PDF in this directory. Replace the condensed PDF as approved blocks are integrated; intermediate editions remain available in Git history.
