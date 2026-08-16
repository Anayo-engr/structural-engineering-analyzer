"""
Tests for the Structural Engineering Analyzer
Beam Calculation Modules.
"""

import sys
from pathlib import Path

# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from calculations.beams.beam_loads import (
    calculate_total_load,
    calculate_design_load
)

from calculations.beams.beam_analysis import (
    calculate_support_reactions,
    calculate_max_shear,
    calculate_max_bending_moment
)

from calculations.beams.beam_design import (
    calculate_effective_depth,
    calculate_required_steel_area
)

from calculations.beams.beam_reinforcement import (
    calculate_bar_area,
    calculate_provided_steel_area,
    calculate_required_number_of_bars
)


# =========================================================
# BEAM LOAD TESTS
# =========================================================

def test_total_service_load():
    """
    Test that dead load + live load gives the correct
    service load.
    """

    result = calculate_total_load(
        dead_load=10,
        live_load=5
    )

    assert result == 15


def test_design_load():
    """
    Test the design load using:

        1.35G + 1.50Q
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
    Test reactions for:

        w = 20 kN/m
        L = 6 m

    Reaction = wL/2
              = 20 × 6 / 2
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
    Test maximum shear:

        V = wL/2
          = 20 × 6 / 2
          = 60 kN
    """

    result = calculate_max_shear(
        load=20,
        span=6
    )

    assert result == 60


def test_max_bending_moment():
    """
    Test maximum bending moment:

        M = wL²/8

          = 20 × 6² / 8

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
    Test effective depth:

        d = h - c - Ø/2

          = 500 - 25 - 8

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
    Test the reinforcement calculation with a known
    design moment.
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
    Test the area of a 16 mm diameter reinforcement bar.
    """

    result = calculate_bar_area(16)

    assert round(result, 2) == 201.06


def test_provided_steel_area():
    """
    Test the area provided by 4Y16 bars.
    """

    result = calculate_provided_steel_area(
        number_of_bars=4,
        bar_diameter=16
    )

    assert round(result, 2) == 804.25


def test_required_number_of_bars():
    """
    Test that the program determines how many bars are
    needed to satisfy a required steel area.
    """

    result = calculate_required_number_of_bars(
        required_area=750,
        bar_diameter=16
    )

    assert result == 4


# =========================================================
# ERROR VALIDATION TESTS
# =========================================================

def test_negative_load_rejected():
    """
    Negative loads should not be accepted.
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
    A beam span of zero must be rejected.
    """

    try:
        calculate_max_bending_moment(
            load=20,
            span=0
        )

        assert False

    except ValueError:
        assert True

from calculations.beams.beam_calculator import calculate_beam


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

    assert "beam" in result
    assert "materials" in result
    assert "loads" in result
    assert "analysis" in result
    assert "design" in result
    assert "reinforcement" in result
    assert "shear" in result
    assert "links" in result

    assert result["beam"]["span_m"] == 6
    assert result["loads"]["service_load_kN_per_m"] == 15
    assert result["loads"]["design_load_kN_per_m"] == 20

    assert result["analysis"]["left_reaction_kN"] == 60
    assert result["analysis"]["right_reaction_kN"] == 60
    assert result["analysis"]["maximum_shear_kN"] == 60
    assert result["analysis"]["maximum_bending_moment_kNm"] == 90

    assert result["design"]["design_bending_moment_kNm"] == 90

    assert result["reinforcement"]["provided_steel_area_mm2"] > 0

    assert result["shear"]["concrete_shear_resistance_kN"] > 0
