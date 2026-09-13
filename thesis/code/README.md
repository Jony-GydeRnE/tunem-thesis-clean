# Build and reproduce

Run everything from the repository root. All generated output goes to the ignored `.build/` directory; inspect a build before replacing a working PDF.

## Requirements

- **TeX:** either [Tectonic](https://tectonic-typesetting.github.io) or an ordinary TeX Live with `latexmk`. `build.py` uses Tectonic when it is installed and falls back to `latexmk` otherwise (`--latexmk` forces the fallback). The proposal and prologue need XeTeX; the proposal also needs **Noto Serif CJK SC**.
- **Python:** NumPy, SciPy, Matplotlib and SymPy for calculations and figures; PyMuPDF and ReportLab for the illustrated guide.
- **Fonts for the guide:** Arial, Liberation Sans (metric-compatible with Arial, so the layout is identical) or DejaVu Sans.

These are prerequisites to install, not permission to rewrite a document around what is missing.

## Documents

```sh
python3 thesis/code/build.py thesis
python3 thesis/code/build.py excerpt              # includes pages 1–28 of thesis/thesis-draft.pdf: build and install the thesis first
python3 thesis/code/build.py prospectus
python3 thesis/code/build.py proposal
python3 thesis/code/build.py executive-summary
python3 thesis/code/build.py prologue
python3 thesis/code/build.py flux-two-parameter
python3 thesis/code/build.py flux-second-invariant
python3 thesis/code/build_thesis_guide.py --figures thesis/figures/final --output .build/thesis-guide/thesis-guide.pdf
```

Tectonic uses cached TeX resources by default; pass `--online` to allow downloads or `--bundle PATH` for an existing bundle.

## Figures and calculations

```sh
python3 thesis/code/render_figure.py thesis figS_st_closure.py
python3 thesis/code/render_figure.py prologue figN_opening.py
python3 thesis/code/calculations/freidberg_baseline_scan.py
python3 thesis/code/calculations/centre_stack_ledger.py
python3 research-ideas/flux-networks/code/g1a_two_parameter_checks.py
python3 research-ideas/flux-networks/code/g1a_second_invariant_checks.py
```

Figure generators write to `.build/figures/<document>/<name>/`; promote a reviewed asset to `figures/final/` only when a document references it. Keep plotting inputs beside their generator.

## The illustrated guide

The 20-page guide is rendered from `thesis_guide_content.json` and reuses the thesis figure PDFs. Edit the JSON, not the PDF. The builder writes page previews to `.build/thesis-guide/.build/page-NN.png`; review them before replacing `progress-report/thesis-guide.pdf`.

A successful build reproduces a document; it does not certify its scientific claims.
