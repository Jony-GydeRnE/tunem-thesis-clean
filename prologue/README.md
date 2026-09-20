# Prologue

[Read the current prologue](before-the-machine.pdf) · [Editable source](before-the-machine.tex)

The current 20-page prologue follows QCD, confinement and the mass gap through pions, nuclear binding, D–T reaction energy, barrier penetration, scattering, thermal averaging, and collective plasma dynamics. It contains 15 pages of main text, two optional mathematical notes, and three pages of sources. Assumptions, measured inputs, and incomplete analytic bridges are identified throughout. It is not yet integrated into the thesis.

Only `before-the-machine.pdf` and its matching `.tex` source are current publication files. Previous versions, including the former published prologue and the separate opening draft, are preserved locally in `archive/`. This folder is excluded by the root `.gitignore`: never stage, force-add, commit, or push archive contents. See the [repository archive policy](../README.md#local-archives-stay-off-github).

Keep prologue documents in this folder. Generated build files and page renders are ignored; no separate top-level output folder is needed.

The current draft uses the binding/recoil and binding/barrier diagrams. The shared diagrams, generator, and numerical data remain in `figures/`. Schematics are not measured nuclear geometry; the binding-energy plot uses AME2020 and the barrier panel is a labelled toy calculation. [Data provenance](figures/source/data/README.md).

Build from the repository root with `python3 thesis/code/build.py prologue`. The build stages its PDF under the ignored `.build/` directory; replace the working PDF only after review.
