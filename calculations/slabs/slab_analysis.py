"""
Structural Engineering Analyzer
Slab Analysis Module

Preliminary structural analysis of reinforced-concrete slabs.

Design basis:
- Simply supported slab
- One-way slab behaviour
- Uniformly distributed area load
- Load converted to a one-metre-wide design strip

Units:
    Loads: kN/m²
    Span: m
    Line load on design strip: kN/m
    Shear: kN/m
    Moment: kNm/m
"""

# =========================================================
# DESIGN STRIP LOAD
# =========================================================

def calculate_design_strip_load(
    area_load,
    strip_width=1.0
):
    """
    Convert an area load into a line load for a
    one-metre-wide slab design strip.

    Formula:

        w = q × b

    Parameters:
        area_load (float):
            Slab area load in kN/m².

        strip_width (float):
            Design strip width in metres.

    Returns:
        float:
            Line load in kN/m.
    """

    if area_load < 0:
        raise ValueError(
            "Area load cannot be negative."
        )

    if strip_width <= 0:
        raise ValueError(
            "Strip width must be greater than zero."
        )

    return area_load * strip_width


# =========================================================
# SUPPORT REACTION
# =========================================================

def calculate_support_reaction(
    design_strip_load,
    span
):
    """
    Calculate the support reaction for a simply supported
    slab strip under a full-span UDL.

    Formula:

        R = wL / 2

    Returns:
        float:
            Support reaction in kN/m.
    """

    if design_strip_load < 0:
        raise ValueError(
            "Design strip load cannot be negative."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    return (
        design_strip_load * span
    ) / 2


# =========================================================
# MAXIMUM SHEAR
# =========================================================

def calculate_maximum_shear(
    design_strip_load,
    span
):
    """
    Calculate maximum shear at the support.

    Formula:

        VEd = wL / 2

    Returns:
        float:
            Maximum shear in kN/m.
    """

    if design_strip_load < 0:
        raise ValueError(
            "Design strip load cannot be negative."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    return (
        design_strip_load * span
    ) / 2


# =========================================================
# MAXIMUM BENDING MOMENT
# =========================================================

def calculate_maximum_bending_moment(
    design_strip_load,
    span
):
    """
    Calculate maximum sagging bending moment.

    For a simply supported slab strip under a full-span UDL:

        MEd = wL² / 8

    Returns:
        float:
            Maximum bending moment in kNm/m.
    """

    if design_strip_load < 0:
        raise ValueError(
            "Design strip load cannot be negative."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    return (
        design_strip_load * span ** 2
    ) / 8


# =========================================================
# SERVICE BENDING MOMENT
# =========================================================

def calculate_service_bending_moment(
    service_strip_load,
    span
):
    """
    Calculate the service-level bending moment.

    Formula:

        Mser = wL² / 8

    Returns:
        float:
            Service bending moment in kNm/m.
    """

    if service_strip_load < 0:
        raise ValueError(
            "Service strip load cannot be negative."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    return (
        service_strip_load * span ** 2
    ) / 8


# =========================================================
# COMPLETE SLAB ANALYSIS
# =========================================================

def analyze_simply_supported_slab(
    design_load,
    service_load,
    span,
    strip_width=1.0
):
    """
    Perform a preliminary structural analysis of a
    simply supported one-way slab.

    The analysis is performed on the specified design strip.

    Returns:
        dict:
            Complete preliminary slab analysis results.
    """

    if design_load < 0:
        raise ValueError(
            "Design load cannot be negative."
        )

    if service_load < 0:
        raise ValueError(
            "Service load cannot be negative."
        )

    if span <= 0:
        raise ValueError(
            "Span must be greater than zero."
        )

    if strip_width <= 0:
        raise ValueError(
            "Strip width must be greater than zero."
        )

    design_strip_load = calculate_design_strip_load(
        design_load,
        strip_width
    )

    service_strip_load = calculate_design_strip_load(
        service_load,
        strip_width
    )

    left_reaction = calculate_support_reaction(
        design_strip_load,
        span
    )

    right_reaction = left_reaction

    maximum_shear = calculate_maximum_shear(
        design_strip_load,
        span
    )

    maximum_moment = calculate_maximum_bending_moment(
        design_strip_load,
        span
    )

    service_moment = calculate_service_bending_moment(
        service_strip_load,
        span
    )

    return {
        "span_m":
            span,

        "strip_width_m":
            strip_width,

        "design_load_kN_per_m2":
            design_load,

        "service_load_kN_per_m2":
            service_load,

        "design_strip_load_kN_per_m":
            design_strip_load,

        "service_strip_load_kN_per_m":
            service_strip_load,

        "left_reaction_kN_per_m":
            left_reaction,

        "right_reaction_kN_per_m":
            right_reaction,

        "maximum_shear_kN_per_m":
            maximum_shear,

        "maximum_bending_moment_kNm_per_m":
            maximum_moment,

        "service_bending_moment_kNm_per_m":
            service_moment
    }
