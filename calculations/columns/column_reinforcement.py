"""
Structural Engineering Analyzer
Column Reinforcement Module

This module provides preliminary reinforcement calculations
for reinforced-concrete columns.

It covers:
- Longitudinal reinforcement area
- Minimum reinforcement
- Maximum reinforcement
- Practical bar selection
- Provided reinforcement area
- Reinforcement ratio

Design basis:
- Preliminary Eurocode-oriented approach
- Rectangular reinforced-concrete column
- Symmetrical longitudinal reinforcement

IMPORTANT:
This module is intended as a preliminary calculation-engine
component. Final column reinforcement must be checked against
the applicable design code, including slenderness, moments,
second-order effects, minimum/maximum reinforcement limits,
bar spacing, cover, anchorage, lap lengths, and detailing
requirements.
"""

import math


# Common reinforcement bar diameters in mm.
AVAILABLE_BAR_DIAMETERS = [
    8,
    10,
    12,
    16,
    20,
    25,
    32,
    40
]


def calculate_bar_area(bar_diameter):
    """
    Calculate the cross-sectional area of one reinforcement bar.

    Formula:

        Abar = πØ² / 4

    Parameters:
        bar_diameter (float): Bar diameter in mm

    Returns:
        float: Area of one bar in mm²
    """

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    return math.pi * bar_diameter ** 2 / 4


def calculate_minimum_steel_area(
    column_area,
    minimum_ratio=0.01
):
    """
    Calculate the minimum longitudinal reinforcement area.

    Formula:

        As,min = ρmin × Ac

    Parameters:
        column_area (float): Gross column area in mm²
        minimum_ratio (float): Minimum reinforcement ratio

    Returns:
        float: Minimum reinforcement area in mm²
    """

    if column_area <= 0:
        raise ValueError(
            "Column area must be greater than zero."
        )

    if minimum_ratio <= 0:
        raise ValueError(
            "Minimum reinforcement ratio must be greater than zero."
        )

    return minimum_ratio * column_area


def calculate_maximum_steel_area(
    column_area,
    maximum_ratio=0.04
):
    """
    Calculate the maximum longitudinal reinforcement area.

    Formula:

        As,max = ρmax × Ac

    Parameters:
        column_area (float): Gross column area in mm²
        maximum_ratio (float): Maximum reinforcement ratio

    Returns:
        float: Maximum reinforcement area in mm²
    """

    if column_area <= 0:
        raise ValueError(
            "Column area must be greater than zero."
        )

    if maximum_ratio <= 0:
        raise ValueError(
            "Maximum reinforcement ratio must be greater than zero."
        )

    return maximum_ratio * column_area


def calculate_required_steel_area(
    design_load,
    concrete_strength,
    steel_strength,
    column_area,
    design_stress_ratio=0.4
):
    """
    Estimate the required longitudinal reinforcement area
    for a preliminary axially loaded column calculation.

    Simplified relationship:

        NEd = Ac × fcd × α + As × fyd

    Rearranged approximately as:

        As = (NEd - Ac × fcd × α) / fyd

    where:

        fcd = fck / γc
        fyd = fy / γs

    Parameters:
        design_load (float): Design axial load in kN
        concrete_strength (float): Concrete strength fck in N/mm²
        steel_strength (float): Steel yield strength fy in N/mm²
        column_area (float): Gross column area in mm²
        design_stress_ratio (float): Preliminary concrete
                                     contribution factor

    Returns:
        float: Required reinforcement area in mm²
    """

    if design_load <= 0:
        raise ValueError(
            "Design load must be greater than zero."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if column_area <= 0:
        raise ValueError(
            "Column area must be greater than zero."
        )

    if not 0 < design_stress_ratio <= 1:
        raise ValueError(
            "Design stress ratio must be greater than zero "
            "and no more than 1."
        )

    # Partial factors.
    gamma_c = 1.5
    gamma_s = 1.15

    # Design material strengths.
    fcd = concrete_strength / gamma_c
    fyd = steel_strength / gamma_s

    # Convert design load from kN to N.
    design_load_n = design_load * 1000

    # Preliminary concrete contribution.
    concrete_capacity = (
        design_stress_ratio
        * fcd
        * column_area
    )

    remaining_load = (
        design_load_n
        - concrete_capacity
    )

    # If concrete contribution already exceeds the load,
    # reinforcement is governed by the minimum requirement.
    if remaining_load <= 0:
        return 0.0

    required_area = remaining_load / fyd

    return required_area


def select_governing_steel_area(
    required_area,
    minimum_area
):
    """
    Select the governing reinforcement area.

    The provided reinforcement must satisfy at least
    the required and minimum reinforcement areas.

    Parameters:
        required_area (float): Calculated required steel area
        minimum_area (float): Minimum steel area

    Returns:
        float: Governing steel area in mm²
    """

    if required_area < 0:
        raise ValueError(
            "Required steel area cannot be negative."
        )

    if minimum_area <= 0:
        raise ValueError(
            "Minimum steel area must be greater than zero."
        )

    return max(required_area, minimum_area)


def calculate_required_number_of_bars(
    required_area,
    bar_diameter,
    minimum_number_of_bars=4
):
    """
    Determine the minimum number of longitudinal bars required.

    Parameters:
        required_area (float): Required steel area in mm²
        bar_diameter (float): Bar diameter in mm
        minimum_number_of_bars (int): Minimum number of
                                      longitudinal column bars

    Returns:
        int: Required number of bars
    """

    if required_area <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    if minimum_number_of_bars < 4:
        raise ValueError(
            "A rectangular column should have at least "
            "four longitudinal bars."
        )

    bar_area = calculate_bar_area(
        bar_diameter
    )

    number_of_bars = math.ceil(
        required_area / bar_area
    )

    # Ensure the minimum number of bars.
    number_of_bars = max(
        number_of_bars,
        minimum_number_of_bars
    )

    return number_of_bars


def calculate_provided_steel_area(
    number_of_bars,
    bar_diameter
):
    """
    Calculate the total longitudinal reinforcement area provided.

    Formula:

        As,prov = n × Abar

    Parameters:
        number_of_bars (int): Number of longitudinal bars
        bar_diameter (float): Bar diameter in mm

    Returns:
        float: Provided reinforcement area in mm²
    """

    if number_of_bars < 4:
        raise ValueError(
            "A rectangular column should have at least "
            "four longitudinal bars."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    return (
        number_of_bars
        * calculate_bar_area(bar_diameter)
    )


def calculate_reinforcement_ratio(
    steel_area,
    column_area
):
    """
    Calculate the longitudinal reinforcement ratio.

    Formula:

        ρ = As / Ac

    Parameters:
        steel_area (float): Reinforcement area in mm²
        column_area (float): Gross column area in mm²

    Returns:
        float: Reinforcement ratio
    """

    if steel_area <= 0:
        raise ValueError(
            "Steel area must be greater than zero."
        )

    if column_area <= 0:
        raise ValueError(
            "Column area must be greater than zero."
        )

    return steel_area / column_area


def check_reinforcement_limits(
    provided_area,
    minimum_area,
    maximum_area
):
    """
    Check whether the provided reinforcement satisfies
    the preliminary minimum and maximum limits.

    Returns:
        dict: Reinforcement limit check.
    """

    if provided_area <= 0:
        raise ValueError(
            "Provided steel area must be greater than zero."
        )

    if minimum_area <= 0:
        raise ValueError(
            "Minimum steel area must be greater than zero."
        )

    if maximum_area <= 0:
        raise ValueError(
            "Maximum steel area must be greater than zero."
        )

    passes_minimum = (
        provided_area >= minimum_area
    )

    passes_maximum = (
        provided_area <= maximum_area
    )

    return {
        "passes_minimum_reinforcement": passes_minimum,
        "passes_maximum_reinforcement": passes_maximum,
        "passes_reinforcement_limits": (
            passes_minimum and passes_maximum
        )
    }


def find_suitable_reinforcement(
    required_area,
    column_area,
    preferred_diameter=16
):
    """
    Find a practical longitudinal reinforcement arrangement.

    The selected arrangement must provide at least the governing
    required area while respecting the preliminary maximum
    reinforcement limit.

    Parameters:
        required_area (float): Governing required steel area in mm²
        column_area (float): Gross column area in mm²
        preferred_diameter (float): Preferred bar diameter in mm

    Returns:
        dict: Recommended reinforcement arrangement.
    """

    if required_area <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if column_area <= 0:
        raise ValueError(
            "Column area must be greater than zero."
        )

    if preferred_diameter not in AVAILABLE_BAR_DIAMETERS:
        raise ValueError(
            "Preferred diameter is not in the available "
            "bar diameter list."
        )

    maximum_area = calculate_maximum_steel_area(
        column_area
    )

    number_of_bars = calculate_required_number_of_bars(
        required_area,
        preferred_diameter
    )

    provided_area = calculate_provided_steel_area(
        number_of_bars,
        preferred_diameter
    )

    # Increase bar diameter if the preferred arrangement
    # would exceed the maximum reinforcement limit.
    if provided_area > maximum_area:

        for diameter in AVAILABLE_BAR_DIAMETERS:

            number_of_bars = calculate_required_number_of_bars(
                required_area,
                diameter
            )

            provided_area = calculate_provided_steel_area(
                number_of_bars,
                diameter
            )

            if provided_area <= maximum_area:
                preferred_diameter = diameter
                break

    return {
        "number_of_bars": number_of_bars,
        "bar_diameter_mm": preferred_diameter,
        "provided_area_mm2": provided_area,
        "required_area_mm2": required_area,
        "maximum_area_mm2": maximum_area,
        "reinforcement_ratio":
            calculate_reinforcement_ratio(
                provided_area,
                column_area
            )
    }
