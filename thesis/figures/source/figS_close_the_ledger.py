#!/usr/bin/env python3
"""Brief 18 — two ways to close the current ledger.

Left  : the pulsed machine.  The solenoid's flux swing is FINITE, so the burn
        is finite.  Flux falls during the burn and is recharged during a dwell.
Right : the long-pulse machine.  I_ohm is retired and I_CD + I_bs carries the
        whole ledger, so the solenoid flux is held flat after start-up.

This is an ACCOUNTING sketch, as the brief requires.  It makes no claim that
either architecture is preferable, and it deliberately shows the price of each:
the pulsed machine buys steady physics with a duty cycle, the steady machine
buys continuity with recirculating power and a pressure gradient it must hold.

The one quantitative statement on the figure is honest arithmetic, not a model:
    V_loop = -dPhi/dt,   I_ohm = V_loop / R_p   =>   t_burn = DeltaPhi/(I_ohm R_p)
(neglecting internal inductance, which is stated on the figure.)

Waveform shapes below are chosen for legibility; the ONLY thing asserted is the
bookkeeping -- flux is consumed, the ledger sums to I_p.

Run:  python3 figS_close_the_ledger.py
Out:  figS_close_the_ledger.pdf / .png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from tokamak_build import PALETTE, LS
from sketch_base import TEXTWIDTH_IN, save

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm",
                     "font.size": 10, "axes.linewidth": 0.9})

# --------------------------------------------------------------------------
# LEFT: pulsed.  burn of length TB, dwell of length TD, repeated.
# --------------------------------------------------------------------------
TB, TD = 1.00, 0.42
t = np.linspace(0, 3 * (TB + TD), 3000)
phase = np.mod(t, TB + TD)
burning = phase < TB

# flux: falls linearly through the burn (constant loop voltage), recharges
# through the dwell.  Amplitude +-1 in units of the half-swing.
phi = np.where(burning,
               1.0 - 2.0 * phase / TB,
               -1.0 + 2.0 * (phase - TB) / TD)
I_ohm = np.where(burning, 1.0, 0.0)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(TEXTWIDTH_IN, 4.35),
                               sharey=True)

for ax in (axL, axR):
    ax.set_ylim(-1.35, 2.05)
    ax.set_xlabel("time  (arbitrary units)")
    ax.grid(True, color="0.90", lw=0.6)
    ax.set_axisbelow(True)

# burn / dwell shading
for k in range(3):
    t0 = k * (TB + TD)
    axL.axvspan(t0, t0 + TB, color=PALETTE["plasma"], alpha=0.07, lw=0)
    axL.axvspan(t0 + TB, t0 + TB + TD, color="0.55", alpha=0.10, lw=0)

axL.fill_between(t, 0, I_ohm, color=PALETTE["cs"], alpha=0.22, lw=0)
axL.plot(t, I_ohm, color=PALETTE["cs"], lw=1.8)
axL.plot(t, phi, color=PALETTE["current"], lw=1.8, ls=LS["pf"])
axL.axhline(0, color="0.4", lw=0.8)

# staggered so the two words never sit side by side at print size
axL.text(TB / 2, 1.88, "BURN", fontsize=8.6, ha="center", va="top",
         color=PALETTE["plasma"])
axL.text(TB + TD / 2, 1.52, "DWELL", fontsize=8.6, ha="center", va="top",
         color="0.42")
axL.annotate("", xy=(0.06, 1.02), xytext=(0.06, -1.02),
             arrowprops=dict(arrowstyle="<->", color=PALETTE["current"],
                             lw=1.1))
axL.text(0.22, -0.30, r"$\Delta\Phi$ is" "\n" "finite", fontsize=8.4,
         va="center", ha="left", color=PALETTE["current"], linespacing=1.35)
axL.set_title("PULSED: the flux swing runs out", fontsize=10.2, pad=8)
axL.set_ylabel("current  /  flux     (normalised)")

# --------------------------------------------------------------------------
# RIGHT: long pulse.  I_bs and I_CD stack to the same I_p, continuously.
# --------------------------------------------------------------------------
t2 = np.linspace(0, 3 * (TB + TD), 3000)
ramp = np.clip(t2 / 0.35, 0, 1)                 # start-up, then steady
f_bs, f_cd = 0.62, 0.38                         # ILLUSTRATIVE split, labelled
I_bs = f_bs * ramp
I_tot = ramp

axR.fill_between(t2, 0, I_bs, color=PALETTE["pf"], alpha=0.30, lw=0)
axR.fill_between(t2, I_bs, I_tot, color=PALETTE["heat"], alpha=0.30, lw=0)
axR.plot(t2, I_tot, color=PALETTE["vessel"], lw=1.7)
axR.plot(t2, I_bs, color=PALETTE["pf"], lw=1.6, ls=LS["pf"])
axR.plot(t2, np.zeros_like(t2), color=PALETTE["cs"], lw=1.8)
# the solenoid flux is given its own lane ABOVE the current stack: it is not a
# current, its normalisation is arbitrary, and overlaying it on the stack was
# unreadable.
phi_R = np.where(t2 > 0.35, 1.30, 1.75 - 0.45 * t2 / 0.35)
axR.plot(t2, phi_R, color=PALETTE["current"], lw=1.8, ls=LS["pf"])
axR.axhline(0, color="0.4", lw=0.8)

axR.text(2.6, 0.28, r"$I_{\rm bs}$", fontsize=10, ha="center",
         color=PALETTE["pf"])
axR.text(2.6, 0.76, r"$I_{\rm CD}$", fontsize=10, ha="center",
         color="#00707E")
axR.text(2.6, -0.12, r"$I_{\rm ohm}\to 0$", fontsize=9, ha="center",
         va="top", color=PALETTE["cs"])
axR.text(4.20, 1.36, r"$\Phi_{\rm CS}$ held after start-up", fontsize=8.4,
         ha="right", va="bottom", color=PALETTE["current"])
axR.text(0.10, -0.62, "start-up still\nneeds the solenoid", fontsize=8.2,
         ha="left", va="top", color="0.42", linespacing=1.4)
axR.set_title("LONG PULSE: the ledger is re-sourced", fontsize=10.2, pad=8)

# --------------------------------------------------------------------------
# one shared legend, below both panels: an in-axes legend collided with the
# waveforms in every position tried.
HANDLES = [
    Line2D([], [], color=PALETTE["cs"], lw=1.8, label=r"$I_{\rm ohm}$"),
    Line2D([], [], color=PALETTE["pf"], lw=1.6, ls=LS["pf"],
           label=r"$I_{\rm bs}$"),
    Line2D([], [], color="#00707E", lw=6, alpha=0.45, label=r"$I_{\rm CD}$"),
    Line2D([], [], color=PALETTE["vessel"], lw=1.7, label=r"$I_p$ (total)"),
    Line2D([], [], color=PALETTE["current"], lw=1.8, ls=LS["pf"],
           label=r"solenoid flux $\Phi_{\rm CS}$"),
]
fig.legend(handles=HANDLES, frameon=False, fontsize=8.4, ncol=5,
           loc="lower center", bbox_to_anchor=(0.5, 0.215), handlelength=2.4,
           columnspacing=1.6)

fig.text(0.5, 0.175,
         r"Left, the only arithmetic on the figure: $V_{\rm loop}=-d\Phi/dt$ "
         r"and $I_{\rm ohm}=V_{\rm loop}/R_p$ give $t_{\rm burn}="
         r"\Delta\Phi/(I_{\rm ohm}R_p)$ — a finite swing buys a finite burn."
         "\n(Internal inductance is neglected; start-up consumes part of "
         r"$\Delta\Phi$ before the burn begins.)  Right, the $I_{\rm bs}$/"
         r"$I_{\rm CD}$ split drawn is ILLUSTRATIVE:"
         "\nonly the sum is constrained here. Neither panel claims its "
         "architecture is preferable — each states a different price.",
         fontsize=7.8, ha="center", va="top", color="0.32", linespacing=1.55)

fig.tight_layout(rect=(0, 0.30, 1, 1))
fig.savefig("figS_close_the_ledger.pdf", bbox_inches="tight")
fig.savefig("figS_close_the_ledger.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("wrote figS_close_the_ledger.pdf/.png")
