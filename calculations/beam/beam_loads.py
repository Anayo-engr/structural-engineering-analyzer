"""
Structural Engineering Analyzer
Beam Load Calculation Module

This module calculates basic service and ultimate/design
loads acting on a structural beam.

Units:
    Load: kN/m
"""


# =========================================================
# SERVICE LOAD
# =========================================================

def calculate_total_load(dead_load, live_load):
    """
    Calculate the total service load on a beam.

    Formula:

        G + Q

    Parameters:
        dead_load (float):
            Dead load in kN/m.

        live_load (float):
            Live load in kN/m.

    Returns:
        float:
            Total service load in kN/m.
    """

    if dead_load < 0:
        raise ValueError("Dead load cannot be negative.")

    if live_load < 0:
        raise ValueError("Live load cannot be negative.")

    total_load = dead_load + live_load

    return total_load


# =========================================================
# ULTIMATE / DESIGN LOAD
# =========================================================

def calculate_design_load(
    dead_load,
    live_load,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the ultimate/design load.

    Default load combination:

        wu = 1.35G + 1.50Q

    Parameters:
        dead_load (float):
            Dead load in kN/m.

        live_load (float):
            Live load in kN/m.

        dead_load_factor (float):
            Partial factor applied to dead load.

        live_load_factor (float):
            Partial factor applied to live load.

    Returns:
        float:
            Ultimate/design load in kN/m.
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
