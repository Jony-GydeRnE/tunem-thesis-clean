#!/usr/bin/env python3
"""Brief 32 — why an H factor is not a knob.

Left  : a broad L-mode-like temperature profile, with long outward turbulent
        heat arrows.
Right : the same core, plus a narrow edge region where the gradient is steep and
        the outward arrows are short -- a transport barrier.

The brief's point, and the figure's: H = tau_E / tau_E^scaling is a RATIO TO A
FIT.  You cannot set it.  There is no dial marked H anywhere on the machine.
What changed between the two panels is a transport state, achieved empirically,
maintained by conditions (a power threshold, a shape, a divertor configuration)
and paid for in ways the figure lists -- NOT a new coil, and not a design
choice one may simply assume.

The profiles are analytic and stated, not traced:

    L : T(r) = T0 (1 - (r/a)^2)^nu
    H : T(r) = T_ped + (T0' - T_ped)(1 - (r/r_ped)^2)^nu  for r < r_ped
        and a linear drop from T_ped to T_sep across the pedestal.

The stored energy ratio printed on the figure is the integral of those two
profiles, computed here -- so the "H" quoted is arithmetic on the drawn curves,
not a number chosen to look plausible.  It is a property of THESE two shapes,
which is exactly the point: H is an output.

Run:  python3 figS_h_factor.py
Out:  figS_h_factor.pdf / .png
"""
import numpy as np
import matplotlib.pyplot as plt

from tokamak_build import PALETTE, LS
from sketch_base import TEXTWIDTH_IN

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm",
                     "font.size": 10, "axes.linewidth": 0.9})

# --------------------------------------------------------------------------
# the two profiles
# --------------------------------------------------------------------------
NU_L, NU_H = 1.40, 1.80
R_PED, T_PED, T_SEP = 0.88, 0.68, 0.08
T0_H = 1.32   # core sits ON the pedestal; NU_H > 1 gives it a visible shoulder

r = np.linspace(0, 1, 1200)

T_L = T_SEP + (1.00 - T_SEP) * (1 - r ** 2) ** NU_L
# clip the base: outside r_ped the core term is not defined, and letting numpy
# raise a negative number to a fractional power silently produced NaNs in the
# first draft.
core = np.clip(1 - (np.minimum(r, R_PED) / R_PED) ** 2, 0.0, None) ** NU_H
T_H = np.where(r < R_PED,
               T_PED + (T0_H - T_PED) * core,
               T_PED + (T_SEP - T_PED) * (r - R_PED) / (1 - R_PED))

# stored energy ~ integral of n T dV with n flat: 2 pi^2 R0 a^2 * int T r dr
W_L = np.trapezoid(T_L * r, r)
W_H = np.trapezoid(T_H * r, r)
RATIO = W_H / W_L

fig, (axL, axH) = plt.subplots(1, 2, figsize=(TEXTWIDTH_IN, 4.55),
                               sharey=True)

for ax, T, ttl, col, nshort in (
        (axL, T_L, "BROAD PROFILE — heat leaves fast", PALETTE["heat"], False),
        (axH, T_H, "EDGE BARRIER — the same core, held up",
         PALETTE["current"], True)):
    ax.plot(r, T, color=col, lw=2.2, zorder=5)
    ax.fill_between(r, 0, T, color=col, alpha=0.13, lw=0, zorder=2)
    ax.set_xlim(0, 1.18)
    ax.set_ylim(0, 1.95)
    ax.set_xlabel(r"normalised minor radius  $r/a$")
    ax.set_title(ttl, fontsize=10.0, pad=8)
    ax.grid(True, color="0.91", lw=0.6)
    ax.set_axisbelow(True)
    ax.axvline(1.0, color=PALETTE["plasma"], lw=1.2, ls=(0, (1.4, 2.0)),
               zorder=3)
    ax.text(1.005, 1.88, "edge", fontsize=8.0, ha="left", va="top",
            color=PALETTE["plasma"], rotation=90)

axL.set_ylabel(r"temperature   $T(r)$   (normalised)")

# outward turbulent heat arrows.  LENGTH is set by the local gradient of the
# panel's own profile, so "shorter where the barrier is" is computed.
for ax, T, col in ((axL, T_L, PALETTE["heat"]),
                   (axH, T_H, PALETTE["current"])):
    for rr in np.linspace(0.18, 0.96, 7):
        i = int(rr * (len(r) - 1))
        y = T[i]
        # a long arrow where transport is unimpeded; short inside the barrier
        long = 0.19
        short = 0.055
        L = short if (ax is axH and rr > R_PED - 0.06) else long
        ax.annotate("", xy=(rr + L, y + 0.10), xytext=(rr, y + 0.10),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.3))

axH.axvspan(R_PED, 1.0, color=PALETTE["cs"], alpha=0.13, lw=0, zorder=1)
axH.annotate("a narrow region where outward transport\n"
             "is SUPPRESSED: steep gradient, short arrows",
             xy=(0.935, 1.52), xytext=(0.03, 1.90), fontsize=8.2,
             ha="left", va="top", color=PALETTE["cs"], linespacing=1.5,
             arrowprops=dict(arrowstyle="-|>", color=PALETTE["cs"], lw=1.0),
             zorder=8)
axL.text(0.03, 1.90, "long arrows everywhere:\nnothing holds the gradient up",
         fontsize=8.2, ha="left", va="top", color=PALETTE["heat"],
         linespacing=1.5)

axH.text(0.03, 0.06, r"stored energy $\times\,%.2f$ versus the left panel"
         % RATIO, fontsize=8.6, ha="left", va="bottom",
         color=PALETTE["vessel"])

# --------------------------------------------------------------------------
fig.text(0.5, 0.175,
         r"$H \equiv \tau_E/\tau_E^{\rm scaling}$ is a RATIO TO A FIT, and "
         "therefore an OUTPUT. There is no dial marked $H$ on the machine: "
         "nothing here\n"
         "is a new coil, a new supply or a new component. What changed is a "
         "TRANSPORT STATE, reached empirically and held only while its\n"
         "conditions hold — an input-power threshold, a shape, a divertor "
         "configuration — and paid for with edge-localised relaxations and\n"
         r"impurity retention. The $\times\,%.2f$ above is the integral of the "
         "two curves drawn here, so even that number is a property of these\n"
         "two shapes, not a design input. Assuming a value of $H$ and then "
         "quoting the performance it implies is assuming the conclusion."
         % RATIO,
         fontsize=7.7, ha="center", va="top", color="0.30", linespacing=1.55)

fig.tight_layout(rect=(0, 0.315, 1, 1))
fig.savefig("figS_h_factor.pdf", bbox_inches="tight")
fig.savefig("figS_h_factor.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print(f"W_L = {W_L:.4f}, W_H = {W_H:.4f}, ratio = {RATIO:.4f}")
print("wrote figS_h_factor.pdf/.png")
