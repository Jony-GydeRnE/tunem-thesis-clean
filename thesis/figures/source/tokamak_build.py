#!/usr/bin/env python3
"""
tokamak_build.py — ONE reusable parametric model of the idealized tokamak.

Everything in the cumulative "machine-state" figure family (figM1 ... figM5)
is generated from this module.  Nothing here is drawn by hand or by an image
model: every curve is an analytic parametrization evaluated by numpy.

Design rules enforced structurally, not by discipline:

  * The machine is described by ONE flag set, STAGES.  Stage k's flag set is a
    strict superset of stage k-1's, so a component can never silently vanish
    from a later picture.  If you want to add a component, add a flag and put
    it in every later stage.
  * Every component has exactly one colour, defined once in PALETTE, used in
    both the 3-D panel and the poloidal cross-section.
  * The only free geometric inputs are R0, a, and (optionally) coil counts.
    Everything else is a fixed multiple of a, declared in Machine, so no
    engineering dimension is invented anywhere in the figure code.

Geometry conventions
--------------------
Cylindrical (R, phi, Z), Z the symmetry axis.  Torus surface at minor radius s:

    x = (R0 + s cos(theta)) cos(phi)
    y = (R0 + s cos(theta)) sin(phi)
    z =  s sin(theta)

theta = poloidal angle (short way round), phi = toroidal angle (long way round).

TF coils are drawn as *circular* loops of radius r_tf centred on the magnetic
axis and lying in planes containing the Z axis.  This is deliberate: it is the
exact object Ampere's law was applied to in the text (Eq. for B_phi).  A real
machine uses a D-shape for hoop-stress reasons that have not been derived yet,
so drawing a D here would be an invented engineering detail.

Author: Jony (TUNEM).  Run the figM*.py scripts, not this file.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Wedge
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from dataclasses import dataclass, field

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 10,
    "axes.linewidth": 0.8,
})

# --------------------------------------------------------------------------
# ONE palette.  Every component keeps this colour in every figure, forever.
# --------------------------------------------------------------------------
PALETTE = {
    "vessel":   "#263238",   # dark blue-grey  — vacuum vessel / chamber wall
    "vesselfc": "#ECEFF1",   #                 — its fill
    "plasma":   "#D81B60",   # dark pink       — plasma body
    "plasmafc": "#F8BBD0",   #                 — its fill
    "tf":       "#1565C0",   # blue            — toroidal-field coils
    "cs":       "#1B5E20",   # green           — central solenoid
    "pf":       "#EF6C00",   # orange          — external poloidal-field coils
    "bfield":   "#6A1B9A",   # purple          — magnetic field (B_phi, B_theta, B_v)
    "current":  "#B71C1C",   # bright red      — plasma current I_p / drive current
    "heat":     "#0097A7",   # teal            — auxiliary heating ports (NBI, RF)
    "guide":    "#9E9E9E",   # grey            — axes, dimensions, construction lines
    # --- the nuclear island, earned only at stage 13 (manuscript SS43-49) ---
    "wall":     "#8D6E63",   # light brown     — first wall
    "blanket":  "#5D4037",   # mid brown       — blanket / breeding region
    "shield":   "#3E2723",   # dark brown      — shield
}
HATCH = {"wall": "xxxx", "blanket": "////", "shield": "...."}

# --------------------------------------------------------------------------
# REDUNDANT ENCODING.  Colour alone cannot separate eight components on a
# black-and-white page: dL* >= 12 for all 28 pairs would need 7 x 12 = 84
# points of lightness, and the usable range on white paper (L* 18..62, the
# floor set by WCAG 1.4.11's 3:1 non-text contrast) is only 44.  The best
# achievable minimum gap is 44/7 = 6.3.  So LINE STYLE carries the identity
# and colour is the accelerator, never the sole channel.
# --------------------------------------------------------------------------
STYLE = {                       # (linestyle, linewidth-multiplier)
    "vessel":  ("solid",              1.35),
    "plasma":  ("solid",              0.90),
    "tf":      ((0, (7.0, 2.6)),      1.00),   # long dash
    "cs":      ((0, (1.2, 1.9)),      1.15),   # dotted
    "pf":      ((0, (9, 2.2, 1.6, 2.2)), 1.10),  # dash-dot
    "bfield":  ((0, (3.6, 2.0)),      1.00),   # short dash
    "current": ("solid",              1.45),
    "escape":  ("solid",              1.45),
    "heat":    ((0, (1.5, 1.6, 7, 1.6)), 1.10),  # dot-long-dash
    "wall":    ("solid",              0.85),
    "blanket": ("solid",              0.85),
    "shield":  ("solid",              0.85),
}
LS = {k: v[0] for k, v in STYLE.items()}
LW = {k: v[1] for k, v in STYLE.items()}

LEGEND_ORDER = ["vessel", "plasma", "tf", "cs", "pf", "bfield", "current",
                "escape", "heat", "wall", "blanket", "shield"]
LEGEND_LABEL = {
    "vessel":  "vacuum vessel (chamber wall)",
    "plasma":  "plasma / fuel region",
    "tf":      "toroidal-field (TF) coils",
    "cs":      "central solenoid (CS)",
    "pf":      "poloidal-field (PF) coils",
    "bfield":  r"magnetic field $\mathbf{B}$",
    "current": r"plasma current $I_p$",
    "escape":  "fuel escaping the open ends",
    "heat":    "auxiliary heating ports",
    "wall":    "first wall",
    "blanket": "blanket / breeding region",
    "shield":  "shield",
}
# Stage 1 has no torus yet: the same blue is a plain solenoid, and the same
# red marks escaping fuel rather than a driven current.  Override, do not
# silently mislabel.
LEGEND_OVERRIDE_S1 = {
    "tf":     "solenoid coil turns",
    "escape": "fuel escaping the open ends",
}
PALETTE["escape"] = PALETTE["current"]

DISCLAIMER = "Idealized schematic; not a fabrication drawing."


# --------------------------------------------------------------------------
# The parametric machine.  Only R0, a and the coil counts are meant to be
# changed.  Everything else is a declared multiple of a.
# --------------------------------------------------------------------------
@dataclass
class Machine:
    R0: float = 3.0          # major radius   [arb. length units]
    a:  float = 1.0          # plasma minor radius
    n_tf: int = 12           # number of TF coils drawn
    n_sol: int = 11          # number of solenoid turns drawn on the straight tube
    L_straight: float = 7.0  # length of the straight corridor (stage 1)

    # --- declared multiples of a (NOT engineering dimensions) ---------------
    f_wall: float = 1.18     # vessel wall at f_wall * a
    f_tf:   float = 1.48     # TF coil radius at f_tf * a
    f_cs_r: float = 0.42     # CS radius as a fraction of a
    f_cs_z: float = 2.55     # CS half-height as a multiple of a

    # --- boundary shape.  Standard Miller-type parametrization:
    #        R(th) = R0 + a cos(th + arcsin(delta) sin th)
    #        Z(th) = kappa a sin th
    #     kappa = 1, delta = 0 recovers the circle used in stages 1-5, so the
    #     earlier figures are the delta->0, kappa->1 limit of this one model
    #     rather than a separate drawing.
    kappa: float = 1.0       # elongation
    delta: float = 0.0       # triangularity

    @property
    def A(self):             # aspect ratio
        return self.R0 / self.a

    @property
    def a_wall(self):
        return self.f_wall * self.a

    @property
    def r_tf(self):
        return self.f_tf * self.a

    @property
    def r_cs(self):
        return self.f_cs_r * self.a

    @property
    def z_cs(self):
        return self.f_cs_z * self.a

    def boundary(self, s=None, n=400):
        """Shaped poloidal boundary at minor radius s (default: the plasma)."""
        s = self.a if s is None else s
        th = np.linspace(0, 2 * np.pi, n)
        d = np.arcsin(np.clip(self.delta, -0.95, 0.95))
        R = self.R0 + s * np.cos(th + d * np.sin(th))
        Z = self.kappa * s * np.sin(th)
        return R, Z

    @property
    def vfb_positions(self):
        """(R, Z, sign) of the vertical-feedback pair.  The two coils carry
        OPPOSITE currents (anti-series), which is what makes their combined
        field radial on the midplane and therefore able to push the plasma up
        or down.  A same-sign pair would only shift it radially."""
        R = self.R0 + 0.62 * self.a
        Z = self.kappa * self.r_tf + 0.42 * self.a
        return [(R, +Z, +1), (R, -Z, -1)]

    @property
    def pf_positions(self):
        """(R, Z) of the PF-coil cross-sections. Placed strictly OUTSIDE the
        TF-coil envelope so they can never be confused with a TF coil."""
        Rout = self.R0 + self.r_tf + 0.42 * self.a
        Zup  = self.kappa * self.r_tf + 0.55 * self.a
        Rin  = self.R0 - 0.28 * self.a
        Zmid = self.kappa * 0.62 * self.a
        return [(Rout,  Zmid), (Rout, -Zmid), (Rin, Zup), (Rin, -Zup)]


# ==========================================================================
#  STAGES — the cumulative flag sets.  Superset property is asserted below.
# ==========================================================================
_S1 = {"straight_vessel", "sol_turns", "straight_plasma", "B_axial", "open_ends"}
_S2 = {"torus_vessel", "tf_coils", "torus_plasma", "B_phi", "dims_R0a"}
_S3 = _S2 | {"cs", "Ip", "B_theta"}
_S4 = _S3 | {"pf_coils", "B_v"}
_S5 = _S4 | {"nbi", "rf"}
_S6 = _S5 | {"elongation"}                 # kappa > 1
_S7 = _S6 | {"vfb"}                        # vertical-feedback coil pair
_S8 = _S7 | {"triangularity"}              # delta > 0
_S9  = _S8 | {"equil_shift"}               # p(psi)/current change moves the axis
_S10 = _S9 | {"alpha", "neutron"}          # self-heating vs. escaping neutrons
_S11 = _S10 | {"ledger"}                   # I_p = I_ohm + I_CD + I_bs
_S12 = _S11 | {"atlas"}                    # capstone: component -> variable map
_S13 = _S12 | {"island"}                   # first wall + blanket + shield: bracket b
_S14 = _S13 | {"radial_build", "tf_sized"}  # coil build c, R_in, B_max
# "tf_sized" marks the stage at which the TF coil's THICKNESS c stops being an
# open parameter (manuscript SS47-48).  It does NOT change how the component is
# drawn.
#
# Cumulative depiction convention: A COMPONENT STAYS SOLID ONCE ITS
# FUNCTION HAS BEEN DERIVED.  An open parameter is shown with a BRACKET or a
# "thickness c: to be derived" ANNOTATION -- never by demoting the component to
# a dashed or ghosted outline.
#
# Two reasons it is the right call.  First, un-drawing something the text has
# already earned contradicts the figure immediately before it and breaks the one
# promise this family makes.  Second, "dashed" is not even available: every
# component carries its own dash pattern as its IDENTITY in greyscale (see
# STYLE), so overloading that channel would destroy the one encoding that
# survives a monochrome printer.  The annotation channel is free; the identity
# channel is not.

# Two annotation layers plus the low-A state, numbered out of the hardware
# sequence for the same reason 7a/7b are: they add no component, so inserting
# them in-sequence would renumber every later state for no physical reason.
_S17 = _S7  | {"atlas1"}                   # numbered atlas over the stage-7 machine
_S18 = _S14 | {"hifield"}                  # conductor-technology callout on c
_S19 = _S14 | {"centrestack"}              # low-A: c_cs resolved, R_cs scarce

STAGES = {
    1: dict(flags=_S1, title=r"Stage 1 — the straight magnetic corridor",
            sub=r"a solenoid makes $B_\parallel$; the ends are open, so the fuel leaves"),
    2: dict(flags=_S2, title=r"Stage 2 — the corridor is closed into a torus",
            sub=r"the same tube bent end-to-end; TF coils now make $B_\varphi\propto 1/R$"),
    3: dict(flags=_S3, title=r"Stage 3 — the tokamak field: a central solenoid drives $I_p$",
            sub=r"the plasma's own current supplies $B_\theta$, so field lines become helical"),
    4: dict(flags=_S4, title=r"Stage 4 — equilibrium and position control",
            sub=r"external PF coils apply a vertical field $B_v$ to hold the current ring at $R_0$"),
    5: dict(flags=_S5, title=r"Stage 5 — auxiliary heating",
            sub=r"a neutral beam and an RF launcher add power the transformer cannot"),
    6: dict(flags=_S6, shape=dict(kappa=1.70, delta=0.0),
            title=r"Stage 6 — the boundary is elongated ($\kappa>1$)",
            sub=r"a taller cross-section buys area, hence $I_p$ at fixed $q_*$; "
                r"the coil set follows the same boundary"),
    7: dict(flags=_S7, shape=dict(kappa=1.70, delta=0.0),
            title=r"Stage 7 — elongation is unstable, so it must be fed back",
            sub=r"an anti-series coil pair supplies the radial field that "
                r"opposes vertical displacement"),
    8: dict(flags=_S8, shape=dict(kappa=1.70, delta=0.40),
            title=r"Stage 8 — triangularity ($\delta>0$) is added",
            sub=r"the outboard corners are pulled apart; the machine is now "
                r"the shaped conventional tokamak"),
    9: dict(flags=_S9, shape=dict(kappa=1.70, delta=0.40),
            title=r"Stage 9 — the same machine, a different equilibrium",
            sub=r"raise $p(\psi)$ or lower $I_p$ and the axis shifts outward; "
                r"the PF currents must change to put it back"),
    10: dict(flags=_S10, shape=dict(kappa=1.70, delta=0.40),
             title=r"Stage 10 — the fuel begins to heat itself",
             sub=r"the $3.5\,$MeV alpha is charged and stays; the "
                 r"$14.1\,$MeV neutron is not, and leaves through a boundary "
                 r"this figure deliberately does not yet draw"),
    11: dict(flags=_S11, shape=dict(kappa=1.70, delta=0.40),
             title=r"Stage 11 — the plasma current has three sources",
             sub=r"$I_p=I_{\rm ohm}+I_{\rm CD}+I_{\rm bs}$: the transformer, "
                 r"the launchers, and the pressure gradient itself"),
    12: dict(flags=_S12, shape=dict(kappa=1.70, delta=0.40),
             title=r"Atlas — the conventional tokamak, and what each part buys",
             sub=r"every component derived so far, and the design variable it "
                 r"puts into the Part II audit. No later reactor hardware."),
    13: dict(flags=_S13, shape=dict(kappa=1.70, delta=0.40),
             title=r"Stage 13 — the earned nuclear island",
             sub=r"the neutron that left at stage 10 has to stop somewhere: "
                 r"first wall, blanket, shield. Their total thickness is $b$."),
    # Two annotation layers over the elongated, feedback-controlled machine.
    # They are NOT new hardware, so they are numbered out of the hardware
    # sequence and named figM7a / figM7b: inserting them as 8 and 9 would
    # renumber every later state for no physical reason.
    15: dict(flags=_S7 | {"profile"}, shape=dict(kappa=1.70, delta=0.0),
             stem="figM7a_profile",
             title=r"Stage 7a — total current is not the same as its profile",
             sub=r"the solenoid and the launchers do not just set $I_p$; "
                 r"they set where the current sits, $j_\varphi(r)$, and that "
                 r"is what fixes $q(r)$"),
    16: dict(flags=_S7 | {"perf"}, shape=dict(kappa=1.70, delta=0.0),
             stem="figM7b_performance",
             title=r"Stage 7b — the performance quantities live on the machine",
             sub=r"every symbol in the fusion-power scaling is a feature you "
                 r"can point at"),
    19: dict(flags=_S19, shape=dict(kappa=1.70, delta=0.40),
             stem="figM16_centrestack",
             title=r"Low aspect ratio — the centre stack becomes the "
                   r"scarce interval",
             sub=r"the same inventory as stage 14, at $A=2$: the plasma, the "
                 r"nuclear island $b$ and the TF function are all preserved"),
    17: dict(flags=_S17, shape=dict(kappa=1.70, delta=0.0),
             stem="figM7c_atlas1",
             title=r"Atlas checkpoint — what has actually been derived so far",
             sub=r"every component on the machine at this point, numbered by "
                 r"the section that forced it. Nothing later appears."),
    18: dict(flags=_S18, shape=dict(kappa=1.70, delta=0.40),
             stem="figM15_highfield",
             title=r"High-field design state — the inboard coil acquires a "
                   r"technology requirement",
             sub=r"the same machine as stage 14. Only the coil bracket $c$ is "
                 r"resolved further, and the demand it now carries is named"),
    14: dict(flags=_S14, shape=dict(kappa=1.70, delta=0.40),
             title=r"Stage 14 — the complete radial build",
             sub=r"$R_{\rm in}=R_0-a-b-c$ is what the inboard side leaves for "
                 r"the coil, and that is what caps $B_0$"),
}

# PRESENTATION flags are not machine components.  They are one-off ways of
# LOOKING at the machine -- an accounting inset, a ghost boundary showing a
# different operating point, illustrative particle tracks, the atlas table.
# Carrying them forward is the same mistake as carrying every caption forward:
# by stage 14 the panel had an atlas table, a current ledger and a shifted
# ghost plasma all on top of the machine.  They are drawn ONLY on the stage
# that introduces them, and are excluded from the superset check below --
# which is, correctly, a statement about hardware.
PRESENTATION = {"atlas", "ledger", "equil_shift", "alpha", "neutron",
                "profile", "perf", "atlas1", "hifield", "centrestack"}
PRESENTATION_INTRO = {"equil_shift": 9, "alpha": 10, "neutron": 10,
                      "ledger": 11, "atlas": 12, "profile": 15, "perf": 16,
                      "atlas1": 17, "hifield": 18, "centrestack": 19}

# Structural guarantee: no COMPONENT is ever lost between consecutive stages.
for _k in range(2, 15):
    _prev, _cur = STAGES[_k - 1]["flags"], STAGES[_k]["flags"]
    if _k > 2:
        assert (_prev - PRESENTATION) <= (_cur - PRESENTATION), \
            f"stage {_k} dropped components from stage {_k-1}"


# ==========================================================================
#  PRIMITIVE GEOMETRY  (pure numpy — every point is computed, none is drawn)
# ==========================================================================
def torus_surface(m: Machine, s, phi0=0.0, phi1=2 * np.pi, nth=48, nph=140):
    """Axisymmetric surface swept by the shaped boundary at minor radius s."""
    th = np.linspace(0, 2 * np.pi, nth)
    ph = np.linspace(phi0, phi1, nph)
    TH, PH = np.meshgrid(th, ph)
    d = np.arcsin(np.clip(m.delta, -0.95, 0.95))
    R = m.R0 + s * np.cos(TH + d * np.sin(TH))
    x = R * np.cos(PH)
    y = R * np.sin(PH)
    z = m.kappa * s * np.sin(TH)
    return x, y, z


def tube_surface(m: Machine, s, nth=48, nx=2):
    """Straight circular tube along the x-axis, centred on the origin."""
    th = np.linspace(0, 2 * np.pi, nth)
    xs = np.linspace(-m.L_straight / 2, m.L_straight / 2, nx)
    TH, X = np.meshgrid(th, xs)
    y = s * np.cos(TH)
    z = s * np.sin(TH)
    return X, y, z


def tf_coil_loop(m: Machine, phi, n=220):
    """TF coil in the plane containing the Z axis at toroidal angle phi.

    It is the SHAPED boundary scaled out to r_tf, so that when the plasma is
    elongated the coil set follows it.  For kappa = 1, delta = 0 this reduces
    exactly to the circle of radius r_tf used in stages 1-5."""
    t = np.linspace(0, 2 * np.pi, n)
    d = np.arcsin(np.clip(m.delta, -0.95, 0.95))
    R = m.R0 + m.r_tf * np.cos(t + d * np.sin(t))
    Z = m.kappa * m.r_tf * np.sin(t)
    return R * np.cos(phi), R * np.sin(phi), Z


def ring(R, Z, n=200):
    """A horizontal current ring of radius R at height Z (PF coil, plasma axis)."""
    t = np.linspace(0, 2 * np.pi, n)
    return R * np.cos(t), R * np.sin(t), np.full_like(t, Z)


def cs_cylinder(m: Machine, n=64):
    t = np.linspace(0, 2 * np.pi, n)
    z = np.array([-m.z_cs, m.z_cs])
    T, Z = np.meshgrid(t, z)
    return m.r_cs * np.cos(T), m.r_cs * np.sin(T), Z


def helix_on_torus(m: Machine, s, q=3.0, n=1400, turns=1.0):
    """Field line with safety factor q: q toroidal circuits per poloidal circuit."""
    th = np.linspace(0, 2 * np.pi * turns, n)
    ph = q * th
    R = m.R0 + s * np.cos(th)
    return R * np.cos(ph), R * np.sin(ph), s * np.sin(th)


# ==========================================================================
#  3-D PANEL
# ==========================================================================
def _cutaway(flags):
    """Toroidal wedge removed from the vessel so the interior is visible.
    The gap is centred on phi = 300 deg, which is the near side of the torus
    for the fixed camera azimuth of -60 deg used in draw_3d.  The gap is kept
    narrow (36 deg) so that stage 2 still reads as a CLOSED tube --- which is
    the entire physical point of that stage."""
    return (np.deg2rad(342), np.deg2rad(342 + 324))


def draw_3d(ax, m: Machine, flags):
    used = []

    # ---------------- Stage 1: straight corridor -------------------------
    if "straight_vessel" in flags:
        X, Y, Z = tube_surface(m, m.a_wall)
        ax.plot_surface(X, Y, Z, color=PALETTE["vessel"], alpha=0.13,
                        edgecolor=PALETTE["vessel"], linewidth=0.25,
                        rstride=1, cstride=3, shade=False)
        # open ends drawn explicitly as rings, with NO end cap
        for xe in (-m.L_straight / 2, m.L_straight / 2):
            t = np.linspace(0, 2 * np.pi, 120)
            ax.plot(np.full_like(t, xe), m.a_wall * np.cos(t), m.a_wall * np.sin(t),
                    color=PALETTE["vessel"], lw=1.8)
        used.append("vessel")

    if "straight_plasma" in flags:
        X, Y, Z = tube_surface(m, m.a)
        ax.plot_surface(X, Y, Z, color=PALETTE["plasmafc"], alpha=0.55,
                        edgecolor="none", rstride=1, cstride=3, shade=False)
        used.append("plasma")

    if "sol_turns" in flags:
        t = np.linspace(0, 2 * np.pi, 160)
        for xc in np.linspace(-m.L_straight / 2 * 0.86, m.L_straight / 2 * 0.86, m.n_sol):
            ax.plot(np.full_like(t, xc), m.r_tf * np.cos(t), m.r_tf * np.sin(t),
                    color=PALETTE["tf"], lw=1.6, ls=LS["tf"], alpha=0.95)
        used.append("tf")

    if "B_axial" in flags:
        for xs in np.linspace(-2.6, 2.0, 5):
            ax.quiver(xs, 0, 0, 1.05, 0, 0, color=PALETTE["bfield"],
                      lw=2.0, arrow_length_ratio=0.28)
        used.append("bfield")

    if "open_ends" in flags:
        for sgn in (-1, 1):
            ax.quiver(sgn * m.L_straight / 2, 0, 0, sgn * 1.5, 0, 0,
                      color=PALETTE["escape"], lw=2.4, arrow_length_ratio=0.32)
        used.append("escape")

    # ---------------- Stage 2+: the torus --------------------------------
    if "torus_vessel" in flags:
        p0, p1 = _cutaway(flags)
        X, Y, Z = torus_surface(m, m.a_wall, p0, p1)
        ax.plot_surface(X, Y, Z, color=PALETTE["vessel"], alpha=0.11,
                        edgecolor=PALETTE["vessel"], linewidth=0.15,
                        rstride=3, cstride=4, shade=False)
        # the two cut faces, so the wall thickness / cutaway reads as deliberate
        for p in (p0, p1):
            t = np.linspace(0, 2 * np.pi, 120)
            R = m.R0 + m.a_wall * np.cos(t)
            ax.plot(R * np.cos(p), R * np.sin(p), m.a_wall * np.sin(t),
                    color=PALETTE["vessel"], lw=1.6)
        used.append("vessel")

    if "torus_plasma" in flags:
        p0, p1 = _cutaway(flags)
        X, Y, Z = torus_surface(m, m.a, p0, p1)
        ax.plot_surface(X, Y, Z, color=PALETTE["plasmafc"], alpha=0.62,
                        edgecolor="none", rstride=3, cstride=4, shade=False)
        used.append("plasma")

    if "tf_coils" in flags:
        # An elongated coil set overlaps itself badly in projection, so draw
        # fewer of them once kappa > 1.2.  The count is cosmetic in the 3-D
        # panel -- the poloidal panel is where coil identity is established --
        # and the figure footer states how many are drawn.
        n_draw = m.n_tf if m.kappa <= 1.2 else max(6, m.n_tf // 2)
        for phi in np.linspace(0, 2 * np.pi, n_draw, endpoint=False):
            x, y, z = tf_coil_loop(m, phi)
            ax.plot(x, y, z, color=PALETTE["tf"], lw=1.25,
                    ls=LS["tf"], alpha=0.85)
        used.append("tf")

    if "B_phi" in flags:
        # B_phi along the magnetic axis, drawn only in the cut-open sector
        for phi in np.linspace(np.deg2rad(340), np.deg2rad(340) + 1.9 * np.pi, 7):
            x, y = m.R0 * np.cos(phi), m.R0 * np.sin(phi)
            dx, dy = -np.sin(phi) * 0.95, np.cos(phi) * 0.95
            ax.quiver(x, y, 0, dx, dy, 0, color=PALETTE["bfield"],
                      lw=1.9, arrow_length_ratio=0.35)
        used.append("bfield")

    if "cs" in flags:
        X, Y, Z = cs_cylinder(m)
        ax.plot_surface(X, Y, Z, color=PALETTE["cs"], alpha=0.55,
                        edgecolor=PALETTE["cs"], linewidth=0.4,
                        rstride=1, cstride=4, shade=False)
        for zc in (-m.z_cs, m.z_cs):
            t = np.linspace(0, 2 * np.pi, 90)
            ax.plot(m.r_cs * np.cos(t), m.r_cs * np.sin(t), np.full_like(t, zc),
                    color=PALETTE["cs"], lw=1.6)
        used.append("cs")

    if "Ip" in flags:
        # the plasma current ring itself, on the magnetic axis
        x, y, z = ring(m.R0, 0.0)
        ax.plot(x, y, z, color=PALETTE["current"], lw=2.4, alpha=0.95)
        for phi in np.linspace(np.deg2rad(40), np.deg2rad(40) + 1.6 * np.pi, 5):
            xx, yy = m.R0 * np.cos(phi), m.R0 * np.sin(phi)
            ax.quiver(xx, yy, 0, -np.sin(phi) * 0.8, np.cos(phi) * 0.8, 0,
                      color=PALETTE["current"], lw=2.2, arrow_length_ratio=0.4)
        used.append("current")

    if "B_theta" in flags:
        # one poloidal loop of B_theta, in the open sector
        phi = np.deg2rad(180)
        t = np.linspace(0, 2 * np.pi, 200)
        s = 0.62 * m.a
        R = m.R0 + s * np.cos(t)
        ax.plot(R * np.cos(phi), R * np.sin(phi), s * np.sin(t),
                color=PALETTE["bfield"], lw=2.0)

    if "pf_coils" in flags:
        for (Rp, Zp) in m.pf_positions:
            x, y, z = ring(Rp, Zp)
            ax.plot(x, y, z, color=PALETTE["pf"], lw=1.5,
                    ls=LS["pf"], alpha=0.8)
        used.append("pf")

    if "nbi" in flags:
        # tangential neutral-beam line entering the outboard midplane
        phi_t = np.deg2rad(150)
        Rt = m.R0 + 0.25 * m.a
        xt, yt = Rt * np.cos(phi_t), Rt * np.sin(phi_t)
        ux, uy = -np.sin(phi_t), np.cos(phi_t)      # tangent to the axis circle
        Ls = 3.3
        ax.plot([xt - ux * Ls, xt], [yt - uy * Ls, yt], [0, 0],
                color=PALETTE["heat"], lw=2.6)
        ax.quiver(xt - ux * 1.1, yt - uy * 1.1, 0, ux * 1.0, uy * 1.0, 0,
                  color=PALETTE["heat"], lw=2.4, arrow_length_ratio=0.45)
        used.append("heat")

    if "rf" in flags:
        # RF launcher: a short radial waveguide stub on the outboard midplane
        phi_r = np.deg2rad(300)
        R1, R2 = m.R0 + m.a_wall + 1.35 * m.a, m.R0 + m.a_wall
        ax.plot([R1 * np.cos(phi_r), R2 * np.cos(phi_r)],
                [R1 * np.sin(phi_r), R2 * np.sin(phi_r)], [0, 0],
                color=PALETTE["heat"], lw=2.6)
        ax.quiver(R1 * np.cos(phi_r), R1 * np.sin(phi_r), 0,
                  (R2 - R1) * np.cos(phi_r) * 0.75, (R2 - R1) * np.sin(phi_r) * 0.75, 0,
                  color=PALETTE["heat"], lw=2.4, arrow_length_ratio=0.45)
        used.append("heat")

    # ---------------- framing --------------------------------------------
    # True isotropic scaling: box_aspect is set from the actual data ranges,
    # so nothing is stretched. Only the z window is cropped to the real extent.
    if "torus_vessel" in flags:
        lim = m.R0 + m.r_tf + 0.60 * m.a
        zhi = max(m.r_tf, m.z_cs if "cs" in flags else 0.0,
                  max((abs(z) for _, z in m.pf_positions), default=0.0)
                  if "pf_coils" in flags else 0.0) + 0.35 * m.a
        ax.view_init(elev=30, azim=-60)
    else:
        lim = m.L_straight / 2 + 2.0
        zhi = m.r_tf + 0.5 * m.a
        ax.view_init(elev=22, azim=-62)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-zhi, zhi)
    ax.set_box_aspect((1.0, 1.0, zhi / lim))
    ax.set_axis_off()

    # dedupe, keep canonical order
    return [k for k in LEGEND_ORDER if k in used]


# ==========================================================================
#  CROSS-SECTION PANEL  (poloidal for the torus; longitudinal for stage 1)
# ==========================================================================
def _odot(ax, x, y, r, color, z=6):
    """Current-out-of-page symbol, sized in data units."""
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.4, zorder=z))
    ax.add_patch(Circle((x, y), 0.30 * r, fc=color, ec=color, zorder=z + 1))


def draw_longitudinal(ax, m: Machine, flags):
    """Stage 1 only: a cut along the straight tube."""
    L, aw, a = m.L_straight, m.a_wall, m.a
    ax.add_patch(Rectangle((-L / 2, -a), L, 2 * a, fc=PALETTE["plasmafc"],
                           ec="none", zorder=1))
    for s in (aw, -aw):
        ax.plot([-L / 2, L / 2], [s, s], color=PALETTE["vessel"], lw=2.0, zorder=3)
    # explicit open ends: dashed, no wall
    for xe in (-L / 2, L / 2):
        ax.plot([xe, xe], [-aw, aw], color=PALETTE["vessel"], lw=1.0,
                ls=(0, (3, 3)), zorder=3)

    # solenoid turns seen edge-on: current out of page above, into page below
    for xc in np.linspace(-L / 2 * 0.86, L / 2 * 0.86, m.n_sol):
        ax.add_patch(Circle((xc,  m.r_tf), 0.115, fc="white",
                            ec=PALETTE["tf"], lw=1.5, zorder=5))
        ax.plot([xc], [m.r_tf], marker="o", ms=3.0, color=PALETTE["tf"], zorder=6)
        ax.add_patch(Circle((xc, -m.r_tf), 0.115, fc="white",
                            ec=PALETTE["tf"], lw=1.5, zorder=5))
        d = 0.115 / np.sqrt(2)
        ax.plot([xc - d, xc + d], [-m.r_tf - d, -m.r_tf + d],
                color=PALETTE["tf"], lw=1.2, zorder=6)
        ax.plot([xc - d, xc + d], [-m.r_tf + d, -m.r_tf - d],
                color=PALETTE["tf"], lw=1.2, zorder=6)

    for ys in (-0.5 * a, 0.0, 0.5 * a):
        for xs in np.linspace(-L / 2 * 0.74, L / 2 * 0.40, 3):
            ax.annotate("", xy=(xs + 1.5, ys), xytext=(xs, ys),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["bfield"],
                                        lw=1.7, shrinkA=0, shrinkB=0), zorder=4)

    for ys in (0.55 * a, -0.55 * a):
        ax.annotate("", xy=(L / 2 + 1.75, ys), xytext=(L / 2 - 0.15, ys),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                                    lw=2.2, shrinkA=0, shrinkB=0), zorder=6)
        ax.annotate("", xy=(-L / 2 - 1.75, ys), xytext=(-L / 2 + 0.15, ys),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                                    lw=2.2, shrinkA=0, shrinkB=0), zorder=6)

    ax.text(0, m.r_tf + 0.34, r"solenoid turns  ($\odot$ out of page, "
                              r"$\otimes$ into page)",
            color=PALETTE["tf"], fontsize=9, ha="center", va="bottom")
    ax.text(0, -m.r_tf - 0.34, "vacuum chamber wall", color=PALETTE["vessel"],
            fontsize=9, ha="center", va="top")
    ax.text(0.0, 0.74 * a, r"$\mathbf{B}=B\,\hat{\mathbf{x}}$   (uniform, axial)",
            color=PALETTE["bfield"], fontsize=10, ha="center", va="center",
            zorder=8)
    ax.text(L / 2 + 1.90, 1.28 * a, "OPEN END\nfuel streams out\nalong $\\mathbf{B}$",
            color=PALETTE["escape"], fontsize=9, ha="center", va="center")
    ax.text(-L / 2 - 1.90, 1.28 * a, "OPEN END\n(same loss,\nother way)",
            color=PALETTE["escape"], fontsize=9, ha="center", va="center")
    ax.text(0, -0.72 * a, "plasma / fuel region", color=PALETTE["plasma"],
            fontsize=9.5, ha="center", va="center", zorder=4)

    ax.set_xlim(-L / 2 - 3.3, L / 2 + 3.3)
    ax.set_ylim(-m.r_tf - 1.05, m.r_tf + 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("longitudinal section", fontsize=10, pad=2)


def draw_poloidal(ax, m: Machine, flags, stage=None):
    """Stages 2-5: the R-Z plane at fixed toroidal angle.

    Label discipline.  The panel is divided into reserved zones and nothing is
    ever written outside its zone, so no two labels can collide:

        inboard channel  0.42a < R < R0-r_tf   : nothing but the CS
        machine zone     the vessel and coils  : one-token math labels only
        label column     R > R0+r_tf+0.7a      : all prose, on fixed y-slots
        bottom band      Z < -(ztop)           : CS caption and the dimensions

    Each prose label is joined to the thing it names by a thin leader line.
    """
    R0, a, aw, rtf = m.R0, m.a, m.a_wall, m.r_tf
    ztop = max(rtf, m.z_cs) + 0.55 * a
    XLAB = R0 + rtf + 0.80 * a           # left edge of the prose label column
    # Prose labels are COLLECTED here and only placed at the end of the
    # function, on slots spaced evenly over the available height.  Hand-tuned
    # slot constants stop working the moment a stage adds a label; this scales.
    _pending = []

    def prose(key, text, anchor, color, intro=None, va="center"):
        """Explanatory caption for a component.

        CUMULATIVE COMPONENTS, NOT CUMULATIVE CAPTIONS.  The superset rule is
        about the machine: every part introduced must still be DRAWN in every
        later figure, and it stays in the legend.  Its paragraph of prose is a
        different thing -- it belongs to the moment the text derives that part.
        Carrying all of them forward puts seven multi-line captions in one
        column by stage 11, which is unreadable and helps nobody.

        `intro` is the stage that first needs the explanation; the caption is
        drawn only there.  Pass intro=None to show it on every stage."""
        if intro is not None and stage is not None and stage != intro:
            return
        _pending.append((key, text, anchor, color, va))

    def _flush_prose(top, bottom):
        if not _pending:
            return
        n = len(_pending)
        ys = ([0.5 * (top + bottom)] if n == 1
              else list(np.linspace(top, bottom, n)))
        for (key, text, anchor, color, va), y in zip(_pending, ys):
            ax.text(XLAB, y, text, color=color, fontsize=9, ha="left",
                    va="center", zorder=10)
            # leader drawn explicitly: annotate would route it from the text
            # bbox CENTRE, i.e. straight through the neighbouring labels
            ax.plot([XLAB - 0.10, anchor[0]], [y, anchor[1]], color=color,
                    lw=0.7, zorder=9, solid_capstyle="butt")

    # ---- symmetry axis --------------------------------------------------
    ax.plot([0, 0], [-ztop, ztop], color=PALETTE["guide"], lw=1.0, ls=(0, (5, 4)))
    ax.text(0, ztop + 0.12, "symmetry axis", color=PALETTE["guide"],
            fontsize=9, ha="center", va="bottom")

    # ---- vertical field, drawn first so everything sits on top -----------
    if "B_v" in flags:
        for Rv in np.linspace(R0 - 1.62 * a, R0 + 1.62 * a, 7):
            ax.annotate("", xy=(Rv, 1.86 * a), xytext=(Rv, -1.86 * a),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["pf"],
                                        lw=0.9, alpha=0.45), zorder=1)

    # ---- central solenoid ------------------------------------------------
    if "cs" in flags:
        ax.add_patch(Rectangle((-m.r_cs, -m.z_cs), 2 * m.r_cs, 2 * m.z_cs,
                               fc="none", ec=PALETTE["cs"], lw=1.8,
                               hatch="////", zorder=3))
        ax.text(0, -m.z_cs - 0.16, "central\nsolenoid", color=PALETTE["cs"],
                fontsize=9, ha="center", va="top")

    # ---- TF coil: dashed outline + the two points where it pierces --------
    if "tf_coils" in flags:
        Rc_, Zc_ = m.boundary(rtf)
        ax.plot(Rc_, Zc_, color=PALETTE["tf"], lw=1.1, alpha=0.5,
                ls=(0, (4, 3)), zorder=2)
        # The marker is the SAME at every stage. The coil was earned in SS4 and
        # it is drawn solid from the figure that earns it onward, full stop.
        for Rc in (R0 - rtf, R0 + rtf):   # midplane, where Z = 0 for any shape
            ax.add_patch(Circle((Rc, 0), 0.165, fc=PALETTE["tf"],
                                ec="black", lw=0.9, zorder=6))
        # A STANDING annotation, not a caption: it is present on every stage
        # where c is still open, and disappears the moment SS47-48 closes it.
        # This is the mechanism the ruling asks for -- the open parameter is
        # named in text, and the component itself is never touched.
        if "tf_sized" not in flags:
            ax.annotate("$c$ : to be derived (§47–48)",
                        xy=(R0 + rtf, -0.19), xytext=(R0 + rtf, -0.98),
                        fontsize=7.6, ha="center", va="top",
                        color=PALETTE["tf"], zorder=9,
                        arrowprops=dict(arrowstyle="-", color=PALETTE["tf"],
                                        lw=0.7, shrinkA=1, shrinkB=1),
                        bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))
        if "tf_sized" in flags:
            prose("tf", "TF coil seen edge-on (it pierces this plane twice).\n"
                        r"Its thickness $c$ is no longer open: \S47--48 derived"
                        "\nit, and the ruler below brackets it.",
                  (R0 + rtf * np.cos(1.15), rtf * np.sin(1.15)), PALETTE["tf"],
                  intro=2)
        else:
            prose("tf", "TF coil seen edge-on (it pierces this plane twice).\n"
                        r"Thickness $c$: TO BE DERIVED (\S47--48). The coil is"
                        "\nsolid because \S4 earned it; only $c$ is still open.",
                  (R0 + rtf * np.cos(1.15), rtf * np.sin(1.15)), PALETTE["tf"],
                  intro=2)

    # ---- vessel + plasma --------------------------------------------------
    Rw, Zw = m.boundary(aw)
    Rp, Zp = m.boundary(a)
    ax.fill(Rw, Zw, facecolor=PALETTE["vesselfc"], edgecolor=PALETTE["vessel"],
            lw=2.4, ls=LS["vessel"], zorder=3)
    ax.fill(Rp, Zp, facecolor=PALETTE["plasmafc"], edgecolor=PALETTE["plasma"],
            lw=1.5, ls=LS["plasma"], zorder=4)

    # ---- B_phi and I_p: both out of the page, stacked on the inboard half --
    if "B_phi" in flags:
        yq = 0.42 * a if "Ip" in flags else 0.0
        _odot(ax, R0 - 0.40 * a, yq, 0.125, PALETTE["bfield"], z=7)
        ax.text(R0 - 0.40 * a - 0.21, yq, r"$B_\varphi$", color=PALETTE["bfield"],
                fontsize=11, ha="right", va="center", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.8))
    if "Ip" in flags:
        _odot(ax, R0 - 0.40 * a, -0.42 * a, 0.125, PALETTE["current"], z=7)
        ax.text(R0 - 0.40 * a - 0.21, -0.42 * a, r"$I_p$", color=PALETTE["current"],
                fontsize=11, ha="right", va="center", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.8))

    # ---- B_theta ----------------------------------------------------------
    if "B_theta" in flags:
        # B_theta lies ON a flux surface, so it must follow the SHAPED
        # boundary.  Drawing it as a circle inside an elongated plasma (which
        # is what this did until 6 Aug) asserts something false about the
        # field geometry.
        Rb, Zb = m.boundary(0.84 * a, n=240)
        ax.plot(Rb, Zb, color=PALETTE["bfield"], lw=1.7, ls=LS["bfield"],
                zorder=5)
        n = len(Rb)
        for j in (int(0.30 * n), int(0.73 * n)):  # CCW, as I_p out of page needs
            ax.annotate("", xy=(Rb[j + 6], Zb[j + 6]), xytext=(Rb[j], Zb[j]),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["bfield"],
                                        lw=1.7), zorder=6)
        j = int(0.94 * n)
        prose("bth", r"$B_\theta$: made by $I_p$ alone," "\n"
                     "not by any external coil",
              (Rb[j], Zb[j]), PALETTE["bfield"], intro=3)

    # ---- PF coils ---------------------------------------------------------
    if "pf_coils" in flags:
        for (Rp, Zp) in m.pf_positions:
            ax.add_patch(Rectangle((Rp - 0.155, Zp - 0.155), 0.31, 0.31,
                                   fc=PALETTE["pf"], ec="black", lw=0.9, zorder=7))
        prose("pf", "PF coils (square markers,\noutside the TF envelope):\n"
                    r"they apply the vertical field $B_v\hat{\mathbf{Z}}$"
                    "\nthat holds the current ring at $R_0$",
              m.pf_positions[0], PALETTE["pf"], intro=4)

    # ---- heating ----------------------------------------------------------
    if "nbi" in flags:
        xtail = XLAB - 0.25 * a
        ax.annotate("", xy=(R0 + 0.25 * a, 0), xytext=(xtail, 0),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["heat"], lw=2.3),
                    zorder=8)
        prose("nbi", "neutral beam (enters as atoms,\nionizes inside)",
              (xtail - 0.02, 0), PALETTE["heat"], intro=5)
    if "rf" in flags:
        xw, yw = XLAB + 0.15 * a, -2.45 * a
        ax.add_patch(Rectangle((xw, yw - 0.21), 0.60, 0.42,
                               fc="white", ec=PALETTE["heat"], lw=1.6, zorder=8))
        tw = np.linspace(0, 1, 90)
        ax.plot(xw - 0.06 - tw * 1.15, yw + 0.11 * np.sin(tw * 7 * np.pi),
                color=PALETTE["heat"], lw=1.4, zorder=8)
        ax.annotate("", xy=(xw - 1.32, yw), xytext=(xw - 1.22, yw),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["heat"], lw=1.7),
                    zorder=8)
        if stage in (None, 5):
            ax.text(xw + 0.72, yw, "RF launcher\n(resonant wave heating)",
                    color=PALETTE["heat"], fontsize=9, ha="left", va="center")
        # RF gets a fixed row rather than a column slot: it carries a drawn
        # waveguide glyph, which cannot float with the text.

    # ---- vertical-feedback pair -------------------------------------------
    if "vfb" in flags:
        for (Rv, Zv, sign) in m.vfb_positions:
            ax.add_patch(Rectangle((Rv - 0.155, Zv - 0.155), 0.31, 0.31,
                                   fc="white", ec=PALETTE["pf"], lw=1.8, zorder=7))
            ax.text(Rv, Zv, r"$\odot$" if sign > 0 else r"$\otimes$",
                    color=PALETTE["pf"], fontsize=8, ha="center", va="center",
                    zorder=8)
        # the destabilizing direction the pair exists to oppose, offset from
        # the delta-a dimension so the two never share a column
        xarr = R0 + 0.48 * a
        ax.annotate("", xy=(xarr, m.kappa * a + 0.78 * a),
                    xytext=(xarr, m.kappa * a + 0.14 * a),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["plasma"],
                                    lw=1.6, ls=(0, (2, 1.6))), zorder=8)
        ax.text(xarr - 0.10, m.kappa * a + 0.46 * a, "unstable",
                color=PALETTE["plasma"], fontsize=8.2, ha="right", va="center",
                rotation=90, zorder=8)
        # label the pair inline: a leader from the right-hand column would have
        # to cross the whole panel diagonally
        # Parked in the empty band below the machine, above the R_0 dimension:
        # the right-hand column is full at this height and a leader from there
        # would cross the TF and PF labels.
        Rv1, Zv1, _ = m.vfb_positions[1]
        ylab = Zv1 - 0.62 * a
        if stage in (None, 7):
          ax.plot([Rv1, Rv1], [Zv1 - 0.17, ylab + 0.30], color=PALETTE["pf"],
                lw=0.7, zorder=8)
          ax.text(Rv1, ylab, "vertical-feedback pair, ANTI-SERIES:\n"
                r"opposite currents $\Rightarrow$ radial field,"
                "\nwhich is what restores $Z$",
                  color=PALETTE["pf"], fontsize=8.4, ha="center", va="top",
                  zorder=9)

    # ---- shape parameters --------------------------------------------------
    if "elongation" in flags:
        ax.annotate("", xy=(R0 - 1.95 * a, m.kappa * a), xytext=(R0 - 1.95 * a, 0),
                    arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.0),
                    zorder=8)
        ax.text(R0 - 2.02 * a, 0.5 * m.kappa * a, r"$\kappa a$", fontsize=10,
                ha="right", va="center", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))
    if "triangularity" in flags:
        Rtop = R0 - a * np.sin(np.arcsin(min(m.delta, 0.95)))
        ax.annotate("", xy=(Rtop, m.kappa * a), xytext=(R0, m.kappa * a),
                    arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.0),
                    zorder=8)
        ax.plot([R0, R0], [0, m.kappa * a], color=PALETTE["guide"], lw=0.6,
                ls=(0, (2, 3)), zorder=2)
        ax.text(Rtop - 0.10, m.kappa * a + 0.14, r"$\delta a$",
                fontsize=10, ha="right", va="bottom", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))

    # ---- stage 9: the same coils, a different equilibrium -----------------
    if "equil_shift" in flags and stage in (None, PRESENTATION_INTRO["equil_shift"]):
        # Outward (Shafranov) shift of the magnetic axis when p-bar rises or
        # I_p falls.  The magnitude here is illustrative and declared as such:
        # the actual shift follows from Grad-Shafranov, which the text has not
        # solved yet, so no number is implied.
        dR = 0.26 * a
        Rs, Zs = m.boundary(a)
        ax.plot(Rs + dR, Zs, color=PALETTE["plasma"], lw=1.4,
                ls=(0, (1.3, 1.9)), alpha=0.9, zorder=6)
        ax.plot([R0, R0 + dR], [0, 0], color=PALETTE["plasma"], lw=0)
        ax.annotate("", xy=(R0 + dR, 0), xytext=(R0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["plasma"],
                                    lw=1.6), zorder=9)
        ax.plot([R0 + dR], [0], marker="o", ms=4, color=PALETTE["plasma"],
                zorder=9)
        prose("shift", r"same coils, larger $\bar p$ (or smaller $I_p$):"
                       "\nthe magnetic axis moves OUTWARD by $\Delta$."
                       "\nThe PF currents must change to undo it ---"
                       "\nequilibrium is a setting, not a shape",
              (R0 + dR, 0.30 * a), PALETTE["plasma"], intro=9)

    # ---- stage 10: alphas stay, neutrons leave ----------------------------
    if "neutron" in flags and stage in (None, PRESENTATION_INTRO["neutron"]):
        # Neutral, so unaffected by B: straight lines out, through everything.
        for th0 in np.linspace(0.35, 2 * np.pi + 0.35, 7, endpoint=False):
            x0 = R0 + 0.30 * a * np.cos(th0)
            y0 = 0.30 * a * m.kappa * np.sin(th0)
            L = 2.35 * a
            ax.annotate("", xy=(x0 + L * np.cos(th0), y0 + L * np.sin(th0)),
                        xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["guide"],
                                        lw=1.1, ls=(0, (4, 2))), zorder=6)
        prose("neutron", r"$14.1\,$MeV neutron: NEUTRAL, so $\mathbf{B}$ does"
                         "\nnothing to it. It leaves in a straight line,"
                         "\nthrough the vessel, carrying 4/5 of the yield"
                         "\nto a boundary not yet derived",
              (R0 + 1.55 * a, 1.15 * a), PALETTE["guide"], intro=10)
    if "alpha" in flags and stage in (None, PRESENTATION_INTRO["alpha"]):
        # Charged, so it gyrates and stays: drawn as a bounded orbit fragment.
        tt = np.linspace(0, 6.5 * np.pi, 500)
        rr = 0.50 * a * (1 - 0.62 * tt / tt[-1])
        xa = R0 + 0.10 * a + rr * np.cos(tt)
        ya = 0.55 * a + 0.85 * rr * np.sin(tt)
        ax.plot(xa, ya, color=PALETTE["heat"], lw=1.6, zorder=7)
        ax.plot([xa[-1]], [ya[-1]], marker="o", ms=4.5,
                color=PALETTE["heat"], zorder=8)
        prose("alpha", r"$3.5\,$MeV alpha: CHARGED, so it gyrates,"
                       "\nstays inside, and thermalises. This is "
                       r"$P_\alpha$:" "\nthe fuel heating itself",
              (R0 + 0.10 * a, 0.55 * a), PALETTE["heat"], intro=10)

    # ---- stage 11: where the plasma current comes from --------------------
    if "ledger" in flags and stage in (None, PRESENTATION_INTRO["ledger"]):
        # A stacked bar, not a pie: the three terms ADD to I_p, and the point
        # of the ledger is that the sum is what must reach the required value.
        frac = [("$I_{\\rm ohm}$", 0.30, PALETTE["cs"]),
                ("$I_{\\rm CD}$",  0.22, PALETTE["heat"]),
                ("$I_{\\rm bs}$",  0.48, PALETTE["plasma"])]
        bx, by, bw, bh = R0 - 1.75 * a, -(ztop + 1.30 * a), 3.5 * a, 0.30 * a
        x = bx
        for lab, f, col in frac:
            ax.add_patch(Rectangle((x, by), f * bw, bh, fc=col, ec="white",
                                   lw=1.0, alpha=0.85, zorder=8))
            ax.text(x + 0.5 * f * bw, by + 0.5 * bh, lab, color="white",
                    fontsize=8.5, ha="center", va="center", zorder=9)
            x += f * bw
        ax.text(bx - 0.12, by + 0.5 * bh, r"$I_p=$", fontsize=10,
                ha="right", va="center", zorder=9)
        ax.text(bx + 0.5 * bw, by - 0.12,
                "the split is illustrative; only the sum is constrained here",
                fontsize=8, ha="center", va="top", color="0.35")
        # tie each term to the component that supplies it
        for xf, src in ((0.15, (0.0, -m.z_cs)),
                        (0.41, (XLAB + 0.15 * a, -1.95 * a)),
                        (0.76, (R0, -m.kappa * a))):
            ax.plot([bx + xf * bw, src[0]], [by + bh, src[1]],
                    color=PALETTE["guide"], lw=0.6, ls=(0, (2, 2.5)), zorder=2)

    # ---- 7a: profile, not just total current ------------------------------
    if "profile" in flags and stage in (None, PRESENTATION_INTRO["profile"]):
        # a small inset of nested surfaces with q rising outward
        cx, cy, sc = XLAB + 1.45 * a, 2.35 * a, 0.55
        for f_, qlab in ((0.30, "$q_0$"), (0.62, ""), (0.95, "$q_a$")):
            Rq, Zq = m.boundary(f_ * a)
            ax.plot(cx + sc * (Rq - R0), cy + sc * Zq, color=PALETTE["bfield"],
                    lw=1.2, ls=LS["bfield"], zorder=8)
            if qlab:
                ax.text(cx + sc * f_ * a + 0.06, cy, qlab, fontsize=8.5,
                        color=PALETTE["bfield"], ha="left", va="center")
        ax.text(cx, cy + sc * m.kappa * a + 0.10, r"$q(r)$ rises outward",
                fontsize=8.5, color=PALETTE["bfield"], ha="center", va="bottom")
        # who actually shapes the profile
        for src, lab in (((0.0, 0.35 * m.z_cs), "CS"),
                         ((XLAB - 0.25 * a, 0.0), "launchers")):
            ax.annotate("", xy=(R0 - 0.55 * a, 0.62 * a), xytext=src,
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["guide"],
                                        lw=0.9, ls=(0, (3, 2)),
                                        connectionstyle="arc3,rad=0.15"),
                        zorder=7)
        ax.text(R0 - 0.55 * a, 0.74 * a, r"$j_\varphi(r)$", fontsize=10,
                color=PALETTE["current"], ha="center", va="bottom", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.8))
        prose("profile",
              r"$I_p=\int j_\varphi\,dA$ is ONE number." "\n"
              r"$j_\varphi(r)$ is a function, and it is the function"
              "\nthat sets $q(r)$. The solenoid and the launchers\n"
              "move the function, not just the number.",
              (cx - sc * a, cy), PALETTE["bfield"], intro=15)

    # ---- 7b: the performance symbols are machine features -----------------
    if "perf" in flags and stage in (None, PRESENTATION_INTRO["perf"]):
        for (x, y, lab, col) in (
                (R0 * 0.5, -(m.kappa * rtf + 0.55 * a), "$R_0$", "black"),
                (R0 + 0.55 * a, 0.30 * a, "$a$", "black"),
                (R0 - 1.30 * a, 0.5 * m.kappa * a, r"$\kappa$", "black"),
                (R0 - rtf - 0.18, 0.0, "$B_0$", PALETTE["tf"]),
                (R0 - 0.40 * a, -0.42 * a, "$I_p$", PALETTE["current"])):
            ax.text(x, y, lab, fontsize=11, color=col, ha="center",
                    va="center", zorder=10,
                    bbox=dict(fc="white", ec=col, lw=0.7, alpha=0.92, pad=1.4))
        prose("perf",
              r"$P_{\rm fus}\propto \bar n^2 V"
              r"\propto \beta^2B_0^4R_0a^2\kappa$" "\n\n"
              "Every symbol on the left is a thing you can point\n"
              "at in this figure. This is a SCALING, not a claim\n"
              "about net electrical power --- nothing here has\n"
              "yet paid for recirculating power or efficiency.",
              (R0 - rtf, 0.4 * a), PALETTE["plasma"], intro=16)

    # ---- stage 13: the nuclear island -------------------------------------
    if "island" in flags:
        # Three conformal layers outside the vessel.  Thicknesses are declared
        # fractions of a, NOT engineering values: the text derives b as a whole
        # from the neutron mean free path, and says nothing about the split.
        t_wall, t_blk, t_shd = 0.10 * a, 0.42 * a, 0.26 * a
        r0_ = aw
        for key, th in (("wall", t_wall), ("blanket", t_blk), ("shield", t_shd)):
            Ri, Zi = m.boundary(r0_)
            Ro_, Zo_ = m.boundary(r0_ + th)
            ax.fill(np.concatenate([Ro_, Ri[::-1]]),
                    np.concatenate([Zo_, Zi[::-1]]),
                    facecolor=PALETTE[key], edgecolor=PALETTE[key],
                    hatch=HATCH[key], alpha=0.34, lw=1.0, zorder=2)
            r0_ += th
        b_out = r0_
        # the bracket the text actually names: first wall -> vacuum boundary
        xb = R0 + b_out + 0.12 * a
        ax.annotate("", xy=(R0 + aw, -1.30 * a), xytext=(R0 + b_out, -1.30 * a),
                    arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.1),
                    zorder=9)
        ax.text(R0 + 0.5 * (aw + b_out), -1.42 * a, "$b$",
                fontsize=11, ha="center", va="top", zorder=9)
        prose("island", "first wall / blanket / shield. The text derives the\n"
                        r"TOTAL $b$ from the neutron mean free path and says"
                        "\nnothing about the split, so the split drawn here is\n"
                        "illustrative. One neutron deposits; one bred triton returns.",
              (R0 + 0.5 * (aw + b_out), 0.42 * m.kappa * a),
              PALETTE["blanket"], intro=13)
        # one neutron stopping in the blanket, one bred triton returning
        _demo = stage in (None, 13)
        if _demo:
         ax.annotate("", xy=(R0 + aw + t_wall + 0.7 * t_blk, 0.20 * a),
                    xytext=(R0 + 0.25 * a, 0.20 * a),
                    arrowprops=dict(arrowstyle="-|>", color=PALETTE["guide"],
                                    lw=1.2, ls=(0, (4, 2))), zorder=8)
         ax.text(R0 + aw + t_wall + 0.72 * t_blk, 0.30 * a, "n stops",
                 fontsize=8, color=PALETTE["guide"], ha="left", va="bottom")
         ax.annotate("", xy=(R0 + 0.30 * a, -0.22 * a),
                     xytext=(R0 + aw + t_wall + 0.6 * t_blk, -0.22 * a),
                     arrowprops=dict(arrowstyle="-|>", color=PALETTE["plasma"],
                                     lw=1.2), zorder=8)
         ax.text(R0 + aw + t_wall + 0.62 * t_blk, -0.34 * a,
                 r"bred T returns", fontsize=8, color=PALETTE["plasma"],
                 ha="left", va="top")

    # ---- stage 14: the radial build that caps B_0 -------------------------
    if "radial_build" in flags:
        t_wall, t_blk, t_shd = 0.10 * a, 0.42 * a, 0.26 * a
        b_tot = t_wall + t_blk + t_shd
        c_wp, c_str = 0.30 * a, 0.18 * a          # winding pack, structure
        yb = -(max(m.kappa * rtf, m.z_cs) + 1.85 * a)
        R_in = R0 - a - b_tot - (c_wp + c_str)
        # the inboard midplane ruler, drawn from the axis outward
        segs = [(R_in, c_str, PALETTE["tf"], "structure", "\\\\"),
                (R_in + c_str, c_wp, PALETTE["tf"], "winding pack", None),
                (R_in + c_str + c_wp, t_shd, PALETTE["shield"], None, HATCH["shield"]),
                (R_in + c_str + c_wp + t_shd, t_blk, PALETTE["blanket"], None, HATCH["blanket"]),
                (R_in + c_str + c_wp + t_shd + t_blk, t_wall, PALETTE["wall"], None, HATCH["wall"]),
                (R0 - a, a, PALETTE["plasmafc"], None, None)]
        h = 0.30 * a
        for x0, w, col, lab, hat in segs:
            ax.add_patch(Rectangle((x0, yb), w, h, facecolor=col, alpha=0.55,
                                   edgecolor=col, hatch=hat, lw=0.9, zorder=8))
            if lab:
                ax.text(x0 + 0.5 * w, yb - 0.05, lab, fontsize=7.0,
                        rotation=90, ha="center", va="top",
                        color=PALETTE["tf"], zorder=9)
        for x0, x1, lab in ((R_in, R_in + c_str + c_wp, "$c$"),
                            (R_in + c_str + c_wp, R0 - a, "$b$"),
                            (R0 - a, R0, "$a$")):
            ax.annotate("", xy=(x1, yb + h + 0.12), xytext=(x0, yb + h + 0.12),
                        arrowprops=dict(arrowstyle="<|-|>", color="black",
                                        lw=1.0), zorder=9)
            ax.text(0.5 * (x0 + x1), yb + h + 0.18, lab, fontsize=10,
                    ha="center", va="bottom", zorder=9)
        ax.plot([R_in, R_in], [yb - 0.10, yb + h + 0.42], color=PALETTE["guide"],
                lw=0.8, ls=(0, (2, 2)), zorder=7)
        ax.text(R_in + 0.62, yb - 0.92, r"$R_{\rm in}=R_0-a-b-c$", fontsize=8.6,
                ha="left", va="top", zorder=9)
        ax.text(R_in - 0.06, yb + h + 0.62, r"$B_{\max}$", fontsize=9,
                ha="center", va="bottom", color=PALETTE["bfield"], zorder=9)
        ax.text(R0, yb + h + 0.62, r"$B_0$", fontsize=9,
                ha="center", va="bottom", color=PALETTE["bfield"], zorder=9)
        # the force the inboard leg has to survive
        for yy in (yb + 0.08, yb + 0.22):
            ax.annotate("", xy=(R_in - 0.22, yy), xytext=(R_in + 0.02, yy),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["current"],
                                        lw=1.1), zorder=9)
        ax.text(R_in - 0.26, yb + 0.15, r"$p_B=B^2/2\mu_0$", fontsize=7.8,
                ha="right", va="center", color=PALETTE["current"], zorder=9)
        if "hifield" in flags and stage in (None, PRESENTATION_INTRO["hifield"]):
            # The brief asks the coil bracket c to be resolved one level
            # further -- structural case, winding pack, insulation/cooling --
            # and for a conductor-technology callout.  Two things it also asks
            # for, and they are the reason the figure exists:
            #   * the force arrows STAY, labelled as NOT removed by HTS;
            #   * the field threshold is a REQUIREMENT ON A CONDUCTOR, not a
            #     property this machine now has.
            # All wording sits to the RIGHT of the ruler: there is no room to
            # the left of R_in, and the first draft ran off the panel there.
            c_ins = 0.07 * a
            x_ins = R_in + c_str + c_wp - c_ins
            ax.add_patch(Rectangle((x_ins, yb), c_ins, h, facecolor="white",
                                   edgecolor=PALETTE["tf"], hatch="||||",
                                   lw=0.9, zorder=9))
            ax.text(R0 + 0.30, yb + h + 0.10,
                    r"$c$ is now resolved: structural case $|$ winding pack "
                    r"$|$ insulation and cooling",
                    fontsize=8.0, ha="left", va="bottom", color=PALETTE["tf"],
                    zorder=9)
            ax.text(R0 + 0.30, yb + h - 0.06,
                    "The magnetic pressure $p_B=B^2/2\\mu_0$ still presses on "
                    "the case.\nHTS does NOT remove that force: it changes "
                    "what conductor can\ncarry the current, not what the "
                    "structure has to hold.",
                    fontsize=8.0, ha="left", va="top",
                    color=PALETTE["current"], zorder=9, linespacing=1.55)
            prose("hifield",
                  "TECHNOLOGY REQUIREMENT, not an achieved property:\n"
                  "the high-field branch needs a conductor whose\n"
                  "critical-current margin still supports\n"
                  r"$B_{\max}\gtrsim 17.6\,$T at the winding pack."  "\n"
                  "Nothing in this figure supplies it. The figure\n"
                  "only says where the demand lands.",
                  (R_in + 0.5 * c_wp, yb + h + 0.30), PALETTE["current"],
                  intro=18)
        if "centrestack" in flags and stage in (None,
                                                PRESENTATION_INTRO["centrestack"]):
            # Low A does not change the inventory; it changes how much room the
            # inventory has.  So this layer adds exactly two things: the name
            # R_cs for the interval that is now scarce, and a MAGNIFIED view of
            # what has to fit inside it.  The four cells are drawn UNFILLED and
            # unsized, because their split is an engineering result this
            # document has not derived -- drawing it would invent it.
            R_cs = R_in
            ax.text(R0 + 0.62, yb + h + 0.60,
                    r"$B_{\max}$ at the column IS $B_{\rm cs}$ here",
                    fontsize=8.4, ha="left", va="bottom",
                    color=PALETTE["bfield"], zorder=9)
            ax.annotate("", xy=(R_cs, yb - 1.80), xytext=(0.0, yb - 1.80),
                        arrowprops=dict(arrowstyle="<|-|>",
                                        color=PALETTE["current"], lw=1.3),
                        zorder=9)
            ax.text(R_cs + 0.80, yb - 1.80,
                    r"$R_{\rm cs}=R_0-a-b-c_{\rm cs}$ — the scarce interval",
                    fontsize=8.6, ha="left", va="center",
                    color=PALETTE["current"], zorder=9)

            # magnified: what has to fit inside c_cs
            zx0, zw = R0 - 1.00 * a, 10.0 * a
            zy, zh = yb - 4.35, 0.64 * a
            ax.plot([R_in, zx0], [yb, zy + zh], color="0.65", lw=0.7,
                    ls=(0, (2, 2)), zorder=6)
            ax.plot([R_in + c_str + c_wp, zx0 + zw], [yb, zy + zh],
                    color="0.65", lw=0.7, ls=(0, (2, 2)), zorder=6)
            CELLS = ["conductor", "structure", "insulation\n& cooling",
                     "optional\nsolenoid"]
            for i, name in enumerate(CELLS):
                ax.add_patch(Rectangle((zx0 + i * zw / 4, zy), zw / 4, zh,
                                       facecolor="white",
                                       edgecolor=PALETTE["tf"], lw=1.2,
                                       zorder=8))
                ax.text(zx0 + (i + 0.5) * zw / 4, zy + 0.5 * zh, name,
                        fontsize=7.6, ha="center", va="center",
                        color=PALETTE["tf"], zorder=9, linespacing=1.35)
            ax.text(zx0 + 0.5 * zw, zy - 0.14,
                    r"magnified: what must fit inside $c_{\rm cs}$ — drawn "
                    "UNFILLED and UNSIZED,\nbecause the split is an "
                    "engineering result this document has not derived",
                    fontsize=8.2, ha="center", va="top", color=PALETTE["tf"],
                    zorder=9, linespacing=1.5)
            prose("centrestack",
                  "LOW ASPECT RATIO CUTS BOTH WAYS. It improves the plasma\n"
                  "geometry the earlier sections wanted --- and it makes\n"
                  r"$R_{\rm cs}$ scarce. $b$ is still demanded by neutrons and"
                  "\n"
                  r"$c_{\rm cs}$ still by current and force, so shrinking $R_0/a$"
                  "\ntakes the room out of the only place left. This is not a\n"
                  "solved reactor: it is a statement of what must fit.",
                  (0.5 * R_cs, yb - 1.80), PALETTE["current"], intro=19)
        prose("build", "inboard midplane ruler. The coil bracket $c$ splits into\n"
                       "winding pack and structure; what is left at the axis is\n"
                       r"$R_{\rm in}$, and $B_{\max}$ there is what caps $B_0$.",
              (R_in + 0.5 * c_wp, yb + h), PALETTE["tf"], intro=14)

    # ---- dimensions -------------------------------------------------------
    if "dims_R0a" in flags:
        # the feedback caption occupies the band directly under the machine,
        # so the R_0 dimension drops below it when that stage is present
        yd = -(ztop + (0.85 if ("vfb" not in flags or stage not in (None, 7))
                       else 2.20) * a)
        if "ledger" in flags and stage in (None, PRESENTATION_INTRO["ledger"]):
            yd -= 1.25 * a
        if "radial_build" in flags:
            yd -= 2.60 * a
        if "centrestack" in flags and stage in (
                None, PRESENTATION_INTRO["centrestack"]):
            yd -= 0.95 * a
        ax.annotate("", xy=(R0, yd), xytext=(0, yd),
                    arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.1))
        ax.plot([R0, R0], [yd, -aw], color=PALETTE["guide"], lw=0.6, ls=(0, (2, 3)))
        ax.text(R0 / 2, yd - 0.14, r"$R_0$  major radius", fontsize=10,
                ha="center", va="top")
        ang = 1.05
        ax.annotate("", xy=(R0 + a * np.cos(ang), a * np.sin(ang)), xytext=(R0, 0.0),
                    arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.1),
                    zorder=8)
        ax.text(R0 + 0.55 * a * np.cos(ang) + 0.20, 0.55 * a * np.sin(ang),
                r"$a$", fontsize=11, ha="left", va="center", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))

    _yod = -(ztop + (1.55 if ("vfb" not in flags
                              or stage not in (None, 7)) else 2.90) * a
             - (0 if "ledger" not in flags else -1.25 * a))
    if "radial_build" in flags:
        _yod -= 3.35 * a          # the inboard ruler occupies that band
    if "centrestack" in flags and stage in (
            None, PRESENTATION_INTRO["centrestack"]):
        _yod -= 3.00 * a          # ... and the magnified c_cs strip below it
    ax.text(R0 / 2, _yod, r"$\odot$ : the vector points out of the page",
            fontsize=8.6, ha="center", va="top", color="0.35")

    if "atlas1" in flags and stage in (None, PRESENTATION_INTRO["atlas1"]):
        # The FIRST atlas checkpoint.  Its brief asks for one thing the later
        # atlas does not: each component NUMBERED BY THE SECTION WHERE ITS
        # PHYSICAL NEED WAS DERIVED.  Those section numbers are read off the
        # manuscript, not assigned by me -- the whole point of the checkpoint is
        # that a reader can walk back to the paragraph that forced each part.
        # Nothing later than SS18 appears: no triangularity, no alpha, no island.
        ATLAS1 = [
            ("vessel",  "§4",  "vacuum vessel / torus",
             "the corridor is closed: $R_0$ and $a$ exist"),
            ("plasma",  "§4",  "plasma boundary",
             "two lengths, hence $A=R_0/a$"),
            ("tf",      "§4",  r"TF coils, $B_\varphi$",
             r"$B_\varphi\propto 1/R$ around the same tube"),
            ("bfield",  "§5",  "toroidal drift",
             "the bottle leaks; a second field is forced"),
            ("cs",      "§6",  r"central solenoid, $I_p$",
             "$B_\\theta$ comes from $I_p$, nothing else"),
            ("current", "§7",  r"pitch, safety factor $q$",
             "the helix has a pitch, and it is bounded"),
            ("pf",      "§9",  "PF / shaping coils",
             "pressure pushes out; $B_v$ holds position"),
            ("heat",    "§12", "NBI / RF port",
             "the transformer cannot reach $T_{\\rm fusion}$"),
            ("guide",   "§13", r"elongation $\kappa$",
             "more room at fixed $R_0$"),
            ("plasma",  "§14", "sensors + feedback",
             "a taller plasma tips: shaping needs a loop"),
        ]
        ytop, ystep = ztop * 0.22, ztop * 2.05 / len(ATLAS1)
        ax.text(XLAB - 0.10, ytop + 0.62 * ystep,
                "component  $\\longrightarrow$  the section that forced it",
                fontsize=9.5, ha="left", va="bottom")
        ax.plot([XLAB - 0.10, XLAB + 9.30 * a],
                [ytop + 0.48 * ystep] * 2, color="0.6", lw=0.8)
        for i, (key, sec, name, why) in enumerate(ATLAS1):
            y = ytop - i * ystep
            ax.plot([XLAB - 0.05, XLAB + 0.42], [y, y], color=PALETTE[key],
                    lw=2.4 * LW.get(key, 1.0), ls=LS.get(key, "solid"),
                    solid_capstyle="butt")
            ax.text(XLAB + 0.58, y, sec, fontsize=9.2, ha="left", va="center",
                    color="0.15")
            ax.text(XLAB + 1.25, y, name, color=PALETTE[key], fontsize=8.8,
                    ha="left", va="center")
            ax.text(XLAB + 5.05, y, why, fontsize=8.0, ha="left",
                    va="center", color="0.32")
        ax.text(-0.60, ytop - len(ATLAS1) * ystep - 1.05 * ystep,
                "NOT here, because not yet derived: triangularity, alpha "
                "heating, the neutron boundary, blanket,\nshield, "
                "superconductors, divertor, and every spherical-tokamak "
                "feature. A component enters this\ntable only after a section "
                "has forced it.",
                fontsize=8.0, ha="left", va="top", color=PALETTE["pf"],
                linespacing=1.5)
        _pending.clear()

    if "atlas" in flags and stage in (None, PRESENTATION_INTRO["atlas"]):
        ATLAS = [
            ("vessel",  "vacuum vessel",      "holds the vacuum; sets no\nvariable of its own yet"),
            ("tf",      "TF coils",           r"$B_0$, via $B_\varphi=\mu_0NI_c/2\pi R$"),
            ("cs",      "central solenoid",   r"volt-seconds $\to I_{\rm ohm}$;"
                                              "\nfinite swing = finite pulse"),
            ("pf",      "PF coils",           r"$B_v$, position, $\kappa$, $\delta$"),
            ("plasma",  "plasma boundary",    r"$R_0$, $a$, $A=R_0/a$, $\bar p$, $\beta$"),
            ("current", r"plasma current $I_p$", r"$q_a$ --- and so the kink wall"),
            ("heat",    "NBI / RF launchers", r"$P_{\rm aux}$, $I_{\rm CD}$, and $\tau_E$"),
            ("guide",   "escaping neutron",   "4/5 of the yield, to a boundary\nnot yet derived"),
        ]
        ytop, ystep = ztop * 0.72, ztop * 2.30 / len(ATLAS)
        ax.text(XLAB - 0.10, ytop + 0.55 * ystep,
                "component  $\\longrightarrow$  the design variable it fixes",
                fontsize=9.5, ha="left", va="bottom")
        ax.plot([XLAB - 0.10, XLAB + 9.30 * a],
                [ytop + 0.42 * ystep] * 2, color="0.6", lw=0.8)
        for i, (key, name, var) in enumerate(ATLAS):
            y = ytop - i * ystep
            ax.plot([XLAB - 0.05, XLAB + 0.42], [y, y], color=PALETTE[key],
                    lw=2.4 * LW.get(key, 1.0), ls=LS.get(key, "solid"),
                    solid_capstyle="butt")
            ax.text(XLAB + 0.55, y, name, color=PALETTE[key], fontsize=9,
                    ha="left", va="center")
            ax.text(XLAB + 4.75, y, var, fontsize=8.6, ha="left", va="center",
                    color="0.2")
        _pending.clear()

    _flush_prose(ztop * 0.92, -ztop * 0.62)

    wide_col = (("atlas" in flags
                 and stage in (None, PRESENTATION_INTRO["atlas"]))
                or ("atlas1" in flags
                    and stage in (None, PRESENTATION_INTRO["atlas1"])))
    ax.set_xlim(-0.75, XLAB + (9.7 if wide_col else 4.35) * a)
    if "island" in flags:
        ax.set_xlim(-0.75, XLAB + 9.7 * a)
    extra = 2.05 if ("vfb" not in flags or stage not in (None, 7)) else 3.40
    if "atlas1" in flags and stage in (None, PRESENTATION_INTRO["atlas1"]):
        extra = 4.60          # the numbered table is taller than the machine
    if "ledger" in flags and stage in (None, PRESENTATION_INTRO["ledger"]):
        extra += 1.25
    if "radial_build" in flags:
        extra += 2.30
    if "centrestack" in flags and stage in (None,
                                            PRESENTATION_INTRO["centrestack"]):
        extra += 2.10          # the magnified c_cs strip lives below the ruler
    ax.set_ylim(-(ztop + extra * a), ztop + 0.75 * a)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("poloidal cross-section  ($R$–$Z$ plane)", fontsize=10, pad=2)


# ==========================================================================
#  TOP-LEVEL RENDER
# ==========================================================================
def render(stage: int, m: Machine = None, outstem: str = None,
           layout: str = "wide"):
    m = m or Machine()
    spec = STAGES[stage]
    flags = spec["flags"]
    # Shape is part of the stage, not of the caller's Machine: stage 6 IS the
    # elongated machine.  Applied by replacement so the caller's R0/a/n_tf win.
    if spec.get("shape"):
        from dataclasses import replace as _replace
        m = _replace(m, **spec["shape"])

    # LAYOUT.  "wide" is the 1x2 screen/reference form.  "tall" stacks the two
    # panels so the figure fits a thesis TEXT BLOCK rather than a slide: at
    # 10.95 in wide the wide form scales to 0.63 on a 6.86 in text block, which
    # prints a 9 pt label at 5.6 pt.  The tall form scales to ~0.98, so the
    # same label prints at ~8.8 pt.  Same model, same palette, two aspects.
    tall = (layout == "tall")
    if tall:
        fig = plt.figure(figsize=(7.4, 9.3))
        gs = fig.add_gridspec(2, 1, height_ratios=[0.80, 1.0], hspace=0.16,
                              left=0.02, right=0.98, top=0.945, bottom=0.062)
        ax3 = fig.add_subplot(gs[0, 0], projection="3d")
    else:
        fig = plt.figure(figsize=(10.6, 5.1))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.06], wspace=0.0,
                              left=0.005, right=0.995, top=0.845, bottom=0.135)
        ax3 = fig.add_subplot(gs[0, 0], projection="3d")
    used = draw_3d(ax3, m, flags)
    ax3.set_title("")

    ax2 = fig.add_subplot(gs[1, 0] if tall else gs[0, 1])
    if "straight_vessel" in flags:
        draw_longitudinal(ax2, m, flags)
        right_caption = "longitudinal section"
    else:
        draw_poloidal(ax2, m, flags, stage)
        right_caption = r"poloidal cross-section  ($R$–$Z$ plane)"
    ax2.set_title("")
    if tall:
        fig.text(0.5, 0.915, "perspective view" +
                 ("  (vessel cut open)" if "torus_vessel" in flags else ""),
                 fontsize=10, ha="center", va="top")
        fig.text(0.30 if (stage == 12) else 0.5, 0.470, right_caption,
                 fontsize=10, ha="center", va="top")
    else:
        fig.text(0.26, 0.862, "perspective view" +
                 ("  (vessel cut open)" if "torus_vessel" in flags else ""),
                 fontsize=10, ha="center", va="top")
        fig.text(0.74, 0.862, right_caption, fontsize=10, ha="center", va="top")

    lab = dict(LEGEND_LABEL)
    if stage == 1:
        lab.update(LEGEND_OVERRIDE_S1)
    # Each legend key shows this component's ACTUAL line style, so the legend
    # survives a black-and-white print.
    # Regions get a filled swatch, lines get a line in that component's own
    # dash pattern.  Two consequences: the legend tells you what KIND of thing
    # each entry is, and no two entries are confusable on a greyscale print.
    AREAS = {"vessel": PALETTE["vesselfc"], "plasma": PALETTE["plasmafc"]}
    handles = []
    for k in used:
        if k in AREAS:
            handles.append(Patch(facecolor=AREAS[k], edgecolor=PALETTE[k],
                                 linewidth=1.6 * LW[k], label=lab[k]))
        else:
            handles.append(Line2D([], [], color=PALETTE[k],
                                  lw=2.6 * LW.get(k, 1.0),
                                  linestyle=LS.get(k, "solid"), label=lab[k]))
    if tall:
        fig.legend(handles=handles, frameon=False, fontsize=7.8,
                   ncol=2, loc="center", bbox_to_anchor=(0.5, 0.545),
                   handlelength=2.4, columnspacing=1.2, labelspacing=0.24,
                   borderpad=0.0)
    else:
        fig.legend(handles=handles, frameon=False, fontsize=8.6, ncol=1,
                   loc="lower left", bbox_to_anchor=(0.015, 0.055),
                   handlelength=3.4, labelspacing=0.34, borderpad=0.0)

    fig.text(0.5, 0.992 if tall else 0.975, spec["title"],
             fontsize=12 if tall else 13, ha="center", va="top")
    fig.text(0.5, 0.962 if tall else 0.912, spec["sub"],
             fontsize=9.2 if tall else 9.8, ha="center", va="top",
             style="italic", color="0.25")
    ndraw = m.n_tf if m.kappa <= 1.2 else max(6, m.n_tf // 2)
    if tall:
        foot = (DISCLAIMER + "\n"
                rf"$R_0/a={m.A:.1f}$, $\kappa={m.kappa:.2f}$, "
                rf"$\delta={m.delta:.2f}$, {ndraw} of {m.n_tf} TF coils in the "
                "3-D panel; all geometry computed by tokamak_build.py.")
    else:
        foot = (DISCLAIMER +
                rf"   Parameters: $R_0/a={m.A:.1f}$, "
                rf"$\kappa={m.kappa:.2f}$, $\delta={m.delta:.2f}$, "
                rf"{ndraw} of {m.n_tf} TF coils drawn in the 3-D panel. "
                "All geometry computed by tokamak_build.py; "
                "no dimension is implied.")
    fig.text(0.5, 0.006 if tall else 0.012, foot,
             fontsize=7.0 if tall else 7.6, ha="center", va="bottom",
             color="0.45", linespacing=1.4)

    stem = outstem or (spec.get("stem", f"figM{stage}_stage{stage}")
                       + ("_tall" if tall else ""))
    bb = None if tall else "tight"
    fig.savefig(stem + ".pdf", bbox_inches=bb)
    fig.savefig(stem + ".png", dpi=180, bbox_inches=bb)
    plt.close(fig)
    print("wrote", stem + ".pdf/.png")
    return stem


if __name__ == "__main__":
    for k in range(1, 6):
        render(k)
