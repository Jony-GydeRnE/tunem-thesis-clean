#!/usr/bin/env python3
"""Brief 30 — the conventional baseline's two coupled closure failures."""
from sketch_base import *

fig, ax = new(h=4.0)
node(ax, 1.0, 3.2, 1.6, 0.50, "mission +\nwall loading", "chosen")
node(ax, 1.0, 2.1, 1.6, 0.42, "$\\bar p,\\ V$", "derived")
node(ax, 1.0, 1.0, 1.6, 0.50, "ignition +\nconfinement fit", "empirical")
node(ax, 3.2, 1.55, 1.25, 0.42, "$I$", "primary")
flow(ax, (1.0, 2.95), (1.0, 2.33)); flow(ax, (1.0, 1.89), (1.0, 1.27))
flow(ax, (1.82, 2.1), (2.58, 1.72), rad=-0.10)
flow(ax, (1.82, 1.0), (2.58, 1.40), rad=0.10)

# branch one
node(ax, 5.3, 2.55, 1.25, 0.42, "$q_*$", "primary")
node(ax, 7.3, 2.55, 1.9, 0.46, "$\\mathcal{R}_K=1.28>1$", "fail", fs=9)
flow(ax, (3.84, 1.72), (4.66, 2.42), rad=-0.10)
flow(ax, (5.94, 2.55), (6.34, 2.55), color=PALETTE["current"], lw=1.8)

# branch two
node(ax, 5.3, 0.60, 2.0, 0.56,
     "pressure profile +\ntrapped-particle model", "empirical")
node(ax, 7.3, 0.60, 1.9, 0.62,
     "$f_{\\rm NC}=0.44$ vs $f_B=0.84$\n$\\mathcal{R}_B=1.91>1$", "fail", fs=8.6)
flow(ax, (3.84, 1.40), (4.28, 0.82), rad=0.10)
flow(ax, (6.32, 0.60), (6.34, 0.60), color=PALETTE["current"], lw=1.8)

# side checks
node(ax, 7.3, 1.60, 1.9, 0.46, "density: PASS      $\\beta$: MARGINAL", "pass", fs=8)

ax.text(4.3, 3.35, "TWO FAILURES, ONE CAUSE: both branches descend from the "
                   "same demanded current $I$",
        fontsize=9, ha="center", color=PALETTE["vessel"], style="italic")
ax.text(4.3, 3.05, "every threshold below is empirical or model-dependent — "
                   "none is a first principle",
        fontsize=8.2, ha="center", color=PALETTE["pf"])
kind_legend(ax, 0.3, -0.30, ["chosen", "primary", "derived", "empirical", "fail"], dx=1.72)
ax.set_xlim(0, 8.6); ax.set_ylim(-0.60, 3.65)
save(fig, "figS_two_closure_failures",
     "Explanatory sketch. Both ratios are properties of the selected 2015 model "
     "set at its reference point, not universal tokamak limits.")
