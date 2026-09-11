# Flux-network scale models

Two idealized calculations test whether tube radius and network length can select finite equilibrium scales. They do not establish a physical plasma junction or reactor.

- [Two-parameter obstruction](notes/g1a-two-parameter-scale.tex): the stated axial-flux/plasma model has a downhill anisotropic direction even when an isotropic restriction has a minimum.
- [Second-invariant model](notes/g1a-second-invariant.tex): under the declared positive-coefficient assumptions, adding a K/L term yields a unique finite minimum in the reduced scale model.
- [First symbolic check](code/g1a_two_parameter_checks.py) and [second symbolic check](code/g1a_second_invariant_checks.py) reproduce the algebra; they are not MHD simulations.

The length-minimization formulas in the first note require C > 0; when C = 0 the positive length derivative directly excludes a stationary point. The second note assumes a shape-independent inductance scaling. Those assumptions must be tested before treating the mathematical result as plasma physics.

Next: aspect-dependent inductance, admissible junction structure, perturbation stability, reconnection and transport. Preserve the distinction between a minimum of a reduced energy and a stable, useful fusion device. Personal review/signoff material is omitted from these technical copies.
