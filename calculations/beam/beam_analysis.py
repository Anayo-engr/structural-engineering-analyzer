"""
Structural Engineering Analyzer
Beam Analysis Module

This module performs basic structural analysis of a
simply supported beam carrying a uniformly distributed
load (UDL) over the full span.

Units:
    Load: kN/m
    Span: m
    Reaction: kN
    Shear force: kN
    Bending moment: kNm
"""

import math


# =========================================================
# INPUT VALIDATION
# =========================================================

def _validate_load_and_span(load, span):
    """
    Validate beam load and span inputs.
    """

    if not isinstance(load, (int, float)):
        raise TypeError("Load must be a number.")

    if not isinstance(span, (int, float)):
        raise TypeError("Span must be a number.")

    if not math.isfinite(load):
        raise ValueError("Load must be a finite number.")

    if not math.isfinite(span):
        raise ValueError("Span must be a finite number.")

    if load < 0:
        raise ValueError("Load cannot be negative.")

    if span <= 0:
        raise ValueError("Span must be greater than zero.")


# =========================================================
# SUPPORT REACTIONS
# =========================================================

def calculate_support_reactions(load, span):
    """
    Calculate the reactions at the two supports.

    For a simply supported beam carrying a full-span
    uniformly distributed load:

        RA = RB = wL / 2

    Parameters:
        load (float):
            Uniformly distributed load in kN/m.

        span (float):
            Beam span in metres.

    Returns:
        tuple:
            (left_reaction, right_reaction) in kN.
    """

    _validate_load_and_span(load, span)

    reaction = (load * span) / 2

    return reaction, reaction


# =========================================================
# MAXIMUM SHEAR FORCE
# =========================================================

def calculate_max_shear(load, span):
    """
    Calculate the maximum shear force.

    For a simply supported beam carrying a full-span
    uniformly distributed load:

        Vmax = wL / 2

    Parameters:
        load (float):
            Uniformly distributed load in kN/m.

        span (float):
            Beam span in metres.

    Returns:
        float:
            Maximum shear force in kN.
    """

    _validate_load_and_span(load, span)

    maximum_shear = (load * span) / 2

    return maximum_shear


# =========================================================
# MAXIMUM BENDING MOMENT
# =========================================================

def calculate_max_bending_moment(load, span):
    """
    Calculate the maximum bending moment.

    For a simply supported beam carrying a full-span
    uniformly distributed load:

        Mmax = wL² / 8

    Parameters:
        load (float):
            Uniformly distributed load in kN/m.

        span (float):
            Beam span in metres.

    Returns:
        float:
            Maximum bending moment in kNm.
    """

    _validate_load_and_span(load, span)

    maximum_moment = (load * span ** 2) / 8

    return maximum_moment


# =========================================================
# COMPLETE SIMPLY SUPPORTED BEAM ANALYSIS
# =========================================================

def analyze_simply_supported_beam(load, span):
    """
    Perform a complete basic analysis of a simply
    supported beam carrying a full-span UDL.

    Parameters:
        load (float):
            Uniformly distributed load in kN/m.

        span (float):
            Beam span in metres.

    Returns:
        dict:
            Complete beam analysis results.
    """

    _validate_load_and_span(load, span)

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
