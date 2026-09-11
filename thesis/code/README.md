# Build and reproduce

Run from the repository root. Document builds require Tectonic; the proposal also requires **Noto Serif CJK SC**. Python calculations/figures use NumPy, SciPy, Matplotlib and SymPy as applicable. These requirements are not a locked or certified environment.

```sh
python3 thesis/code/build.py thesis
python3 thesis/code/build.py prologue
python3 thesis/code/build.py proposal
python3 thesis/code/build.py executive-summary
python3 thesis/code/build.py flux-two-parameter
python3 thesis/code/build.py flux-second-invariant
python3 thesis/code/render_figure.py thesis figM1.py
python3 thesis/code/render_figure.py prologue figN_opening.py
python3 thesis/code/calculations/freidberg_baseline_scan.py
python3 thesis/code/calculations/centre_stack_ledger.py
python3 research-ideas/flux-networks/code/g1a_two_parameter_checks.py
python3 research-ideas/flux-networks/code/g1a_second_invariant_checks.py
```

The document builder uses cached TeX resources by default. Use `--online` only when downloads are intended, or `--bundle PATH` for an existing compatible bundle. Missing packages/fonts are prerequisites to resolve, not permission to rewrite a document.

All generated output goes under the repository's ignored `.build/`. Inspect PDF pages before replacing a working document. The supplied proposal and progress-report PDFs are preserved snapshots; do not overwrite them automatically. A successful build does not certify the scientific claims or establish source/PDF equivalence for preserved submissions.

Figure generators reproduce the included diagrams; some also emit unused layout variants. Only promote a reviewed asset actually referenced by a document. Keep plotting inputs with their generator. No tool here uploads files.
