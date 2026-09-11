#!/usr/bin/env python3
"""Brief 12 — the ignition balance as a two-pan balance."""
from sketch_base import *

fig, ax = new(h=3.6)
# the beam and fulcrum
ax.plot([-1.8, 1.8], [1.9, 1.9], color=PALETTE["vessel"], lw=2.6, zorder=5)
ax.plot([0, -0.28, 0.28, 0], [1.9, 1.35, 1.35, 1.9], color=PALETTE["vessel"],
        lw=1.8, zorder=4)
ax.plot([0], [1.9], marker="o", ms=7, color=PALETTE["vessel"], zorder=6)

# pans
for x, col in ((-1.8, PALETTE["heat"]), (1.8, PALETTE["bfield"])):
    ax.plot([x, x], [1.9, 1.45], color="0.5", lw=1.0, zorder=4)
    ax.plot([x - 0.5, x + 0.5], [1.45, 1.45], color=col, lw=2.4, zorder=5)
box(ax, -1.8, 1.05, 1.5, 0.55, "$P_\\alpha$\nalpha heating IN",
    ec=PALETTE["heat"], fs=9)
box(ax, 1.8, 1.05, 1.5, 0.55, "$P_{\\rm loss}=W/\\tau_E$\nlosses OUT",
    ec=PALETTE["bfield"], fs=9)

box(ax, 0, 2.62, 1.7, 0.42, "plasma energy $W$", ec=PALETTE["plasma"], fs=9.5)
arrow(ax, (-1.5, 2.35), (-0.5, 2.55), color=PALETTE["heat"], lw=1.6)
arrow(ax, (0.5, 2.55), (1.5, 2.35), color=PALETTE["bfield"], lw=1.6)

ax.text(0, 1.62, "IGNITION is the moment these balance\nwith no external help",
        fontsize=8.6, ha="center", va="top", color=PALETTE["vessel"])

ax.text(0, 0.25,
        r"$\frac{1}{4}n^2\langle\sigma v\rangle E_\alpha \;=\; \frac{3nT}{\tau_E}$",
        fontsize=12, ha="center", va="center")
ax.text(0, -0.22, r"$\Longrightarrow\quad n\tau_E \;=\; "
                  r"\frac{12\,T}{\langle\sigma v\rangle E_\alpha}"
                  r"\qquad\Longrightarrow\qquad "
                  r"n T \tau_E \;\gtrsim\; \text{const}$",
        fontsize=11.5, ha="center", va="center")
ax.text(0, -0.72, "three steps, no new physics: cancel one power of $n$, "
                  "solve for $n\\tau_E$, then multiply by $T$\n"
                  "to reach the form the reactor literature quotes",
        fontsize=8.4, ha="center", va="top", color="0.35", linespacing=1.5)
ax.set_xlim(-3.4, 3.4); ax.set_ylim(-1.35, 3.05)
save(fig, "figS_ignition_balance", note="")
