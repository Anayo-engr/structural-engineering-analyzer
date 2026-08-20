"""
Structural Engineering Analyzer
Slab Calculator

Main controller for the preliminary slab calculation modules.

This module combines:
- Slab loading
- Structural analysis
- Flexural design
- Reinforcement selection

Design basis:
- Preliminary Eurocode-oriented approach
- Simply supported one-way reinforced-concrete slab
- Uniformly distributed loading
- One-metre design strip

IMPORTANT:
This is a preliminary calculation engine.
Final structural design must include all applicable
code checks, load combinations, detailing requirements,
serviceability checks, shear checks, durability requirements,
support conditions, and professional engineering review.
"""

# =========================================================
# SLAB LOADS
# =========================================================

from .slab_loads import (
    calculate_slab_loads
)


# =========================================================
# SLAB ANALYSIS
# =========================================================

from .slab_analysis import (
    analyze_simply_supported_slab
)


# =========================================================
# SLAB DESIGN
# =========================================================

from .slab_design import (
    calculate_slab_design
)


# =========================================================
# SLAB REINFORCEMENT
# =========================================================

from .slab_reinforcement import (
    generate_reinforcement_schedule
)


# =========================================================
# COMPLETE SLAB CALCULATOR
# =========================================================

def calculate_slab(
    slab_width=1000,
    overall_depth=150,
    concrete_cover=25,
    main_bar_diameter=10,
    slab_span=4.0,
    finishes_load=1.0,
    ceiling_services_load=0.25,
    partition_load=0.0,
    live_load=2.0,
    concrete_density=25,
    concrete_strength=25,
    steel_strength=500,
    preferred_bar_diameter=None,
    distribution_bar_diameter=8
):
    """
    Perform a complete preliminary one-way slab calculation.

    Parameters:
        slab_width (float):
            Width of the design strip in mm.
            Normally 1000 mm.

        overall_depth (float):
            Slab thickness in mm.

        concrete_cover (float):
            Nominal concrete cover in mm.

        main_bar_diameter (float):
            Main reinforcement diameter in mm.

        slab_span (float):
            Effective span in metres.

        finishes_load (float):
            Finishes load in kN/m².

        ceiling_services_load (float):
            Ceiling/services load in kN/m².

        partition_load (float):
            Allowance for partitions in kN/m².

        live_load (float):
            Imposed/live load in kN/m².

        concrete_density (float):
            Concrete density in kN/m³.

        concrete_strength (float):
            Characteristic concrete strength fck
            in N/mm².

        steel_strength (float):
            Characteristic steel yield strength fyk
            in N/mm².

        preferred_bar_diameter (float):
            Preferred main reinforcement diameter in mm.

        distribution_bar_diameter (float):
            Distribution reinforcement diameter in mm.

    Returns:
        dict:
            Complete preliminary slab calculation.
    """

    # =====================================================
    # 1. INPUT VALIDATION
    # =====================================================

    if slab_width <= 0:
        raise ValueError(
            "Slab width must be greater than zero."
        )

    if overall_depth <= 0:
        raise ValueError(
            "Slab depth must be greater than zero."
        )

    if concrete_cover < 0:
        raise ValueError(
            "Concrete cover cannot be negative."
        )

    if main_bar_diameter <= 0:
        raise ValueError(
            "Main bar diameter must be greater than zero."
        )

    if slab_span <= 0:
        raise ValueError(
            "Slab span must be greater than zero."
        )

    if finishes_load < 0:
        raise ValueError(
            "Finishes load cannot be negative."
        )

    if ceiling_services_load < 0:
        raise ValueError(
            "Ceiling/services load cannot be negative."
        )

    if partition_load < 0:
        raise ValueError(
            "Partition load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    if concrete_density <= 0:
        raise ValueError(
            "Concrete density must be greater than zero."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    # =====================================================
    # 2. SLAB LOADS
    # =====================================================

    loads = calculate_slab_loads(
        slab_thickness=overall_depth,
        finishes_load=finishes_load,
        ceiling_services_load=ceiling_services_load,
        partition_load=partition_load,
        live_load=live_load,
        concrete_density=concrete_density
    )

    # =====================================================
    # 3. STRUCTURAL ANALYSIS
    # =====================================================

    analysis = analyze_simply_supported_slab(
        design_load=loads[
            "design_load_kN_per_m2"
        ],
        service_load=loads[
            "service_load_kN_per_m2"
        ],
        span=slab_span,
        strip_width=slab_width / 1000
    )

    # =====================================================
    # 4. FLEXURAL DESIGN
    # =====================================================

    design = calculate_slab_design(
        slab_width=slab_width,
        overall_depth=overall_depth,
        concrete_cover=concrete_cover,
        bar_diameter=main_bar_diameter,
        design_load=loads[
            "design_load_kN_per_m2"
        ],
        span=slab_span,
        concrete_strength=concrete_strength,
        steel_strength=steel_strength
    )

    # =====================================================
    # 5. REINFORCEMENT
    # =====================================================

    reinforcement = generate_reinforcement_schedule(
        required_area=design[
            "governing_steel_area_mm2_per_m"
        ],
        preferred_diameter=preferred_bar_diameter,
        distribution_bar_diameter=distribution_bar_diameter
    )

    # =====================================================
    # 6. FINAL RESULT
    # =====================================================

    return {
        # -------------------------------------------------
        # SLAB
        # -------------------------------------------------

        "slab": {
            "width_mm":
                slab_width,

            "overall_depth_mm":
                overall_depth,

            "effective_depth_mm":
                design[
                    "effective_depth_mm"
                ],

            "span_m":
                slab_span
        },

        # -------------------------------------------------
        # MATERIALS
        # -------------------------------------------------

        "materials": {
            "concrete_strength_N_per_mm2":
                concrete_strength,

            "steel_strength_N_per_mm2":
                steel_strength,

            "concrete_density_kN_per_m3":
                concrete_density
        },

        # -------------------------------------------------
        # LOADS
        # -------------------------------------------------

        "loads": loads,

        # -------------------------------------------------
        # STRUCTURAL ANALYSIS
        # -------------------------------------------------

        "analysis": analysis,

        # -------------------------------------------------
        # FLEXURAL DESIGN
        # -------------------------------------------------

        "design": design,

        # -------------------------------------------------
        # REINFORCEMENT
        # -------------------------------------------------

        "reinforcement": reinforcement
    }
