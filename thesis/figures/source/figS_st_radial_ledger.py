#!/usr/bin/env python3
"""Brief at v1_fresh l.5221 — the ST radial ledger, neutron first, magnet second.

One outboard-to-inboard midplane cut for the illustrative published state:
A = 2, R0 = 1.87 m.  Components are added on the inboard side IN CAUSAL ORDER,
which is the whole argument of the section: the neutron shield is placed first
because neutrons do not negotiate, and the magnet gets what is left.

The arithmetic is Eq. (eq:menard-geometry-check), evaluated here rather than
quoted:

    a       = R0 / A            = 1.87 / 2      = 0.935 m
    R0 - a                                      = 0.935 m
    minus shield  0.600 m
    minus first wall 0.020 m
    ------------------------------------------------
    remaining                                   = 0.315 m

against the study's stated 0.30 m centre-column radius.  The 15 mm difference is
NOT spare room and the figure says so: it is the residue of a rough check that
has not yet paid for a single cable, support, coolant channel or tolerance.

Two rules from the brief, both structural:

  * inside the centre-column envelope the subdivisions are UNFILLED and
    unlabelled by size -- TF winding, support, insulation/cooling, optional
    solenoid.  The study's own split is not asserted here, because asserting it
    would turn one study's engineering into a template.
  * the whole figure is marked as an ILLUSTRATIVE PUBLISHED ALLOCATION, not a
    universal reactor template.

Run:  python3 figS_st_radial_ledger.py
Out:  figS_st_radial_ledger.pdf / .png
"""
from sketch_base import *
from tokamak_build import HATCH      # hatch vocabulary only, no machinery

# --------------------------------------------------------------------------
# the published illustrative state, and Eq. (eq:menard-geometry-check)
# --------------------------------------------------------------------------
A_ST, R0 = 2.0, 1.87                 # m
T_WALL, T_SHLD = 0.020, 0.600        # m, study-specific allocations
R_CS_STUDY = 0.300                   # m, the study's centre-column radius

a = R0 / A_ST
inboard = R0 - a
remaining = inboard - T_SHLD - T_WALL
slack = remaining - R_CS_STUDY

W, H = TEXTWIDTH_IN, 5.60
fig, ax = canvas(W, H)
SC = 1.42                            # inches per metre
X0 = 0.30                            # x of R = 0
YM = 4.15                            # midplane y
HB = 0.34                            # band height


def X(R):
    return X0 + SC * R


ax.text(W / 2, H - 0.14,
        r"THE ST RADIAL LEDGER — neutron first, magnet second  "
        r"($A=%.0f$, $R_0=%.2f$ m)" % (A_ST, R0),
        fontsize=10.4, ha="center", va="top", color=PALETTE["vessel"])
ax.text(W / 2, H - 0.38,
        "one illustrative published allocation, laid out in the order the "
        "physics forces",
        fontsize=8.4, ha="center", va="top", color="0.38")

# symmetry axis
ax.plot([X0, X0], [YM - 0.95, YM + 0.62], color=PALETTE["guide"], lw=1.1,
        ls=(0, (4, 3)), zorder=3)
ax.text(X0 - 0.04, YM - 0.98, "$R=0$", fontsize=7.8, ha="center", va="top",
        color="0.45")

# ---- the bands, inboard to outboard -------------------------------------
ax.add_patch(Rectangle((X(R0 - a), YM - HB / 2), SC * 2 * a, HB,
                       facecolor=PALETTE["plasmafc"],
                       edgecolor=PALETTE["plasma"], lw=1.5, zorder=5))
ax.text(X(R0), YM, r"plasma   $2a=%.2f$ m" % (2 * a), fontsize=8.4,
        ha="center", va="center", color=PALETTE["plasma"], zorder=7)

ax.add_patch(Rectangle((X(R0 - a - T_WALL), YM - HB / 2), SC * T_WALL, HB,
                       facecolor=PALETTE["wall"], alpha=0.55,
                       edgecolor=PALETTE["wall"], lw=1.0, zorder=6))
ax.add_patch(Rectangle((X(R0 - a - T_WALL - T_SHLD), YM - HB / 2),
                       SC * T_SHLD, HB, facecolor=PALETTE["shield"],
                       alpha=0.30, edgecolor=PALETTE["shield"],
                       hatch=HATCH["shield"], lw=1.2, zorder=5))
ax.text(X(R0 - a - T_WALL - T_SHLD / 2), YM, r"shield  $%.2f$ m" % T_SHLD,
        fontsize=8.2, ha="center", va="center", color="black", zorder=7)

# ---- the centre-column envelope: subdivided, but UNFILLED ----------------
env_x0, env_w = X(0.0), SC * R_CS_STUDY
ax.add_patch(Rectangle((env_x0, YM - HB / 2), env_w, HB, facecolor="white",
                       edgecolor=PALETTE["tf"], lw=1.6, zorder=6))
for f in (0.25, 0.50, 0.75):
    ax.plot([env_x0 + f * env_w] * 2, [YM - HB / 2, YM + HB / 2],
            color=PALETTE["tf"], lw=0.9, ls=(0, (2, 2)), zorder=7)
ax.annotate("centre-column envelope, $%.2f$ m — subdivided but NOT sized:\n"
            "TF winding $|$ support $|$ insulation and cooling $|$ optional "
            "solenoid" % R_CS_STUDY,
            xy=(env_x0 + 0.5 * env_w, YM - HB / 2), xytext=(1.05, 3.46),
            fontsize=8.0, ha="left", va="top", color=PALETTE["tf"],
            linespacing=1.5,
            arrowprops=dict(arrowstyle="-|>", color=PALETTE["tf"], lw=1.0),
            zorder=9)

# ---- brackets ------------------------------------------------------------
for x0, x1, lab, cc, dy in (
        (0.0, R0 - a, r"$R_0-a = %.3f$ m" % inboard, PALETTE["vessel"], 0.66),
        (R0 - a - T_WALL - T_SHLD, R0 - a,
         r"shield $+$ first wall $=%.3f$ m" % (T_SHLD + T_WALL),
         PALETTE["shield"], 0.34)):
    ax.annotate("", xy=(X(x1), YM + dy), xytext=(X(x0), YM + dy),
                arrowprops=dict(arrowstyle="<|-|>", color=cc, lw=1.1),
                zorder=8)
    ax.text(X(0.5 * (x0 + x1)), YM + dy + 0.03, lab, fontsize=8.2,
            ha="center", va="bottom", color=cc, zorder=8)

ax.annotate("", xy=(X(remaining), YM - 0.30), xytext=(X0, YM - 0.30),
            arrowprops=dict(arrowstyle="<|-|>", color=PALETTE["current"],
                            lw=1.2), zorder=8)
ax.text(X0, YM - 0.44, r"what is LEFT: $%.3f$ m" % remaining, fontsize=8.4,
        ha="left", va="top", color=PALETTE["current"])
ax.plot([X(remaining)] * 2, [YM - 0.42, YM + HB / 2], color=PALETTE["current"],
        lw=1.0, ls=(0, (2, 2)), zorder=7)

# ---- the arithmetic, boxed ----------------------------------------------
ax.add_patch(FancyBboxPatch((0.10, 1.92), 2.90, 1.06,
                            boxstyle="round,pad=0.04", facecolor="#FBFBFD",
                            edgecolor=PALETTE["vessel"], lw=1.1, zorder=6))
ax.text(0.22, 2.90, "the geometry check, evaluated", fontsize=8.6, ha="left",
        va="top", color=PALETTE["vessel"], zorder=7)
ax.text(0.22, 2.68,
        r"$a=R_0/A=%.2f/%.0f=%.3f$ m" % (R0, A_ST, a) + "\n"
        r"$R_0-a=%.3f$ m" % inboard + "\n"
        r"$%.3f-%.3f-%.3f=\mathbf{%.3f}$ m" % (inboard, T_SHLD, T_WALL,
                                               remaining),
        fontsize=8.4, ha="left", va="top", zorder=7, linespacing=1.85)

ax.text(3.14, 2.94,
        r"against the study's stated $%.2f$ m centre column:" % R_CS_STUDY
        + "\n"
        r"a difference of $%.0f$ mm." % (1000 * slack),
        fontsize=8.4, ha="left", va="top", color="0.22", linespacing=1.7)
ax.text(3.14, 2.54,
        r"That $%.0f$ mm is NOT spare room. It is the residue of a" % (1000 * slack)
        + "\n"
        "check that has not yet paid for one cable, one support,\n"
        "one coolant channel, one tolerance, or the "
        "current-initiation\nfunction. The low-$A$ inboard budget is already "
        "measured\nin centimetres before engineering begins.",
        fontsize=8.0, ha="left", va="top", color=PALETTE["current"],
        linespacing=1.55)

ax.plot([0.10, W - 0.10], [1.78, 1.78], color="0.85", lw=0.9, zorder=1)
ax.text(0.10, 1.66,
        # Line lengths budgeted, not guessed: 6.66 in of usable width at
        # 7.9 pt in Computer Modern is about 118 characters. Overflow clips.
        "ILLUSTRATIVE PUBLISHED ALLOCATION, NOT A UNIVERSAL REACTOR TEMPLATE."
        r" The $%.2f$ m shield, the $%.0f$ mm" % (T_SHLD, 1000 * T_WALL)
        + "\n"
        r"first wall and the $%.2f$ m column are one study's choices, for one "
        r"mission and one set of material" % R_CS_STUDY
        + "\n"
        "assumptions. Change the mission and they change. What does NOT "
        "change is the ORDER: the neutron\n"
        "shield is sized by neutronics, not by what the magnet would prefer, "
        "so the magnet is designed into\n"
        "whatever is left. That ordering is the section's claim, and it is "
        "the only claim this figure makes.",
        fontsize=7.9, ha="left", va="top", color="0.30", linespacing=1.6)

save_exact(fig, "figS_st_radial_ledger",
           "Explanatory sketch; midplane cut drawn to scale in $R$. "
           "Subdivisions inside the centre-column envelope are indicative "
           "only.", y=0.06)
print(f"a={a:.4f}  R0-a={inboard:.4f}  remaining={remaining:.4f}  "
      f"study={R_CS_STUDY}  slack={1000*slack:.1f} mm")
