#!/usr/bin/env python3
"""Build selected documents into ignored staging; never overwrite source PDFs.

Uses Tectonic when installed, otherwise falls back to latexmk (pdfTeX/XeTeX
from an ordinary TeX Live). Build order matters for one document: the edited
excerpt includes pages of thesis/thesis-draft.pdf, so build `thesis` first
and install its PDF before building `excerpt`.
"""
import argparse
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = {
    'thesis': 'thesis/thesis-draft.tex',
    'prologue': 'prologue/before-the-machine.tex',
    'proposal': 'proposal/proposal.tex',
    'executive-summary': 'proposal/executive-summary.tex',
    'excerpt': 'progress-report/edited-excerpt-30-pages.tex',
    'prospectus': 'research-ideas/centre-stack/research-prospectus.tex',
    'flux-two-parameter': 'research-ideas/flux-networks/notes/g1a-two-parameter-scale.tex',
    'flux-second-invariant': 'research-ideas/flux-networks/notes/g1a-second-invariant.tex',
}
# Documents whose sources need XeTeX (CJK fonts).
XELATEX = {'proposal', 'prologue'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('document', choices=DOCUMENTS)
    parser.add_argument('--online', action='store_true')
    parser.add_argument('--bundle', type=Path)
    parser.add_argument('--latexmk', action='store_true', help='use latexmk even if Tectonic is installed')
    args = parser.parse_args()
    source = ROOT / DOCUMENTS[args.document]
    output = ROOT / '.build' / 'documents' / args.document
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    tectonic = shutil.which('tectonic')
    latexmk = shutil.which('latexmk')
    if tectonic and not args.latexmk:
        env.setdefault('TECTONIC_CACHE_DIR', str(ROOT / '.build' / 'tex-cache'))
        command = [tectonic, '--keep-logs', '--keep-intermediates', '--outdir', str(output)]
        if not args.online:
            command.append('--only-cached')
        if args.bundle:
            command += ['--bundle', str(args.bundle.resolve())]
    elif latexmk:
        engine = '-xelatex' if args.document in XELATEX else '-pdf'
        command = [latexmk, engine, '-interaction=nonstopmode', '-halt-on-error',
                   f'-output-directory={output}']
    else:
        raise SystemExit('Tectonic or latexmk (TeX Live) is required; see thesis/code/README.md.')
    subprocess.run(command + [str(source)], cwd=source.parent, env=env, check=True)
    print(output / source.with_suffix('.pdf').name)

if __name__ == '__main__':
    main()
