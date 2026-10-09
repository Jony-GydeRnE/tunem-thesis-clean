#!/usr/bin/env python3
"""Compare fixed-output and fixed-wall-loading scalings at fixed cross-section."""
from sketch_base import *
W,H=TEXTWIDTH_IN,4.40
fig,ax=canvas(W,H)
R1,R2,a=1.,1.5,.34
f=R2/R1

def torus(cx,cy,R,shade):
    th=np.linspace(0,2*np.pi,400);scale=.27
    for radius in (R-a,R+a):
        ax.plot(cx+scale*radius*np.cos(th),cy+scale*radius*np.sin(th),color=PALETTE['wall'],lw=1)
    x=np.r_[cx+scale*(R+a)*np.cos(th),(cx+scale*(R-a)*np.cos(th))[::-1]]
    y=np.r_[cy+scale*(R+a)*np.sin(th),(cy+scale*(R-a)*np.sin(th))[::-1]]
    ax.fill(x,y,color=PALETTE['plasma'],alpha=shade)
    arrow(ax,(cx,cy),(cx+scale*R,cy),PALETTE['vessel'],lw=.9)
    ax.text(cx+.5*scale*R,cy+.07,r'$R_0$',ha='center',fontsize=9)

for row,y,heading,detail,col,shade in [
 ('A',3.22,r'A. Raise $P_E$ at fixed $W_n$',r'$R_0,\ V,\ P_E:\ \times 1.50$'+'\n'+r'$p,n:\ \times 1.00$'+'\n'+'Same pressure; larger total output.',PALETTE['cs'],.30),
 ('B',1.38,r'B. Lower $W_n$ at fixed $P_E$',r'$R_0,\ V:\ \times 1.50$'+'\n'+r'$W_n:\ \times 0.67;\quad p,n:\ \times 0.82$'+'\n'+'Same output; lower power density.',PALETTE['pf'],.30/np.sqrt(f))]:
    ax.text(.1,y+.67,heading,fontsize=10,va='top',color=col)
    torus(.76,y,R1,.30);torus(2.22,y,R2,shade)
    ax.text(.76,y-.61,'reference',fontsize=8.3,ha='center')
    ax.text(2.22,y-.61,r'$R_0\times1.50$',fontsize=8.3,ha='center')
    ax.text(3.20,y+.34,detail,fontsize=9,va='top',linespacing=1.8)
ax.plot([.1,W-.1],[2.20,2.20],color='.85',lw=.8)
ax.text(W/2,4.32,'TWO WAYS TO INCREASE PLASMA VOLUME',fontsize=10.4,ha='center',va='top')
save_exact(fig,'figS_scale_two_ways',
           'Fixed minor radius, elongation, temperature and profiles. Plan views; shading represents pressure.',y=.12)
print('volume ratio',f,'pressure ratios',1.,1/np.sqrt(f),'wall-loading ratio',1/f)
