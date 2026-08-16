"""
Tests for the Structural Engineering Analyzer
Beam Calculation Modules.
"""

import sys
from pathlib import Path

# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# BEAM LOAD IMPORTS
# =========================================================

from calculations.beam.beam_loads import (
    calculate_total_load,
    calculate_design_load
)


# =========================================================
# BEAM ANALYSIS IMPORTS
# =========================================================

from calculations.beam.beam_analysis import (
    calculate_support_reactions,
    calculate_max_shear,
    calculate_max_bending_moment
)


# =========================================================
# BEAM DESIGN IMPORTS
# =========================================================

from calculations.beam.beam_design import (
    calculate_effective_depth,
    calculate_required_steel_area
)


# =========================================================
# BEAM REINFORCEMENT IMPORTS
# =========================================================

from calculations.beam.beam_reinforcement import (
    calculate_bar_area,
    calculate_provided_steel_area,
    calculate_required_number_of_bars
)


# =========================================================
# COMPLETE BEAM CALCULATOR
# =========================================================

from calculations.beam.beam_calculator import (
    calculate_beam
)


# =========================================================
# BEAM LOAD TESTS
# =========================================================

def test_total_service_load():
    """
    Test dead load + live load.

    10 + 5 = 15 kN/m
    """

    result = calculate_total_load(
        dead_load=10,
        live_load=5
    )

    assert result == 15


def test_design_load():
    """
    Test design load:

        1.35G + 1.50Q

        = 1.35(10) + 1.50(5)

        = 20 kN/m
    """

    result = calculate_design_load(
        dead_load=10,
        live_load=5
    )

    assert result == 20.0


# =========================================================
# BEAM ANALYSIS TESTS
# =========================================================

def test_support_reactions():
    """
    For a simply supported beam:

        w = 20 kN/m
        L = 6 m

        R = wL/2
          = 60 kN
    """

    left, right = calculate_support_reactions(
        load=20,
        span=6
    )

    assert left == 60
    assert right == 60


def test_max_shear():
    """
    Maximum shear:

        V = wL/2
          = 60 kN
    """

    result = calculate_max_shear(
        load=20,
        span=6
    )

    assert result == 60


def test_max_bending_moment():
    """
    Maximum bending moment:

        M = wL²/8
          = 90 kNm
    """

    result = calculate_max_bending_moment(
        load=20,
        span=6
    )

    assert result == 90


# =========================================================
# BEAM DESIGN TESTS
# =========================================================

def test_effective_depth():
    """
    Effective depth:

        d = h - c - Ø/2

          = 500 - 25 - 16/2

          = 467 mm
    """

    result = calculate_effective_depth(
        overall_depth=500,
        concrete_cover=25,
        bar_diameter=16
    )

    assert result == 467


def test_required_steel_area():
    """
    Check that required reinforcement is positive.
    """

    result = calculate_required_steel_area(
        design_moment=100,
        effective_depth=450,
        steel_strength=500
    )

    assert result > 0


# =========================================================
# REINFORCEMENT TESTS
# =========================================================

def test_bar_area():
    """
    Area of one 16 mm bar:

        A = πØ²/4

        = 201.06 mm²
    """

    result = calculate_bar_area(16)

    assert round(result, 2) == 201.06


def test_provided_steel_area():
    """
    Area provided by 4Y16:

        4 × 201.06
        = 804.25 mm²
    """

    result = calculate_provided_steel_area(
        number_of_bars=4,
        bar_diameter=16
    )

    assert round(result, 2) == 804.25


def test_required_number_of_bars():
    """
    Required area = 750 mm².

    3Y16 = 603.19 mm²  -> insufficient

    4Y16 = 804.25 mm²  -> sufficient

    Therefore 4 bars are required.
    """

    result = calculate_required_number_of_bars(
        required_area=750,
        bar_diameter=16
    )

    assert result == 4


# =========================================================
# INPUT VALIDATION TESTS
# =========================================================

def test_negative_load_rejected():
    """
    Negative loads must be rejected.
    """

    try:

        calculate_total_load(
            dead_load=-10,
            live_load=5
        )

        assert False

    except ValueError:

        assert True


def test_zero_span_rejected():
    """
    A zero beam span must be rejected.
    """

    try:

        calculate_max_bending_moment(
            load=20,
            span=0
        )

        assert False

    except ValueError:

        assert True


# =========================================================
# COMPLETE BEAM CALCULATION TEST
# =========================================================

def test_complete_beam_calculation():
    """
    Test the complete beam calculation controller.
    """

    result = calculate_beam(
        beam_width=300,
        overall_depth=500,
        concrete_cover=25,
        main_bar_diameter=16,
        dead_load=10,
        live_load=5,
        span=6,
        concrete_strength=25,
        steel_strength=500,
        link_diameter=8
    )

    # Check major result sections exist.
    assert "beam" in result
    assert "materials" in result
    assert "loads" in result
    assert "analysis" in result
    assert "design" in result
    assert "reinforcement" in result
    assert "shear" in result
    assert "links" in result

    # Check basic beam information.
    assert result["beam"]["span_m"] == 6

    # Check loads.
    assert result["loads"]["service_load_kN_per_m"] == 15
    assert result["loads"]["design_load_kN_per_m"] == 20

    # Check structural analysis.
    assert result["analysis"]["left_reaction_kN"] == 60
    assert result["analysis"]["right_reaction_kN"] == 60
    assert result["analysis"]["maximum_shear_kN"] == 60
    assert result["analysis"]["maximum_bending_moment_kNm"] == 90

    # Check bending design.
    assert result["design"]["design_bending_moment_kNm"] == 90

    # Check reinforcement.
    assert result["reinforcement"]["provided_steel_area_mm2"] > 0

    # Check shear.
    assert result["shear"]["concrete_shear_resistance_kN"] > 0
