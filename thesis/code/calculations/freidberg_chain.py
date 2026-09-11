#!/usr/bin/env python3
"""
Independent reproduction of the Freidberg-Mangiarotti-Minervini (2015) design
chain, from the mission down to the four operational-limit ratios, as a
function of the minor radius a and of the four escape parameters
(H, Bmax, PE, PW).

Nothing is fitted to the paper's answers: every relation is coded from the
physics/algebra as derived in Part I + Part II of the primer, and the paper's
printed values are used only as CHECK targets, printed alongside ours.

Units: SI internally, except T in keV, <sigma v> from the log-polynomial fit
(Freidberg Eq. 21) in m^3/s, and the IPB98 scaling which is evaluated in its
own stated units (I in MA, nbar in 1e20 m^-3, powers in MW).
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---------------------------------------------------------------- constants
mu0   = 4e-7 * np.pi
e_C   = 1.602176634e-19
m_e   = 9.1093837015e-31
eps0  = 8.8541878128e-12
MeV   = 1e6 * e_C
atm   = 101325.0

E_n     = 14.1          # MeV, neutron share of the D-T reaction
E_alpha = 3.5           # MeV, alpha share
E_F     = 22.4          # MeV, total heat per fusion INCLUDING the 4.8 MeV
                        #      Li-6 breeding exotherm
# profile exponents (Freidberg Eq. 20)
nu_T, nu_p, nu_n = 1.0, 1.5, 0.5
PROF = 2.0 * (1 + nu_T) * (1 + nu_n) / (1 + nu_p)      # pbar = PROF * nbar*Tbar

# reference engineering constraints (Table 2)
DEF = dict(kappa=1.70, b=1.20, eta_T=0.40, sigma_max=600e6, J_max=20e6,
           f_RP=0.10, eta_RF=0.40, Tbar=14.0, beta_N=2.8, q_K=2.0,
           A_fuel=2.5, H=1.0, Bmax=13.0, PE=1000.0, PW=4.0, rho_m=0.8)

# ------------------------------------------------------- D-T reactivity fit
_k = (-60.4593, 6.1371, -0.8609, 0.0356, -0.0045)
def sigmav(T_keV):
    """<sigma v> in m^3/s, T in keV (Freidberg Eq. 21)."""
    l = np.log(T_keV)
    return np.exp(_k[0] + _k[1]*l + _k[2]*l**2 + _k[3]*l**3 + _k[4]*l**4)

# ------------------------------------------- bootstrap: current profile b_th
ALPHA = 2.53
_den  = np.exp(ALPHA) - 1.0 - ALPHA
def b_theta(rho):
    """B_theta normalised to mu0 I /(2 pi ahat)  (Freidberg Eq. 43)."""
    x = rho**(9.0/4.0)
    return ((1 + ALPHA - ALPHA*x)*np.exp(ALPHA*x) - 1 - ALPHA) / (rho*_den)

_J_BS = quad(lambda r: r**2.5*np.sqrt(1-r**2)/b_theta(r), 0, 1, limit=200)[0]

# ------------------------------------------------------------- the chain
def design(a, **kw):
    P = dict(DEF); P.update(kw)
    kap, b   = P['kappa'], P['b']
    Bmax, PW = P['Bmax'], P['PW']
    PE, etaT = P['PE'], P['eta_T']
    Tbar     = P['Tbar']
    T_J      = Tbar*1e3*e_C

    # F3 -- the wall-loading hyperbola  R0*a = const
    R0a = (1/(4*np.pi**2)) * (E_n/E_F) * (PE/(etaT*PW)) * np.sqrt(2/(1+kap**2))
    R0  = R0a/a
    eps, epsB = a/R0, (a+b)/R0

    # F4 -- the half-price field, the steel, the superconductor
    B0  = Bmax*(1-epsB)
    aM  = B0**2/(mu0*P['sigma_max']) * (2*epsB/(1+epsB)
                                        + 0.5*np.log((1+epsB)/(1-epsB)))
    cM  = R0*(1-epsB - np.sqrt(max((1-epsB)**2 - aM, 0.0)))
    R1  = R0 - a - b
    Itf = 2*np.pi*R1*Bmax/mu0                      # total TF ampere-turns
    Acu = Itf/P['J_max']
    cJ  = R1 - np.sqrt(max(R1**2 - Acu/np.pi, 0.0))
    c   = cM + cJ

    # F5 -- pressure from the profile-integrated power balance
    VP  = 2*np.pi**2*R0*a**2*kap
    def integrand(r):                              # dV = VP * 2 rho drho
        pr = (1+nu_p)*(1-r**2)**nu_p               # p/pbar
        Tr = Tbar*(1+nu_T)*(1-r**2)**nu_T          # keV
        return pr**2*sigmav(Tr)/(Tr*1e3*e_C)**2 * 2*r
    Ipow  = quad(integrand, 0, 1, limit=200)[0]
    PF    = PE/etaT
    pbar  = np.sqrt(PF*1e6 / (E_F*MeV/16 * VP * Ipow))     # Pa
    nbar  = pbar/(PROF*T_J)                                # m^-3
    beta  = 2*mu0*pbar/B0**2
    Palph = (E_alpha/E_F)*PF                               # MW
    tauE  = 1.5*pbar*VP/(Palph*1e6)                        # s

    # F6 -- IPB98(y,2) inverted for the current
    n20 = nbar/1e20
    K   = 0.145*P['H']*R0**1.39*a**0.58*kap**0.78*n20**0.41 \
          * B0**0.15*P['A_fuel']**0.19 / Palph**0.69
    I   = (tauE/K)**(1/0.93)                               # MA
    qst = 2*np.pi*a**2*B0/(mu0*R0*I*1e6)*(1+kap**2)/2

    # F6b -- the lower-hybrid current-drive budget -> REQUIRED bootstrap
    rm   = P['rho_m']
    n_m  = nbar*(1+nu_n)*(1-rm**2)**nu_n                   # density at rho_m
    B_m  = B0/(1+eps*rm)                                   # outside launch
    wpe  = np.sqrt(n_m*e_C**2/(eps0*m_e))
    Wce  = e_C*B_m/m_e
    y    = wpe/Wce
    nu_par = y + np.sqrt(1+y**2)*np.sqrt(1-0.25)           # omega = 2 omega_LH
    eta_CD = 1.2/nu_par**2                                 # MA/(MW m^2)
    P_CD   = P['eta_RF']*P['f_RP']*PE                      # MW
    I_CD   = eta_CD*P_CD/(R0*n20)                          # MA
    fB     = 1 - I_CD/I

    # F7 -- ACHIEVABLE bootstrap (neoclassical, Freidberg Eq. 44)
    ahat = np.sqrt(kap)*a
    fNC  = 4*np.pi**2*6.771*ahat**2.5*pbar/(mu0*np.sqrt(R0)*(I*1e6)**2)*_J_BS

    # the four walls, as "required / achievable" ratios (must all be < 1)
    nG   = I/(np.pi*a**2)                                  # 1e20 m^-3
    bT   = P['beta_N']*I/(a*B0)                            # %
    VB   = 2*np.pi**2*R0*((a+b)*(kap*a+b) - kap*a**2)
    VTF  = 4*np.pi*c*(2*R0-2*a-2*b-c)*((1+kap)*a + 2*b + c)
    return dict(a=a, R0=R0, R0a=R0a, eps=eps, epsB=epsB, B0=B0, cM=cM, cJ=cJ,
                c=c, VP=VP, p_atm=pbar/atm, n20=n20, beta_pct=beta*100,
                tauE=tauE, Palpha=Palph, I=I, qstar=qst, nu_par=nu_par,
                eta_CD=eta_CD, I_CD=I_CD, fB=fB, fNC=fNC,
                r_green=n20/nG, r_troyon=beta*100/bT,
                r_kink=P['q_K']/qst, r_boot=fB/fNC,
                cost=(VB+VTF)/P['PE'], Qheat=Palph*B0/R0)

def worst(a, **kw):
    d = design(a, **kw)
    return max(d['r_green'], d['r_troyon'], d['r_kink'], d['r_boot'])

def a_max(**kw):
    """largest a for which the machine still closes geometrically:
    the inboard leg must exist, R1 = R0 - a - b > 0, i.e. epsB < 1."""
    P = dict(DEF); P.update(kw)
    R0a = (1/(4*np.pi**2))*(E_n/E_F)*(P['PE']/(P['eta_T']*P['PW'])) \
          * np.sqrt(2/(1+P['kappa']**2))
    b = P['b']
    return 0.999*(-b + np.sqrt(b**2 + 4*R0a))/2

def a_of_balance(lo=0.30, hi=None, **kw):
    """the a at which required bootstrap equals achievable (Freidberg's
    closing condition for every escape route)."""
    if hi is None:
        hi = 0.97*a_max(**kw)
    f = lambda a: design(a, **kw)['r_boot'] - 1.0
    return brentq(f, lo, hi, xtol=1e-12)

# ------------------------------------------------------------------- checks
if __name__ == "__main__":
    P = {'R0a':7.16,'B0':6.83,'cM':0.39,'cJ':0.575,'c':0.97,'p_atm':7.57,
         'n20':1.43,'beta_pct':4.13,'tauE':0.94,'I':14.3,'qstar':1.56,
         'nu_par':1.67,'eta_CD':0.43,'I_CD':2.25,'fB':0.84,'fNC':0.44,
         'r_green':0.56,'r_troyon':0.94,'r_kink':1.28,'r_boot':1.90,
         'cost':1.00,'Qheat':499.}
    d = design(1.34)
    print(f"{'quantity':10s} {'ours':>12s} {'paper':>10s} {'rel.err':>9s}")
    for k, v in P.items():
        o = d[k]
        print(f"{k:10s} {o:12.4f} {v:10.3f} {abs(o-v)/abs(v)*100:8.2f}%")

    print("\n--- escape routes (Table 3): solve fB = fNC for a, then close ---")
    def route(label, target, **kw):
        a = a_of_balance(**kw); d = design(a, **kw)
        print(f"{label:22s} a={a:5.3f} R0={d['R0']:5.2f} B0={d['B0']:5.2f} "
              f"I={d['I']:5.2f} q*={d['qstar']:4.2f} b/bT={d['r_troyon']:4.2f} "
              f"n/nG={d['r_green']:4.2f} fB={d['fB']:4.2f} "
              f"cost={d['cost']:4.2f} Q={d['Qheat']:5.0f}")
        return a, d
    # option 1: raise H until the kink closes
    H1 = brentq(lambda H: design(a_of_balance(H=H), H=H)['r_kink']-1, 1.0, 1.40)
    route(f"1  H={H1:.3f}", None, H=H1)
    B1 = brentq(lambda B: design(a_of_balance(Bmax=B), Bmax=B)['r_kink']-1, 13, 22)
    route(f"2  Bmax={B1:.2f} T", None, Bmax=B1)
    P1 = brentq(lambda p: design(a_of_balance(PE=p), PE=p)['r_kink']-1, 1000, 2200)
    route(f"3  PE={P1:.0f} MW", None, PE=P1)
    W1 = brentq(lambda w: design(a_of_balance(PW=w), PW=w)['r_kink']-1, 1.2, 4.0)
    route(f"4  PW={W1:.2f} MW/m2", None, PW=W1)

    print("\n--- reference sweep: is any a admissible? ---")
    for a in [0.8, 1.0, 1.2, 1.34, 1.6, 2.0]:
        d = design(a)
        print(f"a={a:4.2f}  n/nG={d['r_green']:5.2f} b/bT={d['r_troyon']:5.2f} "
              f"qK/q*={d['r_kink']:5.2f} fB/fNC={d['r_boot']:5.2f} "
              f"-> worst {worst(a):5.2f}")
    from scipy.optimize import minimize_scalar
    aopt = minimize_scalar(worst, bounds=(0.4, 0.97*a_max()), method='bounded').x
    print(f"\nbest compromise near a={aopt:.3f}: worst ratio = {worst(aopt):.3f}")
