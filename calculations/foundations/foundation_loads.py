"""
Structural Engineering Analyzer
Foundation Load Calculation Module

Preliminary foundation load calculations.

Design basis:
- Service load
- Ultimate/design load
- Eurocode-oriented load factors

Units:
    Loads: kN
"""


# =========================================================
# SERVICE LOAD
# =========================================================

def calculate_total_load(dead_load, live_load):
    """
    Calculate total service load.

        G + Q

    Parameters:
        dead_load (float):
            Permanent/dead load in kN.

        live_load (float):
            Variable/live load in kN.

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

    return dead_load + live_load


# =========================================================
# DESIGN LOAD
# =========================================================

def calculate_design_load(
    dead_load,
    live_load,
    dead_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the ultimate/design foundation load.

        NEd = 1.35G + 1.50Q

    Parameters:
        dead_load (float):
            Permanent/dead load in kN.

        live_load (float):
            Variable/live load in kN.

        dead_load_factor (float):
            Partial factor for dead load.

        live_load_factor (float):
            Partial factor for live load.

    Returns:
        float:
            Ultimate/design load in kN.
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
