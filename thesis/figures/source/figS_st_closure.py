#!/usr/bin/env python3
"""Brief at v1_fresh l.4787 — the two-constraint closure, conventional vs ST.

Deliberately non-engineering, as the brief demands: no magnets, no centre stack,
no HTS, no reactor hardware anywhere.  This figure answers Friedberg's PLASMA
question and nothing else.

The four ratios are computed here from the declared model inputs, not quoted:

  conventional reference     kink       q_K / q_*        = 2.00 / 1.56
                             bootstrap  f_B_req / f_B    = 0.84 / 0.44
  A = 1.7 ST model           kink       q_K,ST / q_*     = 2.80 / 3.00
                             bootstrap  (1 - f_NBI)/f_BS = 0.76 / 0.76

Every one is written demand / allowance, so ">1 is a violation" is the same
sentence in all four cells and the reader never has to remember which way a
particular limit points.

Two things this figure must not be read as saying, and both are printed on it:

  * These are DECLARED MODEL RESULTS.  The left column is one analytic model set
    at one operating point; the right column is one published finite-A study at
    one density.  Neither is a statement about tokamaks or about STs in general.
  * The right-hand bootstrap ratio is 1.00 BY CONSTRUCTION, not by measurement.
    Menard's scenarios are fully non-inductive: the paper computes total
    non-inductive current as the sum of bootstrap and NBI currents, so
    f_BS + f_NBI = 1 identically at every point of the scan (60+40 = 84+16 =
    100 at the two ends of figure 9(a)).  The ratio (1 - f_NBI)/f_BS is
    therefore exactly 1 everywhere and could not have come out otherwise.
    That is stated on the figure, because a reader who thinks it is a
    measurement will look for margin in the wrong place: the margin question is
    in P_NBI (80 MW of 0.5 MeV NNBI), not in the ratio.

Run:  python3 figS_st_closure.py
Out:  figS_st_closure.pdf / .png
"""
from sketch_base import *

# --------------------------------------------------------------------------
# declared model inputs -> the four ratios
# --------------------------------------------------------------------------
Q_STAR_CONV, Q_K_CONV = 1.56, 2.00          # conventional reference point
FB_REQ_CONV, FB_CALC_CONV = 0.84, 0.44      # required / calculated bootstrap

Q_STAR_ST, Q_K_ST = 3.00, 2.80              # A = 1.7 ST model, published scan
F_BS_ST, F_NBI_ST = 0.76, 0.24              # graph-read, approximate

R_K_CONV = Q_K_CONV / Q_STAR_CONV
R_B_CONV = FB_REQ_CONV / FB_CALC_CONV
R_K_ST = Q_K_ST / Q_STAR_ST
R_B_ST = (1.0 - F_NBI_ST) / F_BS_ST

W, H = TEXTWIDTH_IN, 6.70
fig, ax = canvas(W, H)

ax.text(W / 2, H - 0.14,
        "FRIEDBERG'S TWO OBSTRUCTIONS — one model set each side, "
        "read the same way",
        fontsize=10.4, ha="center", va="top", color=PALETTE["vessel"])
ax.text(W / 2, H - 0.38,
        r"every cell is written  DEMAND $/$ ALLOWANCE, so $>1$ means "
        "violated in all four",
        fontsize=8.4, ha="center", va="top", color="0.38")

# --------------------------------------------------------------------------
# the two columns
# --------------------------------------------------------------------------
COLS = [
    (1.62, "the conventional reference",
     r"one analytic model set, at its reference point",
     [(r"kink", r"$q_K/q_* = %.2f/%.2f$" % (Q_K_CONV, Q_STAR_CONV), R_K_CONV),
      (r"bootstrap", r"$f_{B,\rm req}/f_{\rm BS} = %.2f/%.2f$"
       % (FB_REQ_CONV, FB_CALC_CONV), R_B_CONV)]),
    (4.66, r"the $A=1.7$ ST model",
     r"one published finite-$A$ scan, near normalised density $0.8$",
     [(r"kink", r"$q_{K,\rm ST}/q_* = %.2f/%.2f$" % (Q_K_ST, Q_STAR_ST),
       R_K_ST),
      (r"bootstrap", r"$(1-f_{\rm NBI})/f_{\rm BS} = %.2f/%.2f$"
       % (1 - F_NBI_ST, F_BS_ST), R_B_ST)]),
]

BAR_W, BAR_H = 2.20, 0.34
Y0, DY = 4.72, 1.02
SCALE = 0.92                                 # bar length per unit ratio


def bar(cx, y, label, expr, r):
    fail = r > 1.0
    col = PALETTE["current"] if fail else PALETTE["cs"]
    x0 = cx - BAR_W / 2
    # the allowance line: where ratio = 1
    ax.add_patch(Rectangle((x0, y - BAR_H / 2), BAR_W, BAR_H,
                           facecolor="0.955", edgecolor="0.75", lw=0.8,
                           zorder=3))
    ax.add_patch(Rectangle((x0, y - BAR_H / 2), min(r, 1.9) * SCALE, BAR_H,
                           facecolor=col, alpha=0.34, edgecolor=col, lw=1.4,
                           zorder=4))
    ax.plot([x0 + SCALE, x0 + SCALE], [y - BAR_H / 2 - 0.09,
                                       y + BAR_H / 2 + 0.09],
            color="black", lw=1.5, zorder=6)
    ax.text(x0 + SCALE, y + BAR_H / 2 + 0.11, "$=1$", fontsize=7.6,
            ha="center", va="bottom", color="black")
    ax.text(x0 + 0.06, y + BAR_H / 2 + 0.11, label, fontsize=8.6, ha="left",
            va="bottom", color=col)
    ax.text(cx, y - BAR_H / 2 - 0.13, expr, fontsize=8.2, ha="center",
            va="top", color="0.25")
    ax.text(x0 + BAR_W + 0.10, y, r"$=%.2f$" % r, fontsize=9.4, ha="left",
            va="center", color=col)
    ax.text(x0 + BAR_W + 0.10, y - 0.20,
            "VIOLATED" if fail else ("IDENTITY"
                                     if abs(r - 1) < 0.005 else "within"),
            fontsize=7.6, ha="left", va="center", color=col)


for cx, title, sub, rows in COLS:
    ax.text(cx, 5.72, title, fontsize=10.0, ha="center", va="center",
            color=PALETTE["vessel"])
    ax.text(cx, 5.50, sub, fontsize=8.0, ha="center", va="center",
            color="0.42")
    for i, (label, expr, r) in enumerate(rows):
        bar(cx, Y0 - i * DY, label, expr, r)

ax.plot([3.16, 3.16], [3.00, 5.88], color="0.82", lw=0.9, zorder=1)
ax.plot([0.10, W - 0.10], [2.72, 2.72], color="0.85", lw=0.9, zorder=1)

# --------------------------------------------------------------------------
ax.text(0.10, 2.60,
        r"WHAT THIS DOES SAY. In the stated finite-$A$ model the kink "
        r"obstruction closes on its own terms: $q_*\geq3$ against"
        "\n"
        r"ST-specific $q_{K,\rm ST}=2.8$ gives $%.2f$, and that IS a test "
        "that could have failed. It is a model-backed existence\n"
        "result — one configuration in which the number that failed on the "
        "left does not fail." % R_K_ST,
        fontsize=8.0, ha="left", va="top", color=PALETTE["cs"],
        linespacing=1.6)

ax.text(0.10, 1.86,
        r"READ THE BOTTOM-RIGHT CELL CAREFULLY. Its $1.00$ is an IDENTITY, "
        "not a measurement. The scenarios are\n"
        r"fully non-inductive — total non-inductive current is computed as "
        r"bootstrap $+$ NBI — so $f_{\rm BS}+f_{\rm NBI}=1$ at every"
        "\n"
        r"point of the scan ($60{+}40$ and $84{+}16$ at its two ends). "
        r"$(1-f_{\rm NBI})/f_{\rm BS}$ is therefore exactly one everywhere and"
        "\ncould not have come out otherwise. The real question the right "
        "column raises is the PRICE of that closure: $80$ MW of\n"
        r"$0.5$ MeV negative-ion NBI supplying $%.2f$ of a $10.8$–$12$ MA "
        "plasma. Margin lives there, not in the ratio. And nothing\n"
        "here says every ST is stable or that this one is feasible: the "
        "centre-stack question is untouched." % F_NBI_ST,
        fontsize=8.0, ha="left", va="top", color=PALETTE["pf"],
        linespacing=1.6)

save_exact(fig, "figS_st_closure",
           "Explanatory sketch; a comparison of declared model results. No "
           "magnet, centre stack, HTS or reactor hardware\nappears: this "
           "figure answers the plasma question only.", y=0.06)
print(f"R_K conv={R_K_CONV:.4f}  R_B conv={R_B_CONV:.4f}  "
      f"R_K ST={R_K_ST:.4f}  R_B ST={R_B_ST:.4f}")
