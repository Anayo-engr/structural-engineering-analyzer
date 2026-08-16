"""
Structural Engineering Analyzer
Beam Load Calculation Module

This module calculates the basic loads acting on a structural beam.
"""


def calculate_total_load(dead_load, live_load):
    """
    Calculate the total service load on a beam.

    Parameters:
        dead_load (float): Dead load in kN/m
        live_load (float): Live load in kN/m

    Returns:
        float: Total service load in kN/m
    """

    if dead_load < 0:
        raise ValueError("Dead load cannot be negative.")

    if live_load < 0:
        raise ValueError("Live load cannot be negative.")

    total_load = dead_load + live_load

    return total_load


def calculate_design_load(dead_load, live_load,
                          dead_load_factor=1.35,
                          live_load_factor=1.50):
    """
    Calculate the ultimate/design load using load factors.

    Default factors are based on the commonly used
    persistent/transient ULS combination:

        Design load = 1.35G + 1.50Q

    Parameters:
        dead_load (float): Dead load in kN/m
        live_load (float): Live load in kN/m
        dead_load_factor (float): Factor applied to dead load
        live_load_factor (float): Factor applied to live load

    Returns:
        float: Ultimate/design load in kN/m
    """

    if dead_load < 0:
        raise ValueError("Dead load cannot be negative.")

    if live_load < 0:
        raise ValueError("Live load cannot be negative.")

    design_load = (
        dead_load * dead_load_factor
        + live_load * live_load_factor
    )

    return design_load


def calculate_max_bending_moment(load, span):
    """
    Calculate maximum bending moment for a simply
    supported beam carrying a uniformly distributed load.

    Formula:

        M = wL² / 8

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

    moment = (load * span ** 2) / 8

    return moment


def calculate_max_shear_force(load, span):
    """
    Calculate maximum shear force for a simply
    supported beam carrying a uniformly distributed load.

    Formula:

        V = wL / 2

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

    shear_force = (load * span) / 2

    return shear_force
