#!/usr/bin/env python3
"""Brief 16 — a trapped orbit.

Nothing here is drawn by hand.  The model is:

  B(theta)/B_0 = R0 / (R0 + r cos theta)                (toroidal field ~ 1/R)
  mu = m v_perp^2 / 2B   and   E = (1/2) m v_par^2 + mu B   are conserved
  =>  (v_par/v)^2 (theta) = 1 - lambda B(theta)/B_min,   lambda = v_perp0^2/v^2

and the radial excursion of the guiding centre follows from conservation of the
canonical toroidal momentum p_phi = m R v_phi + q psi, which makes delta_psi
proportional to v_par.  So the banana below IS the plot of v_par(theta): its
tips are exactly the roots of that expression, not an artist's crescent.

Trapping condition, derived in the right panel:
      (v_par0 / v)^2  <=  2 eps / (1 + eps),      eps = a / R0.

Run:  python3 figS_trapped_orbit.py
Out:  figS_trapped_orbit.pdf / .png
"""
from sketch_base import *

# --------------------------------------------------------------------------
# model constants.  eps is exaggerated and so is the banana width, because a
# real banana at eps ~ 0.3 is a few centimetres wide and would vanish on paper.
# --------------------------------------------------------------------------
R0, r0 = 1.62, 0.50
EPS = r0 / R0
KAP = 1.25
TRAP_CRIT = 2 * EPS / (1 + EPS)

def B_norm(th, r=r0):
    return R0 / (R0 + r * np.cos(th))

B_min, B_max = B_norm(0.0), B_norm(np.pi)

def vpar(th, lam):
    s = 1.0 - lam * B_norm(th) / B_min
    return np.where(s > 0, np.sqrt(np.clip(s, 0, None)), np.nan)

# lambda chosen so the banana tips land at theta_b = 60 deg, which is what a
# reader recognises as a banana.  cos(theta_b) = (lam (R0+r0) - R0)/r0.
COS_TB = 0.50
LAM_TRAP = (R0 + COS_TB * r0) / (R0 + r0)
LAM_PASS = 0.10
TH_B = float(np.arccos(COS_TB))
assert 1.0 - LAM_TRAP <= TRAP_CRIT, "the 'trapped' orbit is not trapped"
assert 1.0 - LAM_PASS > TRAP_CRIT, "the 'passing' orbit is not passing"

fig, (ax, axd) = new(h=4.15, n=2)
# the derivation panel is a text panel, not a drawing: equal aspect
# there would shrink the box to a fraction of the column width.
axd.set_aspect("auto")

# --------------------------------------------------------------------------
# LEFT — the poloidal cross-section
# --------------------------------------------------------------------------
for f in (0.28, 0.62, 1.12):
    R, Z = shaped_boundary(R0=R0, a=f * 0.60, kappa=KAP)
    ax.plot(R, Z, color=PALETTE["bfield"], lw=0.8, ls=LS["bfield"],
            alpha=0.5, zorder=2)
R, Z = shaped_boundary(R0=R0, a=0.60 * 1.12, kappa=KAP)
ax.plot(R, Z, color=PALETTE["plasma"], lw=1.5, zorder=3)
ax.plot([R0], [0.0], marker="+", ms=8, mew=1.4, color=PALETTE["bfield"],
        zorder=4)

# field strength: the SYMBOL SIZE is B(R) = B0 R0 / R, evaluated, not styled.
for Rc in np.linspace(R0 - 0.92, R0 + 0.92, 9):
    otimes(ax, Rc, -1.42, 0.052 * (R0 / Rc), PALETTE["tf"])
arrow(ax, (R0 + 1.02, -1.80), (R0 - 1.02, -1.80), PALETTE["tf"], lw=1.2)
ax.text(R0, -1.96, r"$B_\varphi = B_0R_0/R$ — symbol size is the computed $B$",
        fontsize=8.4, ha="center", va="top", color=PALETTE["tf"])
ax.text(R0 - 1.05, -1.68, "stronger", fontsize=8.0, ha="left", va="bottom",
        color=PALETTE["tf"])

# the two orbits
def orbit(lam, amp, n=1400):
    th = np.linspace(-np.pi, np.pi, n)
    vp = vpar(th, lam)
    keep = ~np.isnan(vp)
    th, vp = th[keep], vp[keep]
    th_c = np.concatenate([th, th[::-1]])           # out along +v_par ...
    dr = amp * np.concatenate([vp, -vp[::-1]])      # ... back along -v_par
    rr = r0 + dr
    return R0 + rr * np.cos(th_c), KAP * rr * np.sin(th_c)

Xb, Yb = orbit(LAM_TRAP, 0.40)
ax.plot(Xb, Yb, color=PALETTE["current"], lw=2.0, zorder=6)
Xp, Yp = orbit(LAM_PASS, 0.075)
ax.plot(Xp, Yp, color=PALETTE["cs"], lw=1.9, ls=LS["cs"], zorder=5)

for sgn in (+1, -1):
    xt = R0 + r0 * np.cos(sgn * TH_B)
    yt = KAP * r0 * np.sin(sgn * TH_B)
    ax.plot([xt], [yt], marker="o", ms=7.5, mfc="white",
            mec=PALETTE["current"], mew=2.0, zorder=8)

ax.annotate(r"$v_\parallel=0$", xy=(R0 + r0 * COS_TB, KAP * r0 * np.sin(TH_B)),
            xytext=(R0 - 0.30, 1.28), fontsize=9.0, ha="center",
            color=PALETTE["current"],
            arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                            lw=1.0, shrinkB=6), zorder=9)
ax.annotate(r"$v_\parallel=0$", xy=(R0 + r0 * COS_TB, -KAP * r0 * np.sin(TH_B)),
            xytext=(R0 - 0.30, -1.15), fontsize=9.0, ha="center",
            color=PALETTE["current"],
            arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                            lw=1.0, shrinkB=6), zorder=9)

ax.text(R0 + 1.24, 0.30, "TRAPPED\n(banana)", fontsize=9.2, ha="center",
        color=PALETTE["current"], linespacing=1.3)
ax.text(R0 - 1.22, 0.30, "PASSING", fontsize=9.2, ha="center",
        color=PALETTE["cs"])
ax.text(R0, 1.62, "the banana never reaches the inboard side —\n"
                  "that is the whole content of the picture",
        fontsize=8.4, ha="center", va="bottom", color="0.32",
        linespacing=1.4)

ax.set_xlim(R0 - 1.72, R0 + 1.72)
ax.set_ylim(-2.35, 2.15)

# --------------------------------------------------------------------------
# RIGHT — the derivation, in four lines
# --------------------------------------------------------------------------
axd.add_patch(FancyBboxPatch((0.02, 1.06), 3.40, 2.02,
                             boxstyle="round,pad=0.035", facecolor="#FBFBFD",
                             edgecolor=PALETTE["vessel"], linewidth=1.2,
                             zorder=2))
axd.text(0.20, 2.90, "the mirror condition, in four lines", fontsize=9.4,
         ha="left", va="center", color=PALETTE["vessel"], zorder=7)
LINES = [
    r"$\mu=\frac{mv_\perp^2}{2B}$,   "
    r"$E=\frac{1}{2}mv_\parallel^2+\mu B$   conserved",
    r"$v_\parallel=0 \;\Rightarrow\; B_{\rm t}=B_{\min}\,v^2/v_{\perp 0}^2$",
    r"trapped $\Leftrightarrow B_{\rm t}\leq B_{\max}=B_{\min}\frac{1+\varepsilon}"
    r"{1-\varepsilon}$",
    r"$\Leftrightarrow\;\left(v_{\parallel 0}/v\right)^2 \leq "
    r"\frac{2\varepsilon}{1+\varepsilon}$",
]
for i, s in enumerate(LINES):
    axd.text(0.20, 2.55 - 0.44 * i, s, fontsize=8.5, ha="left", va="center",
             zorder=7)

axd.text(0.06, 0.86,
         (r"Here $\varepsilon=%.2f$, so the window is "
          r"$(v_{\parallel 0}/v)^2\leq %.2f$." % (EPS, TRAP_CRIT)) +
         "\nThe banana drawn has $%.2f$; the passing orbit $%.2f$."
         % (1 - LAM_TRAP, 1 - LAM_PASS),
         fontsize=8.4, ha="left", va="top", color="0.28", linespacing=1.5,
         zorder=7)

axd.text(0.06, 0.06,
         "The trapped FRACTION is roughly $\\sqrt{2\\varepsilon/(1+\\varepsilon)}"
         "\\approx %.2f$ here.\nThat is not a small correction: a large minority "
         "of particles\nnever sees the inboard side. §37 turns that asymmetry "
         "into a\ncurrent." % np.sqrt(TRAP_CRIT),
         fontsize=8.4, ha="left", va="top", color=PALETTE["pf"],
         linespacing=1.5, zorder=7)

axd.text(0.06, -1.22,
         "Two exaggerations, stated: $\\varepsilon$ is drawn larger than a\n"
         "reactor's, and the banana width is drawn far larger than\n"
         "$q\\rho/\\sqrt{\\varepsilon}$, so that the orbit is visible at print size.",
         fontsize=8.0, ha="left", va="top", color="0.45", linespacing=1.5,
         zorder=7)

axd.set_xlim(0.0, 3.45)
axd.set_ylim(-2.35, 3.20)

save(fig, "figS_trapped_orbit",
     "Explanatory sketch. The orbit shape is computed from "
     r"$v_\parallel(\theta)$; the inverse aspect ratio and the banana width "
     "are exaggerated for legibility.")
