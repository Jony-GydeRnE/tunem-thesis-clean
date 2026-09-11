#!/usr/bin/env python3
"""Brief 8 — reading psi. The mathematical map, no hardware at all."""
from sketch_base import *

fig, ax = new(h=3.9)
for i, (f, lab) in enumerate(((0.35, "$\\psi_1$"), (0.65, "$\\psi_2$"),
                              (0.95, "$\\psi_3$"))):
    R, Z = shaped_boundary(a=f, kappa=1.55, delta=0.32)
    ax.plot(R, Z, color=PALETTE["bfield"], lw=1.5 + 0.3 * i,
            ls=LS["bfield"], zorder=4)
    ax.text(f * 0.62, 1.55 * f * 0.80, lab, fontsize=10,
            color=PALETTE["bfield"], ha="center", va="center", zorder=6,
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))
ax.plot([0], [0], marker="o", ms=5, color=PALETTE["bfield"], zorder=6)
ax.text(-0.30, -0.10, "magnetic axis", fontsize=8, ha="right", va="top",
        color=PALETTE["bfield"])

# B_p tangent to the surfaces
R, Z = shaped_boundary(a=0.65, kappa=1.55, delta=0.32, n=400)
for j in (30, 130, 250, 340):
    p0 = (R[j], Z[j]); p1 = (R[j + 12], Z[j + 12])
    arrow(ax, p0, p1, color=PALETTE["bfield"], lw=2.0)
ax.text(-0.95, 0.62, "$\\mathbf{B}_p$ is TANGENT\nto every surface",
        fontsize=9, ha="right", va="center", color=PALETTE["bfield"])

# grad psi perpendicular
j = 200
n0 = np.array([R[j], Z[j]])
tangent = np.array([R[j + 6] - R[j - 6], Z[j + 6] - Z[j - 6]])
nrm = np.array([-tangent[1], tangent[0]]); nrm /= np.linalg.norm(nrm)
arrow(ax, tuple(n0), tuple(n0 - 0.42 * nrm), color=PALETTE["current"], lw=2.0)
ax.text(*(n0 - 0.52 * nrm), "$\\nabla\\psi$", fontsize=10,
        color=PALETTE["current"], ha="right", va="center")

# B_phi out of the page
odot(ax, 0.30, -0.55, 0.10, PALETTE["tf"])
ax.text(0.46, -0.55, "$B_\\varphi$ out of the page\n(perpendicular to $\\nabla\\psi$ too)",
        fontsize=8.6, color=PALETTE["tf"], ha="left", va="center")

ax.text(0.0, 1.92, r"$\mathbf{B}\cdot\nabla\psi=0$", fontsize=12, ha="center",
        va="bottom", color="black")
ax.text(0.0, 1.88, "a field line can never leave its surface",
        fontsize=8.6, ha="center", va="top", color="0.3")
ax.set_xlim(-2.1, 3.1); ax.set_ylim(-1.95, 2.35)
save(fig, "figS_reading_psi",
     "Explanatory sketch. No hardware is drawn: this is the mathematical map "
     "that makes flux surfaces intelligible, not a picture of a machine.")
