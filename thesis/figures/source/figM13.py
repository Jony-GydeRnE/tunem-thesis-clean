#!/usr/bin/env python3
"""Machine-state figure M13 of the cumulative tokamak-construction sequence.

Run:  python3 figM13.py     Outputs: figM13_stage13.pdf/.png and the _tall pair
"""
from tokamak_build import render, Machine

if __name__ == "__main__":
    m = Machine(R0=3.0, a=1.0, n_tf=12)
    render(13, m)
    render(13, m, layout="tall")
