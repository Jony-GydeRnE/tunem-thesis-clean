#!/usr/bin/env python3
"""Brief at v1_fresh l.4552 — aspect ratio changes the torus, not the inventory.

Two midplane cuts at the SAME wall constraint R0 a = C_wall: a conventional
A = 4 plasma and a low-A = 1.5 plasma.  Same symmetry axis, same components,
same b and c.  Only A differs.

Everything below is computed from two numbers:

    R0 a = C_wall  and  A = R0 / a   =>   a = sqrt(C_wall / A),  R0 = A a

with b (nuclear island) and c (TF build) held FIXED IN METRES, because they are
set by neutron attenuation and by conductor and structure -- not by how round
the plasma is.  Scaling them with a would quietly assume the answer.

The result the figure exists to show is arithmetic, not opinion:

    R_in = R0 - a - b - c

closes comfortably at A = 4 and does NOT close at A = 1.5 with the same b and c.
That is not a verdict against low A.  It is the statement that low A cannot be
adopted while holding b and c fixed -- the inboard allocations have to be
renegotiated, which is exactly what the sections after this one do.  The figure
says so on its face, and labels NEITHER design superior, as the brief requires.

No HTS brand and no ST-specific divertor appear: neither has been derived.

Run:  python3 figS_aspect_ratio_geometry.py
Out:  figS_aspect_ratio_geometry.pdf / .png
"""
from sketch_base import *
from tokamak_build import HATCH      # the hatch vocabulary only, no machinery

# --------------------------------------------------------------------------
# the arithmetic
# --------------------------------------------------------------------------
C_WALL = 4.00          # m^2, the constraint the brief fixes: R0 * a
B_ISL = 0.50           # m, nuclear island -- set by neutrons, not by A
C_TF = 0.40            # m, coil build   -- set by conductor + structure


def state(A):
    a = np.sqrt(C_WALL / A)
    R0 = A * a
    return dict(A=A, a=a, R0=R0, gap=R0 - a, R_in=R0 - a - B_ISL - C_TF)


CONV, LOWA = state(4.0), state(1.5)

W, H = TEXTWIDTH_IN, 5.35
fig, ax = canvas(W, H)
SC = 1.02              # inches per metre of major radius
X0 = 0.42              # x of the symmetry axis, R = 0


def cut(y, s, title, col):
    """One horizontal midplane cut, drawn from the symmetry axis outward."""
    ax.plot([X0, X0], [y - 0.46, y + 0.52], color=PALETTE["guide"], lw=1.0,
            ls=(0, (4, 3)), zorder=3)
    ax.text(X0 - 0.06, y - 0.46, "$R=0$", fontsize=7.4, ha="right",
            va="bottom", color="0.45")

    def X(R):
        return X0 + SC * R

    # plasma
    ax.add_patch(Rectangle((X(s["R0"] - s["a"]), y - 0.15),
                           SC * 2 * s["a"], 0.30, facecolor=PALETTE["plasmafc"],
                           edgecolor=PALETTE["plasma"], lw=1.4, zorder=5))
    ax.text(X(s["R0"]), y, r"plasma  $2a$", fontsize=8.0, ha="center",
            va="center", color=PALETTE["plasma"], zorder=7)
    # nuclear island bracket, inboard side only (that is where it competes)
    ax.add_patch(Rectangle((X(s["R0"] - s["a"] - B_ISL), y - 0.15),
                           SC * B_ISL, 0.30, facecolor=PALETTE["blanket"],
                           alpha=0.35, edgecolor=PALETTE["blanket"],
                           hatch=HATCH["blanket"], lw=1.0, zorder=5))
    # the TF system, if it fits
    fits = s["R_in"] > 0
    xc0 = X(max(s["R_in"], 0.0))
    ax.add_patch(Rectangle((xc0, y - 0.15),
                           SC * (C_TF if fits else C_TF + s["R_in"]), 0.30,
                           facecolor=PALETTE["tf"],
                           alpha=0.30 if fits else 0.18,
                           edgecolor=PALETTE["tf"] if fits else PALETTE["current"],
                           hatch=None if fits else "xxx", lw=1.2, zorder=5))

    # brackets
    for x0, x1, lab, cc in (
            (s["R_in"], s["R_in"] + C_TF, r"$c$", PALETTE["tf"]),
            (s["R0"] - s["a"] - B_ISL, s["R0"] - s["a"], r"$b$",
             PALETTE["blanket"]),
            (s["R0"] - s["a"], s["R0"] + s["a"], r"$2a$", PALETTE["plasma"])):
        ax.annotate("", xy=(X(x1), y + 0.24), xytext=(X(x0), y + 0.24),
                    arrowprops=dict(arrowstyle="<|-|>", color=cc, lw=1.0),
                    zorder=8)
        ax.text(X(0.5 * (x0 + x1)), y + 0.27, lab, fontsize=8.4, ha="center",
                va="bottom", color=cc, zorder=8)
    ax.annotate("", xy=(X(s["R0"]), y - 0.30), xytext=(X0, y - 0.30),
                arrowprops=dict(arrowstyle="<|-|>", color=PALETTE["vessel"],
                                lw=1.1), zorder=8)
    ax.text(X(0.5 * s["R0"]), y - 0.33, r"$R_0=%.2f$ m" % s["R0"],
            fontsize=8.2, ha="center", va="top", color=PALETTE["vessel"])

    ax.text(X0 + 0.02, y + 0.56, title, fontsize=9.6, ha="left", va="bottom",
            color=col)
    ax.text(X0 + 0.02, y - 0.62,
            r"$A=%.1f$,  $a=%.2f$ m,  inboard gap $R_0-a=%.2f$ m"
            % (s["A"], s["a"], s["gap"]),
            fontsize=8.2, ha="left", va="top", color="0.28")
    return X


ax.text(W / 2, H - 0.14,
        r"THE SAME INVENTORY, TWO ASPECT RATIOS — at fixed $R_0a=C_{\rm wall}$",
        fontsize=10.4, ha="center", va="top", color=PALETTE["vessel"])

Xc = cut(4.18, CONV, r"conventional,  $A\simeq4$", PALETTE["cs"])
ax.text(Xc(CONV["R_in"]) - 0.06, 4.18 - 0.15,
        r"$R_{\rm in}=%.2f$ m" % CONV["R_in"], fontsize=8.2, ha="right",
        va="center", color=PALETTE["cs"])

Xl = cut(2.62, LOWA, r"low aspect ratio,  $A\simeq1.5$", PALETTE["current"])
ax.text(5.72, 2.62 - 0.15,
        r"$R_{\rm in}=%.2f$ m  $<0$" % LOWA["R_in"], fontsize=8.2, ha="left",
        va="center", color=PALETTE["current"])
ax.annotate("with the SAME $b$ and $c$, the inboard build\n"
            "runs past the axis: it does not close",
            xy=(X0 + 0.10, 2.62 + 0.02), xytext=(3.05, 2.42),
            fontsize=8.2, ha="left", va="top", color=PALETTE["current"],
            linespacing=1.5,
            arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                            lw=1.0), zorder=9)

ax.plot([0.10, W - 0.10], [1.62, 1.62], color="0.85", lw=0.9, zorder=1)

ax.text(0.10, 1.50,
        r"Both rows hold $R_0a=%.2f\,\mathrm{m}^2$, so the first-wall area is "
        r"the same. $b=%.2f$ m and $c=%.2f$ m are fixed IN"
        "\nMETRES: they are set by neutron attenuation and by conductor and "
        "structure, not by how round the plasma is —\nscaling them with $a$ "
        "would assume the answer. Everything above is then arithmetic: "
        r"$a=\sqrt{C_{\rm wall}/A}$, $R_0=Aa$."
        % (C_WALL, B_ISL, C_TF),
        fontsize=7.9, ha="left", va="top", color="0.30", linespacing=1.6)

ax.text(0.10, 0.82,
        "NEITHER design is superior here, and the figure does not say one is. "
        "It says something narrower: low $A$ cannot\n"
        "be adopted while holding $b$ and $c$ fixed — the inboard allocations "
        "have to be renegotiated. That is exactly\n"
        "what the following sections do, and why they quote their own "
        "shielding allocation and centre-column envelope\n"
        "instead of inheriting the conventional ones. The physics inventory "
        "has not changed; the room it fits into has.",
        fontsize=7.9, ha="left", va="top", color=PALETTE["pf"],
        linespacing=1.6)

save_exact(fig, "figS_aspect_ratio_geometry",
           "Explanatory sketch; midplane cuts at a common radial scale. No HTS "
           "brand and no ST divertor: neither is derived yet.",
           y=0.06)
print("conventional:", {k: round(v, 3) for k, v in CONV.items()})
print("low aspect  :", {k: round(v, 3) for k, v in LOWA.items()})
