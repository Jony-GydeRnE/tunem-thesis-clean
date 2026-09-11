#!/usr/bin/env python3
"""Brief 10 — counting fusion pairs: why the mixture is fifty-fifty."""
from sketch_base import *

fig, ax = new(h=3.3)
def bag(x0, nD, nT, title, pairs, hi=False):
    w, h = 2.5, 1.5
    ax.add_patch(Rectangle((x0, 0.9), w, h, fc="white",
                           ec=PALETTE["vessel"] if not hi else PALETTE["cs"],
                           lw=2.2 if hi else 1.4, zorder=3))
    n = nD + nT
    cols, rows = 6, int(np.ceil((nD + nT) / 6))
    pts = [(x0 + 0.30 + (w - 0.60) * ((k % cols) / (cols - 1)),
            1.05 + (h - 0.30) * ((k // cols) / max(1, rows - 1)))
           for k in range(n)]
    for k, (px, py) in enumerate(pts):
        c = PALETTE["tf"] if k < nD else PALETTE["current"]
        ax.plot([px], [py], marker="o", ms=5.2, color=c, zorder=5)
    ax.text(x0 + w / 2, 2.62, title, fontsize=9.5, ha="center",
            color=PALETTE["cs"] if hi else "black")
    ax.text(x0 + w / 2, 0.72, f"$n_Dn_T \\propto$ {pairs}", fontsize=10.5,
            ha="center", va="top",
            color=PALETTE["cs"] if hi else "0.35")

bag(0.2, 18, 6, "unequal:  $n_D=3n_T$", r"$18\times6=108$")
bag(3.4, 12, 12, "equal:  $n_D=n_T$", r"$12\times12=\mathbf{144}$", hi=True)

ax.plot([1.45], [0.30], marker="o", ms=5.2, color=PALETTE["tf"])
ax.text(1.60, 0.30, "deuteron", fontsize=8.5, va="center", ha="left")
ax.plot([2.75], [0.30], marker="o", ms=5.2, color=PALETTE["current"])
ax.text(2.90, 0.30, "triton", fontsize=8.5, va="center", ha="left")

ax.text(3.05, -0.30,
        "Same 24 ions in both boxes. The reaction rate goes as the number of "
        "D--T PAIRS, $n_Dn_T$,\nand with $n_D+n_T$ fixed that product is a "
        "downward parabola: complete the square,\n"
        r"$n_Dn_T=\frac{1}{4}(n_D+n_T)^2-\frac{1}{4}(n_D-n_T)^2$, "
        "which is largest exactly when $n_D=n_T$.",
        fontsize=8.6, ha="center", va="top", color="0.25", linespacing=1.5)
ax.set_xlim(0, 6.1); ax.set_ylim(-1.25, 2.95)
save(fig, "figS_fusion_pairs", note="")
