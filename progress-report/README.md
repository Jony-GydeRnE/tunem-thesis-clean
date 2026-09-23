# Progress report: guide and edited excerpt

| Document | Pages | Source |
|---|---|---|
| [Illustrated thesis guide](thesis-guide.pdf) | 20 | [`../thesis/code/thesis_guide_content.json`](../thesis/code/thesis_guide_content.json), rendered by [`build_thesis_guide.py`](../thesis/code/build_thesis_guide.py) |
| [Edited excerpt](edited-excerpt-30-pages.pdf) | 30 | [`edited-excerpt-30-pages.tex`](edited-excerpt-30-pages.tex) |

**The guide** is a newly written overview of the full 166-page draft: the argument in three acts, representative derivations, the two obstructions at Freidberg's reference point, the qualified ST verdict, the centre-stack ledger and the research opening. It reuses the thesis's vector figures and points to the detailed calculations by section number.

**The excerpt** is a two-page progress note followed by Sections 1–18 of the thesis, included page-for-page from the current thesis build so it can never drift from the source it samples. It demonstrates the teaching style: every section ends in a boxed design consequence and a *model and limits* note.

Neither document is a reactor design. The guide complements the thesis; it does not replace the derivations.

## Rebuilding

From the repository root:

```sh
python3 thesis/code/build.py thesis        # the excerpt includes pages of thesis/thesis-draft.pdf
python3 thesis/code/build.py excerpt
python3 thesis/code/build_thesis_guide.py --figures thesis/figures/final --output .build/thesis-guide/thesis-guide.pdf
```

Edit the JSON (guide) or the `.tex` (excerpt), never the PDFs. Review the page previews under `.build/` before replacing a PDF here.
