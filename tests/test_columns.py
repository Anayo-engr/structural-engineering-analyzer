"""
Tests for the Structural Engineering Analyzer
Column Calculation Modules.
"""

import sys
from pathlib import Path

# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# COLUMN LOAD IMPORTS
# =========================================================

from calculations.columns.column_loads import (
    calculate_total_load,
    calculate_design_load
)


# =========================================================
# COLUMN ANALYSIS IMPORTS
# =========================================================

from calculations.columns.column_analysis import (
    calculate_column_area,
    calculate_axial_stress
)


# =========================================================
# COLUMN DESIGN IMPORTS
# =========================================================

from calculations.columns.column_design import (
    calculate_design_capacity,
    check_column_capacity
)


# =========================================================
# COLUMN REINFORCEMENT IMPORTS
# =========================================================

from calculations.columns.column_reinforcement import (
    calculate_bar_area,
    calculate_minimum_steel_area,
    calculate_maximum_steel_area,
    calculate_required_steel_area,
    calculate_provided_steel_area,
    calculate_reinforcement_ratio
)


# =========================================================
# COMPLETE COLUMN CALCULATOR
# =========================================================

from calculations.columns.column_calculator import (
    calculate_column
)


# =========================================================
# COLUMN LOAD TESTS
# =========================================================

def test_total_service_load():
    """
    Test total service axial load.

        G + Q

        = 100 + 50

        = 150 kN
    """

    result = calculate_total_load(
        dead_load=100,
        live_load=50
    )

    assert result == 150


def test_design_load():
    """
    Test design axial load.

        NEd = 1.35G + 1.50Q

        = 1.35(100) + 1.50(50)

        = 210 kN
    """

    result = calculate_design_load(
        dead_load=100,
        live_load=50
    )

    assert result == 210.0


# =========================================================
# COLUMN ANALYSIS TESTS
# =========================================================

def test_column_area():
    """
    Test rectangular column area.

        Ac = b × h

        = 300 × 300

        = 90,000 mm²
    """

    result = calculate_column_area(
        column_width=300,
        column_depth=300
    )

    assert result == 90000


def test_axial_stress():
    """
    Test average axial stress.

        σ = N / Ac

        = 210,000 / 90,000

        = 2.333 N/mm²
    """

    result = calculate_axial_stress(
        design_load=210,
        column_area=90000
    )

    assert round(result, 3) == 2.333


# =========================================================
# COLUMN DESIGN TESTS
# =========================================================

def test_design_capacity():
    """
    Test that the calculated column design capacity
    is greater than zero.
    """

    result = calculate_design_capacity(
        column_area=90000,
        steel_area=900,
        concrete_strength=25,
        steel_strength=500
    )

    assert result > 0


def test_column_capacity_check():
    """
    Test column capacity check.
    """

    result = check_column_capacity(
        design_load=210,
        design_capacity=1000
    )

    assert result["passes_capacity_check"] is True
    assert result["utilization_ratio"] < 1


# =========================================================
# COLUMN REINFORCEMENT TESTS
# =========================================================

def test_bar_area():
    """
    Area of one 16 mm bar:

        A = πØ²/4

        ≈ 201.06 mm²
    """

    result = calculate_bar_area(16)

    assert round(result, 2) == 201.06


def test_minimum_steel_area():
    """
    Test minimum reinforcement area.

        As,min = 0.01 × Ac

        = 0.01 × 90,000

        = 900 mm²
    """

    result = calculate_minimum_steel_area(
        column_area=90000
    )

    assert result == 900


def test_maximum_steel_area():
    """
    Test maximum reinforcement area.

        As,max = 0.04 × Ac

        = 0.04 × 90,000

        = 3,600 mm²
    """

    result = calculate_maximum_steel_area(
        column_area=90000
    )

    assert result == 3600


def test_required_steel_area():
    """
    Test that the required reinforcement area
    is not negative.
    """

    result = calculate_required_steel_area(
        design_load=210,
        concrete_strength=25,
        steel_strength=500,
        column_area=90000
    )

    assert result >= 0


def test_provided_steel_area():
    """
    Test reinforcement provided by 8Y16.

        8 × 201.06
        ≈ 1608.50 mm²
    """

    result = calculate_provided_steel_area(
        number_of_bars=8,
        bar_diameter=16
    )

    assert round(result, 2) == 1608.50


def test_reinforcement_ratio():
    """
    Test longitudinal reinforcement ratio.
    """

    result = calculate_reinforcement_ratio(
        steel_area=900,
        column_area=90000
    )

    assert result == 0.01


# =========================================================
# INPUT VALIDATION TESTS
# =========================================================

def test_negative_load_rejected():
    """
    Negative loads must be rejected.
    """

    try:

        calculate_total_load(
            dead_load=-100,
            live_load=50
        )

        assert False

    except ValueError:

        assert True


def test_zero_column_width_rejected():
    """
    A zero column width must be rejected.
    """

    try:

        calculate_column_area(
            column_width=0,
            column_depth=300
        )

        assert False

    except ValueError:

        assert True


# =========================================================
# COMPLETE COLUMN CALCULATION TEST
# =========================================================

def test_complete_column_calculation():
    """
    Test the complete column calculation controller.
    """

    result = calculate_column(
        column_width=300,
        column_depth=300,
        dead_load=100,
        live_load=50,
        concrete_strength=25,
        steel_strength=500,
        preferred_bar_diameter=16
    )

    # Check major result sections exist.
    assert "column" in result
    assert "materials" in result
    assert "loads" in result
    assert "analysis" in result
    assert "design" in result
    assert "reinforcement" in result
    assert "capacity" in result

    # Check column information.
    assert result["column"]["width_mm"] == 300
    assert result["column"]["depth_mm"] == 300
    assert result["column"]["area_mm2"] == 90000

    # Check loads.
    assert result["loads"]["service_load_kN"] == 150
    assert result["loads"]["design_load_kN"] == 210

    # Check analysis.
    assert result["analysis"]["axial_stress_N_per_mm2"] > 0

    # Check reinforcement.
    assert result["reinforcement"]["provided_steel_area_mm2"] > 0

    # Check capacity.
    assert result["capacity"]["design_capacity_kN"] > 0
    assert result["capacity"]["utilization_ratio"] > 0
