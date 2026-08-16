"""
Structural Engineering Analyzer
Beam Calculator

Main controller for the beam calculation modules.

This module combines:
- Beam loading
- Beam analysis
- Bending design
- Shear design
- Reinforcement selection

It provides one main function that can later be
called by the backend/API.
"""

from beam_loads import (
    calculate_total_load,
    calculate_design_load
)

from beam_analysis import (
    calculate_support_reactions,
    calculate_max_shear,
    calculate_max_bending_moment
)

from beam_design import (
    calculate_effective_depth,
    calculate_design_bending_moment,
    calculate_required_steel_area,
    calculate_minimum_steel_area,
    select_required_steel_area
)

from beam_shear import (
    calculate_design_shear_force,
    calculate_shear_stress,
    calculate_longitudinal_reinforcement_ratio,
    calculate_concrete_shear_resistance,
    check_shear_capacity
)

from beam_reinforcement import (
    find_suitable_reinforcement,
    calculate_clear_spacing,
    recommend_links
)


def calculate_beam(
    beam_width,
    overall_depth,
    concrete_cover,
    main_bar_diameter,
    dead_load,
    live_load,
    span,
    concrete_strength=25,
    steel_strength=500,
    link_diameter=8
):
    """
    Perform a complete preliminary beam calculation.

    Parameters:
        beam_width (float): Beam width in mm
        overall_depth (float): Overall beam depth in mm
        concrete_cover (float): Concrete cover in mm
        main_bar_diameter (float): Main reinforcement diameter in mm
        dead_load (float): Dead load in kN/m
        live_load (float): Live load in kN/m
        span (float): Beam span in metres
        concrete_strength (float): Concrete strength fck in N/mm²
        steel_strength (float): Steel yield strength fy in N/mm²
        link_diameter (float): Shear link diameter in mm

    Returns:
        dict: Complete preliminary beam calculation.
    """

    # ---------------------------------------------------------
    # 1. BASIC VALIDATION
    # ---------------------------------------------------------

    if beam_width <= 0:
        raise ValueError("Beam width must be greater than zero.")

    if overall_depth <= 0:
        raise ValueError("Beam depth must be greater than zero.")

    if dead_load < 0:
        raise ValueError("Dead load cannot be negative.")

    if live_load < 0:
        raise ValueError("Live load cannot be negative.")

    if span <= 0:
        raise ValueError("Beam span must be greater than zero.")

    # ---------------------------------------------------------
    # 2. EFFECTIVE DEPTH
    # ---------------------------------------------------------

    effective_depth = calculate_effective_depth(
        overall_depth,
        concrete_cover,
        main_bar_diameter
    )

    # ---------------------------------------------------------
    # 3. SERVICE LOAD
    # ---------------------------------------------------------

    total_service_load = calculate_total_load(
        dead_load,
        live_load
    )

    # ---------------------------------------------------------
    # 4. DESIGN LOAD
    # ---------------------------------------------------------

    design_load = calculate_design_load(
        dead_load,
        live_load
    )

    # ---------------------------------------------------------
    # 5. SUPPORT REACTIONS
    # ---------------------------------------------------------

    left_reaction, right_reaction = (
        calculate_support_reactions(
            design_load,
            span
        )
    )

    # ---------------------------------------------------------
    # 6. MAXIMUM SHEAR
    # ---------------------------------------------------------

    maximum_shear = calculate_max_shear(
        design_load,
        span
    )

    # ---------------------------------------------------------
    # 7. MAXIMUM BENDING MOMENT
    # ---------------------------------------------------------

    maximum_moment = calculate_max_bending_moment(
        design_load,
        span
    )

    # ---------------------------------------------------------
    # 8. DESIGN BENDING MOMENT
    # ---------------------------------------------------------

    design_moment = calculate_design_bending_moment(
        dead_load,
        live_load,
        span
    )

    # ---------------------------------------------------------
    # 9. REQUIRED BENDING REINFORCEMENT
    # ---------------------------------------------------------

    required_steel = calculate_required_steel_area(
        design_moment,
        effective_depth,
        steel_strength
    )

    # ---------------------------------------------------------
    # 10. MINIMUM REINFORCEMENT
    # ---------------------------------------------------------

    minimum_steel = calculate_minimum_steel_area(
        beam_width,
        effective_depth,
        concrete_strength
    )

    # ---------------------------------------------------------
    # 11. GOVERNING STEEL AREA
    # ---------------------------------------------------------

    governing_steel = select_required_steel_area(
        required_steel,
        minimum_steel
    )

    # ---------------------------------------------------------
    # 12. SELECT PRACTICAL REINFORCEMENT
    # ---------------------------------------------------------

    reinforcement = find_suitable_reinforcement(
        governing_steel,
        main_bar_diameter
    )

    # ---------------------------------------------------------
    # 13. BAR SPACING
    # ---------------------------------------------------------

    clear_spacing = calculate_clear_spacing(
        beam_width,
        concrete_cover,
        link_diameter,
        reinforcement["bar_diameter_mm"],
        reinforcement["number_of_bars"]
    )

    # ---------------------------------------------------------
    # 14. SHEAR STRESS
    # ---------------------------------------------------------

    shear_stress = calculate_shear_stress(
        maximum_shear,
        beam_width,
        effective_depth
    )

    # ---------------------------------------------------------
    # 15. REINFORCEMENT RATIO
    # ---------------------------------------------------------

    reinforcement_ratio = (
        calculate_longitudinal_reinforcement_ratio(
            reinforcement["provided_area_mm2"],
            beam_width,
            effective_depth
        )
    )

    # ---------------------------------------------------------
    # 16. CONCRETE SHEAR RESISTANCE
    # ---------------------------------------------------------

    concrete_shear_resistance = (
        calculate_concrete_shear_resistance(
            concrete_strength,
            reinforcement_ratio,
            effective_depth,
            beam_width
        )
    )

    # ---------------------------------------------------------
    # 17. SHEAR CAPACITY CHECK
    # ---------------------------------------------------------

    shear_check = check_shear_capacity(
        maximum_shear,
        concrete_shear_resistance
    )

    # ---------------------------------------------------------
    # 18. PRELIMINARY LINKS
    # ---------------------------------------------------------

    links = recommend_links(
        maximum_shear,
        beam_width,
        effective_depth
    )

    # ---------------------------------------------------------
    # 19. FINAL RESULT
    # ---------------------------------------------------------

    return {
        "beam": {
            "width_mm": beam_width,
            "overall_depth_mm": overall_depth,
            "effective_depth_mm": effective_depth,
            "span_m": span
        },

        "materials": {
            "concrete_strength_N_per_mm2":
                concrete_strength,
            "steel_strength_N_per_mm2":
                steel_strength
        },

        "loads": {
            "dead_load_kN_per_m": dead_load,
            "live_load_kN_per_m": live_load,
            "service_load_kN_per_m":
                total_service_load,
            "design_load_kN_per_m":
                design_load
        },

        "analysis": {
            "left_reaction_kN":
                left_reaction,
            "right_reaction_kN":
                right_reaction,
            "maximum_shear_kN":
                maximum_shear,
            "maximum_bending_moment_kNm":
                maximum_moment
        },

        "design": {
            "design_bending_moment_kNm":
                design_moment,
            "required_steel_area_mm2":
                required_steel,
            "minimum_steel_area_mm2":
                minimum_steel,
            "governing_steel_area_mm2":
                governing_steel
        },

        "reinforcement": {
            "number_of_main_bars":
                reinforcement["number_of_bars"],
            "main_bar_diameter_mm":
                reinforcement["bar_diameter_mm"],
            "provided_steel_area_mm2":
                reinforcement["provided_area_mm2"],
            "clear_spacing_mm":
                clear_spacing
        },

        "shear": {
            "shear_stress_N_per_mm2":
                shear_stress,
            "reinforcement_ratio":
                reinforcement_ratio,
            "concrete_shear_resistance_kN":
                concrete_shear_resistance,
            "utilization_ratio":
                shear_check["utilization_ratio"],
            "passes_concrete_shear_check":
                shear_check[
                    "passes_concrete_shear_check"
                ]
        },

        "links": {
            "diameter_mm":
                links["link_diameter_mm"],
            "number_of_legs":
                links["number_of_legs"],
            "spacing_mm":
                links["link_spacing_mm"]
        }
    }
