"""
Structural Engineering Analyzer
Beam Shear Design Module

Preliminary shear calculations for reinforced-concrete beams.

Design basis:
- Eurocode-oriented approach
- Simply supported beam
- Uniformly distributed load
- Rectangular reinforced-concrete section

IMPORTANT:
This module is a preliminary calculation component.
Final structural design requires complete code checks,
detailing requirements, load combinations, support/load
positions, shear reinforcement design, and engineering review.

Units:
    Loads: kN/m
    Forces: kN
    Dimensions: mm
    Stresses: N/mm²
"""


import math


# =========================================================
# DESIGN SHEAR FORCE
# =========================================================

def calculate_design_shear_force(
    dead_load,
    live_load,
    span,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the design shear force at a support.

    For a simply supported beam carrying a full-span UDL:

        wEd = γG G + γQ Q

        VEd = wEd L / 2

    Parameters:
        dead_load (float):
            Dead load in kN/m.

        live_load (float):
            Live load in kN/m.

        span (float):
            Beam span in metres.

        dead_load_factor (float):
            Dead-load partial factor.

        live_load_factor (float):
            Live-load partial factor.

    Returns:
        float:
            Design shear force in kN.
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

    design_shear = (
        design_load * span
    ) / 2

    return design_shear


# =========================================================
# SHEAR STRESS
# =========================================================

def calculate_shear_stress(
    design_shear,
    beam_width,
    effective_depth
):
    """
    Calculate nominal design shear stress.

        vEd = VEd / (b × d)

    Parameters:
        design_shear (float):
            Design shear force in kN.

        beam_width (float):
            Beam width in mm.

        effective_depth (float):
            Effective depth in mm.

    Returns:
        float:
            Shear stress in N/mm².
    """

    if design_shear < 0:
        raise ValueError(
            "Design shear cannot be negative."
        )

    if beam_width <= 0:
        raise ValueError(
            "Beam width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    # kN → N
    shear_force_n = design_shear * 1000

    shear_stress = (
        shear_force_n
        / (beam_width * effective_depth)
    )

    return shear_stress


# =========================================================
# LONGITUDINAL REINFORCEMENT RATIO
# =========================================================

def calculate_longitudinal_reinforcement_ratio(
    steel_area,
    beam_width,
    effective_depth
):
    """
    Calculate longitudinal reinforcement ratio.

        ρl = As / (b × d)

    Parameters:
        steel_area (float):
            Longitudinal tension reinforcement area in mm².

        beam_width (float):
            Beam width in mm.

        effective_depth (float):
            Effective depth in mm.

    Returns:
        float:
            Longitudinal reinforcement ratio.
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


# =========================================================
# EC2 k-FACTOR
# =========================================================

def calculate_k_factor(effective_depth):
    """
    Calculate the EC2 size-effect factor k.

        k = 1 + sqrt(200/d)

    with:

        k <= 2.0

    Parameters:
        effective_depth (float):
            Effective depth in mm.

    Returns:
        float:
            Size-effect factor k.
    """

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    k = 1 + math.sqrt(
        200 / effective_depth
    )

    return min(k, 2.0)


# =========================================================
# CONCRETE SHEAR RESISTANCE
# =========================================================

def calculate_concrete_shear_resistance(
    concrete_strength,
    reinforcement_ratio,
    effective_depth,
    beam_width,
    gamma_c=1.5
):
    """
    Calculate preliminary concrete shear resistance.

    Simplified EC2-oriented expression:

        VRd,c =
        [CRd,c × k × (100ρl fck)^(1/3)]
        × bw × d

    where:

        CRd,c = 0.18 / γc

        k = 1 + sqrt(200/d) <= 2.0

    Parameters:
        concrete_strength (float):
            Characteristic concrete strength fck in N/mm².

        reinforcement_ratio (float):
            Longitudinal reinforcement ratio.

        effective_depth (float):
            Effective depth in mm.

        beam_width (float):
            Beam width in mm.

        gamma_c (float):
            Concrete partial factor.

    Returns:
        float:
            Concrete shear resistance in kN.
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

    k = calculate_k_factor(
        effective_depth
    )

    c_rd_c = 0.18 / gamma_c

    shear_stress_resistance = (
        c_rd_c
        * k
        * (
            100
            * reinforcement_ratio
            * concrete_strength
        ) ** (1 / 3)
    )

    # N/mm² × mm² = N
    # N → kN
    shear_resistance = (
        shear_stress_resistance
        * beam_width
        * effective_depth
        / 1000
    )

    return shear_resistance


# =========================================================
# MAXIMUM SHEAR STRUT RESISTANCE
# =========================================================

def calculate_maximum_shear_resistance(
    beam_width,
    effective_depth,
    concrete_strength,
    strut_angle=45,
    gamma_c=1.5
):
    """
    Calculate a simplified maximum shear resistance
    associated with the concrete compression strut.

    This is a preliminary check and is not a substitute
    for a complete EC2 shear reinforcement design.

    Parameters:
        beam_width (float):
            Beam width in mm.

        effective_depth (float):
            Effective depth in mm.

        concrete_strength (float):
            Concrete strength fck in N/mm².

        strut_angle (float):
            Assumed compression-strut angle in degrees.

        gamma_c (float):
            Concrete partial factor.

    Returns:
        float:
            Preliminary maximum shear resistance in kN.
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

    if not 21.8 <= strut_angle <= 45:
        raise ValueError(
            "Strut angle must be between "
            "21.8 and 45 degrees."
        )

    if gamma_c <= 0:
        raise ValueError(
            "Concrete partial factor must be greater than zero."
        )

    # EC2:
    #
    # ν1 = 0.6(1 - fck/250)
    #
    # Limited to a non-negative value.
    nu_1 = 0.6 * (
        1 - concrete_strength / 250
    )

    nu_1 = max(nu_1, 0.0)

    alpha_cw = 1.0

    theta = math.radians(
        strut_angle
    )

    cot_theta = 1 / math.tan(theta)

    tan_theta = math.tan(theta)

    # Simplified VRd,max expression:
    #
    # VRd,max =
    # αcw × bw × z × ν1 × fcd
    # / (cotθ + tanθ)

    fcd = (
        concrete_strength
        / gamma_c
    )

    # Preliminary z ≈ 0.9d
    lever_arm = (
        0.9 * effective_depth
    )

    maximum_resistance = (
        alpha_cw
        * beam_width
        * lever_arm
        * nu_1
        * fcd
        / (
            cot_theta
            + tan_theta
        )
    )

    # N → kN
    maximum_resistance /= 1000

    return maximum_resistance


# =========================================================
# SHEAR CAPACITY CHECK
# =========================================================

def check_shear_capacity(
    design_shear,
    concrete_shear_resistance,
    maximum_shear_resistance=None
):
    """
    Check the design shear against available resistance.

    The first check compares VEd against VRd,c.

    If VRd,max is supplied, a second upper-limit check
    is also performed.

    Returns:
        dict:
            Shear capacity results.
    """

    if design_shear < 0:
        raise ValueError(
            "Design shear cannot be negative."
        )

    if concrete_shear_resistance <= 0:
        raise ValueError(
            "Concrete shear resistance must be "
            "greater than zero."
        )

    utilization = (
        design_shear
        / concrete_shear_resistance
    )

    passes_concrete_check = (
        design_shear
        <= concrete_shear_resistance
    )

    result = {
        "design_shear_kN": design_shear,

        "concrete_shear_resistance_kN":
            concrete_shear_resistance,

        "utilization_ratio":
            utilization,

        "passes_concrete_shear_check":
            passes_concrete_check
    }

    if maximum_shear_resistance is not None:

        if maximum_shear_resistance <= 0:
            raise ValueError(
                "Maximum shear resistance must be "
                "greater than zero."
            )

        maximum_utilization = (
            design_shear
            / maximum_shear_resistance
        )

        passes_maximum_check = (
            design_shear
            <= maximum_shear_resistance
        )

        result.update({
            "maximum_shear_resistance_kN":
                maximum_shear_resistance,

            "maximum_utilization_ratio":
                maximum_utilization,

            "passes_maximum_shear_check":
                passes_maximum_check
        })

    return result


# =========================================================
# COMPLETE SHEAR ANALYSIS
# =========================================================

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
        dict:
            Complete preliminary shear analysis results.
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

    maximum_resistance = (
        calculate_maximum_shear_resistance(
            beam_width,
            effective_depth,
            concrete_strength
        )
    )

    capacity_check = check_shear_capacity(
        design_shear,
        concrete_resistance,
        maximum_resistance
    )

    return {
        "design_shear_kN":
            design_shear,

        "shear_stress_N_per_mm2":
            shear_stress,

        "reinforcement_ratio":
            reinforcement_ratio,

        "concrete_shear_resistance_kN":
            concrete_resistance,

        "maximum_shear_resistance_kN":
            maximum_resistance,

        "utilization_ratio":
            capacity_check[
                "utilization_ratio"
            ],

        "maximum_utilization_ratio":
            capacity_check[
                "maximum_utilization_ratio"
            ],

        "passes_concrete_shear_check":
            capacity_check[
                "passes_concrete_shear_check"
            ],

        "passes_maximum_shear_check":
            capacity_check[
                "passes_maximum_shear_check"
            ]
    }
