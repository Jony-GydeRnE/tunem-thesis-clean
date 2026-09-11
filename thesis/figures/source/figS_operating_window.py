#!/usr/bin/env python3
"""Brief 19 — the ordinary tokamak operating window.

The brief is explicit: a SCHEMATIC, clearly labelled overlap diagram, NOT a
numerically calibrated plot; five boundaries corresponding to Eqs. (77)-(81) of
the primer; one small shaded feasible region; and a printed warning that the
picture is conceptual until a named confinement scaling, stability model and
profile model are supplied.

Two decisions worth defending:

1. THE AXES CARRY NO UNITS AND NO NUMBERS.  Every honest candidate for a real
   pair of axes (n vs T, beta vs q, ...) fails, because the five conditions do
   not live in a common two-dimensional space: q_* and the current ledger do not
   depend on (n,T) alone.  Drawing them there would be a lie of convenience.
   So the axes are two schematic design coordinates and are labelled as such.
   The boundary POSITIONS are arbitrary; the TOPOLOGY -- four half-spaces whose
   intersection is small and bounded -- is the content.

2. THE FIFTH CONDITION IS DRAWN DIFFERENTLY.  Eqs. (77)-(80) are inequalities
   and bound a region.  Eq. (81), I_p = I_ohm + I_CD + I_bs, is an EQUALITY: it
   is a surface, not a half-space.  Shading a region with it would misrepresent
   what the primer says one line below it.  So it is drawn as a line the
   operating point must lie ON, and the admissible part of that line -- the bit
   inside the shaded set -- is what is actually available.

Run:  python3 figS_operating_window.py
Out:  figS_operating_window.pdf / .png
"""
import numpy as np
import matplotlib.pyplot as plt

from tokamak_build import PALETTE, LS
from sketch_base import TEXTWIDTH_IN

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm",
                     "font.size": 10, "axes.linewidth": 0.9})

# --------------------------------------------------------------------------
# four inequalities, in schematic coordinates (u, v).  ARBITRARY POSITIONS.
# --------------------------------------------------------------------------
# Chosen so the four inequalities actually CLOSE a bounded region -- four
# half-spaces in the plane need not, and an unbounded "window" running off the
# axis frame would be an artefact of the frame, not a result.  Here the upper
# (beta) and lower (Lawson) boundaries pinch shut on the left at u = 0.07, and
# Greenwald closes the right.
def v_kink(u):      return 2.30 - 1.60 * u        # q_* > q_K        (77)
def v_beta(u):      return 1.55 - 0.30 * u        # beta <= beta_max (78)
U_GREENWALD = 0.74                                # n_e <= n_G       (79)
def v_lawson(u):    return 1.62 - 1.30 * u        # n tau >= ...     (80)
def v_ledger(u):    return 1.55 - 0.62 * u        # I_p = sum   (81), EQUALITY

U = np.linspace(0.0, 1.05, 900)
V = np.linspace(0.35, 1.95, 900)
UU, VV = np.meshgrid(U, V)
feasible = ((VV <= v_kink(UU)) & (VV <= v_beta(UU)) &
            (UU <= U_GREENWALD) & (VV >= v_lawson(UU)))

fig, ax = plt.subplots(figsize=(TEXTWIDTH_IN, 4.55))

ax.contourf(UU, VV, feasible.astype(float), levels=[0.5, 1.5],
            colors=[PALETTE["cs"]], alpha=0.20, zorder=1)
ax.contour(UU, VV, feasible.astype(float), levels=[0.5],
           colors=[PALETTE["cs"]], linewidths=1.1, zorder=2)

BOUNDS = [
    (v_kink,   None, PALETTE["current"], "solid",
     r"(77)  $q_*>q_K$   kink margin",                    "below"),
    (v_beta,   None, PALETTE["pf"], LS["pf"],
     r"(78)  $\beta\lesssim\beta_{N,\max}I_p/aB_0$",      "below"),
    (None, U_GREENWALD, PALETTE["heat"], LS["heat"],
     r"(79)  $n_e\lesssim n_G$",                          "left"),
    (v_lawson, None, PALETTE["bfield"], LS["bfield"],
     r"(80)  $n_i\tau_E\geq 12T/\langle\sigma v\rangle E_\alpha$", "above"),
]
for f, uconst, col, ls, lab, side in BOUNDS:
    if uconst is None:
        ax.plot(U, f(U), color=col, ls=ls, lw=1.9, zorder=4, label=lab)
    else:
        ax.plot([uconst, uconst], [V[0], V[-1]], color=col, ls=ls, lw=1.9,
                zorder=4, label=lab)

# hatch the forbidden side of each, lightly, so "which way is out" is visible
ax.fill_between(U, v_kink(U), V[-1], color=PALETTE["current"], alpha=0.06, lw=0)
ax.fill_between(U, v_beta(U), V[-1], color=PALETTE["pf"], alpha=0.06, lw=0)
ax.fill_between(U, V[0], v_lawson(U), color=PALETTE["bfield"], alpha=0.06, lw=0)
ax.axvspan(U_GREENWALD, U[-1], color=PALETTE["heat"], alpha=0.06, lw=0)

# --------------------------------------------------------------------------
# the fifth condition: an EQUALITY, so a curve and not a region
# --------------------------------------------------------------------------
ax.plot(U, v_ledger(U), color=PALETTE["vessel"], lw=1.6, ls=(0, (1.2, 1.9)),
        zorder=5, label=r"(81)  $I_p=I_{\rm ohm}+I_{\rm CD}+I_{\rm bs}$"
                        "  (equality)")
# evaluate the four inequalities ON the ledger line -- exactly, not by looking
# the line up in the rasterised mask
VL = v_ledger(U)
on = ((VL <= v_kink(U)) & (VL <= v_beta(U)) &
      (U <= U_GREENWALD) & (VL >= v_lawson(U)))
ax.plot(np.where(on, U, np.nan), np.where(on, v_ledger(U), np.nan),
        color=PALETTE["vessel"], lw=4.0, alpha=0.55, zorder=6,
        solid_capstyle="butt")

u_mid = U[on][len(U[on]) // 2] if on.any() else 0.4
ax.annotate("the operating point must lie ON this line\n"
            "AND inside the shaded set — that segment,\n"
            "not the whole region, is what is available",
            xy=(u_mid, v_ledger(u_mid)), xytext=(1.02, 1.90),
            fontsize=8.4, ha="right", va="top", color=PALETTE["vessel"],
            linespacing=1.45,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor="none", alpha=0.88),
            arrowprops=dict(arrowstyle="-|>", color=PALETTE["vessel"], lw=1.0),
            zorder=8)

ax.text(0.545, 1.02, "feasible", fontsize=9.4, ha="center",
        color=PALETTE["cs"], zorder=7)

# --------------------------------------------------------------------------
ax.set_xlim(U[0], U[-1])
ax.set_ylim(V[0], V[-1])
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("schematic design coordinate 1   (no units, no numbers)")
ax.set_ylabel("schematic design coordinate 2")
ax.set_title("THE OPERATING POINT IS AN INTERSECTION, NOT A TARGET NUMBER",
             fontsize=10.6, pad=9)
ax.legend(frameon=True, framealpha=0.88, edgecolor="none",
          fontsize=8.2, loc="lower left", handlelength=2.6,
          labelspacing=0.55)

fig.text(0.5, 0.115,
         "CONCEPTUAL. The axes are two schematic design coordinates, not "
         "physical variables, and no boundary position here is calibrated.\n"
         "The five conditions do not share a common two-dimensional space — "
         r"$q_*$ and the ledger are not functions of $(n,T)$ — so plotting them"
         "\non real axes would be a lie of convenience. What IS asserted is the "
         "topology: four inequalities bound a small region, and the fifth is an\n"
         "equality inside it. The picture stays conceptual until a NAMED "
         "confinement scaling, stability model and profile model are supplied.",
         fontsize=7.7, ha="center", va="top", color="0.32", linespacing=1.55)

fig.tight_layout(rect=(0, 0.235, 1, 1))
fig.savefig("figS_operating_window.pdf", bbox_inches="tight")
fig.savefig("figS_operating_window.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("wrote figS_operating_window.pdf/.png")
