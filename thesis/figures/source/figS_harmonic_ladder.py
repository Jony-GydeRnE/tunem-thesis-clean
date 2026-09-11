#!/usr/bin/env python3
"""Brief 7 — the external-field harmonic ladder, three panels."""
from sketch_base import *

fig, axs = new(h=3.1, n=3)
PANELS = [
    ("$C_1$: uniform vertical", 1.0, 0.0, "translate", 0.0),
    ("$C_2$: quadrupole",       1.55, 0.0, "elongate", 0.0),
    ("$C_3$: hexapole-like",    1.55, 0.42, "add a D corner", 0.0),
]
for ax, (title, kap, dlt, verb, _) in zip(axs, PANELS):
    Rr, Zr = shaped_boundary(a=1.0, kappa=1.0, delta=0.0)
    ax.plot(Rr, Zr, color="0.65", lw=1.2, ls=(0, (3, 2.5)), zorder=3)
    Rs, Zs = shaped_boundary(a=1.0, kappa=kap, delta=dlt)
    off = 0.55 if verb == "translate" else 0.0
    ax.fill(Rs + off, Zs, facecolor=PALETTE["plasmafc"],
            edgecolor=PALETTE["plasma"], lw=1.6, zorder=4, alpha=0.9)
    # the field pattern, as arrows on a ring outside the plasma
    th = np.linspace(0, 2 * np.pi, 400)
    m = {"translate": 0, "elongate": 2, "add a D corner": 3}[verb]
    r = 2.15
    for t in np.linspace(0, 2 * np.pi, 16, endpoint=False):
        amp = 0.42 * (1.0 if m == 0 else np.cos(m * t / 2 * 2 / 2 * 2))
        if m == 0:
            dx, dy = 0.0, 0.42
        else:
            amp = 0.42 * np.cos(m * t)
            dx, dy = amp * np.cos(t), amp * np.sin(t)
        arrow(ax, (r * np.cos(t), r * np.sin(t)),
              (r * np.cos(t) + dx, r * np.sin(t) + dy),
              color=PALETTE["pf"], lw=1.2, z=2)
    ax.set_title(title, fontsize=10, color=PALETTE["pf"], pad=6)
    ax.text(0, -3.05, verb.upper(), fontsize=9, ha="center", va="top",
            color=PALETTE["plasma"])
    ax.set_xlim(-3.0, 3.2); ax.set_ylim(-3.5, 2.9)

axs[0].text(-2.9, -2.55, "grey dashed = the circle\nwe started from",
            fontsize=7.6, ha="left", va="top", color="0.5")
fig.text(0.5, 0.055, "Real PF coils are toroidal rings, not the flat multipoles "
                     "drawn here. These are the leading terms of the external "
                     "field expanded about the plasma —\nthe ladder the coil set "
                     "has to climb, one independently controllable pattern per "
                     "shape parameter.", fontsize=7.8, ha="center", va="bottom",
         color="0.35", linespacing=1.5)
save(fig, "figS_harmonic_ladder", note="")
