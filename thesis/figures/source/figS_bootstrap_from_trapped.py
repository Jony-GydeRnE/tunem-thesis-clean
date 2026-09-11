#!/usr/bin/env python3
"""Brief 29 — from trapped particles to bootstrap current.

The brief is precise about what this figure must NOT say, and that constraint
is the design of the figure.  The net toroidal-current arrow is labelled
"incomplete cancellation", never "free current", and the pressure gradient that
drives it is drawn as an input the machine must keep paying for.

What is drawn:

  * an annular shell of a poloidal cross-section, outboard side to the right;
  * two ADJACENT banana orbits, at r and r + Delta, built from the same
    v_par(theta) construction as figS_trapped_orbit -- these are the same
    objects that figure introduced, not new cartoons;
  * the outward pressure gradient, shown as more particles on the inner orbit;
  * a collision arrow, because without collisions the imbalance stays inside
    the trapped population and never becomes a plasma current;
  * one modest net-current marker.

The mechanism in one sentence: at a given point the two adjacent bananas carry
OPPOSITE parallel velocities, so their currents nearly cancel; because dp/dr < 0
there are slightly more particles on the inner one; what survives is the
difference, and collisions hand that difference to the passing electrons.

The scaling j_bs ~ -C sqrt(eps)/B_theta dp/dr is printed with the coefficient C
left explicitly unwritten, because C is where the kinetic model enters and the
primer's own audit of the 2015 baseline turns on exactly that number.

Run:  python3 figS_bootstrap_from_trapped.py
Out:  figS_bootstrap_from_trapped.pdf / .png
"""
from sketch_base import *

W, H = TEXTWIDTH_IN, 5.55
fig, ax = canvas(W, H)

# ==========================================================================
# BAND A — the drawing (left) with leader-lined labels (right)
# ==========================================================================
R0, ZC, KAP = 1.52, 3.85, 1.12
EPS_DRAW = 0.34
COS_TB = 0.45

def banana(r, amp, n=900):
    """Same construction as figS_trapped_orbit: the orbit IS v_par(theta)."""
    lam = (1.0 + COS_TB * EPS_DRAW) / (1.0 + EPS_DRAW)
    th = np.linspace(-np.pi, np.pi, n)
    Bn = 1.0 / (1.0 + EPS_DRAW * np.cos(th))
    Bmin = 1.0 / (1.0 + EPS_DRAW)
    s = 1.0 - lam * Bn / Bmin
    keep = s > 0
    th, vp = th[keep], np.sqrt(s[keep])
    th_c = np.concatenate([th, th[::-1]])
    dr = amp * np.concatenate([vp, -vp[::-1]])
    rr = r + dr
    return R0 + rr * np.cos(th_c), ZC + KAP * rr * np.sin(th_c)

for rr in (0.42, 0.68):
    Rf, Zf = shaped_boundary(R0=R0, a=rr, kappa=KAP)
    ax.plot(Rf, Zf + ZC, color=PALETTE["bfield"], lw=0.85, ls=LS["bfield"],
            alpha=0.45, zorder=2)
Rf, Zf = shaped_boundary(R0=R0, a=0.92, kappa=KAP)
ax.plot(Rf, Zf + ZC, color=PALETTE["plasma"], lw=1.4, zorder=2)

X1, Y1 = banana(0.50, 0.135)
X2, Y2 = banana(0.68, 0.135)
ax.plot(X1, Y1, color=PALETTE["current"], lw=1.9, zorder=7)
ax.plot(X2, Y2, color=PALETTE["cs"], lw=1.7, ls=LS["cs"], zorder=6)

# population: MORE on the inner orbit, because dp/dr < 0
for xx, yy, col, cnt in ((X1, Y1, PALETTE["current"], 5),
                         (X2, Y2, PALETTE["cs"], 3)):
    for i in (np.linspace(0.08, 0.42, cnt) * len(xx)).astype(int):
        odot(ax, xx[i], yy[i], 0.034, col, z=9)

# The pressure gradient is drawn BELOW the cross-section, not across it: an
# arrow on the midplane runs straight through both bananas and through their
# population markers, which is precisely the region the reader must compare.
arrow(ax, (0.62, 2.74), (2.32, 2.74), PALETTE["pf"], lw=1.7, z=10)
ax.text(1.47, 2.66, r"outward:  $dp/dr<0$", fontsize=8.4, ha="center",
        va="top", color=PALETTE["pf"])

# collisions, on the inboard side
COLL_Y = ZC - 0.30
arrow(ax, (R0 - 1.16, COLL_Y), (R0 - 0.70, COLL_Y), PALETTE["heat"],
      lw=1.5, ls=(0, (2.4, 1.8)), z=10)

# the surviving current, marked on the INBOARD side, which the bananas (all
# outboard, |theta| < 63 deg here) leave clear
CUR_X, CUR_Y = R0 - 0.35, ZC - 0.62
otimes(ax, CUR_X, CUR_Y, 0.075, PALETTE["vessel"])

ax.text(0.10, H - 0.14, "FROM TRAPPED PARTICLES TO A CURRENT — and why it is "
                        "not free", fontsize=10.2, ha="left", va="top",
        color=PALETTE["vessel"])

# ---- leader-lined labels, all in the right-hand column -------------------
# Anchors are picked BY HEIGHT and the labels are listed in the same vertical
# order, so no two leader lines cross.  (The first draft ordered them by
# narrative importance and produced a cat's cradle.)
def at_height(X, Y, ztarget):
    i = int(np.argmin(np.abs(Y - ztarget)))
    return float(X[i]), float(Y[i])

A1 = at_height(X1, Y1, ZC + 0.48)
A2 = at_height(X2, Y2, ZC + 0.12)
LAB = [
    (A1[0], A1[1], 4.92, PALETTE["current"],
     r"inner banana at $r$ — MORE particles, since $p$ falls outward"),
    (A2[0], A2[1], 4.42, PALETTE["cs"],
     r"outer banana at $r+\Delta$ — FEWER, and opposite $v_\parallel$"),
    (R0 - 0.72, COLL_Y, 3.62, PALETTE["heat"],
     "collisions hand the imbalance to the PASSING electrons —\n"
     "without that step it never becomes a plasma current"),
    (CUR_X, CUR_Y, 3.02, PALETTE["vessel"],
     "a MODEST net toroidal current: what SURVIVES the\n"
     "near-cancellation of two opposite banana currents"),
]
for xa, ya, ytxt, col, txt in LAB:
    ax.annotate(txt, xy=(xa, ya), xytext=(2.72, ytxt), fontsize=8.0,
                ha="left", va="center", color=col, linespacing=1.5,
                arrowprops=dict(arrowstyle="-", color=col, lw=0.8,
                                connectionstyle="arc3,rad=0.12",
                                shrinkA=2, shrinkB=4), zorder=11)

ax.plot([0.10, W - 0.10], [2.52, 2.52], color="0.85", lw=0.9, zorder=1)

# ==========================================================================
# BAND B — the chain, and the two things it must not be read as saying
# ==========================================================================
ax.text(0.10, 2.40,
        "1.  At a given point the two adjacent bananas carry OPPOSITE "
        r"$v_\parallel$, so their currents nearly cancel." "\n"
        r"2.  Because $dp/dr<0$, slightly more particles sit on the inner "
        "orbit — the cancellation is INCOMPLETE.\n"
        "3.  Collisions transfer that residue to the passing electrons. "
        "That step is what makes it a plasma current.\n"
        r"4.  Scaling:  $j_{\rm bs}\sim-\,C\,\frac{\sqrt{\varepsilon}}"
        r"{B_\theta}\,\frac{dp}{dr}$,  the $\sqrt{\varepsilon}$ inherited from "
        r"the trapped fraction $\sim\sqrt{2\varepsilon/(1+\varepsilon)}$.",
        fontsize=8.4, ha="left", va="top", color="0.22", linespacing=2.05)

ax.text(0.10, 1.24,
        "The coefficient $C$ is left unwritten ON PURPOSE. It is where the "
        "kinetic model enters — collisionality\nregime, profile shape, impurity "
        "content — and the primer's own audit of the 2015 baseline turns on\n"
        "exactly that number. Quoting one here would hide the modelling choice "
        "the audit later argues about.",
        fontsize=8.0, ha="left", va="top", color=PALETTE["pf"],
        linespacing=1.65)

ax.text(0.10, 0.62,
        "This is an INCOMPLETE CANCELLATION, not free current. It exists only "
        "while the pressure gradient is\nmaintained, and maintaining that "
        "gradient is what the heating system is for.",
        fontsize=8.0, ha="left", va="top", color=PALETTE["current"],
        linespacing=1.65)

save_exact(fig, "figS_bootstrap_from_trapped",
           "Explanatory sketch; schematic, not to scale. The banana width and "
           "the orbit separation are exaggerated for legibility.", y=0.08)
