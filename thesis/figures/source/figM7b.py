#!/usr/bin/env python3
"""Annotation layer 7b: performance quantities on the machine."""
from tokamak_build import render, Machine
if __name__ == "__main__":
    m = Machine(R0=3.0, a=1.0, n_tf=12)
    render(16, m); render(16, m, layout="tall")
