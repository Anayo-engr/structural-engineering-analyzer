"""
Structural Engineering Analyzer
Slab Design Module

Preliminary reinforced-concrete slab flexural design.

Design basis:
- Eurocode-oriented approach
- Simply supported one-way slab
- Rectangular compression section
- Singly reinforced section
- One-metre-wide design strip

IMPORTANT:
This is a preliminary calculation-engine component.
Final slab design must include all applicable code checks,
deflection/serviceability checks, crack control, detailing,
support conditions, load combinations, punching/shear checks
where applicable, and professional engineering review.

Units:
    Dimensions: mm
    Loads: kN/m²
    Moments: kNm/m
    Strengths: N/mm²
    Reinforcement area: mm²/m
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
    Calculate the effective depth of the slab.

        d = h - c - Ø/2

    Returns:
        float:
            Effective depth in mm.
    """

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
        - bar_diameter / 2
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
    design_load,
    span,
    strip_width=1.0
):
    """
    Calculate the design bending moment per metre width.

        w = q × b

        MEd = wL² / 8

    Returns:
        float:
            Design bending moment in kNm/m.
    """

    if design_load <= 0:
        raise ValueError(
            "Design load must be greater than zero."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    if strip_width <= 0:
        raise ValueError(
            "Strip width must be greater than zero."
        )

    design_strip_load = (
        design_load * strip_width
    )

    return (
        design_strip_load
        * span ** 2
        / 8
    )


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
    Estimate the required tensile reinforcement.

        As = MEd / (0.87 fy z)

        z = factor × d

    Returns:
        float:
            Required reinforcement area in mm²/m.
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

    moment_nmm = (
        design_moment * 1_000_000
    )

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
# MEAN TENSILE STRENGTH
# =========================================================

def calculate_mean_tensile_strength(
    concrete_strength
):
    """
    Estimate mean concrete tensile strength.

    For fck <= 50 N/mm²:

        fctm = 0.30 × fck^(2/3)

    Returns:
        float:
            Mean tensile strength in N/mm².
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

    return (
        0.30
        * concrete_strength ** (2 / 3)
    )


# =========================================================
# MINIMUM SLAB REINFORCEMENT
# =========================================================

def calculate_minimum_steel_area(
    slab_width,
    effective_depth,
    concrete_strength,
    steel_strength=500
):
    """
    Calculate minimum tension reinforcement.

    Preliminary expression:

        As,min =
        max(0.26 fctm/fyk, 0.0013) × b × d

    Returns:
        float:
            Minimum reinforcement area in mm².
    """

    if slab_width <= 0:
        raise ValueError(
            "Slab width must be greater than zero."
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

    return (
        reinforcement_ratio
        * slab_width
        * effective_depth
    )


# =========================================================
# GOVERNING STEEL AREA
# =========================================================

def select_required_steel_area(
    required_area,
    minimum_area
):
    """
    Select the governing reinforcement area.

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
# SECTION UTILIZATION
# =========================================================

def calculate_bending_utilization(
    required_steel,
    provided_steel
):
    """
    Calculate flexural reinforcement utilization.

        Utilization = As,required / As,provided

    A value <= 1.0 indicates that the provided steel area
    is at least equal to the required area.

    Returns:
        float:
            Utilization ratio.
    """

    if required_steel <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if provided_steel <= 0:
        raise ValueError(
            "Provided steel area must be greater than zero."
        )

    return (
        required_steel
        / provided_steel
    )


# =========================================================
# COMPLETE SLAB FLEXURAL DESIGN
# =========================================================

def calculate_slab_design(
    slab_width,
    overall_depth,
    concrete_cover,
    bar_diameter,
    design_load,
    span,
    concrete_strength=25,
    steel_strength=500
):
    """
    Perform a preliminary one-way slab flexural design.

    The design is performed on the supplied slab width,
    normally 1000 mm for a one-metre design strip.

    Returns:
        dict:
            Preliminary slab flexural design results.
    """

    effective_depth = calculate_effective_depth(
        overall_depth,
        concrete_cover,
        bar_diameter
    )

    design_moment = calculate_design_bending_moment(
        design_load,
        span,
        slab_width / 1000
    )

    required_steel = calculate_required_steel_area(
        design_moment,
        effective_depth,
        steel_strength
    )

    minimum_steel = calculate_minimum_steel_area(
        slab_width,
        effective_depth,
        concrete_strength,
        steel_strength
    )

    governing_steel = select_required_steel_area(
        required_steel,
        minimum_steel
    )

    return {
        "slab_width_mm":
            slab_width,

        "overall_depth_mm":
            overall_depth,

        "effective_depth_mm":
            effective_depth,

        "concrete_strength_N_per_mm2":
            concrete_strength,

        "steel_strength_N_per_mm2":
            steel_strength,

        "design_load_kN_per_m2":
            design_load,

        "span_m":
            span,

        "design_bending_moment_kNm_per_m":
            design_moment,

        "required_steel_area_mm2_per_m":
            required_steel,

        "minimum_steel_area_mm2_per_m":
            minimum_steel,

        "governing_steel_area_mm2_per_m":
            governing_steel
    }
