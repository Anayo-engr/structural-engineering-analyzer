"""
Structural Engineering Analyzer
Beam Shear Design Module

Preliminary shear calculations for reinforced-concrete beams.

Design basis:
- Eurocode-oriented approach
- Simply supported beam
- Uniformly distributed load

This module is a preliminary calculation component.
Final structural design requires complete code checks,
detailing requirements, load combinations, and engineering review.
"""


import math


def calculate_design_shear_force(
    dead_load,
    live_load,
    span,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the design shear force at a support.

    For a simply supported beam under UDL:

        VEd = wEd × L / 2

    where:

        wEd = 1.35G + 1.50Q

    Parameters:
        dead_load (float): Dead load in kN/m
        live_load (float): Live load in kN/m
        span (float): Beam span in metres
        dead_load_factor (float): Dead-load factor
        live_load_factor (float): Live-load factor

    Returns:
        float: Design shear force in kN
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

    design_shear = (design_load * span) / 2

    return design_shear


def calculate_shear_stress(
    design_shear,
    beam_width,
    effective_depth
):
    """
    Calculate the nominal shear stress.

        vEd = VEd / (b × d)

    Parameters:
        design_shear (float): Design shear force in kN
        beam_width (float): Beam width in mm
        effective_depth (float): Effective depth in mm

    Returns:
        float: Shear stress in N/mm²
    """

    if design_shear < 0:
        raise ValueError("Design shear cannot be negative.")

    if beam_width <= 0:
        raise ValueError(
            "Beam width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    # Convert kN to N
    shear_force_n = design_shear * 1000

    shear_stress = (
        shear_force_n
        / (beam_width * effective_depth)
    )

    return shear_stress


def calculate_longitudinal_reinforcement_ratio(
    steel_area,
    beam_width,
    effective_depth
):
    """
    Calculate the longitudinal reinforcement ratio.

        rho_l = As / (b × d)

    Parameters:
        steel_area (float): Tension reinforcement area in mm²
        beam_width (float): Beam width in mm
        effective_depth (float): Effective depth in mm

    Returns:
        float: Reinforcement ratio
    """

    if steel_area <= 0:
        raise ValueError(
            "Steel area must be greater than zero."
        )

    if beam_width <= 0:
        raise ValueError(
            "Beam width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    reinforcement_ratio = (
        steel_area
        / (beam_width * effective_depth)
    )

    return reinforcement_ratio


def calculate_concrete_shear_resistance(
    concrete_strength,
    reinforcement_ratio,
    effective_depth,
    beam_width,
    gamma_c=1.5
):
    """
    Calculate a simplified concrete shear resistance.

    Simplified EC2-oriented expression:

        VRd,c = [CRd,c × k × (100ρl fck)^(1/3)] × b_w × d

    where:

        CRd,c = 0.18 / gamma_c
        k = 1 + sqrt(200/d), limited to 2.0

    Parameters:
        concrete_strength (float): fck in N/mm²
        reinforcement_ratio (float): Longitudinal reinforcement ratio
        effective_depth (float): Effective depth in mm
        beam_width (float): Beam width in mm
        gamma_c (float): Concrete partial safety factor

    Returns:
        float: Concrete shear resistance in kN
    """

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if reinforcement_ratio <= 0:
        raise ValueError(
            "Reinforcement ratio must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    if beam_width <= 0:
        raise ValueError(
            "Beam width must be greater than zero."
        )

    if gamma_c <= 0:
        raise ValueError(
            "Concrete partial factor must be greater than zero."
        )

    # EC2 k-factor
    k = 1 + math.sqrt(200 / effective_depth)

    # Limit k to 2.0
    k = min(k, 2.0)

    # EC2 coefficient
    c_rd_c = 0.18 / gamma_c

    # Concrete shear stress resistance
    shear_stress_resistance = (
        c_rd_c
        * k
        * (100 * reinforcement_ratio * concrete_strength) ** (1 / 3)
    )

    # Convert N to kN
    shear_resistance = (
        shear_stress_resistance
        * beam_width
        * effective_depth
        / 1000
    )

    return shear_resistance


def check_shear_capacity(
    design_shear,
    concrete_shear_resistance
):
    """
    Check whether the calculated concrete shear resistance
    is sufficient for the design shear force.

    Returns:
        dict: Shear capacity check.
    """

    if design_shear < 0:
        raise ValueError(
            "Design shear cannot be negative."
        )

    if concrete_shear_resistance <= 0:
        raise ValueError(
            "Concrete shear resistance must be greater than zero."
        )

    utilization = (
        design_shear
        / concrete_shear_resistance
    )

    passes = design_shear <= concrete_shear_resistance

    return {
        "design_shear_kN": design_shear,
        "concrete_shear_resistance_kN": concrete_shear_resistance,
        "utilization_ratio": utilization,
        "passes_concrete_shear_check": passes
    }


def analyze_beam_shear(
    dead_load,
    live_load,
    span,
    beam_width,
    effective_depth,
    steel_area,
    concrete_strength=25
):
    """
    Perform a preliminary shear analysis.

    Returns:
        dict: Complete shear analysis results.
    """

    design_shear = calculate_design_shear_force(
        dead_load,
        live_load,
        span
    )

    shear_stress = calculate_shear_stress(
        design_shear,
        beam_width,
        effective_depth
    )

    reinforcement_ratio = (
        calculate_longitudinal_reinforcement_ratio(
            steel_area,
            beam_width,
            effective_depth
        )
    )

    concrete_resistance = (
        calculate_concrete_shear_resistance(
            concrete_strength,
            reinforcement_ratio,
            effective_depth,
            beam_width
        )
    )

    capacity_check = check_shear_capacity(
        design_shear,
        concrete_resistance
    )

    return {
        "design_shear_kN": design_shear,
        "shear_stress_N_per_mm2": shear_stress,
        "reinforcement_ratio": reinforcement_ratio,
        "concrete_shear_resistance_kN": concrete_resistance,
        "utilization_ratio": capacity_check["utilization_ratio"],
        "passes_concrete_shear_check":
            capacity_check["passes_concrete_shear_check"]
    }
