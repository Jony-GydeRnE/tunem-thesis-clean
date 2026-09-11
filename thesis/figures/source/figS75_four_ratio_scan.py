#!/usr/bin/env python3
"""
figS75_four_ratio_scan.py — the four demand-to-allowance ratios versus minor
radius, for the 2015 conventional baseline.

RESET QUANTITATIVE PLOT, not a cumulative machine image.  It belongs to the
figS* namespace and deliberately does NOT import tokamak_build: this is a graph
of an audit, not a picture of hardware.  It does import the SAME palette, so
the two families still read as one document.

Every number here comes from Thesis/code/calculations/freidberg_baseline_scan.py, which
implements the analytic assumptions of Freidberg, Mangiarotti & Minervini
(2015).  Nothing is fitted and nothing is drawn by hand.

What the plot must NOT be read as saying: this is not a universal tokamak
limit.  It is the behaviour of ONE declared set of models -- an analytic coil
build, one empirical confinement fit, one stability threshold, one kinetic
bootstrap coefficient -- and each of those is a modelling choice.  That
sentence is printed on the figure, not left to the caption.

Run from Thesis/: python3 code/build/render_figure.py figS75_four_ratio_scan.py
Out:  figS75_four_ratio_scan.pdf / .png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import freidberg_baseline_scan as F
from tokamak_build import PALETTE          # one palette across both families

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm",
                     "font.size": 10, "axes.linewidth": 0.9})

# --------------------------------------------------------------------------
# the scan
# --------------------------------------------------------------------------
A = np.linspace(0.60, 2.00, 281)
rows = []
for a in A:
    try:
        rows.append(F.state(float(a)))
    except Exception:
        rows.append(None)
ok = np.array([r is not None for r in rows])

def series(key):
    y = np.full(len(A), np.nan)
    for i, r in enumerate(rows):
        if r is not None:
            y[i] = r[key]
    return y

# Each ratio gets a colour AND a dash pattern: the same redundant-encoding rule
# the machine-state family uses, for the same reason (greyscale printing).
RATIOS = [
    ("greenwald_ratio", r"$\mathcal{R}_G$  Greenwald density",
     PALETTE["heat"],    (0, (1.5, 1.6, 7, 1.6))),
    ("troyon_ratio",    r"$\mathcal{R}_T$  Troyon $\beta$",
     PALETTE["pf"],      (0, (9, 2.2, 1.6, 2.2))),
    ("kink_ratio",      r"$\mathcal{R}_K$  kink safety factor",
     PALETTE["current"], "solid"),
    ("bootstrap_ratio", r"$\mathcal{R}_B$  bootstrap fraction",
     PALETTE["plasma"],  (0, (5.5, 2.2))),
]

Y = {k: series(k) for k, _, _, _ in RATIOS}
worst = np.nanmax(np.vstack([Y[k] for k, _, _, _ in RATIOS]), axis=0)
i_best = int(np.nanargmin(worst))
a_best, w_best = A[i_best], worst[i_best]

# --------------------------------------------------------------------------
# the figure
# --------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.9, 4.9))

# shade ONLY above one -- the violated region, as requested
ax.axhspan(1.0, 10.0, color="0.5", alpha=0.13, lw=0, zorder=0)
ax.axhline(1.0, color="black", lw=1.4, zorder=3)
ax.text(1.99, 1.03, "demand = allowance", fontsize=8.6, va="bottom",
        ha="right", color="black")
ax.text(1.99, 0.955, "below: the model allows it", fontsize=8.6, va="top",
        ha="right", color="0.35")

for key, lab, col, ls in RATIOS:
    ax.plot(A, Y[key], color=col, ls=ls, lw=1.9, label=lab, zorder=4)

# the least-violating machine
ax.plot([a_best], [w_best], marker="o", ms=7, mfc="white",
        mec=PALETTE["vessel"], mew=1.8, zorder=6)
ax.annotate(f"least-violating point\n$a={a_best:.2f}$ m, worst ratio "
            f"$={w_best:.2f}$\n(still $>1$: no radius passes)",
            xy=(a_best, w_best), xytext=(a_best + 0.20, w_best + 0.92),
            fontsize=8.8, color=PALETTE["vessel"], ha="left",
            arrowprops=dict(arrowstyle="-|>", color=PALETTE["vessel"], lw=1.0),
            zorder=7)

# The scan simply stops: past this radius the analytic coil model has NO REAL
# thickness solution, i.e. the inboard build has run out of room before any
# plasma constraint is even consulted.  That is a result, not missing data,
# so it is drawn rather than silently cropped.
a_stop = A[ok][-1]
ax.axvline(a_stop, color=PALETTE["tf"], lw=1.2, ls=(0, (3, 2.5)), zorder=3)
ax.axvspan(a_stop, A[-1], color=PALETTE["tf"], alpha=0.07, lw=0, zorder=0)
ax.text(a_stop - 0.02, 0.13,
        f"$a>{a_stop:.2f}$ m: the coil model has\nno real thickness solution --\n"
        "the inboard build is already full",
        fontsize=8.2, ha="right", va="bottom", color=PALETTE["tf"],
        linespacing=1.4)

ax.set_xlim(A[0], A[-1])
ax.set_ylim(0.0, min(4.2, np.nanmax(worst) * 1.05))
ax.set_xlabel(r"plasma minor radius  $a$   [m]")
ax.set_ylabel(r"demand / allowance     $\mathcal{R}$")
ax.set_title("2015 BASELINE MODELS — four-ratio scan versus minor radius",
             fontsize=11.5, pad=9)
ax.grid(True, color="0.88", lw=0.6, zorder=1)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9, loc="upper center", ncol=2,
          handlelength=2.8, columnspacing=1.4)

fig.text(0.5, -0.015,
         "Reproduced from code/calculations/freidberg_baseline_scan.py. "
         "These are the ratios implied by ONE declared model set — an analytic\n"
         "coil build, one empirical confinement fit, one stability threshold, "
         "one kinetic bootstrap coefficient. This is NOT a universal\n"
         "tokamak limit: it is the behaviour of that model set, and each "
         "ingredient is a modelling choice that can be argued with.",
         fontsize=7.6, ha="center", va="top", color="0.35", linespacing=1.5)

fig.tight_layout()
fig.savefig("figS75_four_ratio_scan.pdf", bbox_inches="tight")
fig.savefig("figS75_four_ratio_scan.png", dpi=180, bbox_inches="tight")
print(f"least-violating a = {a_best:.4f} m, worst ratio = {w_best:.4f}")
for key, lab, _, _ in RATIOS:
    print(f"   {key:18s} at a_best = {Y[key][i_best]:.4f}")
print("wrote figS75_four_ratio_scan.pdf/.png")
