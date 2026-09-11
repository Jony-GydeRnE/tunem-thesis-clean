#!/usr/bin/env python3
"""Run one included figure generator in ignored staging, with local imports."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('document', choices=['thesis', 'prologue'])
    parser.add_argument('generator')
    args = parser.parse_args()
    if Path(args.generator).name != args.generator or not args.generator.endswith('.py'):
        raise SystemExit('Pass a generator filename, not a path.')
    source_dir = ROOT / args.document / 'figures' / 'source'
    script = source_dir / args.generator
    if not script.is_file() or not script.name.startswith('fig'):
        raise SystemExit('No included figure generator with that name.')
    output = ROOT / '.build' / 'figures' / args.document / script.stem
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['MPLBACKEND'] = 'Agg'
    env['MPLCONFIGDIR'] = str(ROOT / '.build' / 'matplotlib')
    paths = [str(source_dir), str(ROOT / 'thesis/code/calculations')]
    if env.get('PYTHONPATH'):
        paths.append(env['PYTHONPATH'])
    env['PYTHONPATH'] = os.pathsep.join(paths)
    subprocess.run([sys.executable, str(script)], cwd=output, env=env, check=True)
    print(output)

if __name__ == '__main__':
    main()
