#!/usr/bin/env python3
"""Machine-state figure M3 of the cumulative tokamak-construction sequence.

All geometry, colours and labels come from tokamak_build.py, so this stage is
guaranteed to retain every component introduced in the earlier stages.
Run:  python3 figM3.py     Outputs: figM3_stage3[_tall].pdf and .png
"""
from tokamak_build import render, Machine

if __name__ == "__main__":
    render(3, Machine(R0=3.0, a=1.0, n_tf=12), layout="tall")
    render(3, Machine(R0=3.0, a=1.0, n_tf=12))
