#!/usr/bin/env python3
"""Brief 25 — field is performance AND burden. A two-sided causal diagram."""
from sketch_base import *

fig, ax = new(h=3.1)
node(ax, 3.5, 2.55, 1.9, 0.44, "raise $B_{\\max}$ at the coil", "chosen")

# left: what it buys
node(ax, 1.5, 1.45, 1.9, 0.44, "higher $B_0$ at fixed build", "derived")
node(ax, 1.5, 0.50, 1.9, 0.50, "$P_{\\rm fus}\\propto\\beta^2B_0^4$\nrises steeply", "derived")
flow(ax, (2.85, 2.40), (1.9, 1.72), color=PALETTE["cs"], rad=0.12)
flow(ax, (1.5, 1.23), (1.5, 0.78), color=PALETTE["cs"])
ax.text(1.5, 3.02, "WHAT IT BUYS", fontsize=9.5, ha="center",
        color=PALETTE["cs"], weight="bold")

# right: what it costs
node(ax, 5.6, 1.45, 2.0, 0.50, "$p_B=B^2/2\\mu_0$\nstructural demand rises", "derived")
node(ax, 5.6, 0.50, 2.0, 0.44, "coil thickness $c$ grows", "primary")
flow(ax, (4.2, 2.40), (5.2, 1.72), color=PALETTE["current"], rad=-0.12)
flow(ax, (5.6, 1.20), (5.6, 0.75), color=PALETTE["current"])
ax.text(5.6, 3.02, "WHAT IT COSTS", fontsize=9.5, ha="center",
        color=PALETTE["current"], weight="bold")

# the loop that closes
flow(ax, (4.6, 0.50), (2.5, 0.50), color=PALETTE["current"], ls=(0, (4, 2)),
     rad=0.30)
ax.text(3.55, 0.02, "and a thicker coil eats the very radial build\n"
                    "that was supposed to deliver the higher $B_0$",
        fontsize=8, ha="center", va="top", color=PALETTE["current"])

arrow(ax, (6.7, 2.55), (7.6, 2.55), color="0.45", ls=(0, (4, 2)), lw=1.4)
ax.text(7.65, 2.55, "test only AFTER\nbaseline closure", fontsize=8,
        ha="left", va="center", color="0.35")
ax.set_xlim(0, 9.3); ax.set_ylim(-0.55, 3.3)
save(fig, "figS_field_two_sided",
     "Explanatory sketch. No magnet technology, vendor or numerical performance "
     "claim is implied; this is the shape of the trade-off only.")
