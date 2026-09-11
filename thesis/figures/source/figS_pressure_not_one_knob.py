#!/usr/bin/env python3
"""Brief 15 — pressure is not one knob.

The brief asks for linked sliders for n, T and p = 2nT, with the Greenwald
reference, the beta limit and the Lawson requirement labelled, and it
explicitly forbids implying a precise universal operating boundary.  So:

  TOP     the linkage.  Two dials exist; the third reads out.  p is an OUTPUT.
  BOTTOM  the fan-out.  Raising n reaches three separate constraints, and NOT
          with the same sign -- two get worse, one gets better.

Deliberately NOT an (n,T) operating map with a shaded feasible region: that is
brief 19's job, and drawing one here would be exactly the "precise universal
operating boundary" the brief forbids.  No axis in this figure carries a number.

LAYOUT NOTE (learned the hard way on this project): a sketch whose content is
mostly TEXT must not use equal aspect and must not be split into two side-by-side
columns.  Font size is absolute (points) while data units are not, so an
equal-aspect panel silently shrinks until labels collide, and a half-width column
is simply too narrow for a sentence at 8 pt.  This figure uses aspect "auto",
uses canvas() so one data unit is EXACTLY one inch (72 pt), and stacks its two
claims vertically so every text box has the full text block to live in.

Run:  python3 figS_pressure_not_one_knob.py
Out:  figS_pressure_not_one_knob.pdf / .png
"""
from sketch_base import *

W, H = TEXTWIDTH_IN, 5.05
fig, ax = canvas(W, H)         # see LAYOUT NOTE above: 1 data unit = 1 inch

# ==========================================================================
# BAND A — the control panel a reactor actually has
# ==========================================================================
ax.text(W / 2, 4.87, "the control panel a reactor actually has",
        fontsize=10.0, ha="center", va="center", color=PALETTE["vessel"])

X0, TW = 1.55, 3.60
ROWS = [
    (4.43, r"density  $n$",      0.62, PALETTE["heat"],    True),
    (4.07, r"temperature  $T$",  0.46, PALETTE["current"], True),
    (3.71, r"pressure  $p=2nT$", 0.55, PALETTE["plasma"],  False),
]
for y, lab, frac, col, free in ROWS:
    ax.add_patch(FancyBboxPatch((X0, y - 0.035), TW, 0.07,
                                boxstyle="round,pad=0.006", facecolor="0.92",
                                edgecolor="0.60", linewidth=0.8, zorder=3))
    hx = X0 + frac * TW
    ax.add_patch(FancyBboxPatch((hx - 0.042, y - 0.105), 0.084, 0.21,
                                boxstyle="round,pad=0.006",
                                facecolor="white" if free else col,
                                edgecolor=col, linewidth=1.8, zorder=7))
    ax.text(X0 - 0.12, y, lab, fontsize=8.8, ha="right", va="center",
            color=col)
    ax.text(X0 + TW + 0.12, y,
            "you may set this" if free else "you may NOT set this",
            fontsize=7.8, ha="left", va="center",
            color="0.45" if free else PALETTE["plasma"])

# the linkage: the two dials drive the readout.  Routed down the side so the
# arrows never cross a slider label.
for y, frac in ((4.43, 0.62), (4.07, 0.46)):
    hx = X0 + frac * TW
    ax.plot([hx, hx, X0 + 0.55 * TW], [y - 0.12, 3.55, 3.55],
            color=PALETTE["plasma"], lw=1.0, ls=(0, (3.0, 2.0)), zorder=4)
arrow(ax, (X0 + 0.55 * TW, 3.55), (X0 + 0.55 * TW, 3.61),
      color=PALETTE["plasma"], lw=1.0, z=5)

ax.text(W / 2, 3.41, "$p$ is an OUTPUT of the two dials above — there is no "
                     "third dial on this panel.",
        fontsize=8.8, ha="center", va="top", color=PALETTE["plasma"])

ax.plot([0.55, W - 0.55], [3.15, 3.15], color="0.82", lw=0.9, zorder=1)

# ==========================================================================
# BAND B — and n is not a private dial either
# ==========================================================================
ax.text(W / 2, 2.95, "and $n$ is not a private dial either",
        fontsize=10.0, ha="center", va="center", color=PALETTE["vessel"])

node(ax, W / 2, 2.57, 0.92, 0.28, r"raise $n$", "chosen", fs=9.2)

TARGETS = [
    (1.24, PALETTE["heat"], "empirical",
     "Greenwald density reference\n"
     r"$n_e \lesssim n_G$" "\n"
     "moves TOWARD the limit"),
    (3.43, PALETTE["pf"], "empirical",
     r"$\beta$ / MHD margin" "\n"
     r"entered through $p=2nT$" "\n"
     "moves TOWARD the limit"),
    (5.62, PALETTE["cs"], "derived",
     "Lawson self-heating\n"
     r"$n_i\tau_E \geq 12T/\langle\sigma v\rangle E_\alpha$" "\n"
     "moves AWAY from failure"),
]
for x, col, kind, txt in TARGETS:
    node(ax, x, 1.77, 2.05, 0.86, txt, kind, fs=7.9)
    flow(ax, (W / 2, 2.41), (x, 2.13), color=col, lw=1.5,
         rad=0.0 if abs(x - W / 2) < 0.05 else (0.16 if x < W / 2 else -0.16))

# Line lengths below are budgeted, not guessed: canvas() gives 6.86 in of
# usable width, and Computer Modern at f pt averages ~0.5 f pt per glyph, so
# ~115 characters is the ceiling at 8 pt.  Overflow would CLIP, visibly.
ax.text(W / 2, 1.14,
        "Two of the three are $\\lesssim$, not $=$ — empirical or "
        "model-dependent margins. Only the third is derived.",
        fontsize=8.0, ha="center", va="top", color=PALETTE["pf"])

ax.text(W / 2, 0.86,
        "The design question is therefore not \"what is the right pressure?\" "
        "but \"which $(n,T)$ pair satisfies all three\n"
        "at once?\" — and the three do not share an optimum. No numerical axis "
        "is drawn here on purpose: there is no\n"
        "universal $(n,T)$ boundary to draw. §41 turns this into an "
        "intersection problem.",
        fontsize=8.2, ha="center", va="top", color="0.28", linespacing=1.5)

save_exact(fig, "figS_pressure_not_one_knob",
           "Explanatory sketch; schematic, not to scale. Slider positions are "
           "illustrative and carry no numerical value.")
