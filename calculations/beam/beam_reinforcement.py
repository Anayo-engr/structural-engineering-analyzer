"""
Structural Engineering Analyzer
Beam Reinforcement Module

This module converts a required reinforcement area into
practical reinforcement bar arrangements.

Design basis:
- Reinforced concrete beam
- Preliminary Eurocode-oriented detailing
- Main longitudinal reinforcement
- Shear links/stirrups

Final reinforcement detailing must be checked against
the applicable design code and project requirements.
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


def calculate_provided_steel_area(
    number_of_bars,
    bar_diameter
):
    """
    Calculate the total steel area provided by a group of bars.

    Formula:

        As,prov = n × Abar

    Parameters:
        number_of_bars (int): Number of reinforcement bars
        bar_diameter (float): Bar diameter in mm

    Returns:
        float: Provided steel area in mm²
    """

    if number_of_bars < 1:
        raise ValueError(
            "Number of bars must be at least 1."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    bar_area = calculate_bar_area(bar_diameter)

    return number_of_bars * bar_area


def calculate_required_number_of_bars(
    required_area,
    bar_diameter
):
    """
    Determine the minimum whole number of bars required
    to provide at least the required steel area.

    Parameters:
        required_area (float): Required steel area in mm²
        bar_diameter (float): Bar diameter in mm

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

    bar_area = calculate_bar_area(bar_diameter)

    number_of_bars = math.ceil(
        required_area / bar_area
    )

    return max(number_of_bars, 2)


def find_suitable_reinforcement(
    required_area,
    preferred_diameter=None
):
    """
    Find a practical reinforcement arrangement that provides
    at least the required steel area.

    Parameters:
        required_area (float): Required steel area in mm²
        preferred_diameter (float, optional):
            Preferred bar diameter in mm

    Returns:
        dict: Recommended reinforcement arrangement.
    """

    if required_area <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if preferred_diameter is not None:

        if preferred_diameter not in AVAILABLE_BAR_DIAMETERS:
            raise ValueError(
                "Preferred diameter is not in the available "
                "bar diameter list."
            )

        diameters = [preferred_diameter]

    else:
        diameters = AVAILABLE_BAR_DIAMETERS

    best_option = None

    for diameter in diameters:

        number_of_bars = calculate_required_number_of_bars(
            required_area,
            diameter
        )

        provided_area = calculate_provided_steel_area(
            number_of_bars,
            diameter
        )

        excess_area = provided_area - required_area

        option = {
            "number_of_bars": number_of_bars,
            "bar_diameter_mm": diameter,
            "provided_area_mm2": provided_area,
            "required_area_mm2": required_area,
            "excess_area_mm2": excess_area
        }

        if best_option is None:
            best_option = option

        elif excess_area < best_option["excess_area_mm2"]:
            best_option = option

    return best_option


def calculate_clear_spacing(
    beam_width,
    concrete_cover,
    link_diameter,
    main_bar_diameter,
    number_of_bars
):
    """
    Calculate approximate clear spacing between longitudinal bars.

    Formula:

        Available width =
        b - 2c - 2Ølink - nØbar

        Clear spacing =
        Available width / (n - 1)

    Parameters:
        beam_width (float): Beam width in mm
        concrete_cover (float): Concrete cover in mm
        link_diameter (float): Link diameter in mm
        main_bar_diameter (float): Main bar diameter in mm
        number_of_bars (int): Number of main bars

    Returns:
        float: Approximate clear spacing in mm
    """

    if beam_width <= 0:
        raise ValueError(
            "Beam width must be greater than zero."
        )

    if concrete_cover < 0:
        raise ValueError(
            "Concrete cover cannot be negative."
        )

    if link_diameter <= 0:
        raise ValueError(
            "Link diameter must be greater than zero."
        )

    if main_bar_diameter <= 0:
        raise ValueError(
            "Main bar diameter must be greater than zero."
        )

    if number_of_bars < 2:
        raise ValueError(
            "At least two bars are required to calculate spacing."
        )

    available_width = (
        beam_width
        - (2 * concrete_cover)
        - (2 * link_diameter)
        - (number_of_bars * main_bar_diameter)
    )

    if available_width <= 0:
        raise ValueError(
            "There is insufficient beam width for the selected bars."
        )

    clear_spacing = (
        available_width
        / (number_of_bars - 1)
    )

    return clear_spacing


def check_bar_spacing(
    clear_spacing,
    minimum_spacing
):
    """
    Check whether the calculated clear spacing satisfies
    the specified minimum spacing.

    Parameters:
        clear_spacing (float): Clear spacing in mm
        minimum_spacing (float): Required minimum spacing in mm

    Returns:
        bool: True if spacing is adequate.
    """

    if clear_spacing < 0:
        raise ValueError(
            "Clear spacing cannot be negative."
        )

    if minimum_spacing <= 0:
        raise ValueError(
            "Minimum spacing must be greater than zero."
        )

    return clear_spacing >= minimum_spacing


def calculate_link_area(
    number_of_legs,
    link_diameter
):
    """
    Calculate the cross-sectional area of a shear link.

    Parameters:
        number_of_legs (int): Number of effective link legs
        link_diameter (float): Link diameter in mm

    Returns:
        float: Total link area in mm²
    """

    if number_of_legs < 2:
        raise ValueError(
            "A typical beam link must have at least two legs."
        )

    if link_diameter <= 0:
        raise ValueError(
            "Link diameter must be greater than zero."
        )

    single_bar_area = calculate_bar_area(
        link_diameter
    )

    return number_of_legs * single_bar_area


def recommend_links(
    design_shear,
    beam_width,
    effective_depth
):
    """
    Provide a preliminary shear-link recommendation.

    This is NOT a complete EC2 link-design calculation.
    It provides a starting reinforcement arrangement based
    on the beam's design shear.

    Returns:
        dict: Preliminary link recommendation.
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

    # Preliminary starting arrangements.
    if design_shear <= 50:
        diameter = 8
        spacing = 200

    elif design_shear <= 100:
        diameter = 8
        spacing = 150

    elif design_shear <= 150:
        diameter = 10
        spacing = 150

    else:
        diameter = 10
        spacing = 100

    return {
        "link_diameter_mm": diameter,
        "number_of_legs": 2,
        "link_spacing_mm": spacing,
        "design_shear_kN": design_shear,
        "note": (
            "Preliminary link arrangement. "
            "Complete shear reinforcement design is required."
        )
    }


def generate_reinforcement_schedule(
    required_area,
    beam_width,
    concrete_cover,
    link_diameter=8,
    preferred_diameter=None
):
    """
    Generate a preliminary beam reinforcement schedule.

    Returns:
        dict: Main reinforcement and spacing information.
    """

    reinforcement = find_suitable_reinforcement(
        required_area,
        preferred_diameter
    )

    number_of_bars = reinforcement["number_of_bars"]

    main_bar_diameter = reinforcement["bar_diameter_mm"]

    spacing = calculate_clear_spacing(
        beam_width,
        concrete_cover,
        link_diameter,
        main_bar_diameter,
        number_of_bars
    )

    return {
        "main_bars": number_of_bars,
        "main_bar_diameter_mm": main_bar_diameter,
        "provided_steel_area_mm2":
            reinforcement["provided_area_mm2"],
        "required_steel_area_mm2":
            reinforcement["required_area_mm2"],
        "clear_spacing_mm": spacing
    }
