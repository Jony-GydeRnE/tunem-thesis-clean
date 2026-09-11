#!/usr/bin/env python3
"""Atlas checkpoint (state 12) of the cumulative tokamak-construction sequence.

The conventional machine through state 11, with a component-to-variable map
and no later reactor hardware.
Run:  python3 figM12.py     Outputs: figM12_stage12[_tall].pdf and .png
"""
from tokamak_build import render, Machine

if __name__ == "__main__":
    render(12, Machine(R0=3.0, a=1.0, n_tf=12), layout="tall")
    render(12, Machine(R0=3.0, a=1.0, n_tf=12))
