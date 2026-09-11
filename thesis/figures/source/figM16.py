#!/usr/bin/env python3
"""Low-aspect-ratio centre-stack state (brief at v1_fresh l.4934).

The ONLY change from stage 14 is the aspect ratio: R0/a = 2 instead of 3.  The
plasma, the nuclear island b and the TF function are the same objects.  That is
the brief's point and it is enforced by construction -- this script passes a
different Machine to the same renderer, it does not draw a different machine.
"""
from tokamak_build import render, Machine

m = Machine(R0=2.0, a=1.0, kappa=1.70, delta=0.40)
render(19, m=m, layout="tall")
render(19, m=m)
