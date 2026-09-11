#!/usr/bin/env python3
"""Brief 23 — why the inboard build limits the central field.

A horizontal midplane cut, with the brackets the primer defines:

    R_in = R0 - a - b - c                                        Eq. (88)
    B_max = B0 R0 / (R0 - a - b - c)                             Eq. (89)
    B0    = B_max ( 1 - (a+b+c)/R0 )                             Eq. (90)

The brief asks for "toroidal-field arrows with increasing density inward".
This figure does something stronger and cheaper to defend: the TOP panel plots
B(R) = B0 R0 / R as an actual curve, so "increasing inward" is a computed
hyperbola rather than a hand-spaced set of arrows, and B_max is read off the
curve at R_in rather than asserted.  The arrow row is kept underneath as the
visual cue the brief asked for, with arrow SPACING taken from the same 1/R.

The numbers a, b, c below are ILLUSTRATIVE and labelled as such on the figure:
b is not derived until the nuclear island section and c not until the coil
stress section.  What is NOT illustrative is the arithmetic between them --
that is Eq. (89) evaluated, printed with its inputs.

Run:  python3 figS_inboard_build.py
Out:  figS_inboard_build.pdf / .png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

from tokamak_build import PALETTE, HATCH
from sketch_base import TEXTWIDTH_IN

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm",
                     "font.size": 10, "axes.linewidth": 0.9})

# --------------------------------------------------------------------------
# geometry.  ILLUSTRATIVE values, chosen only so the brackets are legible.
# --------------------------------------------------------------------------
R0, a, b, c = 3.00, 1.00, 0.50, 0.40
R_IN = R0 - a - b - c
B0 = 1.0                                     # everything normalised to B0
B_MAX = B0 * R0 / R_IN                       # Eq. (89)
assert abs(B0 - B_MAX * (1 - (a + b + c) / R0)) < 1e-12   # Eq. (90) is the same

fig, (axB, axG) = plt.subplots(
    2, 1, figsize=(TEXTWIDTH_IN, 6.15), sharex=True,
    gridspec_kw=dict(height_ratios=[1.35, 1.0], hspace=0.10))

R = np.linspace(R_IN * 0.92, R0 + a + 0.55, 900)

# ==========================================================================
# TOP — B(R) = B0 R0 / R, the whole reason the build matters
# ==========================================================================
axB.plot(R, B0 * R0 / R, color=PALETTE["tf"], lw=2.0, zorder=5)
axB.axhline(B0, color="0.55", lw=0.9, ls=(0, (4, 3)), zorder=3)
axB.axhline(B_MAX, color=PALETTE["current"], lw=0.9, ls=(0, (4, 3)), zorder=3)

for x, lab, col in ((R_IN, r"$R_{\rm in}$", PALETTE["current"]),
                    (R0 - a, r"$R_0-a$", "0.45"),
                    (R0, r"$R_0$", PALETTE["plasma"])):
    axB.axvline(x, color=col, lw=0.9, ls=(0, (1.4, 2.0)), zorder=2)

axB.plot([R_IN], [B_MAX], marker="o", ms=7, mfc="white",
         mec=PALETTE["current"], mew=1.8, zorder=7)
axB.annotate(r"$B_{\max}=\dfrac{B_0R_0}{R_0-a-b-c}=%.2f\,B_0$" % B_MAX,
             xy=(R_IN, B_MAX), xytext=(R_IN + 0.42, B_MAX + 0.28),
             fontsize=9.4, color=PALETTE["current"], ha="left",
             arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                             lw=1.0), zorder=8)
axB.text(R0 + a + 0.50, B0 + 0.06, r"$B_0$  (on axis)", fontsize=8.8,
         ha="right", va="bottom", color="0.35")
axB.text(R_IN * 0.94, 0.35, r"$B_\varphi(R)=B_0R_0/R$", fontsize=9.6,
         ha="left", va="bottom", color=PALETTE["tf"])

axB.set_ylim(0.0, B_MAX + 1.05)
axB.set_ylabel(r"toroidal field   $B_\varphi / B_0$")
axB.grid(True, color="0.91", lw=0.6)
axB.set_axisbelow(True)
axB.set_title("THE INBOARD BUILD SETS THE FIELD: every millimetre inboard is "
              "spent twice", fontsize=10.4, pad=9)

# ==========================================================================
# BOTTOM — the radial build itself, with the brackets the primer names
# ==========================================================================
BANDS = [
    (R_IN, c, PALETTE["tf"], HATCH.get("shield", "...."), r"$c$" "\n"
     "TF coil", 0.30),
    (R_IN + c, b, PALETTE["blanket"], HATCH.get("blanket", "////"), r"$b$" "\n"
     "nuclear\nisland", 0.30),
    (R0 - a, a, PALETTE["plasma"], None, r"$a$" "\n" "plasma", 0.16),
]
for x0, wdt, col, hat, lab, alp in BANDS:
    axG.add_patch(Rectangle((x0, 0.18), wdt, 0.62, facecolor=col, alpha=alp,
                            edgecolor=col, hatch=hat, lw=1.2, zorder=4))
    axG.annotate("", xy=(x0, 0.90), xytext=(x0 + wdt, 0.90),
                 arrowprops=dict(arrowstyle="<->", color=col, lw=1.2))
    axG.text(x0 + wdt / 2, 0.49, lab, fontsize=7.9, ha="center", va="center",
             color="black", linespacing=1.4, zorder=6)

axG.plot([R0, R0], [0.18, 0.80], color=PALETTE["plasma"], lw=1.2,
         ls=(0, (1.4, 2.0)), zorder=6)
axG.annotate("", xy=(R_IN, 1.16), xytext=(R0, 1.16),
             arrowprops=dict(arrowstyle="<->", color=PALETTE["vessel"], lw=1.4))
axG.text((R_IN + R0) / 2, 1.22, r"$a+b+c$   —   everything between the machine "
                                r"axis and the plasma centre",
         fontsize=8.4, ha="center", va="bottom", color=PALETTE["vessel"])
axG.text(R_IN, 0.04, r"$R_{\rm in}=R_0-a-b-c=%.2f$ m" % R_IN, fontsize=8.8,
         ha="center", va="top", color=PALETTE["current"])
axG.text(R0, 0.04, r"$R_0=%.2f$ m" % R0, fontsize=8.8, ha="center", va="top",
         color=PALETTE["plasma"])

# the arrow row the brief asked for: SPACING taken from the same 1/R law, so
# "denser inward" is computed rather than eyeballed.
# cumulative 1/R spacing: put a marker wherever the integral of B has advanced
# by a fixed step.
Rg = np.linspace(R_IN, R0 + a + 0.4, 4000)
S = np.cumsum(1.0 / Rg)
S = (S - S[0]) / (S[-1] - S[0])
for frac in np.linspace(0.02, 0.98, 16):
    xr = float(np.interp(frac, S, Rg))
    axG.annotate("", xy=(xr, -0.66), xytext=(xr, -0.46),
                 arrowprops=dict(arrowstyle="-|>", color=PALETTE["tf"],
                                 lw=1.0))
axG.text(R0 + a + 0.5, -0.20, "arrow spacing follows the same $1/R$: "
                              "denser inward", fontsize=8.0, ha="right",
         va="top", color=PALETTE["tf"])

axG.set_ylim(-0.95, 1.55)
axG.set_yticks([])
axG.set_xlabel(r"major radius  $R$   [m]     (machine axis is at $R=0$, "
               "off the left of this cut)", labelpad=7)
axG.set_xlim(R.min(), R.max())
for s in ("left", "right", "top"):
    axG.spines[s].set_visible(False)

# ==========================================================================
fig.subplots_adjust(left=0.105, right=0.985, top=0.935, bottom=0.315,
                    hspace=0.10)

fig.text(0.5, 0.212,
         r"Rearranged, Eq. (90): $B_0=B_{\max}\left(1-(a{+}b{+}c)/R_0\right)$ "
         r"$=%.2f\times(1-%.2f/%.2f)=%.2f\,B_0$ — the identity, evaluated."
         "\nThe consequence is the one the primer draws out: at a FIXED "
         r"material limit $B_{\max}$, a larger plasma, a thicker nuclear island"
         "\nor a thicker coil each reduce the attainable $B_0$. The three "
         "compete for the same inboard radius, and none of them is free.\n"
         r"$a$, $b$, $c$ here are ILLUSTRATIVE: $b$ is not derived until the "
         r"nuclear-island section and $c$ not until the coil-stress section."
         % (B_MAX, a + b + c, R0, B_MAX * (1 - (a + b + c) / R0)),
         fontsize=7.8, ha="center", va="top", color="0.30", linespacing=1.55)

fig.savefig("figS_inboard_build.pdf", bbox_inches=None)
fig.savefig("figS_inboard_build.png", dpi=180, bbox_inches=None)
plt.close(fig)
print(f"R_in = {R_IN:.3f} m, B_max/B0 = {B_MAX:.4f}")
print("wrote figS_inboard_build.pdf/.png")
