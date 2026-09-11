#!/usr/bin/env python3
"""Briefs at v1_fresh l.4066 and l.4250, built as ONE figure.

Both briefs ask for the same drawing: "two conventional torus silhouettes",
differing only in which quantity is held fixed.  Building them separately puts
the same picture on two pages and makes the reader compare across a gap.  Under
the standing rule that redundancy is an error to be FIXED rather than expanded,
they are merged into two rows of one figure, which is also the only arrangement
in which the two chains can actually be compared.  The paired layout makes the comparison explicit.

  ROW A  (l.4066)  fixed wall loading W_n.   P_E up => R0 a up => V up, and
                   P_E ~ p^2 V leaves p unchanged at fixed a.
  ROW B  (l.4250)  fixed electrical power P_E.   W_n down => V up => p, n down,
                   and the exported cost is more blanket, shield and coil volume.

NOTHING on this figure is asserted.  With V = 2 pi^2 R0 a^2 and
A_w = 4 pi^2 R0 a, every ratio printed is computed from the two radii:

  Row A: fixed W_n means P_n ~ A_w ~ R0, so P_E ~ R0 and V ~ R0, hence
         p ~ sqrt(P_E / V) is EXACTLY unchanged.  That is the brief's claim,
         and it is an identity, not an estimate.
  Row B: fixed P_E with V ~ R0 gives p ~ R0^(-1/2), and W_n ~ 1/R0.

This is a reset SCALING sketch. It is not a claim that large plants are
economical, and it is not a cumulative machine state.

Run:  python3 figS_scale_two_ways.py
Out:  figS_scale_two_ways.pdf / .png
"""
from sketch_base import *

# --------------------------------------------------------------------------
# the arithmetic
# --------------------------------------------------------------------------
R1, R2, AA = 1.00, 1.50, 0.34          # major radii (ratio is what matters)
f = R2 / R1
V_ratio = f                            # V = 2 pi^2 R0 a^2, a fixed
Aw_ratio = f                           # A_w = 4 pi^2 R0 a, a fixed
pA_ratio = np.sqrt(f / V_ratio)        # row A: P_E ~ f, so p ~ sqrt(f/V) = 1
pB_ratio = np.sqrt(1.0 / V_ratio)      # row B: P_E fixed
WnB_ratio = 1.0 / Aw_ratio             # row B: same neutron power, more wall

W, H = TEXTWIDTH_IN, 6.28
fig, ax = canvas(W, H)

SC = 0.32                              # drawing scale, inches per unit radius


def torus(cx, cy, R0, a, shade, lab_R0=True, tag=""):
    """Plan view: the annulus the first wall actually is."""
    th = np.linspace(0, 2 * np.pi, 400)
    for r, lw, col in ((R0 + a, 1.5, PALETTE["wall"]),
                       (R0 - a, 1.5, PALETTE["wall"])):
        ax.plot(cx + SC * r * np.cos(th), cy + SC * r * np.sin(th),
                color=col, lw=lw, zorder=5)
    ax.fill(np.concatenate([cx + SC * (R0 + a) * np.cos(th),
                            (cx + SC * (R0 - a) * np.cos(th))[::-1]]),
            np.concatenate([cy + SC * (R0 + a) * np.sin(th),
                            (cy + SC * (R0 - a) * np.sin(th))[::-1]]),
            color=PALETTE["plasma"], alpha=shade, lw=0, zorder=3)
    ax.plot(cx + SC * R0 * np.cos(th), cy + SC * R0 * np.sin(th),
            color=PALETTE["plasma"], lw=0.9, ls=(0, (3, 3)), zorder=6)
    arrow(ax, (cx, cy), (cx + SC * R0, cy), PALETTE["vessel"], lw=1.1, z=7)
    if lab_R0:
        ax.text(cx + 0.5 * SC * R0, cy + 0.05, r"$R_0$", fontsize=8.6,
                ha="center", va="bottom", color=PALETTE["vessel"], zorder=8)
    ax.text(cx, cy - SC * (R0 + a) - 0.12, tag, fontsize=8.2, ha="center",
            va="top", color="0.25", linespacing=1.5)


# ==========================================================================
ax.text(W / 2, H - 0.14, "TWO WAYS TO GROW THE SAME MACHINE — and what each "
                         "one exports", fontsize=10.4, ha="center", va="top",
        color=PALETTE["vessel"])

# ---- ROW A ---------------------------------------------------------------
yA = 4.75
ax.text(0.10, 5.67, r"A.  fixed wall loading $W_n$ — the plant gets bigger "
                    r"because $P_E$ did", fontsize=9.6, ha="left", va="top",
        color=PALETTE["cs"])
torus(0.98, yA, R1, AA, 0.30, tag="reference")
torus(2.60, yA, R2, AA, 0.30,
      tag=r"$R_0\times%.2f$,  wall area $\times%.2f$,  $P_E\times%.2f$"
          % (f, Aw_ratio, f))
ax.text(3.78, yA + 0.72,
        r"$P_E\uparrow \Rightarrow R_0a\uparrow \Rightarrow V\uparrow$" "\n"
        r"$P_E \propto p^2V$, and $V$ grew by the" "\n"
        r"same factor, so at fixed $a$:" "\n"
        r"      $p \times %.2f$  —  UNCHANGED" % pA_ratio,
        fontsize=8.4, ha="left", va="top", color="0.22", linespacing=1.75)
ax.text(3.78, yA - 0.52,
        "Exported: capital scale — nothing about\nthe plasma itself got any easier.",
        fontsize=8.2, ha="left", va="top", color=PALETTE["pf"],
        linespacing=1.55)

ax.plot([0.10, W - 0.10], [3.25, 3.25], color="0.85", lw=0.9, zorder=1)

# ---- ROW B ---------------------------------------------------------------
yB = 2.13
ax.text(0.10, 3.13, r"B.  fixed $P_E$, lower $W_n$ — the plant gets bigger to "
                    "spread the SAME neutron power", fontsize=9.6, ha="left",
        va="top", color=PALETTE["cs"])
torus(0.98, yB, R1, AA, 0.30, tag="reference")
torus(2.60, yB, R2, AA, 0.30 * pB_ratio,
      tag=r"$R_0\times%.2f$,  $W_n\times%.2f$,  $p,n\times%.2f$"
          % (f, WnB_ratio, pB_ratio))
ax.text(3.78, yB + 0.72,
        r"$W_n\downarrow \Rightarrow V\uparrow \Rightarrow p,\,n\downarrow$"
        "\n"
        r"same $P_E$ over $\times%.2f$ the volume:" "\n"
        r"      $p \times %.2f$,   $W_n \times %.2f$" % (V_ratio, pB_ratio,
                                                         WnB_ratio),
        fontsize=8.4, ha="left", va="top", color="0.22", linespacing=1.75)
ax.text(3.78, yB - 0.42,
        "Exported, and not small: MORE blanket,\nMORE shield, MORE TF-coil volume — all\ncompeting for the inboard radius §46\nalready showed is full.",
        fontsize=8.2, ha="left", va="top", color=PALETTE["current"],
        linespacing=1.55)

# ==========================================================================
ax.text(W / 2, 0.86,
        "Both rows are the SAME drawing with a different quantity held "
        "fixed — which is why they are one figure, not two.\n"
        r"Every ratio is computed from $V=2\pi^2R_0a^2$ and $A_w=4\pi^2R_0a$ "
        r"at fixed $a$; none is estimated. Row A's" "\n"
        r"''$p$ unchanged'' is an identity, not an approximation. A scaling "
        "sketch only: it says nothing about economics.",
        fontsize=8.0, ha="center", va="top", color="0.30", linespacing=1.6)

save_exact(fig, "figS_scale_two_ways",
           "Explanatory sketch; schematic, not to scale. Plan view: the "
           "annulus is the first wall, its shading the pressure.\n"
           "Not a cumulative machine state.", y=0.06)
print(f"f = {f:.3f}  V x{V_ratio:.3f}  A_w x{Aw_ratio:.3f}  "
      f"pA x{pA_ratio:.4f}  pB x{pB_ratio:.4f}  WnB x{WnB_ratio:.4f}")
