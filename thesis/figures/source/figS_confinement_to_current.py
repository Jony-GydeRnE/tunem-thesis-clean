#!/usr/bin/env python3
"""Brief 27 — the confinement requirement becomes a current demand."""
from sketch_base import *

fig, ax = new(h=2.9)
node(ax, 1.0, 1.8, 1.75, 0.55, "ignition power balance\n$P_\\alpha = W/\\tau_E$", "derived")
node(ax, 3.4, 1.8, 1.35, 0.45, "$\\tau_{E,\\rm req}$", "derived")
node(ax, 3.4, 0.55, 2.25, 0.62,
     "empirical confinement fit\n$\\tau_E(I)\\propto I^{0.93}B_0^{-0.16}a^{1.63}$",
     "empirical")
node(ax, 6.1, 1.2, 1.35, 0.50, "set equal\n$\\Rightarrow I_{\\rm req}$", "primary")

flow(ax, (1.88, 1.8), (2.72, 1.8))
flow(ax, (4.08, 1.8), (5.42, 1.42), rad=-0.10)
flow(ax, (4.53, 0.62), (5.42, 1.00), rad=0.10)

ax.text(3.4, 0.12, "FIT, NOT THEOREM", fontsize=10, ha="center", va="top",
        color=PALETTE["pf"], weight="bold")
ax.text(3.4, -0.12, "a regression over a database of machines;\n"
                    "its exponents are measurements, not consequences",
        fontsize=7.8, ha="center", va="top", color=PALETTE["pf"])
ax.text(6.1, 0.62, "weak in $B_0$ ($-0.16$),\nstrong in $a$ ($1.63$):\n"
                   "size buys confinement,\nfield barely does",
        fontsize=7.8, ha="center", va="top", color="0.3")
ax.set_xlim(0, 7.1); ax.set_ylim(-0.75, 2.25)
save(fig, "figS_confinement_to_current",
     "Explanatory sketch. Exponents are those of the reference regression "
     "quoted in the text; they are empirical.")
