"""
Structural Engineering Analyzer
Beam Design Module

Preliminary reinforced-concrete beam design calculations.

Design basis:
- Eurocode-oriented approach
- Rectangular reinforced-concrete section
- Simply supported beam
- Sagging bending moment
- Singly reinforced section

IMPORTANT:
This module is a preliminary calculation-engine component.
Final structural design must be checked against the applicable
design code, project conditions, detailing requirements,
load combinations, durability requirements, and a qualified
structural engineer's review.

Units:
    Dimensions: mm
    Loads: kN/m
    Moments: kNm
    Strengths: N/mm²
    Reinforcement area: mm²
"""

import math


# =========================================================
# EFFECTIVE DEPTH
# =========================================================

def calculate_effective_depth(
    overall_depth,
    concrete_cover,
    bar_diameter
):
    """
    Calculate the effective depth of a reinforced-concrete beam.

    Formula:

        d = h - c - Ø/2

    Parameters:
        overall_depth (float):
            Overall beam depth in mm.

        concrete_cover (float):
            Nominal concrete cover in mm.

        bar_diameter (float):
            Main reinforcement diameter in mm.

    Returns:
        float:
            Effective depth in mm.
    """

    if not isinstance(overall_depth, (int, float)):
        raise TypeError("Overall depth must be a number.")

    if not isinstance(concrete_cover, (int, float)):
        raise TypeError("Concrete cover must be a number.")

    if not isinstance(bar_diameter, (int, float)):
        raise TypeError("Bar diameter must be a number.")

    if not math.isfinite(overall_depth):
        raise ValueError("Overall depth must be finite.")

    if not math.isfinite(concrete_cover):
        raise ValueError("Concrete cover must be finite.")

    if not math.isfinite(bar_diameter):
        raise ValueError("Bar diameter must be finite.")

    if overall_depth <= 0:
        raise ValueError(
            "Overall depth must be greater than zero."
        )

    if concrete_cover < 0:
        raise ValueError(
            "Concrete cover cannot be negative."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

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


# =========================================================
# DESIGN BENDING MOMENT
# =========================================================

def calculate_design_bending_moment(
    dead_load,
    live_load,
    span,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the preliminary design bending moment.

    Design load:

        wEd = γG G + γQ Q

    Maximum moment for a simply supported beam under
    full-span UDL:

        MEd = wEd L² / 8

    Default factors:

        γG = 1.35
        γQ = 1.50

    Parameters:
        dead_load (float):
            Dead load in kN/m.

        live_load (float):
            Live load in kN/m.

        span (float):
            Beam span in metres.

        dead_load_factor (float):
            Dead-load factor.

        live_load_factor (float):
            Live-load factor.

    Returns:
        float:
            Design bending moment in kNm.
    """

    if dead_load < 0:
        raise ValueError(
            "Dead load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    if dead_load_factor <= 0:
        raise ValueError(
            "Dead load factor must be greater than zero."
        )

    if live_load_factor <= 0:
        raise ValueError(
            "Live load factor must be greater than zero."
        )

    design_load = (
        dead_load * dead_load_factor
        + live_load * live_load_factor
    )

    moment = (
        design_load * span ** 2
    ) / 8

    return moment


# =========================================================
# REQUIRED TENSION REINFORCEMENT
# =========================================================

def calculate_required_steel_area(
    design_moment,
    effective_depth,
    steel_strength,
    lever_arm_factor=0.90
):
    """
    Estimate the required tensile reinforcement area.

    Simplified singly-reinforced relationship:

        As = MEd / (0.87 fy z)

    where:

        z = factor × d

    The default lever-arm factor is 0.90.

    Conversion:

        1 kNm = 1,000,000 Nmm

    Parameters:
        design_moment (float):
            Design bending moment in kNm.

        effective_depth (float):
            Effective depth in mm.

        steel_strength (float):
            Characteristic steel yield strength in N/mm².

        lever_arm_factor (float):
            Approximate z/d ratio.

    Returns:
        float:
            Required tensile reinforcement area in mm².
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
            "Lever arm factor must be greater than 0 "
            "and no more than 1."
        )

    # Convert kNm to Nmm.
    moment_nmm = design_moment * 1_000_000

    # Approximate lever arm.
    lever_arm = (
        lever_arm_factor * effective_depth
    )

    required_area = (
        moment_nmm
        / (
            0.87
            * steel_strength
            * lever_arm
        )
    )

    return required_area


# =========================================================
# MEAN TENSILE STRENGTH OF CONCRETE
# =========================================================

def calculate_mean_tensile_strength(concrete_strength):
    """
    Estimate the mean tensile strength of normal-strength
    concrete using an Eurocode-oriented relationship.

    For fck <= 50 N/mm²:

        fctm = 0.30 × fck^(2/3)

    For higher-strength concrete, a different expression
    is required by the applicable design standard.

    Parameters:
        concrete_strength (float):
            Characteristic compressive strength fck
            in N/mm².

    Returns:
        float:
            Mean tensile strength fctm in N/mm².
    """

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if concrete_strength > 50:
        raise ValueError(
            "This preliminary tensile-strength model is "
            "limited to concrete strength of 50 N/mm² or less."
        )

    mean_tensile_strength = (
        0.30
        * concrete_strength ** (2 / 3)
    )

    return mean_tensile_strength


# =========================================================
# MINIMUM TENSION REINFORCEMENT
# =========================================================

def calculate_minimum_steel_area(
    beam_width,
    effective_depth,
    concrete_strength,
    steel_strength=500
):
    """
    Calculate the minimum tension reinforcement area.

    Preliminary Eurocode-oriented expression:

        As,min = max(
            0.26 × fctm / fyk,
            0.0013
        ) × b × d

    where:

        fctm = mean tensile strength of concrete
        fyk  = characteristic yield strength of steel
        b    = beam width
        d    = effective depth

    Parameters:
        beam_width (float):
            Beam width in mm.

        effective_depth (float):
            Effective depth in mm.

        concrete_strength (float):
            Characteristic concrete strength fck
            in N/mm².

        steel_strength (float):
            Characteristic steel yield strength fyk
            in N/mm².

    Returns:
        float:
            Minimum reinforcement area in mm².
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

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    fctm = calculate_mean_tensile_strength(
        concrete_strength
    )

    reinforcement_ratio = max(
        (0.26 * fctm) / steel_strength,
        0.0013
    )

    minimum_area = (
        reinforcement_ratio
        * beam_width
        * effective_depth
    )

    return minimum_area


# =========================================================
# GOVERNING STEEL AREA
# =========================================================

def select_required_steel_area(
    required_area,
    minimum_area
):
    """
    Select the governing reinforcement area.

    The provided design reinforcement must not be less
    than the applicable minimum reinforcement.

    Parameters:
        required_area (float):
            Flexural reinforcement required by moment.

        minimum_area (float):
            Minimum required reinforcement.

    Returns:
        float:
            Governing reinforcement area in mm².
    """

    if required_area <= 0:
        raise ValueError(
            "Required reinforcement area must be "
            "greater than zero."
        )

    if minimum_area <= 0:
        raise ValueError(
            "Minimum reinforcement area must be "
            "greater than zero."
        )

    return max(
        required_area,
        minimum_area
    )


# =========================================================
# COMPLETE BEAM DESIGN
# =========================================================

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
    Perform a preliminary reinforced-concrete beam
    flexural design calculation.

    Returns:
        dict:
            Beam design results.
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
        concrete_strength,
        steel_strength
    )

    governing_steel = select_required_steel_area(
        required_steel,
        minimum_steel
    )

    return {
        "beam_width_mm": beam_width,
        "overall_depth_mm": overall_depth,
        "effective_depth_mm": effective_depth,

        "concrete_strength_N_per_mm2":
            concrete_strength,

        "steel_strength_N_per_mm2":
            steel_strength,

        "design_bending_moment_kNm":
            design_moment,

        "required_steel_area_mm2":
            required_steel,

        "minimum_steel_area_mm2":
            minimum_steel,

        "governing_steel_area_mm2":
            governing_steel
    }
