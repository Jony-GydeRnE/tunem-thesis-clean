"""Checks for the G1a.2 second-invariant scale theorem.


"""

import sympy as sp


r, L = sp.symbols("r L", positive=True)
A, D, F, B, K, C = sp.symbols("A D F B K C", positive=True)
x, y = sp.symbols("x y", real=True)

E = (
    A * L
    + D * r * L
    + F * r**2 * L
    + B * L / r**2
    + K / L
    + C * (r**2 * L) ** sp.Rational(-2, 3)
)

print("=" * 72)
print("G1a.2: SECOND-INVARIANT SCALE THEOREM")
print("=" * 72)
print("Energy:")
sp.print_latex(E)

Elog = sp.expand(E.subs({r: sp.exp(x), L: sp.exp(y)}))
Hlog = sp.hessian(Elog, (x, y))

# Verify the Hessian is the sum of positive weighted outer products.
terms = [
    (A * sp.exp(y), sp.Matrix([0, 1])),
    (D * sp.exp(x + y), sp.Matrix([1, 1])),
    (F * sp.exp(2 * x + y), sp.Matrix([2, 1])),
    (B * sp.exp(-2 * x + y), sp.Matrix([-2, 1])),
    (K * sp.exp(-y), sp.Matrix([0, -1])),
    (
        C * sp.exp(-sp.Rational(4, 3) * x - sp.Rational(2, 3) * y),
        sp.Matrix([-sp.Rational(4, 3), -sp.Rational(2, 3)]),
    ),
]
Hclaim = sp.zeros(2)
for weight, vector in terms:
    Hclaim += weight * vector * vector.T
assert sp.simplify(Hlog - Hclaim) == sp.zeros(2)

print("\nLog-Hessian outer-product identity: VERIFIED")
print("The B and K exponent vectors are (-2,1) and (0,-1); they span R^2.")
print("With B,K>0 the log-Hessian is positive definite everywhere.")

# Verify the positive convex combination used for coercivity.
q = sp.symbols("q", positive=True)
vB = sp.Matrix([-2, 1])
vK = sp.Matrix([0, -1])
vQ = sp.Matrix([q, 1])
combo = sp.simplify(vB + (1 + 2 / q) * vK + (2 / q) * vQ)
assert combo == sp.zeros(2, 1)
print("\nCoercivity convex-combination identity: VERIFIED")
print("vB + (1+2/q)vK + (2/q)vQ = 0 with all weights positive.")

# Closed-form no-plasma control.
g = A + D * r + F * r**2 + B / r**2
Lstar_C0 = sp.sqrt(K / g)
assert sp.simplify(sp.diff(E.subs(C, 0), L).subs(L, Lstar_C0)) == 0
Ered_C0 = sp.simplify(E.subs(C, 0).subs(L, Lstar_C0))
assert sp.simplify(Ered_C0 - 2 * sp.sqrt(K * g)) == 0
radius_polynomial = 2 * F * r**4 + D * r**3 - 2 * B
assert sp.simplify(sp.diff(g, r) * r**3 - radius_polynomial) == 0

print("\nC=0 control:")
print("L_*(r) = sqrt(K/g(r)); E_*(r) = 2 sqrt(K g(r))")
print("r_* is the unique positive root of 2 F r^4 + D r^3 - 2 B = 0.")

# Numerical example with every coefficient set to one.
En = E.subs({A: 1, D: 1, F: 1, B: 1, K: 1, C: 1})
dEr = sp.diff(En, r)
dEL = sp.diff(En, L)
solution = sp.nsolve((dEr, dEL), (r, L), (0.9, 0.8), tol=1e-40, maxsteps=100)
rstar = sp.N(solution[0], 15)
Lstar = sp.N(solution[1], 15)
Hphys = sp.hessian(En, (r, L)).subs({r: solution[0], L: solution[1]})
eigenvalues = [sp.N(value, 15) for value in Hphys.eigenvals().keys()]

print("\nAll-coefficients-one numerical example:")
print(f"r_* = {rstar}")
print(f"L_* = {Lstar}")
print("physical-Hessian eigenvalues:")
for value in eigenvalues:
    print(f"  {value}")
assert all(float(value) > 0 for value in eigenvalues)

# Check the log/physical Hessian congruence at a stationary point.
J = sp.diag(r, L)
Hphys_general = sp.hessian(E, (r, L))
grad_phys = sp.Matrix([sp.diff(E, r), sp.diff(E, L)])
Hlog_from_physical = J * Hphys_general * J + sp.diag(
    r * grad_phys[0], L * grad_phys[1]
)
Hlog_sub = Hlog.subs({x: sp.log(r), y: sp.log(L)})
assert sp.simplify(Hlog_sub - Hlog_from_physical) == sp.zeros(2)

print("\nLog/physical Hessian transformation: VERIFIED")
print("At the critical point the gradient term vanishes, leaving a positive")
print("congruence. The physical 2x2 Hessian is positive definite.")
print("\nRESULT: the K/L second invariant produces one finite strict global minimum.")
