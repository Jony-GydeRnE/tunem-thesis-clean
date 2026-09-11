#!/usr/bin/env python3
"""Machine-state figure M14 of the cumulative tokamak-construction sequence.

Run:  python3 figM14.py     Outputs: figM14_stage14.pdf/.png and the _tall pair
"""
from tokamak_build import render, Machine

if __name__ == "__main__":
    m = Machine(R0=3.0, a=1.0, n_tf=12)
    render(14, m)
    render(14, m, layout="tall")
