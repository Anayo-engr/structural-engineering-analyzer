"""
Structural Engineering Analyzer
Slab Reinforcement Module

Preliminary reinforced-concrete slab reinforcement calculations.

Design basis:
- Reinforced concrete one-way slab
- Eurocode-oriented preliminary detailing
- Main flexural reinforcement
- Distribution reinforcement

IMPORTANT:
This module is a preliminary calculation component.
Final reinforcement detailing must be checked against the
applicable design code, spacing limits, anchorage,
development length, laps, crack control, durability,
support conditions, and project requirements.
"""

import math


# =========================================================
# AVAILABLE REINFORCEMENT DIAMETERS
# =========================================================

AVAILABLE_BAR_DIAMETERS = [
    6,
    8,
    10,
    12,
    16,
    20,
    25,
    32
]


# =========================================================
# BAR AREA
# =========================================================

def calculate_bar_area(bar_diameter):
    """
    Calculate the cross-sectional area of one reinforcement bar.

        Abar = πØ² / 4

    Returns:
        float:
            Bar area in mm².
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
# PROVIDED STEEL AREA PER METRE
# =========================================================

def calculate_provided_steel_area(
    bar_diameter,
    spacing
):
    """
    Calculate reinforcement area provided per metre width.

        As,prov = Abar × 1000 / spacing

    Returns:
        float:
            Provided steel area in mm²/m.
    """

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    if spacing <= 0:
        raise ValueError(
            "Bar spacing must be greater than zero."
        )

    bar_area = calculate_bar_area(
        bar_diameter
    )

    return (
        bar_area
        * 1000
        / spacing
    )


# =========================================================
# REQUIRED SPACING
# =========================================================

def calculate_required_spacing(
    required_area,
    bar_diameter
):
    """
    Calculate the maximum spacing needed to provide
    the required reinforcement area.

        s = Abar × 1000 / As,required

    Returns:
        float:
            Required spacing in mm.
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

    spacing = (
        bar_area
        * 1000
        / required_area
    )

    return spacing


# =========================================================
# SUITABLE MAIN REINFORCEMENT
# =========================================================

def find_suitable_reinforcement(
    required_area,
    preferred_diameter=None,
    maximum_spacing=200
):
    """
    Find a practical slab reinforcement arrangement.

    The selected arrangement must provide at least the
    required steel area and must not exceed the specified
    maximum spacing.

    Returns:
        dict:
            Reinforcement arrangement.
    """

    if required_area <= 0:
        raise ValueError(
            "Required steel area must be greater than zero."
        )

    if maximum_spacing <= 0:
        raise ValueError(
            "Maximum spacing must be greater than zero."
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

        required_spacing = calculate_required_spacing(
            required_area,
            diameter
        )

        spacing = min(
            required_spacing,
            maximum_spacing
        )

        # Round spacing down to a practical 5 mm increment.
        spacing = (
            math.floor(spacing / 5)
            * 5
        )

        if spacing < 25:
            spacing = 25

        provided_area = (
            calculate_provided_steel_area(
                diameter,
                spacing
            )
        )

        if provided_area < required_area:
            continue

        excess_area = (
            provided_area
            - required_area
        )

        option = {
            "bar_diameter_mm":
                diameter,

            "spacing_mm":
                spacing,

            "provided_area_mm2_per_m":
                provided_area,

            "required_area_mm2_per_m":
                required_area,

            "excess_area_mm2_per_m":
                excess_area
        }

        if best_option is None:

            best_option = option

        elif (
            excess_area
            < best_option[
                "excess_area_mm2_per_m"
            ]
        ):

            best_option = option

    if best_option is None:
        raise ValueError(
            "No suitable reinforcement arrangement "
            "was found for the selected parameters."
        )

    return best_option


# =========================================================
# MINIMUM SPACING CHECK
# =========================================================

def check_minimum_spacing(
    spacing,
    minimum_spacing=100
):
    """
    Check whether reinforcement spacing satisfies
    the specified minimum spacing.

    Returns:
        bool:
            True if spacing is adequate.
    """

    if spacing <= 0:
        raise ValueError(
            "Spacing must be greater than zero."
        )

    if minimum_spacing <= 0:
        raise ValueError(
            "Minimum spacing must be greater than zero."
        )

    return spacing >= minimum_spacing


# =========================================================
# MAXIMUM SPACING CHECK
# =========================================================

def check_maximum_spacing(
    spacing,
    maximum_spacing=200
):
    """
    Check whether reinforcement spacing satisfies
    the specified maximum spacing.

    Returns:
        bool:
            True if spacing is adequate.
    """

    if spacing <= 0:
        raise ValueError(
            "Spacing must be greater than zero."
        )

    if maximum_spacing <= 0:
        raise ValueError(
            "Maximum spacing must be greater than zero."
        )

    return spacing <= maximum_spacing


# =========================================================
# DISTRIBUTION REINFORCEMENT
# =========================================================

def calculate_distribution_reinforcement(
    main_steel_area,
    distribution_ratio=0.20,
    bar_diameter=8,
    maximum_spacing=300
):
    """
    Calculate preliminary transverse/distribution
    reinforcement.

    The default distribution ratio is 20% of the main
    flexural reinforcement.

    Returns:
        dict:
            Distribution reinforcement arrangement.
    """

    if main_steel_area <= 0:
        raise ValueError(
            "Main steel area must be greater than zero."
        )

    if not 0 < distribution_ratio <= 1:
        raise ValueError(
            "Distribution ratio must be greater than 0 "
            "and no more than 1."
        )

    required_distribution_area = (
        main_steel_area
        * distribution_ratio
    )

    spacing = calculate_required_spacing(
        required_distribution_area,
        bar_diameter
    )

    spacing = min(
        spacing,
        maximum_spacing
    )

    spacing = (
        math.floor(spacing / 5)
        * 5
    )

    if spacing < 25:
        spacing = 25

    provided_area = (
        calculate_provided_steel_area(
            bar_diameter,
            spacing
        )
    )

    return {
        "bar_diameter_mm":
            bar_diameter,

        "spacing_mm":
            spacing,

        "required_area_mm2_per_m":
            required_distribution_area,

        "provided_area_mm2_per_m":
            provided_area
    }


# =========================================================
# COMPLETE SLAB REINFORCEMENT SCHEDULE
# =========================================================

def generate_reinforcement_schedule(
    required_area,
    preferred_diameter=None,
    maximum_main_spacing=200,
    distribution_ratio=0.20,
    distribution_bar_diameter=8,
    maximum_distribution_spacing=300
):
    """
    Generate a preliminary slab reinforcement schedule.

    Returns:
        dict:
            Main and distribution reinforcement information.
    """

    main_reinforcement = (
        find_suitable_reinforcement(
            required_area,
            preferred_diameter,
            maximum_main_spacing
        )
    )

    distribution = (
        calculate_distribution_reinforcement(
            main_reinforcement[
                "provided_area_mm2_per_m"
            ],
            distribution_ratio,
            distribution_bar_diameter,
            maximum_distribution_spacing
        )
    )

    main_spacing_ok = check_maximum_spacing(
        main_reinforcement["spacing_mm"],
        maximum_main_spacing
    )

    distribution_spacing_ok = check_maximum_spacing(
        distribution["spacing_mm"],
        maximum_distribution_spacing
    )

    return {
        "main_reinforcement": {
            "bar_diameter_mm":
                main_reinforcement[
                    "bar_diameter_mm"
                ],

            "spacing_mm":
                main_reinforcement[
                    "spacing_mm"
                ],

            "required_area_mm2_per_m":
                main_reinforcement[
                    "required_area_mm2_per_m"
                ],

            "provided_area_mm2_per_m":
                main_reinforcement[
                    "provided_area_mm2_per_m"
                ],

            "excess_area_mm2_per_m":
                main_reinforcement[
                    "excess_area_mm2_per_m"
                ],

            "spacing_adequate":
                main_spacing_ok
        },

        "distribution_reinforcement": {
            "bar_diameter_mm":
                distribution[
                    "bar_diameter_mm"
                ],

            "spacing_mm":
                distribution[
                    "spacing_mm"
                ],

            "required_area_mm2_per_m":
                distribution[
                    "required_area_mm2_per_m"
                ],

            "provided_area_mm2_per_m":
                distribution[
                    "provided_area_mm2_per_m"
                ],

            "spacing_adequate":
                distribution_spacing_ok
        }
    }
