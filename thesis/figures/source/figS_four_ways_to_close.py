#!/usr/bin/env python3
"""Brief at v1_fresh l.4388 — four ways to move the same current closure.

One compact causal map.  A central block holds the quantity everything else is
trying to move: the plasma current REQUIRED BY THE EMPIRICAL CONFINEMENT FIT.
Four branches arrive at it, and the brief's real demand is that each branch
carries a DISTINCT EXPORTED BURDEN -- because the four are usually presented as
four options and they are not: they are four different places to put the same
difficulty.

Two labelling rules from the brief, both load-bearing:

  * H = 1.26 is marked as a BETA FAILURE, not a closure.  Raising the
    confinement multiplier until the current requirement falls does close the
    current ledger, and then the pressure it implies violates the beta limit.
    Drawing it as a success would be the exact error the primer is written
    against.
  * The other three are marked as four-ratio closure ONLY WITHIN THE STATED
    2015 MODELS.  They are not results about tokamaks.

This is a reset causal graphic.  It is not a new machine drawing, and it does
not import the machine model.

Run:  python3 figS_four_ways_to_close.py
Out:  figS_four_ways_to_close.pdf / .png
"""
from sketch_base import *

W, H = TEXTWIDTH_IN, 6.05
fig, ax = canvas(W, H)

ax.text(W / 2, H - 0.14,
        "FOUR WAYS TO MOVE THE SAME NUMBER — and where each one puts the cost",
        fontsize=10.4, ha="center", va="top", color=PALETTE["vessel"])

# ---- the thing all four are trying to move -------------------------------
CX, CY = 1.02, 3.10
node(ax, CX, CY, 1.78, 0.86,
     "REQUIRED\nplasma current $I$\n"
     r"from the empirical" "\n" r"confinement fit",
     "empirical", fs=8.6)
ax.text(CX, CY - 0.56, "everything below is an attempt\nto make THIS number "
                       "smaller", fontsize=8.0, ha="center", va="top",
        color="0.38", linespacing=1.5)

# ---- the four branches ---------------------------------------------------
BR = [
    (4.62, r"$H\uparrow$", PALETTE["current"], "fail",
     "raise the confinement multiplier",
     "EXPORTS: an assumption about transport that\n"
     "no component supplies. And at $H=1.26$ the\n"
     r"implied pressure fails the $\beta$ limit —"  "\n"
     "the current ledger closes, the machine does not."),
    (3.66, r"$B_{\max}\uparrow$", PALETTE["tf"], "primary",
     "raise the field",
     "EXPORTS: a conductor technology requirement\n"
     "and a structural load. The case still has to\n"
     r"hold $p_B=B^2/2\mu_0$; HTS does not remove it."),
    (2.70, r"$P_E\uparrow$", PALETTE["cs"], "chosen",
     r"bigger plant, fixed $W_n$",
     "EXPORTS: capital scale. The plasma is not\n"
     r"easier — $p$ is unchanged (see the scaling"  "\n"
     "sketch); only the plant is larger."),
    (1.74, r"$W_n\downarrow$", PALETTE["pf"], "chosen",
     r"lower wall loading, fixed $P_E$",
     "EXPORTS: volume, inboard. More blanket, more\n"
     "shield, more coil — all competing for the\n"
     r"radius $R_{\rm in}=R_0-a-b-c$ that is already full."),
]

for y, sym, col, kind, what, burden in BR:
    node(ax, 2.58, y, 0.78, 0.34, sym, kind, fs=9.6)
    ax.text(2.58, y - 0.24, what, fontsize=7.4, ha="center", va="top",
            color=col)
    ax.text(3.14, y + 0.20, burden, fontsize=7.8, ha="left", va="top",
            color=col, linespacing=1.55)
    flow(ax, (2.17, y), (CX + 0.92, CY + (y - CY) * 0.30), color=col, lw=1.5,
         rad=0.10 if y > CY else -0.10)

# ---- the two things the figure refuses to blur ---------------------------
ax.plot([0.10, W - 0.10], [1.24, 1.24], color="0.85", lw=0.9, zorder=1)
ax.text(0.10, 1.12,
        r"Only the top branch is marked as a FAILURE. $H=1.26$ closes the "
        r"current ledger and then violates the $\beta$ limit — it is"
        "\nnot a fourth option, it is the same difficulty moved where the "
        "ledger cannot see it. The other three DO close the four\n"
        "ratios, but only inside the stated 2015 model set, whose confinement "
        "fit, stability threshold, coil build and bootstrap\n"
        "coefficient are each a modelling choice. None of the four is a result "
        "about tokamaks — all four are results about that\n"
        "model set, and each hands its cost to a different engineer.",
        fontsize=7.9, ha="left", va="top", color="0.30", linespacing=1.6)

kind_legend(ax, 0.12, 5.62, ["empirical", "primary", "chosen", "fail"],
            fs=7.8, dx=1.62)

save_exact(fig, "figS_four_ways_to_close",
           "Explanatory sketch; a causal map, not a machine drawing. Branch "
           "positions carry no ordering.", y=0.06)
