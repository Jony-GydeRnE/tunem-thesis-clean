#!/usr/bin/env python3
"""Dependencies of the reduced Freidberg baseline, with c checked separately."""
from sketch_base import *
fig, ax = new(h=3.15)
node(ax, 1.05, 2.3, 1.85, .60, "mission and wall loading\n$R_0(a)$", "chosen")
node(ax, 1.05, 1.1, 1.85, .60, "neutron build\n$b$", "chosen")
node(ax, 3.85, 1.7, 2.15, .70, "analytic field convention\n$B_0=B_{max}[1-(a+b)/R_0]$", "derived")
node(ax, 6.65, 2.3, 2.20, .60, "stress and winding pack\nreal $c(a,B_0)$ required", "derived")
node(ax, 6.65, 1.1, 2.20, .60, "plasma closure\nfour ratios at the same $a$", "empirical")
flow(ax, (2.0,2.3),(2.76,1.92))
flow(ax, (2.0,1.1),(2.76,1.48))
flow(ax, (4.95,1.92),(5.53,2.3))
flow(ax, (4.95,1.48),(5.53,1.1))
ax.text(4,.38,"Trial radius $a$ sets a candidate; coil feasibility and plasma allowances jointly test it.",ha="center",fontsize=9)
ax.set_xlim(0,8);ax.set_ylim(.05,2.85)
save(fig,"figS_causal_scan_in_a", "Dependencies within the source's reduced radial-build convention.")
