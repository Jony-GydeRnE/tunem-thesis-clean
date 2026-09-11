#!/usr/bin/env python3
"""Four original vector figures for Before the Machine; no network at build time.

Run through code/build/render_figure.py. PDFs, SVGs, PNG previews, and a small
verification JSON stage in the runner's output folder. Schematic coordinates
are NOT measured nuclear geometry. Numerical data and model checks are explicit.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch

INK = '#183C50'
BLUE = '#21678A'
ORANGE = '#AF5427'
TEAL = '#24776D'
GRAY = '#65717A'
LIGHT = '#EAF1F4'
DATA = Path(__file__).parent / 'data/ame2020_mass_1.mas20.txt'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 9,
    'axes.labelsize': 9, 'axes.titlesize': 10, 'text.color': INK,
    'axes.labelcolor': INK, 'axes.edgecolor': GRAY,
    'xtick.color': GRAY, 'ytick.color': GRAY,
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
    'figure.facecolor': 'white', 'savefig.facecolor': 'white',
})


def save(fig, name):
    # Fixed canvas size, rather than tight cropping, keeps final label sizes stable.
    for ext in ('pdf', 'svg', 'png'):
        fig.savefig(f'{name}.{ext}', dpi=220,
                    metadata={'Creator': 'Terra; figN_opening.py'} if ext == 'pdf' else None)
    plt.close(fig)


def clean(ax, x=(0, 3), y=(0, 2)):
    ax.set(xlim=x, ylim=y)
    ax.axis('off')


def arrow(ax, start, end, color=INK, lw=1.4, style='-|>', **kw):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style,
                                mutation_scale=10, lw=lw, color=color, **kw))


def soft_cloud(ax, center, width, height, color, alpha=.035):
    # Smooth vector fill, without outlines suggesting orbital tracks or hard walls.
    for scale in np.linspace(1.45, .12, 30):
        ax.add_patch(Ellipse(center, width*scale, height*scale,
                             facecolor=color, edgecolor='none', alpha=alpha))


def y_radius(ax, r):
    pos=ax.get_position(); w,h=ax.figure.get_size_inches()
    return r*(pos.width*w/np.ptp(ax.get_xlim()))/(pos.height*h/np.ptp(ax.get_ylim()))


def nucleon(ax, x, y, kind, r=.14, size=9):
    color = ORANGE if kind == 'p' else BLUE
    ax.add_patch(Ellipse((x, y), 2*r, 2*y_radius(ax,r), facecolor=color, edgecolor='white', lw=.6))
    ax.text(x, y, kind, ha='center', va='center', color='white',
            fontsize=size, fontweight='bold')


def nucleus(ax, center, kind, r=.14):
    x, y = center
    shapes = {
        'D': [(-.7, 0, 'p'), (.7, 0, 'n')],
        'T': [(-.75, .4, 'p'), (.75, .4, 'n'), (0, -.85, 'n')],
        'alpha': [(-.65, .65, 'p'), (.65, .65, 'n'),
                  (-.65, -.65, 'n'), (.65, -.65, 'p')],
        'n': [(0, 0, 'n')],
    }
    for dx, dy, k in shapes[kind]:
        nucleon(ax, x+dx*1.3*r, y+dy*1.3*y_radius(ax,r), k, r=r)


def atom():
    fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.40))
    fig.subplots_adjust(left=.015, right=.985, top=.86, bottom=.06, wspace=.23)
    for ax in axes:
        clean(ax)
    axes[0].set_title('A   ATOM', loc='left', color=INK, fontweight='bold')
    axes[1].set_title('B   NUCLEUS', loc='left', color=INK, fontweight='bold')
    axes[2].set_title('C   A PROTON', loc='left', color=INK, fontweight='bold')
    a = axes[0]
    soft_cloud(a, (1.45, 1.15), 1.5, 1.20, BLUE)
    a.add_patch(Circle((1.45, 1.15), .095, color=ORANGE))
    a.annotate(r'nucleus: $+2e$', xy=(1.45, 1.15), xytext=(.12, 1.86),
               arrowprops={'arrowstyle':'-', 'color':GRAY, 'lw':.8}, fontsize=8.6)
    a.text(1.5, .27, 'Helium atom: 2 electrons\ncloud has total charge '+r'$-2e$',
           ha='center', fontsize=8.5, linespacing=1.4)
    b = axes[1]
    soft_cloud(b, (1.5, 1.15), 1.20, 1.0, GRAY, alpha=.015)
    nucleus(b, (1.5, 1.15), 'alpha', r=.26)
    b.text(1.5, .27, '2 protons + 2 neutrons\n'+r'$p: +e\qquad n: 0$',
           ha='center', fontsize=8.5, linespacing=1.4)
    c = axes[2]
    soft_cloud(c, (1.5, 1.15), 1.7, 1.06, TEAL)
    c.text(1.5, 1.28, r'net $uud$', ha='center', fontsize=15, fontweight='bold')
    c.text(1.5, .92, r'net electric charge $+e$', ha='center', fontsize=8.4)
    c.text(1.5, .27, 'Quarks, gluons and fluctuations\nnot just three static objects',
           ha='center', fontsize=8.1, linespacing=1.4)
    fig.text(.5, .94, 'Separate scale windows; schematic, not to scale',
             ha='center', fontsize=8.3, color=GRAY)
    for x in [.323, .66]:
        fig.add_artist(FancyArrowPatch((x, .56), (x+.025, .56),
                       transform=fig.transFigure, arrowstyle='-|>',
                       mutation_scale=11, color=GRAY, lw=1))
    save(fig, 'figN0_atom_to_quarks')


def charge(ax, x, y, label, heavy=True):
    ax.add_patch(Circle((x, y), .17 if heavy else .15,
                        facecolor=INK if heavy else ORANGE, edgecolor='white', lw=.6))
    ax.text(x, y, label, color='white', va='center', ha='center', fontsize=9.2)


def tube(ax, x1, x2, y):
    for width, alpha in [(16,.04),(11,.09),(6,.16),(2,.35)]:
        ax.plot([x1,x2],[y,y],color=TEAL,lw=width,alpha=alpha,solid_capstyle='round')


def string_breaking():
    fig = plt.figure(figsize=(6.8, 3.20))
    xs = [.025,.355,.685]
    axs = [fig.add_axes([x,.55,.29,.35]) for x in xs]
    for ax in axs: clean(ax, y=(0,1.8))
    a,b,c = axs
    for ax,title in zip(axs,['A   Nearby sources','B   Work stretches the tube','C   A light pair forms']):
        ax.set_title(title,loc='left',fontsize=9.4,fontweight='bold')
    tube(a, .9, 1.8, 1.0)
    charge(a,.9,1.,r'$Q$'); charge(a,1.8,1.,r'$\bar Q$')
    a.text(1.45,.16,'external heavy sources',ha='center',fontsize=8.3)
    tube(b, .3,2.7,1.)
    charge(b,.3,1.,r'$Q$'); charge(b,2.7,1.,r'$\bar Q$')
    b.text(1.5,.16,'approximately linear energy cost',ha='center',fontsize=8.1)
    for center in [.67,2.35]:
        c.add_patch(Ellipse((center,1.0),1.05,.86,facecolor=LIGHT,
                           edgecolor=GRAY,lw=.7,linestyle=(0,(3,2))))
    tube(c,.39,.92,1.); tube(c,2.08,2.61,1.)
    charge(c,.39,1.,r'$Q$'); charge(c,.92,1.,r'$\bar q$',False)
    charge(c,2.08,1.,r'$q$',False); charge(c,2.61,1.,r'$\bar Q$')
    c.text(1.5,.16,'two color-neutral mesons',ha='center',fontsize=8.4)
    ax=fig.add_axes([.105,.15,.42,.27])
    r=np.linspace(.05,3.4,250)
    ax.plot(r,np.minimum(r,2),color=TEAL,lw=2)
    ax.plot([2,3.4],[2,3.4],color=GRAY,lw=1,ls='--')
    ax.set(xlim=(0,3.5),ylim=(0,3.6),xticks=[],yticks=[])
    ax.set_xlabel(r'separation $r$ (schematic)',fontsize=8.5,labelpad=1)
    ax.set_ylabel(r'$V(r)$',rotation=0,labelpad=12)
    ax.spines[['top','right']].set_visible(False)
    ax.text(.45,.23,'tube',fontsize=8.4)
    ax.text(2.1,1.55,'broken string',fontsize=8.1)
    fig.text(.60,.37,'Solid: lower-energy branch\nDashed: unbroken-string branch',
             fontsize=8.3,linespacing=1.6)
    fig.text(.60,.16,'Qualitative crossover, no physical scale.\nNot a picture of a proton.\nNo isolated colored products.',
             fontsize=8.3,linespacing=1.4,color=GRAY)
    save(fig,'figN1_string_breaking')


def binding_recoil():
    fig=plt.figure(figsize=(6.8,3.15))
    a=fig.add_axes([.02,.07,.58,.80]); clean(a,x=(0,10),y=(0,4))
    a.set_title('A   Same nucleons, different arrangement',loc='left',fontweight='bold',fontsize=9.5)
    for center,kind in [((1.0,2.9),'D'),((2.95,2.9),'T'),((6.5,2.9),'alpha'),((8.8,2.9),'n')]:
        nucleus(a,center,kind,r=.22)
    a.text(1.95,2.9,'+',ha='center',va='center',fontsize=14)
    a.text(7.7,2.9,'+',ha='center',va='center',fontsize=14)
    arrow(a,(4.,2.9),(5.,2.9))
    for x,label in [(1,'D'),(2.95,'T'),(6.5,r'$\alpha$'),(8.8,'free n')]:
        a.text(x,2.3,label,ha='center',fontsize=9)
    a.text(5,1.80,'Each side contains 2 protons + 3 neutrons',ha='center',fontsize=8.7)
    a.plot([.3,9.7],[1.52,1.52],color=GRAY,lw=.5,alpha=.4)
    a.text(5,1.22,'CENTER-OF-MOMENTUM RECOIL',ha='center',fontsize=8.1,color=GRAY)
    nucleus(a,(3.4,.77),'alpha',r=.16); nucleus(a,(6.7,.77),'n',r=.16)
    arrow(a,(3.02,.77),(1.55,.77),color=ORANGE,lw=1.8)
    arrow(a,(7.08,.77),(8.55,.77),color=BLUE,lw=1.8)
    a.text(2.6,.20,r'$K_\alpha\simeq3.5$ MeV',ha='center',fontsize=9,color=ORANGE)
    a.text(7.4,.20,r'$K_n\simeq14.1$ MeV',ha='center',fontsize=9,color=BLUE)
    b=fig.add_axes([.68,.16,.29,.67])
    b.set(xlim=(0,1),ylim=(-33,6),xticks=[],yticks=[])
    b.spines[:].set_visible(False)
    b.set_title('B   Rest-energy difference',loc='center',fontweight='bold',fontsize=9.5,pad=20)
    b.hlines(0,0,.9,color=GRAY,lw=.8,ls=':')
    b.text(.45,2,'free 2p + 3n',ha='center',fontsize=8.5,color=GRAY)
    for e,color in [(-10.706,ORANGE),(-28.296,BLUE)]: b.hlines(e,.08,.86,color=color,lw=2)
    b.text(.46,-8.0,'D + T',ha='center',fontsize=10,color=ORANGE)
    b.text(.46,-32.,r'$\alpha+n$',ha='center',fontsize=10,color=BLUE)
    arrow(b,(.19,-11.0),(.19,-28.0),style='<->',color=TEAL)
    b.text(.31,-19.5,r'$Q\simeq17.6$ MeV',va='center',fontsize=9,color=TEAL)
    fig.text(.82,.055,'Reference: free nucleons at rest',ha='center',fontsize=8,color=GRAY)
    save(fig,'figN3_binding_recoil')


def read_ame():
    rows=[]
    for line in DATA.read_text().splitlines()[36:]:
        try:
            n,z,a=int(line[4:9]),int(line[9:14]),int(line[14:19])
            symbol=line[20:23].strip()
            field=line[54:67].strip()
            if '#' in field or '*' in field: continue
            binding=float(field)/1000
        except ValueError: continue
        if a==n+z and a>0 and binding>=0:
            rows.append((a,z,symbol,binding))
    assert len(rows)>2000, len(rows)
    by={(a,z):b for a,z,s,b in rows}
    assert abs(by[(62,28)]-8.7945555)<1e-7
    assert abs(by[(56,26)]-8.7903563)<1e-7
    return rows


def barrier_solution():
    # Dimensionless x is x/ell, ell=hbar/sqrt(2*mu*U0); E/U0=0.35.
    E=.35; L=2.2; k=np.sqrt(E); q=np.sqrt(1-E)
    ep,em,et=np.exp(q*L),np.exp(-q*L),np.exp(1j*k*L)
    M=np.array([[1,-1,-1,0],[-1j*k,-q,q,0],
                [0,ep,em,-et],[0,q*ep,-q*em,-1j*k*et]],complex)
    rhs=np.array([-1,-1j*k,0,0],complex)
    refl,ap,am,trans=np.linalg.solve(M,rhs)
    assert np.max(np.abs(M@np.array([refl,ap,am,trans])-rhs))<1e-12
    R,T=abs(refl)**2,abs(trans)**2
    assert abs(R+T-1)<1e-12
    T_exact=1/(1+np.sinh(q*L)**2/(4*E*(1-E)))
    assert abs(T-T_exact)<1e-12
    x=np.linspace(-3,5.2,1300)
    psi=np.where(x<0,np.exp(1j*k*x)+refl*np.exp(-1j*k*x),
                 np.where(x<=L,ap*np.exp(q*x)+am*np.exp(-q*x),trans*np.exp(1j*k*x)))
    return x,psi,E,L,R,T


def energy_landscape():
    rows=read_ame()
    fig=plt.figure(figsize=(6.8,3.75))
    a=fig.add_axes([.085,.27,.40,.58])
    fig.text(.025,.96,'A   Binding energy across nuclei',fontsize=9.5,fontweight='bold')
    subset=[r for r in rows if r[0]<=260]
    aa=np.array([r[0] for r in subset]); bb=np.array([r[3] for r in subset])
    a.scatter(aa,bb,s=3,color=GRAY,alpha=.25,linewidths=0)
    env={}
    for A,Z,S,B in subset: env[A]=max(env.get(A,0),B)
    a.plot(sorted(env),[env[k] for k in sorted(env)],color=BLUE,lw=1.25)
    a.scatter([56,62],[8.7903563,8.7945555],s=18,color=ORANGE,zorder=5)
    a.set(xlim=(0,260),ylim=(0,9.7),xlabel=r'nucleon count $A$',
          ylabel=r'binding per nucleon $B/A$ (MeV)',xticks=[0,60,120,180,240],yticks=[0,3,6,9])
    a.spines[['top','right']].set_visible(False)
    a.annotate('iron–nickel',xy=(62,8.7945),xytext=(135,9.1),fontsize=8.5,
               arrowprops={'arrowstyle':'-', 'color':ORANGE,'lw':.7},color=ORANGE)
    a.text(110,6.1,'Ni-62: 8.795 MeV\nFe-56: 8.790 MeV',fontsize=8.2,linespacing=1.5)
    arrow(a,(13,4.4),(48,7.1),color=TEAL,lw=1)
    a.text(15,3.2,'light fusion',fontsize=8,color=TEAL)
    arrow(a,(237,6.7),(155,7.4),color=TEAL,lw=1)
    a.text(152,5.0,'heavy fission',fontsize=8,color=TEAL)
    fig.text(.06,.04,'AME2020 measured entries (no # estimates).\nLine: largest tabulated B/A at each A.',
             fontsize=8.1,color=GRAY,linespacing=1.4)
    fig.text(.57,.96,'B   An approach barrier',fontsize=9.5,fontweight='bold')
    b=fig.add_axes([.60,.61,.36,.23]); c=fig.add_axes([.60,.27,.36,.23],sharex=b)
    x,psi,E,L,R,T=barrier_solution()
    b.plot([-3,0,0,L,L,5.2],[0,0,1,1,0,0],color=INK,lw=1.5)
    b.axhline(E,color=ORANGE,lw=1.2,ls='--')
    b.text(3.2,E+.1,r'$E/U_0=0.35$',ha='center',fontsize=8,color=ORANGE)
    b.set(xlim=(-3,5.2),ylim=(-.08,1.28),yticks=[0,1],ylabel=r'$U/U_0$')
    b.tick_params(labelbottom=False,bottom=False)
    c.plot(x,abs(psi),color=TEAL,lw=1.5)
    for ax in [b,c]:
        ax.axvspan(0,L,color=GRAY,alpha=.10)
        ax.spines[['top','right']].set_visible(False)
        ax.tick_params(labelsize=8)
    c.set(ylim=(0,2.1),yticks=[0,1,2],xticks=[-2,0,2.2,4],
          xlabel=r'position $x/\ell$',ylabel=r'$|\psi|$')
    c.text(2.9,.9,'nonzero\ntransmission',fontsize=8,linespacing=1.2)
    fig.text(.60,.04,r'Toy model: $\ell=\hbar/\sqrt{2\mu U_0}$.'+'\nNot a D–T cross-section calculation.',
             fontsize=8.1,color=GRAY,linespacing=1.4)
    save(fig,'figN4_binding_and_barrier')
    return {'measured_rows':len(rows),'plotted_rows':len(subset),
            'barrier_E_over_U0':E,'barrier_width_over_ell':L,
            'reflection':R,'transmission':T,'R_plus_T':R+T,
            'ame_sha256':hashlib.sha256(DATA.read_bytes()).hexdigest()}


if __name__=='__main__':
    atom(); string_breaking(); binding_recoil(); checks=energy_landscape()
    Path('figN_opening_validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
