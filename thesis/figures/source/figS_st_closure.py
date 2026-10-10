#!/usr/bin/env python3
"""Approved compact comparison: kink test versus external-drive requirement."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

Q_K_CONV, Q_STAR_CONV = 2., 1.56
FB_REQ_CONV, FB_CALC_CONV = .84, .44
Q_K_ST, Q_STAR_ST = 2.8, 3.
F_BS_ST, F_NBI_ST = .76, .24
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10, "pdf.fonttype":42})
fig, ax = plt.subplots(figsize=(7.2, 2.7))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
ax.text(.24,.93,"Conventional reference",ha="center",fontsize=11)
ax.text(.75,.93,"Finite-aspect-ratio ST case",ha="center",fontsize=11)
ax.text(.24,.78,f"Kink: 2/1.56 = {Q_K_CONV/Q_STAR_CONV:.2f} > 1",ha="center")
ax.text(.24,.67,"Fails the adopted boundary",ha="center",fontsize=9)
ax.text(.75,.78,f"Kink: 2.8/3.0 ≃ {Q_K_ST/Q_STAR_ST:.2f} < 1",ha="center")
ax.text(.75,.67,"Passes the adopted boundary",ha="center",fontsize=9)
ax.text(.24,.48,f"Bootstrap: 0.84/0.44 = {FB_REQ_CONV/FB_CALC_CONV:.2f} > 1",ha="center")
ax.text(.24,.34,"Required share exceeds\ncalculated bootstrap supply",ha="center",va="center",fontsize=9)
x, y, w, h = .55, .4, .4, .13
ax.add_patch(Rectangle((x,y),w*F_BS_ST,h,facecolor="#c6dce5",edgecolor="#315a70",lw=.8))
ax.add_patch(Rectangle((x+w*F_BS_ST,y),w*F_NBI_ST,h,facecolor="#ead7b5",edgecolor="#806b4d",lw=.8))
ax.text(x+w*F_BS_ST/2,y+h/2,"76% bootstrap",ha="center",va="center",fontsize=9)
ax.text(x+w*(F_BS_ST+F_NBI_ST/2),y+h/2,"24%",ha="center",va="center",fontsize=9)
ax.text(.75,.29,"External drive: about 2.6–2.9 MA",ha="center",fontsize=10)
ax.text(.75,.16,"An independent power budget\nmust afford this share.",ha="center",va="center",fontsize=9)
fig.text(.5,.025,"Two specified models with different missions; the ST current split is a supply requirement.",ha="center",fontsize=8)
fig.subplots_adjust(left=.015,right=.985,bottom=.12,top=.97)
fig.savefig("figS_st_closure.pdf")
fig.savefig("figS_st_closure.png",dpi=180)
