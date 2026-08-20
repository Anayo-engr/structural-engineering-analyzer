"""
Structural Engineering Analyzer
Foundation Reinforcement Module

Preliminary reinforcement selection for isolated
reinforced-concrete pad foundations.

Design basis:
- Rectangular/square pad foundation
- Bottom flexural reinforcement
- Preliminary bar selection and spacing

IMPORTANT:
This is a preliminary calculation component.
Final reinforcement detailing must be checked against
the applicable design code, development length,
anchorage, minimum reinforcement, spacing limits,
cover, punching shear, one-way shear, and project
conditions by a qualified structural engineer.

Units:
    Dimensions: mm
    Reinforcement area: mm²
"""


import math


# =========================================================
# AVAILABLE BAR DIAMETERS
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
# REQUIRED NUMBER OF BARS
# =========================================================

def calculate_required_number_of_bars(
    required_area,
    bar_diameter
):
    """
    Calculate the minimum whole number of bars required.

    A minimum of two bars is maintained.

    Returns:
        int:
            Required number of bars.
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

    return max(
        number_of_bars,
        2
    )


# =========================================================
# PROVIDED STEEL AREA
# =========================================================

def calculate_provided_steel_area(
    number_of_bars,
    bar_diameter
):
    """
    Calculate provided reinforcement area.

        As,prov = n × Abar

    Returns:
        float:
            Provided steel area in mm².
    """

    if number_of_bars < 2:
        raise ValueError(
            "At least two reinforcement bars are required."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    return (
        number_of_bars
        * calculate_bar_area(
            bar_diameter
        )
    )


# =========================================================
# SUITABLE FOUNDATION REINFORCEMENT
# =========================================================

def find_suitable_reinforcement(
    required_area,
    preferred_diameter=None
):
    """
    Select a practical reinforcement arrangement.

    If a preferred diameter is supplied, it is used.
    Otherwise the available diameters are examined and
    the arrangement with the smallest excess steel area
    is selected.

    Returns:
        dict:
            Reinforcement arrangement.
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
            < best_option[
                "excess_area_mm2"
            ]
        ):

            best_option = option

    return best_option


# =========================================================
# BAR SPACING
# =========================================================

def calculate_bar_spacing(
    foundation_dimension,
    concrete_cover,
    bar_diameter,
    number_of_bars
):
    """
    Calculate approximate centre-to-centre spacing
    between reinforcement bars.

    Returns:
        float:
            Bar spacing in mm.
    """

    if foundation_dimension <= 0:
        raise ValueError(
            "Foundation dimension must be greater than zero."
        )

    if concrete_cover < 0:
        raise ValueError(
            "Concrete cover cannot be negative."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    if number_of_bars < 2:
        raise ValueError(
            "At least two bars are required."
        )

    available_length = (
        foundation_dimension * 1000
        - 2 * concrete_cover
        - bar_diameter
    )

    if available_length <= 0:
        raise ValueError(
            "Insufficient foundation dimension for reinforcement."
        )

    return (
        available_length
        / (number_of_bars - 1)
    )


# =========================================================
# MINIMUM SPACING CHECK
# =========================================================

def check_bar_spacing(
    spacing,
    minimum_spacing=75
):
    """
    Check whether reinforcement spacing satisfies
    a preliminary minimum spacing.

    Returns:
        bool:
            True if spacing is adequate.
    """

    if spacing <= 0:
        raise ValueError(
            "Bar spacing must be greater than zero."
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
    maximum_spacing=300
):
    """
    Check whether reinforcement spacing satisfies
    a preliminary maximum spacing.

    Returns:
        bool:
            True if spacing is adequate.
    """

    if spacing <= 0:
        raise ValueError(
            "Bar spacing must be greater than zero."
        )

    if maximum_spacing <= 0:
        raise ValueError(
            "Maximum spacing must be greater than zero."
        )

    return spacing <= maximum_spacing


# =========================================================
# COMPLETE FOUNDATION REINFORCEMENT SCHEDULE
# =========================================================

def generate_foundation_reinforcement_schedule(
    required_area_x,
    required_area_y,
    foundation_width,
    foundation_length,
    concrete_cover,
    preferred_diameter=None,
    minimum_spacing=75,
    maximum_spacing=300
):
    """
    Generate preliminary bottom reinforcement
    arrangements in two directions.

    Returns:
        dict:
            Foundation reinforcement schedule.
    """

    reinforcement_x = (
        find_suitable_reinforcement(
            required_area_x,
            preferred_diameter
        )
    )

    reinforcement_y = (
        find_suitable_reinforcement(
            required_area_y,
            preferred_diameter
        )
    )

    spacing_x = calculate_bar_spacing(
        foundation_width,
        concrete_cover,
        reinforcement_x[
            "bar_diameter_mm"
        ],
        reinforcement_x[
            "number_of_bars"
        ]
    )

    spacing_y = calculate_bar_spacing(
        foundation_length,
        concrete_cover,
        reinforcement_y[
            "bar_diameter_mm"
        ],
        reinforcement_y[
            "number_of_bars"
        ]
    )

    spacing_x_min_ok = check_bar_spacing(
        spacing_x,
        minimum_spacing
    )

    spacing_y_min_ok = check_bar_spacing(
        spacing_y,
        minimum_spacing
    )

    spacing_x_max_ok = check_maximum_spacing(
        spacing_x,
        maximum_spacing
    )

    spacing_y_max_ok = check_maximum_spacing(
        spacing_y,
        maximum_spacing
    )

    return {
        "x_direction": {
            "number_of_bars":
                reinforcement_x[
                    "number_of_bars"
                ],

            "bar_diameter_mm":
                reinforcement_x[
                    "bar_diameter_mm"
                ],

            "required_area_mm2":
                reinforcement_x[
                    "required_area_mm2"
                ],

            "provided_area_mm2":
                reinforcement_x[
                    "provided_area_mm2"
                ],

            "excess_area_mm2":
                reinforcement_x[
                    "excess_area_mm2"
                ],

            "spacing_mm":
                spacing_x,

            "minimum_spacing_ok":
                spacing_x_min_ok,

            "maximum_spacing_ok":
                spacing_x_max_ok
        },

        "y_direction": {
            "number_of_bars":
                reinforcement_y[
                    "number_of_bars"
                ],

            "bar_diameter_mm":
                reinforcement_y[
                    "bar_diameter_mm"
                ],

            "required_area_mm2":
                reinforcement_y[
                    "required_area_mm2"
                ],

            "provided_area_mm2":
                reinforcement_y[
                    "provided_area_mm2"
                ],

            "excess_area_mm2":
                reinforcement_y[
                    "excess_area_mm2"
                ],

            "spacing_mm":
                spacing_y,

            "minimum_spacing_ok":
                spacing_y_min_ok,

            "maximum_spacing_ok":
                spacing_y_max_ok
        }
    }
