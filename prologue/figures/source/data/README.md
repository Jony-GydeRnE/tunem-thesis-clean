# AME2020 plot input

[ame2020_mass_1.mas20.txt](ame2020_mass_1.mas20.txt) is the unmodified mass table downloaded on 11 September 2026 from the [IAEA Atomic Mass Data Center](https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt).

Evaluation: Huang et al., *Chinese Physics C* 45, 030002 (2021), and Wang et al., 45, 030003 (2021). Retain the original header and attribution.

SHA-256: `e8599c6d7f724fac91934e59f1b9de8fb8f63e820f4b39456b790665ed2a3307`.

[The generator](../figN_opening.py) reads binding energy per nucleon, converts keV to MeV, excludes estimated/unavailable entries, and plots 2,539 retained entries through A = 260. The line is their upper envelope at each A, not a reaction trajectory or stability boundary. The table convention is retained; no electron-binding correction is introduced by the plot.

The barrier panel is an independent constant-barrier model; it does not predict a D–T cross section. Its matching and current-conservation checks are generated alongside the figures.
