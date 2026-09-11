#!/usr/bin/env python3
"""
sketch_base.py — shared foundation for the figS_* reset-explanatory family.

Two families, one document:

  * figM*  cumulative MACHINE STATES.  Built from tokamak_build.py.  Each one
           shows the whole accumulated machine.
  * figS*  reset EXPLANATORY SKETCHES.  Built from this module.  Each one
           isolates a single mechanism and deliberately shows NO accumulated
           hardware, because carrying the machine into a mechanism sketch is
           what makes mechanism sketches unreadable.

They share PALETTE and the redundant-encoding discipline, so the document reads
as one thing; they share nothing else, and a figS_* script must never import
the machine model.

Everything here is computed or laid out explicitly.  No AI art, no tracing.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Ellipse

from tokamak_build import PALETTE, LS, LW      # palette + line styles only

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm",
                     "font.size": 10, "axes.linewidth": 0.9})

# Thesis text block on letter paper with 0.82 in margins.  Sketches are drawn
# at (or just under) this width so a 9 pt label prints at ~9 pt -- the same
# measurement that forced the tall machine-state layout.
TEXTWIDTH_IN = 6.86

DISCLAIMER = "Explanatory sketch; schematic, not to scale."


def new(w=TEXTWIDTH_IN, h=3.6, n=1):
    """A blank sketch canvas: no axes, no frame, equal aspect."""
    fig, axes = plt.subplots(1, n, figsize=(w, h))
    axes = np.atleast_1d(axes)
    for ax in axes:
        ax.set_aspect("equal")
        ax.axis("off")
    return fig, (axes[0] if n == 1 else axes)


def canvas(w=TEXTWIDTH_IN, h=4.0):
    """A canvas on which ONE DATA UNIT IS EXACTLY ONE INCH.

    Why this exists.  The obvious construction -- subplots() + axis("off") +
    tight_layout() + savefig(bbox_inches="tight") -- has a trap that cost this
    project two rebuilds.  Font size is absolute (points); data units are not.
    tight_layout shrinks the axes to fit the figure, and then bbox_inches
    "tight" EXPANDS the saved image to enclose whatever text overflowed.  The
    two effects compound: the axes ends up a fraction of the image, one data
    unit becomes far less than an inch, and every box you sized against its own
    text turns out too small.  Worse, it fails silently -- the figure is
    written, it just has collided labels.

    Here the axes is the whole figure and the bbox is fixed, so a box 2.05 units
    wide is 2.05 in = 148 pt wide, and text at 8 pt (mean glyph ~ 0.5 em = 4 pt
    in Computer Modern) fits if it is under ~37 characters.  That is a
    calculation, not a guess.  Overflow now CLIPS at the figure edge, which is
    visible, instead of silently rescaling everything.

    Use this for text-heavy sketches (flow diagrams, panels of prose).  Use
    new() for drawings, where equal aspect actually matters.
    """
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect("auto")
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def save_exact(fig, stem, note=None, y=0.10):
    """Companion to canvas(): writes with the bbox UNCHANGED.

    The limits line is placed in data coordinates (inches from the bottom) so
    it obeys the same one-unit-one-inch rule as everything else.
    """
    if note:
        w = fig.get_size_inches()[0]
        fig.axes[0].text(w / 2, y, note, fontsize=7.6, ha="center",
                         va="bottom", color="0.45", linespacing=1.45)
    fig.savefig(stem + ".pdf", bbox_inches=None)
    fig.savefig(stem + ".png", dpi=180, bbox_inches=None)
    plt.close(fig)
    print("wrote", stem + ".pdf/.png   (exact canvas)")


def save(fig, stem, note=None, tight=True):
    """Write the pair, with the standard limits line."""
    fig.text(0.5, 0.005, note or DISCLAIMER, fontsize=7.6, ha="center",
             va="bottom", color="0.45", linespacing=1.45)
    if tight:
        fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(stem + ".pdf", bbox_inches="tight")
    fig.savefig(stem + ".png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("wrote", stem + ".pdf/.png")


# --------------------------------------------------------------------------
# small primitives used by more than one sketch
# --------------------------------------------------------------------------
def arrow(ax, p0, p1, color="black", lw=1.6, ls="solid", style="-|>", z=5,
          alpha=1.0):
    ax.annotate("", xy=p1, xytext=p0, zorder=z,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, alpha=alpha,
                                shrinkA=0, shrinkB=0))


def box(ax, x, y, w, h, text, fc="white", ec="black", fs=8.8, lw=1.2, z=6,
        tc=None, style="round,pad=0.02"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle=style, facecolor=fc,
                                edgecolor=ec, linewidth=lw, zorder=z))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=tc or ec, zorder=z + 1, linespacing=1.35)
    return (x, y, w, h)


def shaped_boundary(R0=0.0, Z0=0.0, a=1.0, kappa=1.0, delta=0.0, n=400):
    """The same Miller boundary the machine family uses, so a flux surface in a
    sketch has the same shape as the plasma in the machine figures."""
    th = np.linspace(0, 2 * np.pi, n)
    d = np.arcsin(np.clip(delta, -0.95, 0.95))
    return (R0 + a * np.cos(th + d * np.sin(th)), Z0 + kappa * a * np.sin(th))


def odot(ax, x, y, r, color, z=6):
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.3, zorder=z))
    ax.add_patch(Circle((x, y), 0.30 * r, fc=color, ec=color, zorder=z + 1))


def otimes(ax, x, y, r, color, z=6):
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.3, zorder=z))
    d = r / np.sqrt(2)
    ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=1.1, zorder=z + 1)
    ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=1.1, zorder=z + 1)


# --------------------------------------------------------------------------
# causal / flow diagrams
# --------------------------------------------------------------------------
# Four explanatory diagrams are directed graphs, not physical layouts. They share a
# vocabulary, and the vocabulary is the point: the reader must be able to see at
# a glance which boxes are CHOSEN, which are DERIVED, and which are EMPIRICAL or
# MODEL inputs.  That distinction is the manuscript's own evidence ladder, so
# the diagrams encode it in the box style rather than leaving it to prose.
KIND = {
    "chosen":    dict(fc="#FFFFFF", ec=PALETTE["vessel"],  lw=1.6),
    "primary":   dict(fc="#E8F0FE", ec=PALETTE["tf"],      lw=1.6),
    "derived":   dict(fc="#F3E8F7", ec=PALETTE["bfield"],  lw=1.3),
    "empirical": dict(fc="#FFF1E0", ec=PALETTE["pf"],      lw=1.6),
    "fail":      dict(fc="#FDE7E7", ec=PALETTE["current"], lw=1.8),
    "pass":      dict(fc="#E8F5EC", ec=PALETTE["cs"],      lw=1.4),
}
KIND_LABEL = {
    "chosen":    "chosen input",
    "primary":   "primary parameter",
    "derived":   "derived quantity",
    "empirical": "empirical / model input",
    "fail":      "fails the test",
    "pass":      "passes",
}


def node(ax, x, y, w, h, text, kind="derived", fs=8.4):
    st = KIND[kind]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.015",
                                facecolor=st["fc"], edgecolor=st["ec"],
                                linewidth=st["lw"], zorder=6))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color="black", zorder=7, linespacing=1.35)


def flow(ax, p0, p1, color=None, ls="solid", lw=1.5, label=None, fs=7.8,
         rad=0.0):
    ax.annotate("", xy=p1, xytext=p0, zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=color or "0.35",
                                lw=lw, linestyle=ls,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=3, shrinkB=4))
    if label:
        ax.text(0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1]) + 0.055, label,
                fontsize=fs, ha="center", va="bottom", color=color or "0.35")


def kind_legend(ax, x, y, kinds, fs=7.8, dx=1.02):
    """One row explaining the box vocabulary."""
    for i, k in enumerate(kinds):
        st = KIND[k]
        ax.add_patch(FancyBboxPatch((x + i * dx, y - 0.055), 0.20, 0.11,
                                    boxstyle="round,pad=0.01",
                                    facecolor=st["fc"], edgecolor=st["ec"],
                                    linewidth=st["lw"], zorder=6))
        ax.text(x + i * dx + 0.24, y, KIND_LABEL[k], fontsize=fs,
                ha="left", va="center", color="0.25")
