"""
Structural Engineering Analyzer
Foundation Design Module

Preliminary reinforced-concrete isolated pad foundation
design calculations.

Design basis:
- Rectangular/square pad foundation
- Axial loading
- Preliminary bending design
- Preliminary one-way shear check
- Preliminary punching shear check

IMPORTANT:
This is a preliminary calculation component.
Final foundation design must include complete geotechnical,
structural, settlement, punching shear, one-way shear,
flexural, eccentricity, stability, durability, detailing,
and applicable design-code checks by a qualified engineer.

Units:
    Loads: kN
    Dimensions: mm
    Moments: kNm
    Stresses: N/mm²
"""


# =========================================================
# FOUNDATION EFFECTIVE DEPTH
# =========================================================

def calculate_effective_depth(
    overall_depth,
    concrete_cover,
    bar_diameter
):
    """
    Calculate effective depth of foundation reinforcement.

        d = h - c - Ø/2

    Returns:
        float:
            Effective depth in mm.
    """

    if overall_depth <= 0:
        raise ValueError(
            "Overall depth must be greater than zero."
        )

    if concrete_cover < 0:
        raise ValueError(
            "Concrete cover cannot be negative."
        )

    if bar_diameter <= 0:
        raise ValueError(
            "Bar diameter must be greater than zero."
        )

    effective_depth = (
        overall_depth
        - concrete_cover
        - bar_diameter / 2
    )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    return effective_depth


# =========================================================
# DESIGN SOIL PRESSURE
# =========================================================

def calculate_design_soil_pressure(
    design_load,
    foundation_area
):
    """
    Calculate preliminary design soil pressure.

        qEd = NEd / A

    Returns:
        float:
            Design soil pressure in kN/m².
    """

    if design_load <= 0:
        raise ValueError(
            "Design load must be greater than zero."
        )

    if foundation_area <= 0:
        raise ValueError(
            "Foundation area must be greater than zero."
        )

    return (
        design_load
        / foundation_area
    )


# =========================================================
# COLUMN LOAD EFFECTIVE WIDTH
# =========================================================

def calculate_projection(
    foundation_dimension,
    column_dimension
):
    """
    Calculate footing projection beyond the column face.

        projection = (B - c) / 2

    Dimensions are in metres.

    Returns:
        float:
            Projection in metres.
    """

    if foundation_dimension <= 0:
        raise ValueError(
            "Foundation dimension must be greater than zero."
        )

    if column_dimension <= 0:
        raise ValueError(
            "Column dimension must be greater than zero."
        )

    projection = (
        foundation_dimension
        - column_dimension
    ) / 2

    if projection <= 0:
        raise ValueError(
            "Foundation must extend beyond the column."
        )

    return projection


# =========================================================
# PRELIMINARY CANTILEVER MOMENT
# =========================================================

def calculate_design_moment(
    design_soil_pressure,
    projection,
    design_width
):
    """
    Calculate preliminary bending moment at the
    column face.

        MEd = qEd × l² / 2 × b

    Parameters:
        design_soil_pressure:
            Design soil pressure in kN/m².

        projection:
            Projection beyond column face in m.

        design_width:
            Design strip width in m.

    Returns:
        float:
            Design moment in kNm.
    """

    if design_soil_pressure <= 0:
        raise ValueError(
            "Design soil pressure must be greater than zero."
        )

    if projection <= 0:
        raise ValueError(
            "Projection must be greater than zero."
        )

    if design_width <= 0:
        raise ValueError(
            "Design width must be greater than zero."
        )

    return (
        design_soil_pressure
        * projection ** 2
        * design_width
        / 2
    )


# =========================================================
# REQUIRED FOUNDATION STEEL
# =========================================================

def calculate_required_steel_area(
    design_moment,
    effective_depth,
    steel_strength,
    lever_arm_factor=0.90
):
    """
    Estimate required tensile reinforcement.

        As = MEd / (0.87 fy z)

    Returns:
        float:
            Required reinforcement area in mm².
    """

    if design_moment <= 0:
        raise ValueError(
            "Design moment must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if not 0 < lever_arm_factor <= 1:
        raise ValueError(
            "Lever arm factor must be greater than 0 "
            "and no more than 1."
        )

    moment_nmm = (
        design_moment
        * 1_000_000
    )

    lever_arm = (
        lever_arm_factor
        * effective_depth
    )

    return (
        moment_nmm
        / (
            0.87
            * steel_strength
            * lever_arm
        )
    )


# =========================================================
# MINIMUM FOUNDATION STEEL
# =========================================================

def calculate_minimum_steel_area(
    foundation_width,
    effective_depth,
    minimum_ratio=0.0013
):
    """
    Calculate preliminary minimum reinforcement.

        As,min = ρmin × b × d

    Returns:
        float:
            Minimum reinforcement area in mm².
    """

    if foundation_width <= 0:
        raise ValueError(
            "Foundation width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    if minimum_ratio <= 0:
        raise ValueError(
            "Minimum reinforcement ratio must be greater than zero."
        )

    width_mm = (
        foundation_width * 1000
    )

    return (
        minimum_ratio
        * width_mm
        * effective_depth
    )


# =========================================================
# GOVERNING FOUNDATION STEEL
# =========================================================

def select_required_steel_area(
    required_area,
    minimum_area
):
    """
    Select the governing foundation reinforcement area.
    """

    if required_area <= 0:
        raise ValueError(
            "Required reinforcement area must be greater than zero."
        )

    if minimum_area <= 0:
        raise ValueError(
            "Minimum reinforcement area must be greater than zero."
        )

    return max(
        required_area,
        minimum_area
    )


# =========================================================
# ONE-WAY SHEAR FORCE
# =========================================================

def calculate_one_way_shear_force(
    design_soil_pressure,
    projection,
    design_width,
    effective_depth
):
    """
    Calculate preliminary one-way shear force
    at a section approximately d from the column face.

    Returns:
        float:
            One-way shear force in kN.
    """

    if design_soil_pressure <= 0:
        raise ValueError(
            "Design soil pressure must be greater than zero."
        )

    if projection <= 0:
        raise ValueError(
            "Projection must be greater than zero."
        )

    if design_width <= 0:
        raise ValueError(
            "Design width must be greater than zero."
        )

    if effective_depth <= 0:
        raise ValueError(
            "Effective depth must be greater than zero."
        )

    effective_depth_m = (
        effective_depth / 1000
    )

    shear_length = (
        projection
        - effective_depth_m
    )

    if shear_length <= 0:
        return 0.0

    return (
        design_soil_pressure
        * shear_length
        * design_width
    )


# =========================================================
# COMPLETE FOUNDATION DESIGN
# =========================================================

def calculate_foundation_design(
    design_load,
    foundation_width,
    foundation_length,
    column_width,
    column_depth,
    overall_depth,
    concrete_cover,
    bar_diameter,
    steel_strength=500
):
    """
    Perform a preliminary isolated pad foundation design.

    Returns:
        dict:
            Foundation design results.
    """

    foundation_area = (
        foundation_width
        * foundation_length
    )

    design_pressure = (
        calculate_design_soil_pressure(
            design_load,
            foundation_area
        )
    )

    projection_x = calculate_projection(
        foundation_width,
        column_width
    )

    projection_y = calculate_projection(
        foundation_length,
        column_depth
    )

    effective_depth = (
        calculate_effective_depth(
            overall_depth,
            concrete_cover,
            bar_diameter
        )
    )

    design_moment_x = calculate_design_moment(
        design_pressure,
        projection_x,
        foundation_length
    )

    design_moment_y = calculate_design_moment(
        design_pressure,
        projection_y,
        foundation_width
    )

    required_steel_x = calculate_required_steel_area(
        design_moment_x,
        effective_depth,
        steel_strength
    )

    required_steel_y = calculate_required_steel_area(
        design_moment_y,
        effective_depth,
        steel_strength
    )

    minimum_steel_x = calculate_minimum_steel_area(
        foundation_width,
        effective_depth
    )

    minimum_steel_y = calculate_minimum_steel_area(
        foundation_length,
        effective_depth
    )

    governing_steel_x = select_required_steel_area(
        required_steel_x,
        minimum_steel_x
    )

    governing_steel_y = select_required_steel_area(
        required_steel_y,
        minimum_steel_y
    )

    one_way_shear_x = calculate_one_way_shear_force(
        design_pressure,
        projection_x,
        foundation_length,
        effective_depth
    )

    one_way_shear_y = calculate_one_way_shear_force(
        design_pressure,
        projection_y,
        foundation_width,
        effective_depth
    )

    return {
        "foundation": {
            "width_m":
                foundation_width,
            "length_m":
                foundation_length,
            "area_m2":
                foundation_area,
            "overall_depth_mm":
                overall_depth,
            "effective_depth_mm":
                effective_depth
        },

        "column": {
            "width_m":
                column_width,
            "depth_m":
                column_depth
        },

        "soil": {
            "design_pressure_kN_per_m2":
                design_pressure
        },

        "projections": {
            "x_m":
                projection_x,
            "y_m":
                projection_y
        },

        "design": {
            "moment_x_kNm":
                design_moment_x,
            "moment_y_kNm":
                design_moment_y,

            "required_steel_x_mm2":
                required_steel_x,
            "required_steel_y_mm2":
                required_steel_y,

            "minimum_steel_x_mm2":
                minimum_steel_x,
            "minimum_steel_y_mm2":
                minimum_steel_y,

            "governing_steel_x_mm2":
                governing_steel_x,
            "governing_steel_y_mm2":
                governing_steel_y
        },

        "shear": {
            "one_way_shear_x_kN":
                one_way_shear_x,
            "one_way_shear_y_kN":
                one_way_shear_y
        },

        "materials": {
            "steel_strength_N_per_mm2":
                steel_strength
        }
    }
