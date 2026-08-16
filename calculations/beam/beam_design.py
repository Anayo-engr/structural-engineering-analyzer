"""
Structural Engineering Analyzer
Beam Design Module

Basic reinforced-concrete beam design calculations.

Design basis:
- Eurocode-oriented approach
- Rectangular reinforced concrete section
- Simply supported beam
- Sagging bending moment
- Singly reinforced section

IMPORTANT:
This module is intended as a calculation-engine component.
Final structural design must be checked against the applicable
design code, project conditions, detailing requirements,
and a qualified structural engineer's review.
"""


import math


def calculate_effective_depth(overall_depth, concrete_cover, bar_diameter):
    """
    Calculate the effective depth of a reinforced concrete beam.

    Formula:

        d = h - c - Ø/2

    Parameters:
        overall_depth (float): Overall beam depth in mm
        concrete_cover (float): Nominal concrete cover in mm
        bar_diameter (float): Main reinforcement diameter in mm

    Returns:
        float: Effective depth in mm
    """

    if overall_depth <= 0:
        raise ValueError("Overall depth must be greater than zero.")

    if concrete_cover < 0:
        raise ValueError("Concrete cover cannot be negative.")

    if bar_diameter <= 0:
        raise ValueError("Bar diameter must be greater than zero.")

    effective_depth = (
        overall_depth
        - concrete_cover
        - (bar_diameter / 2)
    )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    return effective_depth


def calculate_design_bending_moment(
    dead_load,
    live_load,
    span,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the design bending moment for a simply supported
    beam carrying a uniformly distributed load.

    Design load:

        wEd = 1.35G + 1.50Q

    Maximum moment:

        MEd = wEd L² / 8

    Parameters:
        dead_load (float): Dead load in kN/m
        live_load (float): Live load in kN/m
        span (float): Beam span in metres
        dead_load_factor (float): Dead-load factor
        live_load_factor (float): Live-load factor

    Returns:
        float: Design bending moment in kNm
    """

    if dead_load < 0:
        raise ValueError("Dead load cannot be negative.")

    if live_load < 0:
        raise ValueError("Live load cannot be negative.")

    if span <= 0:
        raise ValueError("Span must be greater than zero.")

    design_load = (
        dead_load * dead_load_factor
        + live_load * live_load_factor
    )

    moment = (design_load * span ** 2) / 8

    return moment


def calculate_required_steel_area(
    design_moment,
    effective_depth,
    steel_strength,
    lever_arm_factor=0.9
):
    """
    Estimate the required tensile reinforcement area.

    Simplified relationship:

        As = MEd / (0.87 fy z)

    where:

        z = 0.9d

    Parameters:
        design_moment (float): Design bending moment in kNm
        effective_depth (float): Effective depth in mm
        steel_strength (float): Characteristic yield strength of steel
                                 in N/mm²
        lever_arm_factor (float): Approximate z/d ratio

    Returns:
        float: Required reinforcement area in mm²
    """

    if design_moment <= 0:
        raise ValueError(
            "Design moment must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if not 0 < lever_arm_factor <= 1:
        raise ValueError(
            "Lever arm factor must be greater than 0 and no more than 1."
        )

    # Convert kNm to Nmm
    moment_nmm = design_moment * 1_000_000

    # Approximate lever arm
    lever_arm = lever_arm_factor * effective_depth

    required_area = (
        moment_nmm
        / (0.87 * steel_strength * lever_arm)
    )

    return required_area


def calculate_minimum_steel_area(
    beam_width,
    effective_depth,
    concrete_strength,
    minimum_ratio=0.0013
):
    """
    Calculate a simplified minimum tension reinforcement area.

    Basic form:

        As,min = rho_min × b × d

    Parameters:
        beam_width (float): Beam width in mm
        effective_depth (float): Effective depth in mm
        concrete_strength (float): Concrete characteristic strength
                                    in N/mm²
        minimum_ratio (float): Minimum reinforcement ratio used
                               for this preliminary calculation

    Returns:
        float: Minimum reinforcement area in mm²
    """

    if beam_width <= 0:
        raise ValueError(
            "Beam width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if minimum_ratio <= 0:
        raise ValueError(
            "Minimum reinforcement ratio must be greater than zero."
        )

    minimum_area = (
        minimum_ratio
        * beam_width
        * effective_depth
    )

    return minimum_area


def select_required_steel_area(
    required_area,
    minimum_area
):
    """
    Select the governing reinforcement area.

    The required reinforcement must not be less than
    the specified minimum reinforcement.

    Returns:
        float: Governing reinforcement area in mm²
    """

    if required_area <= 0:
        raise ValueError(
            "Required reinforcement area must be greater than zero."
        )

    if minimum_area <= 0:
        raise ValueError(
            "Minimum reinforcement area must be greater than zero."
        )

    return max(required_area, minimum_area)


def calculate_beam_design(
    beam_width,
    overall_depth,
    concrete_cover,
    bar_diameter,
    dead_load,
    live_load,
    span,
    concrete_strength=25,
    steel_strength=500
):
    """
    Perform a preliminary reinforced-concrete beam design calculation.

    Returns:
        dict: Design results.
    """

    effective_depth = calculate_effective_depth(
        overall_depth,
        concrete_cover,
        bar_diameter
    )

    design_moment = calculate_design_bending_moment(
        dead_load,
        live_load,
        span
    )

    required_steel = calculate_required_steel_area(
        design_moment,
        effective_depth,
        steel_strength
    )

    minimum_steel = calculate_minimum_steel_area(
        beam_width,
        effective_depth,
        concrete_strength
    )

    governing_steel = select_required_steel_area(
        required_steel,
        minimum_steel
    )

    return {
        "beam_width_mm": beam_width,
        "overall_depth_mm": overall_depth,
        "effective_depth_mm": effective_depth,
        "concrete_strength_N_per_mm2": concrete_strength,
        "steel_strength_N_per_mm2": steel_strength,
        "design_bending_moment_kNm": design_moment,
        "required_steel_area_mm2": required_steel,
        "minimum_steel_area_mm2": minimum_steel,
        "governing_steel_area_mm2": governing_steel
    }
