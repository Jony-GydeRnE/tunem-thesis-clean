"""Reproduce the necessary central-TF-winding area checks on thesis page 120.

This is a transparent teaching ledger, not a reactor design optimizer.  Inputs are
declared below so a reader can alter one at a time and see which necessary condition
changes.  Passing the check does not certify stress, nuclear, plasma, or operations.
"""

from math import pi, sqrt

MU0 = 4.0 * pi * 1e-7  # H/m

# Declared teaching inputs; see the explicit warning in the manuscript.
R0_M = 3.0
B_INBOARD_M = 0.65
J_WP_A_PER_M2 = 70e6
F_WP = 0.40
TEST_ASPECT_RATIO = 2.0
TEST_FIELDS_T = (4.0, 6.0, 8.0)


def column_envelope_radius_m(major_radius_m: float, aspect_ratio: float,
                             inboard_nuclear_build_m: float) -> float:
    """Radius outside the central column after plasma and nuclear build."""
    return major_radius_m * (1.0 - 1.0 / aspect_ratio) - inboard_nuclear_build_m


def required_winding_area_m2(major_radius_m: float, field_t: float,
                             winding_pack_current_density_a_per_m2: float) -> float:
    """Ampere-law lower bound: area needed if all pack area carries current uniformly."""
    ampere_turns = 2.0 * pi * major_radius_m * field_t / MU0
    return ampere_turns / winding_pack_current_density_a_per_m2


def winding_occupancy(major_radius_m: float, aspect_ratio: float, field_t: float,
                      inboard_nuclear_build_m: float,
                      winding_pack_current_density_a_per_m2: float) -> float:
    """Fraction of total column envelope that the necessary winding area consumes."""
    radius_m = column_envelope_radius_m(
        major_radius_m, aspect_ratio, inboard_nuclear_build_m
    )
    if radius_m <= 0.0:
        return float("inf")
    return required_winding_area_m2(
        major_radius_m, field_t, winding_pack_current_density_a_per_m2
    ) / (pi * radius_m**2)


def minimum_aspect_ratio_for_winding(major_radius_m: float, field_t: float,
                                     inboard_nuclear_build_m: float,
                                     winding_pack_current_density_a_per_m2: float,
                                     winding_fraction: float) -> float:
    """Equation (centre-stack-aspect-bound), or infinity if its bracket is nonpositive."""
    if not 0.0 < winding_fraction < 1.0:
        raise ValueError("winding_fraction must lie between zero and one")
    bracket = (
        1.0
        - inboard_nuclear_build_m / major_radius_m
        - sqrt(
            2.0 * field_t
            / (
                MU0
                * winding_pack_current_density_a_per_m2
                * winding_fraction
                * major_radius_m
            )
        )
    )
    return float("inf") if bracket <= 0.0 else 1.0 / bracket


if __name__ == "__main__":
    envelope_radius_m = column_envelope_radius_m(
        R0_M, TEST_ASPECT_RATIO, B_INBOARD_M
    )
    print(f"R_env at A={TEST_ASPECT_RATIO:.1f}: {envelope_radius_m:.3f} m")
    print("B0 [T] | A_min,wp | eta_wp at A=2")
    for field_t in TEST_FIELDS_T:
        minimum_aspect_ratio = minimum_aspect_ratio_for_winding(
            R0_M, field_t, B_INBOARD_M, J_WP_A_PER_M2, F_WP
        )
        occupancy = winding_occupancy(
            R0_M, TEST_ASPECT_RATIO, field_t, B_INBOARD_M, J_WP_A_PER_M2
        )
        print(f"{field_t:6.1f} | {minimum_aspect_ratio:8.2f} | {occupancy:13.3f}")
