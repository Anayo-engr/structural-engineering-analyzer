"""
Structural Engineering Analyzer
Foundation Shear Design Module

Preliminary shear checks for reinforced-concrete
isolated pad foundations.

Design basis:
- Isolated pad foundation
- One-way shear
- Punching shear
- Uniform soil pressure assumption
- Preliminary Eurocode-oriented approach

IMPORTANT:
This module is a preliminary calculation component.
Final foundation design requires complete code checks,
geotechnical verification, punching shear perimeter checks,
column load effects, eccentricity, bending, detailing,
and professional engineering review.

Units:
    Loads: kN
    Dimensions: mm
    Stresses: N/mm²
"""


import math


# =========================================================
# ONE-WAY SHEAR FORCE
# =========================================================

def calculate_one_way_shear_force(
    design_soil_pressure,
    projection,
    effective_depth,
    design_width
):
    """
    Calculate preliminary one-way shear force.

    The critical section is assumed approximately one
    effective depth from the column face.

    Parameters:
        design_soil_pressure:
            Design soil pressure in kN/m².

        projection:
            Foundation projection beyond the column face in m.

        effective_depth:
            Effective depth in mm.

        design_width:
            Width of the design strip in m.

    Returns:
        float:
            One-way shear force in kN.
    """

    if design_soil_pressure <= 0:
        raise ValueError(
            "Design soil pressure must be greater than zero."
        )

    if projection <= 0:
        raise ValueError(
            "Projection must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    if design_width <= 0:
        raise ValueError(
            "Design width must be greater than zero."
        )

    effective_depth_m = (
        effective_depth / 1000
    )

    shear_length = (
        projection
        - effective_depth_m
    )

    if shear_length <= 0:
        return 0.0

    return (
        design_soil_pressure
        * shear_length
        * design_width
    )


# =========================================================
# ONE-WAY SHEAR STRESS
# =========================================================

def calculate_one_way_shear_stress(
    shear_force,
    design_width,
    effective_depth
):
    """
    Calculate one-way shear stress.

        vEd = VEd / (b × d)

    Returns:
        float:
            Shear stress in N/mm².
    """

    if shear_force < 0:
        raise ValueError(
            "Shear force cannot be negative."
        )

    if design_width <= 0:
        raise ValueError(
            "Design width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    width_mm = (
        design_width * 1000
    )

    shear_force_n = (
        shear_force * 1000
    )

    return (
        shear_force_n
        / (
            width_mm
            * effective_depth
        )
    )


# =========================================================
# PUNCHING SHEAR PERIMETER
# =========================================================

def calculate_punching_perimeter(
    column_width,
    column_depth,
    effective_depth
):
    """
    Calculate the perimeter of a preliminary punching
    shear control perimeter at approximately 2d from
    the column face.

    Simplified rectangular perimeter:

        u = 2(c1 + c2 + 4d)

    where dimensions are in mm.

    Returns:
        float:
            Punching perimeter in mm.
    """

    if column_width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if column_depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    return (
        2
        * (
            column_width
            + column_depth
            + 4 * effective_depth
        )
    )


# =========================================================
# PUNCHING SHEAR AREA
# =========================================================

def calculate_punching_shear_area(
    column_width,
    column_depth,
    effective_depth
):
    """
    Calculate the enclosed area inside the simplified
    punching shear perimeter.

    Returns:
        float:
            Punching area in mm².
    """

    if column_width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if column_depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    control_width = (
        column_width
        + 4 * effective_depth
    )

    control_depth = (
        column_depth
        + 4 * effective_depth
    )

    return (
        control_width
        * control_depth
    )


# =========================================================
# PUNCHING SHEAR FORCE
# =========================================================

def calculate_punching_shear_force(
    design_load,
    design_soil_pressure,
    punching_area
):
    """
    Calculate net punching shear force.

    The soil reaction inside the control perimeter is
    deducted from the applied column load.

    Returns:
        float:
            Punching shear force in kN.
    """

    if design_load <= 0:
        raise ValueError(
            "Design load must be greater than zero."
        )

    if design_soil_pressure < 0:
        raise ValueError(
            "Design soil pressure cannot be negative."
        )

    if punching_area <= 0:
        raise ValueError(
            "Punching area must be greater than zero."
        )

    punching_area_m2 = (
        punching_area / 1_000_000
    )

    soil_reaction = (
        design_soil_pressure
        * punching_area_m2
    )

    punching_force = (
        design_load
        - soil_reaction
    )

    return max(
        punching_force,
        0.0
    )


# =========================================================
# PUNCHING SHEAR STRESS
# =========================================================

def calculate_punching_shear_stress(
    punching_force,
    punching_perimeter,
    effective_depth
):
    """
    Calculate preliminary punching shear stress.

        vEd = VEd / (u × d)

    Returns:
        float:
            Punching shear stress in N/mm².
    """

    if punching_force < 0:
        raise ValueError(
            "Punching shear force cannot be negative."
        )

    if punching_perimeter <= 0:
        raise ValueError(
            "Punching perimeter must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    punching_force_n = (
        punching_force * 1000
    )

    return (
        punching_force_n
        / (
            punching_perimeter
            * effective_depth
        )
    )


# =========================================================
# PRELIMINARY CONCRETE SHEAR CAPACITY
# =========================================================

def calculate_punching_shear_capacity(
    concrete_strength,
    reinforcement_ratio,
    gamma_c=1.5
):
    """
    Calculate a simplified preliminary punching
    shear resistance.

    Simplified relationship:

        vRd,c =
        CRd,c × k × (100ρl fck)^(1/3)

    Returns:
        float:
            Punching shear resistance in N/mm².
    """

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if reinforcement_ratio <= 0:
        raise ValueError(
            "Reinforcement ratio must be greater than zero."
        )

    if gamma_c <= 0:
        raise ValueError(
            "Concrete partial factor must be greater than zero."
        )

    k = min(
        1 + math.sqrt(200 / 200),
        2.0
    )

    c_rd_c = (
        0.18 / gamma_c
    )

    return (
        c_rd_c
        * k
        * (
            100
            * reinforcement_ratio
            * concrete_strength
        ) ** (1 / 3)
    )


# =========================================================
# SHEAR CAPACITY CHECK
# =========================================================

def check_shear_capacity(
    shear_stress,
    shear_capacity
):
    """
    Check whether shear stress is within
    the preliminary shear capacity.

    Returns:
        dict:
            Shear check results.
    """

    if shear_stress < 0:
        raise ValueError(
            "Shear stress cannot be negative."
        )

    if shear_capacity <= 0:
        raise ValueError(
            "Shear capacity must be greater than zero."
        )

    utilization_ratio = (
        shear_stress
        / shear_capacity
    )

    passes = (
        shear_stress
        <= shear_capacity
    )

    return {
        "shear_stress_N_per_mm2":
            shear_stress,

        "shear_capacity_N_per_mm2":
            shear_capacity,

        "utilization_ratio":
            utilization_ratio,

        "passes_shear_check":
            passes
    }
