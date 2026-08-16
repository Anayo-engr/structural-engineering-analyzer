"""
Structural Engineering Analyzer
Beam Reinforcement Module

Preliminary reinforced-concrete beam reinforcement calculations.

Design basis:
- Reinforced concrete beam
- Eurocode-oriented preliminary detailing
- Main longitudinal reinforcement
- Shear links/stirrups

IMPORTANT:
This module is a preliminary calculation component.
Final reinforcement detailing must be checked against the
applicable design code, structural drawings, anchorage,
development length, lap requirements, congestion,
and project conditions by a qualified structural engineer.
"""

import math


# =========================================================
# AVAILABLE REINFORCEMENT DIAMETERS
# =========================================================

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


# =========================================================
# BAR AREA
# =========================================================

def calculate_bar_area(bar_diameter):
    """
    Calculate the cross-sectional area of one reinforcement bar.

        Abar = πØ² / 4

    Returns:
        float: Bar area in mm².
    """

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    return (
        math.pi
        * bar_diameter ** 2
        / 4
    )


# =========================================================
# PROVIDED STEEL AREA
# =========================================================

def calculate_provided_steel_area(
    number_of_bars,
    bar_diameter
):
    """
    Calculate total reinforcement area.

        As,prov = n × Abar

    Returns:
        float: Provided steel area in mm².
    """

    if number_of_bars < 1:
        raise ValueError(
            "Number of bars must be at least 1."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    return (
        number_of_bars
        * calculate_bar_area(bar_diameter)
    )


# =========================================================
# REQUIRED NUMBER OF BARS
# =========================================================

def calculate_required_number_of_bars(
    required_area,
    bar_diameter
):
    """
    Determine the minimum whole number of bars
    required to provide the required steel area.

    A minimum of two longitudinal bars is maintained.

    Returns:
        int: Required number of bars.
    """

    if required_area <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    bar_area = calculate_bar_area(
        bar_diameter
    )

    number_of_bars = math.ceil(
        required_area / bar_area
    )

    return max(number_of_bars, 2)


# =========================================================
# SUITABLE MAIN REINFORCEMENT
# =========================================================

def find_suitable_reinforcement(
    required_area,
    preferred_diameter=None
):
    """
    Find a practical reinforcement arrangement.

    If a preferred diameter is supplied, that diameter
    is used. Otherwise available diameters are examined
    and the arrangement with the smallest excess steel
    area is selected.

    Returns:
        dict: Reinforcement arrangement.
    """

    if required_area <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if preferred_diameter is not None:

        if preferred_diameter not in AVAILABLE_BAR_DIAMETERS:
            raise ValueError(
                "Preferred diameter is not in the "
                "available bar diameter list."
            )

        diameters = [
            preferred_diameter
        ]

    else:
        diameters = AVAILABLE_BAR_DIAMETERS

    best_option = None

    for diameter in diameters:

        number_of_bars = (
            calculate_required_number_of_bars(
                required_area,
                diameter
            )
        )

        provided_area = (
            calculate_provided_steel_area(
                number_of_bars,
                diameter
            )
        )

        excess_area = (
            provided_area
            - required_area
        )

        option = {
            "number_of_bars":
                number_of_bars,

            "bar_diameter_mm":
                diameter,

            "provided_area_mm2":
                provided_area,

            "required_area_mm2":
                required_area,

            "excess_area_mm2":
                excess_area
        }

        if best_option is None:
            best_option = option

        elif (
            excess_area
            < best_option["excess_area_mm2"]
        ):
            best_option = option

    return best_option


# =========================================================
# CLEAR BAR SPACING
# =========================================================

def calculate_clear_spacing(
    beam_width,
    concrete_cover,
    link_diameter,
    main_bar_diameter,
    number_of_bars
):
    """
    Calculate approximate horizontal clear spacing
    between longitudinal bars.

        Available width =
        b - 2c - 2Ølink - nØbar

        Clear spacing =
        Available width / (n - 1)

    Returns:
        float: Clear spacing in mm.
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
            "At least two bars are required."
        )

    available_width = (
        beam_width
        - 2 * concrete_cover
        - 2 * link_diameter
        - number_of_bars * main_bar_diameter
    )

    if available_width <= 0:
        raise ValueError(
            "Insufficient beam width for the selected bars."
        )

    return (
        available_width
        / (number_of_bars - 1)
    )


# =========================================================
# MINIMUM BAR SPACING CHECK
# =========================================================

def check_bar_spacing(
    clear_spacing,
    minimum_spacing
):
    """
    Check whether clear spacing satisfies
    the specified minimum.

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


# =========================================================
# LINK AREA
# =========================================================

def calculate_link_area(
    number_of_legs,
    link_diameter
):
    """
    Calculate total steel area of a shear link.

        Asw = number of legs × Abar

    Returns:
        float: Link area in mm².
    """

    if number_of_legs < 2:
        raise ValueError(
            "A typical beam link must have at least two legs."
        )

    if link_diameter <= 0:
        raise ValueError(
            "Link diameter must be greater than zero."
        )

    return (
        number_of_legs
        * calculate_bar_area(link_diameter)
    )


# =========================================================
# PRELIMINARY LINK RECOMMENDATION
# =========================================================

def recommend_links(
    design_shear,
    beam_width,
    effective_depth
):
    """
    Provide a preliminary shear-link arrangement.

    This is NOT a complete shear reinforcement design.

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

    link_area = calculate_link_area(
        number_of_legs=2,
        link_diameter=diameter
    )

    return {
        "link_diameter_mm":
            diameter,

        "number_of_legs":
            2,

        "link_area_mm2":
            link_area,

        "link_spacing_mm":
            spacing,

        "design_shear_kN":
            design_shear,

        "note":
            "Preliminary link arrangement. "
            "Complete shear reinforcement design "
            "is required."
    }


# =========================================================
# REINFORCEMENT SCHEDULE
# =========================================================

def generate_reinforcement_schedule(
    required_area,
    beam_width,
    concrete_cover,
    link_diameter=8,
    preferred_diameter=None,
    minimum_spacing=20
):
    """
    Generate a preliminary beam reinforcement schedule.

    Returns:
        dict: Main reinforcement and spacing information.
    """

    reinforcement = (
        find_suitable_reinforcement(
            required_area,
            preferred_diameter
        )
    )

    number_of_bars = (
        reinforcement["number_of_bars"]
    )

    main_bar_diameter = (
        reinforcement["bar_diameter_mm"]
    )

    spacing = calculate_clear_spacing(
        beam_width,
        concrete_cover,
        link_diameter,
        main_bar_diameter,
        number_of_bars
    )

    spacing_ok = check_bar_spacing(
        spacing,
        minimum_spacing
    )

    return {
        "main_bars":
            number_of_bars,

        "main_bar_diameter_mm":
            main_bar_diameter,

        "provided_steel_area_mm2":
            reinforcement[
                "provided_area_mm2"
            ],

        "required_steel_area_mm2":
            reinforcement[
                "required_area_mm2"
            ],

        "excess_steel_area_mm2":
            reinforcement[
                "excess_area_mm2"
            ],

        "clear_spacing_mm":
            spacing,

        "minimum_spacing_mm":
            minimum_spacing,

        "spacing_adequate":
            spacing_ok
    }
