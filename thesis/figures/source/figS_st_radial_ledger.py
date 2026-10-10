#!/usr/bin/env python3
"""Approved compact radial envelope from the illustrative Menard allocation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

A, R0 = 2., 1.87
SHIELD, WALL = .600, .020
a = R0/A
inboard = R0-a
envelope = inboard-SHIELD-WALL
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10, "pdf.fonttype":42})
fig, ax = plt.subplots(figsize=(7.2, 2.65))
ax.set(xlim=(-.07,2.88),ylim=(-.48,.88))
ax.axis("off")
ax.set_title(r"Illustrative radial budget: $A=2$, $R_0=1.87$ m",fontsize=11,pad=7)
for x, w, fc, ec in [(0,envelope,"white","#315a70"),(envelope,SHIELD,"#deded0","#757567"),(inboard-WALL,WALL,"#737373","#737373"),(inboard,2*a,"#e5edf3","#315a70")]:
    ax.add_patch(Rectangle((x,0),w,.29,facecolor=fc,edgecolor=ec,lw=1))
ax.text(envelope/2,.145,"column\nenvelope",ha="center",va="center",fontsize=8)
ax.text(envelope+SHIELD/2,.145,"shield\n0.60 m",ha="center",va="center",fontsize=9)
ax.text(R0,.145,r"plasma: $2a=1.87$ m",ha="center",va="center",fontsize=10)
ax.annotate("",(inboard,.48),(0,.48),arrowprops={"arrowstyle":"<->","lw":.8})
ax.text(inboard/2,.53,r"$R_0-a=0.935$ m",ha="center",fontsize=9)
ax.annotate("first wall: 0.02 m",(inboard-WALL/2,.3),(1.34,.72),ha="center",fontsize=9,arrowprops={"arrowstyle":"->","lw":.8})
ax.text(.02,-.17,r"$R_{\rm env}=0.935-0.600-0.020=0.315$ m",fontsize=10)
ax.text(.02,-.36,"Approximately the study's 0.30 m column; winding, support and start-up share its area.",fontsize=8)
fig.subplots_adjust(left=.025,right=.995,bottom=.04,top=.83)
fig.savefig("figS_st_radial_ledger.pdf")
fig.savefig("figS_st_radial_ledger.png",dpi=180)
