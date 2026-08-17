"""
Structural Engineering Analyzer
Column Calculator

Main controller for the column calculation modules.

This module combines:
- Column loading
- Column analysis
- Column design
- Column reinforcement

It provides one main function that can later be
called by the backend/API.

Design basis:
- Preliminary Eurocode-oriented approach
- Rectangular reinforced-concrete column
- Predominantly axial loading

IMPORTANT:
This is a preliminary calculation engine.
Final structural design must include all applicable
code checks, slenderness, eccentricity, second-order
effects, detailing requirements, fire requirements,
and professional engineering review.
"""

from .column_loads import (
    calculate_total_load,
    calculate_design_load
)

from .column_analysis import (
    calculate_column_area,
    calculate_axial_stress
)

from .column_design import (
    calculate_design_capacity,
    check_column_capacity
)

from .column_reinforcement import (
    calculate_minimum_steel_area,
    calculate_maximum_steel_area,
    calculate_required_steel_area,
    select_governing_steel_area,
    find_suitable_reinforcement
)


def calculate_column(
    column_width,
    column_depth,
    dead_load,
    live_load,
    concrete_strength=25,
    steel_strength=500,
    preferred_bar_diameter=16
):
    """
    Perform a complete preliminary column calculation.

    Parameters:
        column_width (float):
            Column width in mm.

        column_depth (float):
            Column depth in mm.

        dead_load (float):
            Dead axial load in kN.

        live_load (float):
            Live axial load in kN.

        concrete_strength (float):
            Concrete characteristic strength fck
            in N/mm².

        steel_strength (float):
            Steel yield strength fy in N/mm².

        preferred_bar_diameter (float):
            Preferred longitudinal reinforcement
            diameter in mm.

    Returns:
        dict:
            Complete preliminary column calculation.
    """

    # =========================================================
    # 1. BASIC VALIDATION
    # =========================================================

    if column_width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if column_depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    if dead_load < 0:
        raise ValueError(
            "Dead load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if preferred_bar_diameter <= 0:
        raise ValueError(
            "Preferred bar diameter must be greater than zero."
        )

    # =========================================================
    # 2. COLUMN AREA
    # =========================================================

    column_area = calculate_column_area(
        column_width,
        column_depth
    )

    # =========================================================
    # 3. SERVICE LOAD
    # =========================================================

    service_load = calculate_total_load(
        dead_load,
        live_load
    )

    # =========================================================
    # 4. DESIGN LOAD
    # =========================================================

    design_load = calculate_design_load(
        dead_load,
        live_load
    )

    # =========================================================
    # 5. AXIAL STRESS
    # =========================================================

    axial_stress = calculate_axial_stress(
        design_load,
        column_area
    )

    # =========================================================
    # 6. REQUIRED REINFORCEMENT
    # =========================================================

    required_steel = calculate_required_steel_area(
        design_load,
        concrete_strength,
        steel_strength,
        column_area
    )

    # =========================================================
    # 7. MINIMUM REINFORCEMENT
    # =========================================================

    minimum_steel = calculate_minimum_steel_area(
        column_area
    )

    # =========================================================
    # 8. MAXIMUM REINFORCEMENT
    # =========================================================

    maximum_steel = calculate_maximum_steel_area(
        column_area
    )

    # =========================================================
    # 9. GOVERNING REINFORCEMENT
    # =========================================================

    governing_steel = select_governing_steel_area(
        required_steel,
        minimum_steel
    )

    # =========================================================
    # 10. PRACTICAL REINFORCEMENT
    # =========================================================

    reinforcement = find_suitable_reinforcement(
        governing_steel,
        column_area,
        preferred_bar_diameter
    )

    # =========================================================
    # 11. COLUMN CAPACITY
    # =========================================================

    column_capacity = calculate_design_capacity(
        column_area,
        reinforcement["provided_area_mm2"],
        concrete_strength,
        steel_strength
    )

    # =========================================================
    # 12. CAPACITY CHECK
    # =========================================================

    capacity_check = check_column_capacity(
        design_load,
        column_capacity
    )

    # =========================================================
    # 13. FINAL RESULT
    # =========================================================

    return {
        "column": {
            "width_mm": column_width,
            "depth_mm": column_depth,
            "area_mm2": column_area
        },

        "materials": {
            "concrete_strength_N_per_mm2":
                concrete_strength,

            "steel_strength_N_per_mm2":
                steel_strength
        },

        "loads": {
            "dead_load_kN":
                dead_load,

            "live_load_kN":
                live_load,

            "service_load_kN":
                service_load,

            "design_load_kN":
                design_load
        },

        "analysis": {
            "axial_stress_N_per_mm2":
                axial_stress
        },

        "design": {
            "required_steel_area_mm2":
                required_steel,

            "minimum_steel_area_mm2":
                minimum_steel,

            "maximum_steel_area_mm2":
                maximum_steel,

            "governing_steel_area_mm2":
                governing_steel
        },

        "reinforcement": {
            "number_of_bars":
                reinforcement["number_of_bars"],

            "bar_diameter_mm":
                reinforcement["bar_diameter_mm"],

            "provided_steel_area_mm2":
                reinforcement["provided_area_mm2"],

            "reinforcement_ratio":
                reinforcement["reinforcement_ratio"]
        },

        "capacity": {
            "design_capacity_kN":
                column_capacity,

            "utilization_ratio":
                capacity_check["utilization_ratio"],

            "passes_capacity_check":
                capacity_check["passes_capacity_check"]
        }
    }

