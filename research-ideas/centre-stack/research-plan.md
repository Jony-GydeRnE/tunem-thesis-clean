# Where does the solenoid burden go?

**Question:** for one fixed spherical-tokamak plasma mission, how much central-solenoid burden can merging-compression remove, and where does that burden reappear?

This is a proposed research programme, not an established optimum or a demonstration of reactor closure. The immediate deliverable is the bounded feasibility study in the [prospectus](research-prospectus.pdf) ([source](research-prospectus.tex)). The broader options are indexed in [ideas.md](ideas.md).

## Common mission, different startup allocations

Compare CS-heavy, hybrid and merge-heavy cases at the same post-startup plasma current, density/temperature range, pulse duration, allowable field error and reliability target. Otherwise a smaller architecture can appear superior merely by doing less.

Use an allocation coordinate

\[
x_{\rm CS}=\Phi_{\rm CS}/\Phi_{\rm req},\qquad 0\le x_{\rm CS}\le1.
\]

This is a bookkeeping coordinate after the required flux and operating sequence are defined. Raw merging-coil flux is **not** solenoid-equivalent flux. Infer the equivalent benefit from the delivered plasma state and CS volt-seconds saved during a matched ramp. Avoid double-counting PF and merging contributions.

## Model blocks

1. **Startup:** a measured or validated current-formation and ramp requirement, including shot reliability.
2. **Radial build:** non-overlapping TF conductor, support, cooling, shielding, wall, solenoid and clearance regions. Shared functions must not be counted twice.
3. **Transient response:** actuator-to-plasma and actuator-to-winding coupling, including significant vessel/casing currents.
4. **Thermal recovery:** heat by location and material, removal before the next event, and the wall-plug cost of refrigeration.
5. **Duty and life:** a timeline of ramp, burn, recharge and recovery; overlap is counted once. Use fatigue life only where supported by data.

A local linearized circuit model may take the form

\[
L\dot{\mathbf i}+R\mathbf i=-M\dot{\mathbf I}_{\rm act}+\mathbf u.
\]

Here the matrices and operating point must be specified. A nonlinear superconducting model needs constitutive laws and differential inductances; positive-definite resistance and a global modal decomposition cannot simply be assumed.

Decompose energy before optimizing contacts:

\[
E_{\rm cold/event}=E_{\rm hyst}+E_{\rm structure,eddy}
+E_{\rm contact}+E_{\rm coupling}+E_{\rm joint}+\cdots.
\]

Define channels to avoid double-counting electromagnetic energy. For a repeated steady cycle, an initial refrigeration estimate is

\[
\overline P_{\rm cryo,e}=f_{\rm rep}E_{\rm cold/event}/{\rm COP}.
\]

COP depends on temperature and plant efficiency. Average heat removal alone does not establish acceptable peak temperature or recovery between events.

## First six weeks

1. Reproduce one published NI-HTS charging/discharging case.
2. Define one representative startup waveform and its field at the winding.
3. Add essential passive-current paths and check energy conservation.
4. Identify dominant loss, field-error and recovery channels.
5. Sweep only parameters that move those channels and useful plasma-field transfer.
6. Report signal, obstruction, indeterminate result or negligible coupling, with uncertainties.

Negligible forcing stops this magnet-coupling branch. Hysteresis points toward orientation/field angle; casing loss toward segmentation; consequential contact response toward manufacturable resistance zones. If formation uncertainty dominates, investigate delivered plasma state and reliability instead.

## Architecture and mechanism hypotheses

- **H0:** the active constraint may move from radial/startup limits to thermal recovery, fatigue or availability as cadence rises.
- **H1:** a hybrid allocation may outperform both extremes after all relevant penalties are included.
- **H2:** actuator placement, structure, conductor topology and waveform may separate useful plasma coupling from harmful winding response without sacrificing fault protection.
- **H3:** if a robust numerical tradeoff persists, investigate whether passivity or reciprocity bounds the achievable selectivity. Do not assume a familiar integral bound transfers unchanged to this system.

Start the feasibility map in \((x_{\rm CS},f_{\rm rep})\); add aspect ratio only after the reduced model is stable. Different turn counts and circuit topologies define different architecture families, not merely endpoints of one smooth contact-conductance sweep.

## Inputs to discuss with Professor Tan

What actually repeats and what stays energized? Which waveform and approximate geometry can be shared? What limits the winding or plasma scenario? Can external mutual forcing be added to the available model? What work already exists, and what are the publication/IP boundaries?

The prospectus identifies the initial literature to reproduce. For the separate bootstrap-affordability condition of thesis §§110–111, the decisive next input is a power-plant-mission ST equilibrium with its own recirculating-power budget; Menard's archived FNSF/pilot-plant dataset (DOI 10.11578/1366722) is the natural first source to check. A publication requires a consequential, credible and sufficiently new result; neither a positive nor a negative outcome is automatically publishable.
