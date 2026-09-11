#!/usr/bin/env python3
"""Brief 13 — collisional random walk across flux surfaces."""
from sketch_base import *

fig, ax = new(h=3.5)
for f in (0.30, 0.50, 0.70, 0.90, 1.10):
    R, Z = shaped_boundary(a=f, kappa=1.45, delta=0.0)
    ax.plot(R - 2.6, Z, color=PALETTE["bfield"], lw=1.0, ls=LS["bfield"],
            alpha=0.8, zorder=3)

rng = np.random.RandomState(11)
r, th = 0.34, 0.0
xs, ys = [], []
for k in range(150):
    th += 0.20
    r += rng.normal(0, 0.028)
    r = float(np.clip(r, 0.12, 1.08))
    xs.append(-2.6 + r * np.cos(th)); ys.append(1.45 * r * np.sin(th))
ax.plot(xs, ys, color=PALETTE["current"], lw=1.0, zorder=5)
ax.plot([xs[0]], [ys[0]], marker="o", ms=5, color=PALETTE["current"], zorder=6)
ax.plot([xs[-1]], [ys[-1]], marker="s", ms=5, color=PALETTE["current"], zorder=6)
ax.text(-2.6, -1.95, "one guiding centre, 150 collisions:\n"
                     "each kick moves it about one gyro-radius $\\rho$",
        fontsize=8.4, ha="center", va="top", color=PALETTE["current"])

ax.text(0.35, 1.35, "the estimate that follows", fontsize=9.5, ha="left",
        color=PALETTE["vessel"])
for i, t in enumerate((r"$N=\nu t$   collisions in time $t$",
                       r"$\langle\Delta r^2\rangle \sim N\rho^2 = \nu t\,\rho^2$",
                       r"$D_{\rm cl}\sim \rho^2\nu/2$")):
    ax.text(0.45, 0.85 - 0.55 * i, t, fontsize=10.5, ha="left", va="center")
ax.text(0.35, -0.95, "a diffusion coefficient built from ONE step size and\n"
                     "ONE step rate --- this is the CLASSICAL estimate",
        fontsize=8.4, ha="left", va="top", color="0.3")
ax.text(0.35, -1.75, "Real tokamaks lose heat faster than this. Toroidal geometry\n"
                     "adds a neoclassical enhancement, and TURBULENCE adds a\n"
                     "further channel that this picture does not model at all.",
        fontsize=8.4, ha="left", va="top", color=PALETTE["pf"])
ax.set_xlim(-4.3, 5.6); ax.set_ylim(-2.9, 1.85)
save(fig, "figS_random_walk", note="")
