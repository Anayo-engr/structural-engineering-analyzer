"""
Structural Engineering Analyzer
Column Load Calculation Module

This module calculates the basic loads used in
reinforced-concrete column design.

Design basis:
- Preliminary Eurocode-oriented approach
- Ultimate limit state load combination
- Axial load calculations

IMPORTANT:
This module is a preliminary calculation component.
Final structural design must consider the applicable
design code, load combinations, eccentricity, second-order
effects, frame action, imperfections, and professional
engineering review.
"""


def calculate_total_load(dead_load, live_load):
    """
    Calculate the total service axial load on a column.

    Formula:

        N = G + Q

    Parameters:
        dead_load (float):
            Characteristic dead load in kN.

        live_load (float):
            Characteristic live load in kN.

    Returns:
        float:
            Total service load in kN.
    """

    if dead_load < 0:
        raise ValueError(
            "Dead load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    total_load = dead_load + live_load

    return total_load


def calculate_design_load(
    dead_load,
    live_load,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the ultimate/design axial load.

    Default load combination:

        NEd = 1.35G + 1.50Q

    Parameters:
        dead_load (float):
            Characteristic dead load in kN.

        live_load (float):
            Characteristic live load in kN.

        dead_load_factor (float):
            Partial factor applied to dead load.

        live_load_factor (float):
            Partial factor applied to live load.

    Returns:
        float:
            Ultimate/design axial load in kN.
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

    design_load = (
        dead_load * dead_load_factor
        + live_load * live_load_factor
    )

    return design_load


def calculate_column_self_weight(
    width,
    depth,
    height,
    concrete_density=25
):
    """
    Calculate the self-weight of a rectangular concrete column.

    Formula:

        Volume = b × h × L

        Self-weight = Volume × concrete density

    Parameters:
        width (float):
            Column width in metres.

        depth (float):
            Column depth in metres.

        height (float):
            Column height in metres.

        concrete_density (float):
            Concrete density in kN/m³.
            Default = 25 kN/m³.

    Returns:
        float:
            Column self-weight in kN.
    """

    if width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    if height <= 0:
        raise ValueError(
            "Column height must be greater than zero."
        )

    if concrete_density <= 0:
        raise ValueError(
            "Concrete density must be greater than zero."
        )

    volume = width * depth * height

    self_weight = volume * concrete_density

    return self_weight


def calculate_design_load_with_self_weight(
    dead_load,
    live_load,
    self_weight,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the design axial load including column self-weight.

    The column self-weight is treated as part of the permanent
    dead load.

    Formula:

        NEd =
        1.35 × (G + Gcolumn) + 1.50 × Q

    Parameters:
        dead_load (float):
            Applied characteristic dead load in kN.

        live_load (float):
            Applied characteristic live load in kN.

        self_weight (float):
            Column self-weight in kN.

        dead_load_factor (float):
            Partial factor applied to permanent load.

        live_load_factor (float):
            Partial factor applied to variable load.

    Returns:
        float:
            Ultimate/design axial load including self-weight
            in kN.
    """

    if dead_load < 0:
        raise ValueError(
            "Dead load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    if self_weight < 0:
        raise ValueError(
            "Column self-weight cannot be negative."
        )

    if dead_load_factor <= 0:
        raise ValueError(
            "Dead load factor must be greater than zero."
        )

    if live_load_factor <= 0:
        raise ValueError(
            "Live load factor must be greater than zero."
        )

    total_dead_load = dead_load + self_weight

    design_load = (
        total_dead_load * dead_load_factor
        + live_load * live_load_factor
    )

    return design_load


def calculate_load_ratio(
    design_load,
    reference_capacity
):
    """
    Calculate the ratio of design axial load to a reference
    column capacity.

    Formula:

        Utilization = NEd / NRd

    Parameters:
        design_load (float):
            Design axial load in kN.

        reference_capacity (float):
            Reference axial capacity in kN.

    Returns:
        float:
            Load utilization ratio.
    """

    if design_load < 0:
        raise ValueError(
            "Design load cannot be negative."
        )

    if reference_capacity <= 0:
        raise ValueError(
            "Reference capacity must be greater than zero."
        )

    return design_load / reference_capacity
