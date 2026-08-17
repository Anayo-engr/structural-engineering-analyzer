"""
Structural Engineering Analyzer
Column Analysis Module

This module performs basic analysis of reinforced-concrete
columns subjected primarily to axial loading.

Design basis:
- Preliminary Eurocode-oriented approach
- Short, axially loaded rectangular column
- Centric axial-load analysis

IMPORTANT:
This is a preliminary calculation component.
Final column design must consider eccentricity, slenderness,
second-order effects, imperfections, moments, frame action,
buckling, fire, detailing, and all applicable code requirements.
"""


def calculate_design_axial_load(
    dead_load,
    live_load,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the ultimate/design axial load.

    Formula:

        NEd = 1.35G + 1.50Q

    Returns:
        float: Design axial load in kN.
    """

    if dead_load < 0:
        raise ValueError(
            "Dead load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    if dead_load_factor <= 0:
        raise ValueError(
            "Dead load factor must be greater than zero."
        )

    if live_load_factor <= 0:
        raise ValueError(
            "Live load factor must be greater than zero."
        )

    return (
        dead_load * dead_load_factor
        + live_load * live_load_factor
    )


def calculate_column_area(
    column_width,
    column_depth
):
    """
    Calculate the gross cross-sectional area
    of a rectangular column.

    Formula:

        Ac = b × h

    Parameters:
        column_width (float):
            Column width in mm.

        column_depth (float):
            Column depth in mm.

    Returns:
        float:
            Gross concrete area in mm².
    """

    if column_width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if column_depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    return column_width * column_depth


def calculate_axial_stress(
    design_load,
    column_area
):
    """
    Calculate the average axial compressive stress.

    Formula:

        sigma = NEd / Ac

    Parameters:
        design_load (float):
            Design axial load in kN.

        column_area (float):
            Gross column area in mm².

    Returns:
        float:
            Average axial stress in N/mm².
    """

    if design_load < 0:
        raise ValueError(
            "Design load cannot be negative."
        )

    if column_area <= 0:
        raise ValueError(
            "Column area must be greater than zero."
        )

    # Convert kN to N.
    load_n = design_load * 1000

    return load_n / column_area


def calculate_slenderness_ratio(
    effective_length,
    radius_of_gyration
):
    """
    Calculate the basic slenderness ratio.

    Formula:

        lambda = l0 / i

    Returns:
        float: Slenderness ratio.
    """

    if effective_length <= 0:
        raise ValueError(
            "Effective length must be greater than zero."
        )

    if radius_of_gyration <= 0:
        raise ValueError(
            "Radius of gyration must be greater than zero."
        )

    return effective_length / radius_of_gyration


def calculate_radius_of_gyration(
    width,
    depth,
    axis="y"
):
    """
    Calculate the radius of gyration for a rectangular column.

    For a rectangular section:

        iy = h / sqrt(12)
        iz = b / sqrt(12)

    Returns:
        float: Radius of gyration in mm.
    """

    if width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    if axis not in ("y", "z"):
        raise ValueError(
            "Axis must be either 'y' or 'z'."
        )

    if axis == "y":
        return depth / (12 ** 0.5)

    return width / (12 ** 0.5)


def analyze_axially_loaded_column(
    dead_load,
    live_load,
    width,
    depth,
    effective_length=None,
    axis="y"
):
    """
    Perform a preliminary analysis of an axially loaded
    rectangular column.

    Returns:
        dict:
            Column analysis results.
    """

    design_load = calculate_design_axial_load(
        dead_load,
        live_load
    )

    column_area = calculate_column_area(
        width,
        depth
    )

    axial_stress = calculate_axial_stress(
        design_load,
        column_area
    )

    result = {
        "design_axial_load_kN": design_load,
        "column_area_mm2": column_area,
        "axial_stress_N_per_mm2": axial_stress
    }

    if effective_length is not None:

        radius = calculate_radius_of_gyration(
            width,
            depth,
            axis
        )

        slenderness = calculate_slenderness_ratio(
            effective_length,
            radius
        )

        result["effective_length_mm"] = effective_length
        result["radius_of_gyration_mm"] = radius
        result["slenderness_ratio"] = slenderness

    return result
