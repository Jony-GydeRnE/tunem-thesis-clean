#!/usr/bin/env python3
"""Build selected documents into ignored staging; never overwrite source PDFs."""
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
    'flux-two-parameter': 'research-ideas/flux-networks/notes/g1a-two-parameter-scale.tex',
    'flux-second-invariant': 'research-ideas/flux-networks/notes/g1a-second-invariant.tex',
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('document', choices=DOCUMENTS)
    parser.add_argument('--online', action='store_true')
    parser.add_argument('--bundle', type=Path)
    args = parser.parse_args()
    executable = shutil.which('tectonic')
    if not executable:
        raise SystemExit('Tectonic is required; see thesis/code/README.md.')
    source = ROOT / DOCUMENTS[args.document]
    output = ROOT / '.build' / 'documents' / args.document
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault('TECTONIC_CACHE_DIR', str(ROOT / '.build' / 'tex-cache'))
    command = [executable, '--keep-logs', '--keep-intermediates', '--outdir', str(output)]
    if not args.online:
        command.append('--only-cached')
    if args.bundle:
        command += ['--bundle', str(args.bundle.resolve())]
    subprocess.run(command + [str(source)], cwd=source.parent, env=env, check=True)
    print(output / source.with_suffix('.pdf').name)

if __name__ == '__main__':
    main()
