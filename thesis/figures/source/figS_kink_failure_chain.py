#!/usr/bin/env python3
"""Brief 28 — why the kink ratio exceeds one."""
from sketch_base import *

fig, ax = new(h=2.5)
xs = [0.75, 2.25, 3.75, 5.25, 6.75]
labs = [("$P_E,\\ W_n$", "chosen"), ("$\\bar p,\\ V$", "derived"),
        ("$\\tau_{E,\\rm req}$", "derived"), ("$I_{\\rm req}$", "primary"),
        ("$q_*$", "primary")]
for x, (t, k) in zip(xs, labs):
    node(ax, x, 1.45, 1.15, 0.42, t, k)
for x0, x1 in zip(xs[:-1], xs[1:]):
    flow(ax, (x0 + 0.60, 1.45), (x1 - 0.60, 1.45))

node(ax, 6.75, 0.45, 1.9, 0.50,
     "$\\mathcal{R}_K=\\dfrac{q_K}{q_*}=\\dfrac{2}{1.56}=1.28>1$", "fail", fs=9)
flow(ax, (6.75, 1.22), (6.75, 0.72), color=PALETTE["current"], lw=1.8)

ax.text(6.75, 0.10, "REFERENCE-MODEL FAILURE", fontsize=9, ha="center",
        va="top", color=PALETTE["current"], weight="bold")
ax.text(3.2, 0.45, "$q_K\\simeq2$ is a stability-MODEL input:\n"
                   "it depends on the current profile and on\n"
                   "the conducting wall. It is not a theorem.",
        fontsize=8, ha="center", va="center", color=PALETTE["pf"])
kind_legend(ax, 0.35, -0.42, ["chosen", "primary", "derived", "fail"], dx=1.85)
ax.set_xlim(0, 7.9); ax.set_ylim(-0.70, 1.95)
save(fig, "figS_kink_failure_chain",
     "Explanatory sketch. The failure is a failure OF THE SELECTED MODEL SET at "
     "the reference point, not a statement about tokamaks in general.")
