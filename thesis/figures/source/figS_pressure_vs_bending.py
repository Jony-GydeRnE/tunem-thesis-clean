#!/usr/bin/env python3
"""Brief 14 — pressure drive versus poloidal-field line bending."""
from sketch_base import *

fig, ax = new(h=3.2)
th = np.linspace(-np.pi, np.pi, 400)
bulge = 1.0 + 0.42 * np.exp(-(th / 0.55) ** 2)
x = th * 1.5
ax.plot(x, bulge * 0.55, color=PALETTE["bfield"], lw=2.0, zorder=5)
ax.plot(x, -bulge * 0.55, color=PALETTE["bfield"], lw=2.0, zorder=5)
ax.fill_between(x, -bulge * 0.55, bulge * 0.55,
                color=PALETTE["plasmafc"], alpha=0.75, zorder=3)

for t in (-0.55, 0.0, 0.55):
    j = int((t + np.pi) / (2 * np.pi) * 399)
    arrow(ax, (x[j], bulge[j] * 0.55), (x[j], bulge[j] * 0.55 + 0.55),
          color=PALETTE["current"], lw=2.0)
    arrow(ax, (x[j], -bulge[j] * 0.55), (x[j], -bulge[j] * 0.55 - 0.55),
          color=PALETTE["current"], lw=2.0)
ax.text(0, 1.72, "PRESSURE DRIVE   $p$", fontsize=10, ha="center",
        color=PALETTE["current"])
ax.text(0, -1.72, "pushes the bulge outwards", fontsize=8.6, ha="center",
        va="top", color=PALETTE["current"])

for xx in (-3.6, 3.6):
    arrow(ax, (xx, 0.0), (xx - np.sign(xx) * 0.85, 0.0),
          color=PALETTE["bfield"], lw=2.4)
ax.text(-4.0, 0.35, "field-line TENSION\n$B_\\theta^2/\\mu_0$", fontsize=9.5,
        ha="center", va="bottom", color=PALETTE["bfield"])
ax.text(4.0, 0.35, "pulls it back straight", fontsize=9.5, ha="center",
        va="bottom", color=PALETTE["bfield"])

ax.text(0, -2.45, r"edge estimate:  $B_\theta \sim \mu_0 I_p/(2\pi a)$,"
                  r"   so the restoring term goes as $I_p^2$ while the drive goes as $p$",
        fontsize=9, ha="center", va="top")
ax.text(0, -2.95, "This is a SCALING argument for which way each term pushes. "
                  "It is not the MHD stability calculation,\nand it does not by "
                  "itself give a numerical beta limit.",
        fontsize=8.2, ha="center", va="top", color=PALETTE["pf"], linespacing=1.5)
ax.set_xlim(-5.6, 5.6); ax.set_ylim(-3.9, 2.2)
save(fig, "figS_pressure_vs_bending", note="")
