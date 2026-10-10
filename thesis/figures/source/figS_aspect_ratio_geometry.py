#!/usr/bin/env python3
"""Approved compact aspect-ratio comparison at fixed R0*a = 4 m²."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "pdf.fonttype": 42})
fig, ax = plt.subplots(figsize=(7.2, 2.7))
ax.set(xlim=(-.25, 6.1), ylim=(-.55, 2.1))
ax.axis("off")
ax.set_title(r"Lower aspect ratio at fixed $R_0a$", fontsize=11, pad=8)
for A, y in [(4., 1.25), (1.5, .1)]:
    a = np.sqrt(4. / A)
    R0 = A * a
    ax.plot([0, 0], [y-.4, y+.42], color=".45", lw=.8, ls="--")
    ax.add_patch(Rectangle((R0-a, y-.12), 2*a, .34, facecolor="#e5edf3", edgecolor="#315a70"))
    ax.text(R0, y+.05, "plasma", ha="center", va="center", fontsize=9)
    ax.text(.05, y+.34, f"A = {A:.1f}", fontsize=10)
    ax.annotate("", (R0-a, y+.05), (0, y+.05), arrowprops={"arrowstyle":"<->", "lw":.8})
    ax.text((R0-a)/2, y+.12, "inboard gap", ha="center", fontsize=8)
    ax.annotate("", (R0, y-.28), (0, y-.28), arrowprops={"arrowstyle":"<->", "lw":.8})
    ax.text(R0/2, y-.32, r"$R_0$", ha="center", va="top")
    ax.annotate("", (R0+a, y+.35), (R0, y+.35), arrowprops={"arrowstyle":"<->", "lw":.8})
    ax.text(R0+a/2, y+.39, r"$a$", ha="center")
fig.text(.5, .015, r"Illustrative $R_0a=4$ m$^2$; fixed elongation. The nuclear build and column must fit inside the gap.", ha="center", fontsize=8)
fig.subplots_adjust(left=.03, right=.99, bottom=.12, top=.84)
fig.savefig("figS_aspect_ratio_geometry.pdf")
fig.savefig("figS_aspect_ratio_geometry.png", dpi=180)
