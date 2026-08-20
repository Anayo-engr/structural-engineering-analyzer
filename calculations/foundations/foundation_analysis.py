"""
Structural Engineering Analyzer
Foundation Analysis Module

Preliminary analysis of isolated pad foundations.

Design basis:
- Axial load
- Allowable soil bearing pressure
- Preliminary square footing sizing
- Uniform soil pressure assumption

IMPORTANT:
This is a preliminary calculation component.
Final foundation design requires geotechnical data,
settlement checks, groundwater considerations,
eccentricity, punching shear, one-way shear,
flexure, sliding, overturning, durability, detailing,
and applicable design-code checks.

Units:
    Loads: kN
    Dimensions: m
    Pressure: kN/m²
"""


# =========================================================
# FOUNDATION AREA
# =========================================================

def calculate_required_foundation_area(
    service_load,
    allowable_soil_pressure
):
    """
    Calculate the required foundation bearing area.

        Areq = N / qallow

    Parameters:
        service_load (float):
            Service axial load in kN.

        allowable_soil_pressure (float):
            Allowable soil bearing pressure in kN/m².

    Returns:
        float:
            Required foundation area in m².
    """

    if service_load <= 0:
        raise ValueError(
            "Service load must be greater than zero."
        )

    if allowable_soil_pressure <= 0:
        raise ValueError(
            "Allowable soil pressure must be greater than zero."
        )

    return (
        service_load
        / allowable_soil_pressure
    )


# =========================================================
# SQUARE FOUNDATION DIMENSION
# =========================================================

def calculate_square_foundation_size(
    required_area
):
    """
    Calculate the side length of a square foundation.

        B = √A

    Parameters:
        required_area (float):
            Required foundation area in m².

    Returns:
        float:
            Required square foundation side in metres.
    """

    if required_area <= 0:
        raise ValueError(
            "Required foundation area must be greater than zero."
        )

    return required_area ** 0.5


# =========================================================
# ACTUAL FOUNDATION AREA
# =========================================================

def calculate_foundation_area(
    foundation_width,
    foundation_length
):
    """
    Calculate the actual foundation bearing area.

        A = B × L

    Parameters:
        foundation_width (float):
            Foundation width in metres.

        foundation_length (float):
            Foundation length in metres.

    Returns:
        float:
            Foundation area in m².
    """

    if foundation_width <= 0:
        raise ValueError(
            "Foundation width must be greater than zero."
        )

    if foundation_length <= 0:
        raise ValueError(
            "Foundation length must be greater than zero."
        )

    return (
        foundation_width
        * foundation_length
    )


# =========================================================
# SOIL BEARING PRESSURE
# =========================================================

def calculate_soil_bearing_pressure(
    service_load,
    foundation_area
):
    """
    Calculate average soil bearing pressure.

        q = N / A

    Parameters:
        service_load (float):
            Service axial load in kN.

        foundation_area (float):
            Foundation bearing area in m².

    Returns:
        float:
            Average soil pressure in kN/m².
    """

    if service_load <= 0:
        raise ValueError(
            "Service load must be greater than zero."
        )

    if foundation_area <= 0:
        raise ValueError(
            "Foundation area must be greater than zero."
        )

    return (
        service_load
        / foundation_area
    )


# =========================================================
# SOIL PRESSURE CHECK
# =========================================================

def check_soil_bearing_capacity(
    soil_pressure,
    allowable_soil_pressure
):
    """
    Check whether calculated soil pressure is within
    the allowable bearing pressure.

    Returns:
        dict:
            Bearing-pressure check results.
    """

    if soil_pressure < 0:
        raise ValueError(
            "Soil pressure cannot be negative."
        )

    if allowable_soil_pressure <= 0:
        raise ValueError(
            "Allowable soil pressure must be greater than zero."
        )

    utilization_ratio = (
        soil_pressure
        / allowable_soil_pressure
    )

    passes = (
        soil_pressure
        <= allowable_soil_pressure
    )

    return {
        "soil_pressure_kN_per_m2":
            soil_pressure,

        "allowable_soil_pressure_kN_per_m2":
            allowable_soil_pressure,

        "utilization_ratio":
            utilization_ratio,

        "passes_bearing_capacity_check":
            passes
    }


# =========================================================
# COMPLETE FOUNDATION ANALYSIS
# =========================================================

def analyze_isolated_foundation(
    service_load,
    allowable_soil_pressure,
    foundation_width,
    foundation_length
):
    """
    Perform a preliminary isolated-foundation analysis.

    Returns:
        dict:
            Foundation analysis results.
    """

    required_area = calculate_required_foundation_area(
        service_load,
        allowable_soil_pressure
    )

    required_square_size = (
        calculate_square_foundation_size(
            required_area
        )
    )

    actual_area = calculate_foundation_area(
        foundation_width,
        foundation_length
    )

    soil_pressure = calculate_soil_bearing_pressure(
        service_load,
        actual_area
    )

    bearing_check = check_soil_bearing_capacity(
        soil_pressure,
        allowable_soil_pressure
    )

    return {
        "service_load_kN":
            service_load,

        "allowable_soil_pressure_kN_per_m2":
            allowable_soil_pressure,

        "required_area_m2":
            required_area,

        "required_square_foundation_size_m":
            required_square_size,

        "foundation_width_m":
            foundation_width,

        "foundation_length_m":
            foundation_length,

        "actual_foundation_area_m2":
            actual_area,

        "soil_bearing_pressure_kN_per_m2":
            soil_pressure,

        "utilization_ratio":
            bearing_check[
                "utilization_ratio"
            ],

        "passes_bearing_capacity_check":
            bearing_check[
                "passes_bearing_capacity_check"
            ]
    }
