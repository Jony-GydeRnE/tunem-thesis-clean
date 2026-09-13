#!/usr/bin/env python3
"""
Price the bootstrap-closure condition of thesis Sections 110-111.

The published finite-A ST point (Menard et al., Nucl. Fusion 56 (2016) 106023,
Figs. 8-9, f_GW = 0.8) is fully non-inductive by construction, so its current
balance cannot test Freidberg's affordability constraint. What it does fix is
the external drive that an independent budget would have to afford. This
script states that price against Freidberg's own allowance (100 MW of wall
electricity for current drive) and Menard's 40% wall-to-injected assumption,
so the condition
I_CD,allow >= I_CD,needed becomes a number a reader can judge.

Every input is a published scalar already quoted in the thesis; nothing is
fitted or digitized here. The thresholds are frozen-state bounds on the
published beam state: reducing beam power changes heating, fast-ion pressure,
fusion power, current and bootstrap fraction, so they bound that state, not a
redesigned ST.
"""

# ---- Menard et al. (2016), Figs. 8-9 at f_GW = 0.8 (Sec. 2.1.3-2.1.6)
I_p    = 10.8   # MA, plasma current at the plotted point
f_BS   = 0.76   # bootstrap fraction reported at that point
P_inj  = 80.0   # MW, injected 0.5 MeV neutral-beam power assumed by the scan

# ---- Freidberg, Mangiarotti & Minervini (2015), Sec. 4.6: the drive allowance
P_wall_allow = 100.0   # MW electric, 10% of Freidberg's 1000 MW pre-RF electric output
eta_wi       = 0.40    # wall-to-injected efficiency from Menard Sec. 2.1.6; not Freidberg's RF absorption chain

I_CD_needed  = (1.0 - f_BS) * I_p                 # MA
P_wall_state = P_inj / eta_wi                     # MW_e to keep the published beams
eta_needed   = P_inj / P_wall_allow               # wall efficiency to fit the cap
P_inj_cap    = eta_wi * P_wall_allow              # MW injected affordable under the cap
gamma_needed = I_CD_needed / P_inj_cap * 1e3      # kA per MW injected, at the cap

print(f"External drive the ST point needs:    I_CD,needed = (1 - {f_BS}) x {I_p} MA = {I_CD_needed:.2f} MA")
print(f"Wall power to keep its {P_inj:.0f} MW beams:      {P_inj:.0f} / {eta_wi} = {P_wall_state:.0f} MW_e  "
      f"(vs the {P_wall_allow:.0f} MW_e allowance)")
print(f"Wall efficiency to fit the allowance:    {P_inj:.0f} / {P_wall_allow:.0f} = {eta_needed:.2f}  "
      f"(assumed {eta_wi})")
print(f"Drive efficacy if only {P_inj_cap:.0f} MW is injected: {I_CD_needed:.2f} MA / {P_inj_cap:.0f} MW = "
      f"{gamma_needed:.0f} kA/MW")
