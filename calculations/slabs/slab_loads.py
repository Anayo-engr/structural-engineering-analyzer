"""
Structural Engineering Analyzer
Slab Load Calculation Module

Preliminary reinforced-concrete slab load calculations.

This module calculates:
- Self-weight of slab
- Finishes load
- Ceiling/services load
- Partition allowance
- Live load
- Total service load
- Ultimate/design load

Units:
    Dimensions: mm
    Loads: kN/m²
"""

# =========================================================
# SLAB SELF-WEIGHT
# =========================================================

def calculate_slab_self_weight(
    slab_thickness,
    concrete_density=25
):
    """
    Calculate the self-weight of a reinforced-concrete slab.

    Formula:

        Self-weight = thickness × density

    Parameters:
        slab_thickness (float):
            Slab thickness in mm.

        concrete_density (float):
            Concrete density in kN/m³.

    Returns:
        float:
            Slab self-weight in kN/m².
    """

    if slab_thickness <= 0:
        raise ValueError(
            "Slab thickness must be greater than zero."
        )

    if concrete_density <= 0:
        raise ValueError(
            "Concrete density must be greater than zero."
        )

    thickness_m = slab_thickness / 1000

    self_weight = (
        thickness_m
        * concrete_density
    )

    return self_weight


# =========================================================
# TOTAL PERMANENT LOAD
# =========================================================

def calculate_total_permanent_load(
    slab_self_weight,
    finishes_load=1.0,
    ceiling_services_load=0.25,
    partition_load=0.0
):
    """
    Calculate the total permanent load on the slab.

    Formula:

        Gk =
        self-weight
        + finishes
        + ceiling/services
        + partitions

    Units:
        Loads: kN/m²

    Returns:
        float:
            Total permanent load in kN/m².
    """

    if slab_self_weight < 0:
        raise ValueError(
            "Slab self-weight cannot be negative."
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

    return (
        slab_self_weight
        + finishes_load
        + ceiling_services_load
        + partition_load
    )


# =========================================================
# SERVICE LOAD
# =========================================================

def calculate_total_service_load(
    permanent_load,
    live_load
):
    """
    Calculate the total service load.

    Formula:

        Gk + Qk

    Units:
        Loads: kN/m²

    Returns:
        float:
            Total service load in kN/m².
    """

    if permanent_load < 0:
        raise ValueError(
            "Permanent load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    return permanent_load + live_load


# =========================================================
# ULTIMATE / DESIGN LOAD
# =========================================================

def calculate_design_load(
    permanent_load,
    live_load,
    permanent_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Calculate the preliminary ultimate/design load.

    Formula:

        wEd = γG Gk + γQ Qk

    Default factors:

        γG = 1.35
        γQ = 1.50

    Units:
        Loads: kN/m²

    Returns:
        float:
            Ultimate/design load in kN/m².
    """

    if permanent_load < 0:
        raise ValueError(
            "Permanent load cannot be negative."
        )

    if live_load < 0:
        raise ValueError(
            "Live load cannot be negative."
        )

    if permanent_load_factor <= 0:
        raise ValueError(
            "Permanent load factor must be greater than zero."
        )

    if live_load_factor <= 0:
        raise ValueError(
            "Live load factor must be greater than zero."
        )

    design_load = (
        permanent_load * permanent_load_factor
        + live_load * live_load_factor
    )

    return design_load


# =========================================================
# COMPLETE SLAB LOAD CALCULATION
# =========================================================

def calculate_slab_loads(
    slab_thickness,
    finishes_load=1.0,
    ceiling_services_load=0.25,
    partition_load=0.0,
    live_load=2.0,
    concrete_density=25,
    permanent_load_factor=1.35,
    live_load_factor=1.50
):
    """
    Perform a complete preliminary slab load calculation.

    Returns:
        dict:
            Complete slab load results.
    """

    slab_self_weight = calculate_slab_self_weight(
        slab_thickness,
        concrete_density
    )

    permanent_load = calculate_total_permanent_load(
        slab_self_weight,
        finishes_load,
        ceiling_services_load,
        partition_load
    )

    service_load = calculate_total_service_load(
        permanent_load,
        live_load
    )

    design_load = calculate_design_load(
        permanent_load,
        live_load,
        permanent_load_factor,
        live_load_factor
    )

    return {
        "slab_thickness_mm":
            slab_thickness,

        "slab_self_weight_kN_per_m2":
            slab_self_weight,

        "finishes_load_kN_per_m2":
            finishes_load,

        "ceiling_services_load_kN_per_m2":
            ceiling_services_load,

        "partition_load_kN_per_m2":
            partition_load,

        "permanent_load_kN_per_m2":
            permanent_load,

        "live_load_kN_per_m2":
            live_load,

        "service_load_kN_per_m2":
            service_load,

        "design_load_kN_per_m2":
            design_load
    }
