#!/usr/bin/env python3
"""Brief 26 — how the reference design reduces to a one-parameter scan in a.

The manuscript's own point: nothing here is a free choice once the mission is
fixed. Four arrows turn a whole reactor into a function of one variable.
"""
from sketch_base import *

fig, ax = new(h=3.5)
node(ax, 0.9, 2.6, 1.5, 0.52, "mission:\n$P_E$, wall loading $W_n$", "chosen")
node(ax, 0.9, 1.5, 1.5, 0.40, "neutron transport", "chosen")
node(ax, 0.9, 0.5, 1.5, 0.52, "field, stress,\nampere-turns", "chosen")

node(ax, 3.1, 2.6, 1.25, 0.40, "$R_0(a)$", "primary")
node(ax, 3.1, 1.5, 1.25, 0.40, "$b$", "primary")
node(ax, 3.1, 0.5, 1.25, 0.40, "$c(a,B_0)$", "primary")

node(ax, 5.1, 1.5, 1.5, 0.52, "inboard radial build\n$\\Rightarrow B_0(a)$", "derived")
node(ax, 7.0, 1.5, 1.35, 0.52, "test plasma\nconstraints", "empirical")

for y in (2.6, 1.5, 0.5):
    flow(ax, (1.66, y), (2.46, y))
flow(ax, (3.74, 2.6), (4.45, 1.78), rad=-0.12)
flow(ax, (3.74, 1.5), (4.34, 1.5))
flow(ax, (3.74, 0.5), (4.45, 1.22), rad=0.12)
flow(ax, (5.86, 1.5), (6.31, 1.5))

ax.text(5.1, 0.72, "every primary parameter is now a function of $a$ alone",
        fontsize=8.4, ha="center", color="0.3", style="italic")
ax.text(7.0, 0.80, "ends here on purpose:\nthis is a test, not\na success claim",
        fontsize=7.8, ha="center", va="top", color=PALETTE["pf"])
kind_legend(ax, 0.15, -0.15, ["chosen", "primary", "derived", "empirical"], dx=2.0)
ax.set_xlim(0, 8.0); ax.set_ylim(-0.45, 3.05)
save(fig, "figS_causal_scan_in_a",
     "Explanatory sketch. The arrows are the manuscript's own causal chain; no "
     "numerical claim is made here.")
