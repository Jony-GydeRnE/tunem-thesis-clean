#!/usr/bin/env python3
"""Build the illustrated thesis guide, preserving PDF figures as vectors.

Usage: python3 build_thesis_guide.py --figures PATH --output PATH
Content is owned by the adjacent thesis_guide_content.json. Build intermediates
stay beside the output in .build; no thesis source or excerpt is modified.
"""
import argparse
import json
import re
import importlib.util
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz  # Compatibility with PyMuPDF releases before the renamed import.
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

W, H = 612, 792
LEFT, WIDTH = 52, 508
NAVY = HexColor('#18354B')
TEAL = HexColor('#176F74')
GOLD = HexColor('#D7A646')
INK = HexColor('#233342')
MUTED = HexColor('#586D7B')
PALE = HexColor('#EEF5F5')
RULE = HexColor('#CDDADE')


def register_fonts():
    # Read installed fonts only; never copy licensed system fonts into a repo.
    # Liberation Sans is metric-compatible with Arial, so the page layout is
    # identical on Linux; DejaVu Sans is wider and is a last resort only.
    roots = [Path('/System/Library/Fonts/Supplemental'),
             Path('/usr/share/fonts/truetype/liberation'),
             Path('/usr/share/fonts/truetype/liberation2'),
             Path('/usr/share/fonts/truetype/dejavu')]
    choices = [('Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'),
               ('LiberationSans-Regular.ttf', 'LiberationSans-Bold.ttf', 'LiberationSans-Italic.ttf'),
               ('LiberationSans-Regular.ttf', 'LiberationSans-Bold.ttf', 'LiberationSans-Italic.ttf'),
               ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSans-Oblique.ttf')]
    for root, files in zip(roots, choices):
        if all((root / f).exists() for f in files):
            for name, filename in zip(('Body', 'BodyBold', 'BodyItalic'), files):
                pdfmetrics.registerFont(TTFont(name, str(root / filename)))
            pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic')
            mpl = importlib.util.find_spec('matplotlib')
            math_font = Path(mpl.origin).parent/'mpl-data/fonts/ttf/DejaVuSans.ttf' if mpl else roots[-1]/'DejaVuSans.ttf'
            pdfmetrics.registerFont(TTFont('MathSymbols', str(math_font)))
            return
    raise RuntimeError('Install Arial, Liberation Sans or DejaVu Sans; no unembedded font fallback.')


class Guide:
    def __init__(self, path, figures):
        register_fonts()
        self.c = canvas.Canvas(str(path), pagesize=(W, H))
        self.c.setTitle('From Fusion Physics to the Centre Stack')
        self.c.setAuthor('Jony (TUNEM)')
        self.c.setSubject('Illustrated guide to the 166-page working thesis; September 2026')
        self.figures, self.placements, self.pages = figures, [], []
        self.styles = {
            'body': ParagraphStyle('body', fontName='Body', fontSize=10.5, leading=14.8,
                                   textColor=INK, spaceAfter=8),
            'small': ParagraphStyle('small', fontName='Body', fontSize=8.7, leading=11.7,
                                    textColor=MUTED),
            'caption': ParagraphStyle('caption', fontName='Body', fontSize=8.5, leading=11.4,
                                      textColor=MUTED),
            'equation': ParagraphStyle('equation', fontName='MathSymbols', fontSize=11.3, leading=21,
                                       textColor=NAVY, alignment=1),
            'cell': ParagraphStyle('cell', fontName='Body', fontSize=9.1, leading=12.6, textColor=INK),
            'headcell': ParagraphStyle('headcell', fontName='BodyBold', fontSize=9, leading=12, textColor=white),
        }

    def supported(self, text):
        for ch, replacement in {'²':'<super>2</super>', '³':'<super>3</super>', '⁴':'<super>4</super>'}.items():
            text=text.replace(ch,replacement)
        chars=pdfmetrics.getFont('Body').face.charToGlyph
        fallback=pdfmetrics.getFont('MathSymbols').face.charToGlyph
        def replace(match):
            ch=match.group(0)
            if ord(ch) in chars: return ch
            if ord(ch) not in fallback: raise ValueError(f'No glyph for {ch!r}')
            return f'<font name="MathSymbols">{ch}</font>'
        return re.sub(r'[^\x00-\x7f]', replace, text)

    def paragraph(self, text, style='body', x=LEFT, width=WIDTH, gap=8):
        p = Paragraph(self.supported(text), self.styles[style])
        _, height = p.wrap(width, H)
        p.drawOn(self.c, x, H - self.y - height)
        self.y += height + gap

    def heading(self, text):
        self.y += 3
        self.c.setFillColor(TEAL); self.c.setFont('BodyBold', 11.6)
        self.c.drawString(LEFT, H-self.y-11.6, text)
        self.y += 22

    def box(self, label, text):
        p=Paragraph(self.supported(text), self.styles['body']); _,ph=p.wrap(WIDTH-28,H)
        height=ph+42
        self.c.setFillColor(PALE); self.c.roundRect(LEFT,H-self.y-height,WIDTH,height,6,fill=1,stroke=0)
        self.c.setFillColor(TEAL);self.c.setFont('BodyBold',9)
        self.c.drawString(LEFT+14,H-self.y-18,label.upper())
        p.drawOn(self.c,LEFT+14,H-self.y-30-ph)
        self.y+=height+12

    def table(self, headers, rows, widths=None):
        widths=[WIDTH/len(headers)]*len(headers) if widths is None else [WIDTH*w for w in widths]
        cells=[[Paragraph(self.supported(h),self.styles['headcell']) for h in headers]]
        cells += [[Paragraph(self.supported(s),self.styles['cell']) for s in row] for row in rows]
        t=Table(cells,colWidths=widths,hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,PALE]),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),
            ('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),
            ('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,-1),(-1,-1),0.5,RULE)]))
        _,height=t.wrap(WIDTH,H);t.drawOn(self.c,LEFT,H-self.y-height);self.y+=height+12

    def figure(self, name, height, caption, clip=None):
        path=self.figures/(name+'.pdf')
        if not path.exists(): raise FileNotFoundError(path)
        doc=fitz.open(path);src=fitz.Rect(clip) if clip else doc[0].rect
        scale=min(WIDTH/src.width,height/src.height)
        fw,fh=src.width*scale,src.height*scale
        rect=fitz.Rect(LEFT+(WIDTH-fw)/2,self.y,LEFT+(WIDTH+fw)/2,self.y+fh)
        self.placements.append((self.index,path,rect,clip))
        self.y+=fh+5
        self.paragraph(caption,'caption',gap=12)

    def flow(self, rows):
        for i,(title,desc) in enumerate(rows):
            self.box(f'{i+1:02d}  {title}',desc)
            if i<len(rows)-1:
                self.c.setStrokeColor(GOLD);self.c.setLineWidth(1.5)
                cy=H-self.y+9
                self.c.line(W/2,cy,W/2,cy-7)
                self.c.line(W/2,cy-7,W/2-3,cy-3)
                self.c.line(W/2,cy-7,W/2+3,cy-3)

    def radial(self, variant):
        # Computed midplane intervals, not artwork inferred from a reactor photo.
        c=self.c; y0=self.y; x0=LEFT+28; scale=(WIDTH-65)/4
        rows=[(1.0,'Reference geometry: A = 4'),(2.0,'Lower aspect ratio: A = 2')] if variant=='aspect' else [(1.5,'Radial field convention: source-model geometry')]
        for i,(a,title) in enumerate(rows):
            top=y0+i*110
            c.setFont('BodyBold',9.7);c.setFillColor(NAVY);c.drawString(x0,H-top-12,title)
            rface=4-a-.65;yin=H-top-57
            segments=[(rface-.40,rface,HexColor('#CBDAEE'),'TF pack c'),(rface,4-a,HexColor('#D8DCDC'),'nuclear b'),(4-a,4,HexColor('#F2BDD5'),'plasma a')]
            for lo,hi,col,label in segments:
                c.setFillColor(col);c.setStrokeColor(MUTED);c.setLineWidth(.5)
                c.rect(x0+lo*scale,yin,(hi-lo)*scale,23,fill=1,stroke=1)
                c.setFillColor(INK);c.setFont('Body',7.5)
                if label=='TF pack c':
                    c.drawCentredString(x0+(lo+hi)*scale/2,yin+34,'c')
                else: c.drawCentredString(x0+(lo+hi)*scale/2,yin+8,label)
            c.setStrokeColor(MUTED);c.line(x0,yin-17,x0+4*scale,yin-17)
            for radius,label in [(0,'axis'),(4-a,f'R0 - a = {4-a:.1f} m'),(4,'R0 = 4 m')]:
                xx=x0+radius*scale;c.line(xx,yin-20,xx,yin-14)
                c.setFillColor(INK);c.setFont('Body',7.7);c.drawCentredString(xx,yin-31,label)
            if variant!='aspect':
                xx=x0+rface*scale;c.setStrokeColor(TEAL);c.line(xx,yin+26,xx,yin+40)
                c.setFillColor(TEAL);c.setFont('Body',8)
                c.drawString(xx+4,yin+38,'Bmax at the plasma-facing coil surface')
        self.y+=len(rows)*110
        self.paragraph('Computed schematic, not a proposed reactor. Both radial allocations are illustrative: b = 0.65 m and c = 0.40 m. Only the inboard half of the plasma section is shown.','caption',gap=12)

    def remedies(self):
        c=self.c;top=self.y
        labels=['Confinement H','Field ceiling','Plant output','Wall loading']
        width=116;gap=(WIDTH-4*width)/3
        for i,label in enumerate(labels):
            x=LEFT+i*(width+gap)
            c.setFillColor(PALE);c.setStrokeColor(TEAL);c.setLineWidth(.7)
            c.roundRect(x,H-top-32,width,32,4,fill=1,stroke=1)
            c.setFont('BodyBold',9);c.setFillColor(NAVY);c.drawCentredString(x+width/2,H-top-20,label)
            c.setStrokeColor(GOLD);c.line(x+width/2,H-top-35,W/2,H-top-66)
        c.setFillColor(NAVY);c.roundRect(LEFT+83,H-top-107,WIDTH-166,39,4,fill=1,stroke=0)
        c.setFont('BodyBold',10);c.setFillColor(white);c.drawCentredString(W/2,H-top-91,'Re-solve the coupled operating point')
        c.setStrokeColor(GOLD);c.line(W/2,H-top-110,W/2,H-top-130)
        c.line(W/2,H-top-130,W/2-4,H-top-125);c.line(W/2,H-top-130,W/2+4,H-top-125)
        c.setFont('BodyBold',10);c.setFillColor(TEAL);c.drawCentredString(W/2,H-top-149,'Retest density, pressure, pitch and current replacement')
        self.y+=167
        self.paragraph('One branch at a time changes an input; none bypasses the simultaneous tests. This summary diagram is reconstructed from the thesis comparison.','caption',gap=12)

    def page(self, index, data):
        self.index=index;self.pages.append(data['title']);c=self.c
        c.setFillColor(TEAL);c.setFont('BodyBold',8.2)
        c.drawString(LEFT,H-35,data['part'].upper())
        c.setFillColor(MUTED);c.setFont('Body',8)
        c.drawRightString(W-LEFT,H-35,'TUNEM  /  ILLUSTRATED THESIS GUIDE')
        title_style=ParagraphStyle('title',fontName='BodyBold',fontSize=23 if index else 30,
                                   leading=27 if index else 34,textColor=NAVY)
        title=Paragraph(data['title'],title_style);_,th=title.wrap(WIDTH,H)
        title.drawOn(c,LEFT,H-57-th)
        self.y=57+th+12
        c.setStrokeColor(GOLD);c.setLineWidth(2);c.line(LEFT,H-self.y,LEFT+85,H-self.y)
        self.y+=14
        for block in data['blocks']:
            kind=block[0]
            if kind=='p': self.paragraph(block[1])
            elif kind=='small': self.paragraph(block[1],'small')
            elif kind=='h': self.heading(block[1])
            elif kind=='eq': self.paragraph(block[1],'equation',gap=11)
            elif kind=='box': self.box(block[1],block[2])
            elif kind=='table': self.table(*block[1:])
            elif kind=='figure': self.figure(*block[1:])
            elif kind=='flow': self.flow(block[1])
            elif kind=='radial': self.radial(block[1])
            elif kind=='remedies': self.remedies()
            else: raise ValueError(kind)
        if self.y>701: raise RuntimeError(f'Page {index+1} overflows: body ends at {self.y:.1f}, max 701')
        # A stable thesis-section locator on every page; compact live source links.
        self.y=714
        self.paragraph(data['source'],'small',gap=0)
        if self.y>754: raise RuntimeError(f'Page {index+1}: footer source too long')
        c.setStrokeColor(RULE);c.setLineWidth(.5);c.line(LEFT,31,W-LEFT,31)
        c.setFillColor(MUTED);c.setFont('Body',7.7)
        c.drawString(LEFT,19,'Jony (TUNEM)  |  Working overview  |  September 2026')
        c.drawRightString(W-LEFT,19,f'{index+1:02d} / 20')
        c.showPage()

    def finish(self, raw, output):
        self.c.save();doc=fitz.open(raw)
        for index,path,rect,clip in self.placements:
            source=fitz.open(path)
            doc[index].show_pdf_page(rect,source,0,clip=fitz.Rect(clip) if clip else None)
        doc.set_toc([[1,title.replace('<br/>',' '),i+1] for i,title in enumerate(self.pages)])
        doc.set_metadata({'title':'From Fusion Physics to the Centre Stack',
                          'author':'Jony (TUNEM)',
                          'subject':'Illustrated guide to the 166-page working thesis; September 2026',
                          'keywords':'tokamak, spherical tokamak, fusion, centre stack, Freidberg, TUNEM',
                          'creator':'TUNEM thesis repository, thesis/code/build_thesis_guide.py',
                          'producer':'TUNEM thesis repository'})
        doc.save(output,garbage=4,deflate=True)
        return doc


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--figures',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--content',type=Path,default=Path(__file__).with_name('thesis_guide_content.json'))
    args=ap.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    work=args.output.parent/'.build';work.mkdir(exist_ok=True)
    raw=work/'guide-text.pdf';data=json.loads(args.content.read_text())
    assert len(data)==20
    guide=Guide(raw,args.figures)
    for i,page in enumerate(data):guide.page(i,page)
    doc=guide.finish(raw,args.output)
    for i in range(len(doc)):
        doc[i].get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(work/f'page-{i+1:02d}.png')
    print(f'Built {len(doc)} pages with {len(guide.placements)} vector figure placements: {args.output}')


if __name__=='__main__':main()
