"""G1a two-parameter scale-existence checks.



This verifies the algebra in ../notes/g1a-two-parameter-scale.tex.  It is a
symbolic check of a proof, not a replacement for the proof and not a numerical
MHD simulation.
"""

import sympy as sp


r, L = sp.symbols("r L", positive=True)
A, D, F, B, C = sp.symbols("A D F B C", positive=True)

# Independent radius and network-length scale factors.
# A L                 : effective line tension
# D r L               : tube interface/surface cost
# F r^2 L             : core/condensate volume cost
# B L/r^2             : axial magnetic energy at fixed tube flux
# C (r^2 L)^(-2/3)    : gamma=5/3 adiabatic plasma energy at fixed content
g = A + D * r + F * r**2 + B / r**2
E = L * g + C * r ** sp.Rational(-4, 3) * L ** sp.Rational(-2, 3)

print("=" * 72)
print("G1a: TWO-PARAMETER SCALE-EXISTENCE TEST")
print("=" * 72)
print("Energy:")
sp.print_latex(E)

# First minimize exactly in L for each fixed r.
L_star = ((sp.Rational(2, 3) * C * r ** sp.Rational(-4, 3)) / g) ** sp.Rational(3, 5)
assert sp.simplify(sp.diff(E, L).subs(L, L_star)) == 0

E_reduced = sp.factor(E.subs(L, L_star))
target = (
    sp.Rational(5, 2)
    * (sp.Rational(2, 3) * C) ** sp.Rational(3, 5)
    * (g / r**2) ** sp.Rational(2, 5)
)
assert sp.simplify(E_reduced - target) == 0

H = sp.factor(g / r**2)
dH = sp.factor(sp.diff(H, r))
expected_dH = -D / r**2 - 2 * A / r**3 - 4 * B / r**5
assert sp.simplify(dH - expected_dH) == 0

print("\nExact length minimizer L_*(r):")
sp.print_latex(L_star)
print("\nReduced energy E_*(r):")
sp.print_latex(E_reduced)
print("\nMonotone factor H(r) = g(r)/r^2:")
sp.print_latex(H)
print("\nH'(r):")
sp.print_latex(dH)
print("\nBecause A,D,B,r > 0, H'(r) < 0 for every finite r.")
print("RESULT: no finite-radius stationary point exists in this model.")

# Independent direct contradiction from the two stationarity equations.
P = C * r ** sp.Rational(-4, 3) * L ** sp.Rational(-2, 3)
dL_scaled = sp.factor(L * sp.diff(E, L))
dr_scaled = sp.factor(r * sp.diff(E, r))

# On dE/dL=0, P=(3/2)Lg. Substitute that relation into r*dE/dr.
radial_on_length_stationary = sp.expand(
    L * (D * r + 2 * F * r**2 - 2 * B / r**2)
    - sp.Rational(4, 3) * (sp.Rational(3, 2) * L * g)
)
radial_target = -L * (2 * A + D * r + 4 * B / r**2)
assert sp.simplify(radial_on_length_stationary - radial_target) == 0

print("\nDirect stationarity contradiction:")
print("At dE/dL=0, the radial stationarity residual is")
sp.print_latex(radial_on_length_stationary)
print("which is strictly negative for positive A, D, and B.")

# The one-parameter isotropic result is recovered on r=lambda*r0, L=lambda*L0.
lam, r0, L0 = sp.symbols("lambda r_0 L_0", positive=True)
E_iso = sp.expand(E.subs({r: lam * r0, L: lam * L0}))
print("\nIsotropic restriction r=lambda*r0, L=lambda*L0:")
sp.print_latex(E_iso)
print("This restriction can have a minimum while the full two-dimensional model")
print("has a downhill anisotropic direction. The one-parameter pass was therefore")
print("necessary but not sufficient.")

print("\nVERIFIED: all symbolic identities and the no-stationary-point conclusion.")
