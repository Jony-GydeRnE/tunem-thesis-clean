#!/usr/bin/env python3
"""Reproduce the disclosed 2015 conventional-baseline constraint scan.

This is an audit calculation, not a general tokamak design tool. It implements the
analytic assumptions stated in Freidberg, Mangiarotti, and Minervini (2015), Eqs.
(5)--(16), (23)--(25), (29)--(32), and (41)--(44).  It can also reproduce the
paper's Sections 6.1--6.3 scans: for each confinement multiplier H, inboard field
limit Bmax, or electric output PE, it finds the radius where required and calculated
bootstrap fractions agree. The script deliberately prints only calculations; it
neither writes design data nor makes a figure.
"""

from math import exp, log, pi, sqrt

MU0 = 4.0 * pi * 1.0e-7
ATM = 101325.0
E_CHARGE = 1.602176634e-19
EPS0 = 8.8541878128e-12
M_E = 9.1093837e-31
M_I = 2.5 * 1.67262192369e-27

KAPPA = 1.70
B_BLANKET = 1.20
B_MAX = 13.0
SIGMA_MAX = 600.0e6
J_MAX = 20.0e6
P_CD = 40.0
P_E_REF = 1000.0
W_N_REF = 4.0
ALPHA = 2.53
RHO_M = 0.80


def btheta(rho: float) -> float:
    """Dimensionless poloidal field from Eq. (43)."""
    if rho == 0.0:
        return 0.0
    x = rho ** (9.0 / 4.0)
    numerator = (1.0 + ALPHA - ALPHA * x) * exp(ALPHA * x) - 1.0 - ALPHA
    return numerator / (rho * (exp(ALPHA) - 1.0 - ALPHA))


def simpson_integral(n: int = 20000) -> float:
    """Dimensionless integral in Eq. (44), evaluated once deterministically."""
    if n % 2:
        raise ValueError("Simpson grid must have an even number of intervals")
    h = 1.0 / n

    def integrand(rho: float) -> float:
        if rho == 0.0 or rho == 1.0:
            return 0.0
        return rho ** 2.5 * sqrt(1.0 - rho * rho) / btheta(rho)

    total = integrand(0.0) + integrand(1.0)
    for k in range(1, n):
        total += (4.0 if k % 2 else 2.0) * integrand(k * h)
    return total * h / 3.0


BOOTSTRAP_INTEGRAL = simpson_integral()


def state(
    a: float,
    h: float = 1.0,
    b_max: float = B_MAX,
    p_e: float = P_E_REF,
    w_n: float = W_N_REF,
) -> dict[str, float]:
    """Return the stated-model state and four demand-to-allowance ratios.

    H changes only the empirical confinement multiplier. Since the confinement
    regression has I**0.93, solving it gives I proportional to H**(-1/0.93).
    Bmax, PE, and Wn are kept explicit for the later remedy scans.
    """
    if p_e <= 0.0 or w_n <= 0.0:
        raise ValueError("electric output and wall loading must be positive")
    power_ratio = p_e / P_E_REF
    wall_ratio = w_n / W_N_REF
    r0 = 7.16 * power_ratio / (wall_ratio * a)
    epsilon_b = (a + B_BLANKET) / r0
    b0 = b_max * (1.0 - epsilon_b)
    if b0 <= 0.0:
        raise ValueError("central field is non-positive")

    alpha_m = (b0 * b0 / (MU0 * SIGMA_MAX)) * (
        2.0 * epsilon_b / (1.0 + epsilon_b)
        + 0.5 * log((1.0 + epsilon_b) / (1.0 - epsilon_b))
    )
    alpha_j = 2.0 * b0 / (MU0 * r0 * J_MAX)
    root_m = (1.0 - epsilon_b) ** 2 - alpha_m
    root_j = (1.0 - epsilon_b) ** 2 - alpha_j
    if root_m <= 0.0 or root_j <= 0.0:
        raise ValueError("TF-coil model has no real thickness solution")
    c = r0 * (2.0 * (1.0 - epsilon_b) - sqrt(root_m) - sqrt(root_j))

    p_atm = 8.76 * sqrt(wall_ratio) / sqrt(a)
    n20 = 1.66 * sqrt(wall_ratio) / sqrt(a)
    # At fixed wall loading, R0*a is proportional to PE. The confinement
    # numerator contributes P_alpha**0.69 while R0**1.39 contributes PE**1.39,
    # so I**0.93 is proportional to PE**-0.70. At fixed PE, lowering Wn
    # makes R0 proportional to Wn**-1, n proportional to Wn**1/2, and
    # tau_E proportional to Wn**-1/2, hence I**0.93 proportional to Wn**0.685.
    current_ma = (
        12.1
        * a ** 1.63
        / b0 ** 0.16
        * h ** (-1.0 / 0.93)
        * power_ratio ** (-0.70 / 0.93)
        * wall_ratio ** (0.685 / 0.93)
    )
    # The printed compact beta relation has B_max=13 T absorbed in 1.31.
    # Restore the explicit B_max dependence before using the state for a
    # high-field scan: beta = 2 mu_0 p / B_0**2.
    beta_percent = (
        1.31
        * sqrt(wall_ratio)
        / (sqrt(a) * (1.0 - epsilon_b) ** 2)
        * (B_MAX / b_max) ** 2
    )
    # Use the defining safety-factor relation rather than its H=1 compact form.
    # This preserves q_* proportional to 1/I when H is varied.
    q_star = (
        2.0 * pi * a * a * b0 / (MU0 * r0 * current_ma * 1.0e6)
        * (1.0 + KAPPA * KAPPA) / 2.0
    )

    a_hat = sqrt(KAPPA) * a
    f_nc = (
        268.0
        * a_hat ** 2.5
        * (p_atm * ATM)
        / (MU0 * sqrt(r0) * (current_ma * 1.0e6) ** 2)
        * BOOTSTRAP_INTEGRAL
    )

    n_local = 1.5 * n20 * 1.0e20 * sqrt(1.0 - RHO_M * RHO_M)
    b_local = b0 / (1.0 + (a / r0) * RHO_M)
    omega_pe = sqrt(n_local * E_CHARGE**2 / (EPS0 * M_E))
    omega_pi = sqrt(n_local * E_CHARGE**2 / (EPS0 * M_I))
    omega_e = E_CHARGE * b_local / M_E
    omega_lh = sqrt(omega_pi**2 / (1.0 + (omega_pe / omega_e) ** 2))
    n_parallel = (
        omega_pe / omega_e
        + sqrt(1.0 + (omega_pe / omega_e) ** 2)
        * sqrt(1.0 - omega_lh**2 / (2.0 * omega_lh) ** 2)
    )
    eta_cd = 1.2 / n_parallel**2
    current_cd_ma = P_CD * power_ratio * eta_cd / (r0 * n20)
    f_required = 1.0 - current_cd_ma / current_ma

    greenwald20 = current_ma / (pi * a * a)
    beta_troyon_percent = 2.8 * current_ma / (a * b0)
    return {
        "a": a, "H": h, "Bmax": b_max, "PE": p_e, "Wn": w_n, "R0": r0, "B0": b0, "c": c, "I": current_ma,
        "p_atm": p_atm, "n20": n20, "q_star": q_star,
        "f_required": f_required, "f_nc": f_nc, "eta_cd": eta_cd,
        "greenwald_ratio": n20 / greenwald20,
        "troyon_ratio": beta_percent / beta_troyon_percent,
        "kink_ratio": 2.0 / q_star,
        "bootstrap_ratio": f_required / f_nc,
    }


def bootstrap_matched_state(
    h: float,
    b_max: float = B_MAX,
    p_e: float = P_E_REF,
    w_n: float = W_N_REF,
) -> dict[str, float]:
    """Find the tabulated-radius point at which f_required is closest to f_NC."""
    best = None
    for step in range(400, 4001):
        try:
            s = state(step / 1000.0, h=h, b_max=b_max, p_e=p_e, w_n=w_n)
        except ValueError:
            continue
        mismatch = abs(s["bootstrap_ratio"] - 1.0)
        if best is None or mismatch < best[0]:
            best = (mismatch, s)
    if best is None:
        raise RuntimeError("no valid TF-coil and bootstrap-matched radius was found")
    return best[1]


def main() -> None:
    print(f"Eq. (44) dimensionless integral = {BOOTSTRAP_INTEGRAL:.6f}")
    print(" a[m]  R_G     R_T     R_K     R_B     max(R)  B0[T]  I[MA]")
    best = None
    valid_radii = []
    for step in range(40, 401):
        a = step / 100.0
        try:
            s = state(a)
        except ValueError:
            continue
        valid_radii.append(a)
        worst = max(s["greenwald_ratio"], s["troyon_ratio"], s["kink_ratio"], s["bootstrap_ratio"])
        row = (worst, s)
        if best is None or row[0] < best[0]:
            best = row
        if step % 20 == 0:
            print(f" {a:4.2f}  {s['greenwald_ratio']:5.2f}  {s['troyon_ratio']:5.2f}  "
                  f"{s['kink_ratio']:5.2f}  {s['bootstrap_ratio']:5.2f}  "
                  f"{worst:5.2f}  {s['B0']:5.2f}  {s['I']:5.2f}")
    if best is None:
        raise RuntimeError("no valid radius was found")
    worst, s = best
    print("\nleast-violating sampled point:")
    print(f"a={s['a']:.3f} m, max ratio={worst:.3f}, "
          f"R_G={s['greenwald_ratio']:.3f}, R_T={s['troyon_ratio']:.3f}, "
          f"R_K={s['kink_ratio']:.3f}, R_B={s['bootstrap_ratio']:.3f}")
    print(f"largest valid baseline radius on this 0.01 m grid: {max(valid_radii):.3f} m")

    print("\nSection 6.1 scan: impose f_B = f_NC, then test the other ratios")
    print(" H      a[m]   R_G    R_T    R_K    R_B   I[MA]")
    for h in (1.00, 1.10, 1.20, 1.26, 1.30, 1.40, 1.65):
        s = bootstrap_matched_state(h)
        print(f"{h:4.2f}  {s['a']:5.3f}  {s['greenwald_ratio']:5.2f}  "
              f"{s['troyon_ratio']:5.2f}  {s['kink_ratio']:5.2f}  "
              f"{s['bootstrap_ratio']:5.2f}  {s['I']:5.2f}")

    print("\nSection 6.2 scan: hold H=1, impose f_B = f_NC, then raise Bmax")
    print(" Bmax[T]  a[m]  B0[T]  c[m]  I[MA]  R_G   R_T   R_K   R_B")
    for b_max in (13.0, 15.0, 17.0, 17.6, 18.0, 20.0, 22.0):
        s = bootstrap_matched_state(1.0, b_max)
        print(f" {b_max:5.1f}  {s['a']:5.3f}  {s['B0']:5.2f}  {s['c']:4.2f}  "
              f"{s['I']:5.2f}  {s['greenwald_ratio']:4.2f}  "
              f"{s['troyon_ratio']:4.2f}  {s['kink_ratio']:4.2f}  "
              f"{s['bootstrap_ratio']:4.2f}")

    # The radius grid is 0.001 m, so this is a transparent, approximate
    # threshold rather than a falsely precise root of the source's full model.
    first_passing = None
    for step in range(1300, 2201):
        b_max = step / 100.0
        s = bootstrap_matched_state(1.0, b_max)
        if max(s["greenwald_ratio"], s["troyon_ratio"], s["kink_ratio"],
               s["bootstrap_ratio"]) <= 1.0:
            first_passing = (b_max, s)
            break
    if first_passing is not None:
        b_max, s = first_passing
        print("\nfirst all-pass point on the 0.01 T / 0.001 m grids:")
        print(f"Bmax={b_max:.2f} T, a={s['a']:.3f} m, "
              f"R_G={s['greenwald_ratio']:.3f}, R_T={s['troyon_ratio']:.3f}, "
              f"R_K={s['kink_ratio']:.3f}, R_B={s['bootstrap_ratio']:.3f}")

    print("\nSection 6.3 scan: hold H=1 and Bmax=13 T, then raise PE")
    print(" PE[MW]  a[m]  R0[m]  B0[T]  I[MA]  R_G   R_T   R_K   R_B")
    for p_e in (1000.0, 1200.0, 1400.0, 1550.0, 1600.0, 1800.0, 2000.0):
        s = bootstrap_matched_state(1.0, B_MAX, p_e)
        print(f" {p_e:6.0f}  {s['a']:5.3f}  {s['R0']:5.2f}  {s['B0']:5.2f}  "
              f"{s['I']:5.2f}  {s['greenwald_ratio']:4.2f}  "
              f"{s['troyon_ratio']:4.2f}  {s['kink_ratio']:4.2f}  "
              f"{s['bootstrap_ratio']:4.2f}")

    first_passing = None
    for p_e in range(1000, 3001):
        s = bootstrap_matched_state(1.0, B_MAX, float(p_e))
        if max(s["greenwald_ratio"], s["troyon_ratio"], s["kink_ratio"],
               s["bootstrap_ratio"]) <= 1.0:
            first_passing = (p_e, s)
            break
    if first_passing is not None:
        p_e, s = first_passing
        print("\nfirst all-pass output on the 1 MW / 0.001 m grids:")
        print(f"PE={p_e:.0f} MW, a={s['a']:.3f} m, "
              f"R_G={s['greenwald_ratio']:.3f}, R_T={s['troyon_ratio']:.3f}, "
              f"R_K={s['kink_ratio']:.3f}, R_B={s['bootstrap_ratio']:.3f}")

    print("\nSection 6.4 scan: hold H=1, Bmax=13 T, and PE=1000 MW, then lower Wn")
    print(" Wn[MW/m2]  a[m]  R0[m]  B0[T]  I[MA]  R_G   R_T   R_K   R_B")
    for w_n in (4.0, 3.5, 3.0, 2.5, 2.1, 2.0, 1.5):
        s = bootstrap_matched_state(1.0, B_MAX, P_E_REF, w_n)
        print(f" {w_n:8.2f}  {s['a']:5.3f}  {s['R0']:5.2f}  {s['B0']:5.2f}  "
              f"{s['I']:5.2f}  {s['greenwald_ratio']:4.2f}  "
              f"{s['troyon_ratio']:4.2f}  {s['kink_ratio']:4.2f}  "
              f"{s['bootstrap_ratio']:4.2f}")

    last_passing = None
    for step in range(400, 41, -1):
        w_n = step / 100.0
        s = bootstrap_matched_state(1.0, B_MAX, P_E_REF, w_n)
        if max(s["greenwald_ratio"], s["troyon_ratio"], s["kink_ratio"],
               s["bootstrap_ratio"]) <= 1.0:
            last_passing = (w_n, s)
            break
    if last_passing is not None:
        w_n, s = last_passing
        print("\nhighest all-pass wall loading on the 0.01 MW/m2 / 0.001 m grids:")
        print(f"Wn={w_n:.2f} MW/m2, a={s['a']:.3f} m, "
              f"R_G={s['greenwald_ratio']:.3f}, R_T={s['troyon_ratio']:.3f}, "
              f"R_K={s['kink_ratio']:.3f}, R_B={s['bootstrap_ratio']:.3f}")


if __name__ == "__main__":
    main()
