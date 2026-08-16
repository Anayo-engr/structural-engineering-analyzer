"""
Structural Engineering Analyzer
Beam Analysis Module

This module calculates support reactions,
maximum shear force, and maximum bending moment
for a simply supported beam carrying a
uniformly distributed load (UDL).
"""


def calculate_support_reactions(load, span):
    """
    Calculate the reactions at the two supports.

    For a simply supported beam with a symmetrical
    uniformly distributed load:

        RA = RB = wL / 2

    Parameters:
        load (float): Uniformly distributed load in kN/m
        span (float): Beam span in metres

    Returns:
        tuple: Left and right support reactions in kN
    """

    if load < 0:
        raise ValueError("Load cannot be negative.")

    if span <= 0:
        raise ValueError("Span must be greater than zero.")

    reaction = (load * span) / 2

    return reaction, reaction


def calculate_max_shear(load, span):
    """
    Calculate the maximum shear force.

    For a simply supported beam under a UDL:

        Vmax = wL / 2

    Parameters:
        load (float): Uniformly distributed load in kN/m
        span (float): Beam span in metres

    Returns:
        float: Maximum shear force in kN
    """

    if load < 0:
        raise ValueError("Load cannot be negative.")

    if span <= 0:
        raise ValueError("Span must be greater than zero.")

    return (load * span) / 2


def calculate_max_bending_moment(load, span):
    """
    Calculate the maximum bending moment.

    For a simply supported beam under a UDL:

        Mmax = wL² / 8

    Parameters:
        load (float): Uniformly distributed load in kN/m
        span (float): Beam span in metres

    Returns:
        float: Maximum bending moment in kNm
    """

    if load < 0:
        raise ValueError("Load cannot be negative.")

    if span <= 0:
        raise ValueError("Span must be greater than zero.")

    return (load * span ** 2) / 8


def analyze_simply_supported_beam(load, span):
    """
    Perform a basic analysis of a simply supported beam.

    Parameters:
        load (float): Uniformly distributed load in kN/m
        span (float): Beam span in metres

    Returns:
        dict: Beam analysis results
    """

    left_reaction, right_reaction = calculate_support_reactions(
        load,
        span
    )

    maximum_shear = calculate_max_shear(
        load,
        span
    )

    maximum_moment = calculate_max_bending_moment(
        load,
        span
    )

    return {
        "span_m": span,
        "load_kN_per_m": load,
        "left_reaction_kN": left_reaction,
        "right_reaction_kN": right_reaction,
        "maximum_shear_kN": maximum_shear,
        "maximum_bending_moment_kNm": maximum_moment
    }

