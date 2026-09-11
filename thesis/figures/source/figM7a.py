#!/usr/bin/env python3
"""Annotation layer 7a: total plasma current versus its profile."""
from tokamak_build import render, Machine
if __name__ == "__main__":
    m = Machine(R0=3.0, a=1.0, n_tf=12)
    render(15, m); render(15, m, layout="tall")
