"""
Structural Engineering Analyzer
Column Design Module

Preliminary reinforced-concrete column design calculations.

Design basis:
- Eurocode-oriented approach
- Rectangular reinforced-concrete column
- Predominantly axial compression
- Preliminary reinforcement sizing

IMPORTANT:
This module is a preliminary calculation component.
Final column design must consider eccentricity, minimum moments,
slenderness, second-order effects, interaction diagrams,
buckling, concrete stress limits, detailing requirements,
load combinations, and all applicable design-code provisions.
"""


def calculate_gross_area(width, depth):
    """
    Calculate the gross cross-sectional area of a rectangular column.

    Formula:

        Ac = b × h

    Parameters:
        width (float): Column width in mm
        depth (float): Column depth in mm

    Returns:
        float: Gross concrete area in mm²
    """

    if width <= 0:
        raise ValueError(
            "Column width must be greater than zero."
        )

    if depth <= 0:
        raise ValueError(
            "Column depth must be greater than zero."
        )

    return width * depth


def calculate_minimum_longitudinal_steel(
    gross_area,
    minimum_ratio=0.002
):
    """
    Calculate preliminary minimum longitudinal reinforcement.

    Formula:

        As,min = rho_min × Ac

    The default ratio is 0.2% for this preliminary calculation.

    Parameters:
        gross_area (float): Gross column area in mm²
        minimum_ratio (float): Minimum reinforcement ratio

    Returns:
        float: Minimum longitudinal steel area in mm²
    """

    if gross_area <= 0:
        raise ValueError(
            "Gross area must be greater than zero."
        )

    if minimum_ratio <= 0:
        raise ValueError(
            "Minimum reinforcement ratio must be greater than zero."
        )

    return minimum_ratio * gross_area


def calculate_maximum_longitudinal_steel(
    gross_area,
    maximum_ratio=0.04
):
    """
    Calculate preliminary maximum longitudinal reinforcement.

    Formula:

        As,max = rho_max × Ac

    The default ratio is 4% for this preliminary calculation.

    Parameters:
        gross_area (float): Gross column area in mm²
        maximum_ratio (float): Maximum reinforcement ratio

    Returns:
        float: Maximum longitudinal steel area in mm²
    """

    if gross_area <= 0:
        raise ValueError(
            "Gross area must be greater than zero."
        )

    if maximum_ratio <= 0:
        raise ValueError(
            "Maximum reinforcement ratio must be greater than zero."
        )

    return maximum_ratio * gross_area


def calculate_required_steel_area(
    design_axial_load,
    concrete_strength,
    steel_strength=500,
    concrete_capacity_factor=0.35,
    steel_contribution_factor=0.87
):
    """
    Estimate the required longitudinal reinforcement area
    for a preliminary axially loaded column.

    Simplified relationship:

        NEd = 0.35 fck Ac + 0.87 fy As

    Therefore:

        As = (NEd - 0.35 fck Ac) / (0.87 fy)

    This expression is intended only as a preliminary sizing
    calculation and does not replace a complete column design.

    Parameters:
        design_axial_load (float):
            Design axial load in kN.

        concrete_strength (float):
            Concrete characteristic strength fck in N/mm².

        steel_strength (float):
            Steel yield strength fy in N/mm².

        concrete_capacity_factor (float):
            Simplified concrete contribution factor.

        steel_contribution_factor (float):
            Steel design strength factor.

    Returns:
        float:
            Required steel area in mm².
    """

    if design_axial_load <= 0:
        raise ValueError(
            "Design axial load must be greater than zero."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if concrete_capacity_factor <= 0:
        raise ValueError(
            "Concrete capacity factor must be greater than zero."
        )

    if steel_contribution_factor <= 0:
        raise ValueError(
            "Steel contribution factor must be greater than zero."
        )

    # Convert design load from kN to N.
    design_load_n = design_axial_load * 1000

    # The required area cannot be calculated without the
    # gross concrete area. This function therefore returns
    # the required steel based on the supplied concrete area
    # through the separate complete design function.
    raise ValueError(
        "Gross concrete area is required. "
        "Use calculate_column_steel_area()."
    )


def calculate_column_steel_area(
    design_axial_load,
    gross_area,
    concrete_strength,
    steel_strength=500,
    concrete_capacity_factor=0.35,
    steel_contribution_factor=0.87
):
    """
    Calculate preliminary longitudinal steel area.

    Formula:

        NEd = alpha_c × fck × Ac + alpha_s × fy × As

        As =
        (NEd - alpha_c × fck × Ac)
        / (alpha_s × fy)

    If the concrete contribution is already sufficient,
    the result is returned as zero before minimum reinforcement
    is applied.

    Parameters:
        design_axial_load (float): Design axial load in kN
        gross_area (float): Gross concrete area in mm²
        concrete_strength (float): fck in N/mm²
        steel_strength (float): fy in N/mm²
        concrete_capacity_factor (float): Concrete contribution factor
        steel_contribution_factor (float): Steel contribution factor

    Returns:
        float: Preliminary required steel area in mm².
    """

    if design_axial_load <= 0:
        raise ValueError(
            "Design axial load must be greater than zero."
        )

    if gross_area <= 0:
        raise ValueError(
            "Gross area must be greater than zero."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if concrete_capacity_factor <= 0:
        raise ValueError(
            "Concrete capacity factor must be greater than zero."
        )

    if steel_contribution_factor <= 0:
        raise ValueError(
            "Steel contribution factor must be greater than zero."
        )

    design_load_n = design_axial_load * 1000

    concrete_capacity = (
        concrete_capacity_factor
        * concrete_strength
        * gross_area
    )

    remaining_load = design_load_n - concrete_capacity

    if remaining_load <= 0:
        return 0.0

    steel_area = (
        remaining_load
        / (
            steel_contribution_factor
            * steel_strength
        )
    )

    return steel_area


def select_governing_steel_area(
    required_steel,
    minimum_steel,
    maximum_steel
):
    """
    Select the governing longitudinal reinforcement area.

    The selected area must be:
        - At least the required area
        - At least the minimum area
        - Not greater than the maximum permitted area

    Returns:
        float: Governing steel area in mm².
    """

    if required_steel < 0:
        raise ValueError(
            "Required steel area cannot be negative."
        )

    if minimum_steel <= 0:
        raise ValueError(
            "Minimum steel area must be greater than zero."
        )

    if maximum_steel <= 0:
        raise ValueError(
            "Maximum steel area must be greater than zero."
        )

    governing_area = max(
        required_steel,
        minimum_steel
    )

    if governing_area > maximum_steel:
        raise ValueError(
            "Required reinforcement exceeds the "
            "preliminary maximum reinforcement limit."
        )

    return governing_area


def calculate_column_design(
    width,
    depth,
    design_axial_load,
    concrete_strength=25,
    steel_strength=500,
    minimum_ratio=0.002,
    maximum_ratio=0.04
):
    """
    Perform a preliminary reinforced-concrete column design.

    Returns:
        dict: Complete preliminary column design results.
    """

    gross_area = calculate_gross_area(
        width,
        depth
    )

    minimum_steel = calculate_minimum_longitudinal_steel(
        gross_area,
        minimum_ratio
    )

    maximum_steel = calculate_maximum_longitudinal_steel(
        gross_area,
        maximum_ratio
    )

    required_steel = calculate_column_steel_area(
        design_axial_load,
        gross_area,
        concrete_strength,
        steel_strength
    )

    governing_steel = select_governing_steel_area(
        required_steel,
        minimum_steel,
        maximum_steel
    )

    reinforcement_ratio = (
        governing_steel / gross_area
    )

    return {
        "width_mm": width,
        "depth_mm": depth,
        "gross_area_mm2": gross_area,
        "concrete_strength_N_per_mm2":
            concrete_strength,
        "steel_strength_N_per_mm2":
            steel_strength,
        "design_axial_load_kN":
            design_axial_load,
        "required_steel_area_mm2":
            required_steel,
        "minimum_steel_area_mm2":
            minimum_steel,
        "maximum_steel_area_mm2":
            maximum_steel,
        "governing_steel_area_mm2":
            governing_steel,
        "reinforcement_ratio":
            reinforcement_ratio
    }

def calculate_design_capacity(
    gross_area,
    steel_area,
    concrete_strength,
    steel_strength=500,
    concrete_capacity_factor=0.35,
    steel_contribution_factor=0.87
):
    """
    Calculate the preliminary design axial capacity of a
    reinforced-concrete column.

    Formula:

        NEd,Rd = alpha_c × fck × Ac
               + alpha_s × fy × As

    Parameters:
        gross_area (float): Gross concrete area in mm².
        steel_area (float): Longitudinal steel area in mm².
        concrete_strength (float): Concrete strength fck in N/mm².
        steel_strength (float): Steel strength fy in N/mm².
        concrete_capacity_factor (float): Concrete contribution factor.
        steel_contribution_factor (float): Steel contribution factor.

    Returns:
        float: Preliminary design capacity in kN.
    """

    if gross_area <= 0:
        raise ValueError(
            "Gross area must be greater than zero."
        )

    if steel_area < 0:
        raise ValueError(
            "Steel area cannot be negative."
        )

    if concrete_strength <= 0:
        raise ValueError(
            "Concrete strength must be greater than zero."
        )

    if steel_strength <= 0:
        raise ValueError(
            "Steel strength must be greater than zero."
        )

    if concrete_capacity_factor <= 0:
        raise ValueError(
            "Concrete capacity factor must be greater than zero."
        )

    if steel_contribution_factor <= 0:
        raise ValueError(
            "Steel contribution factor must be greater than zero."
        )

    concrete_capacity = (
        concrete_capacity_factor
        * concrete_strength
        * gross_area
    )

    steel_capacity = (
        steel_contribution_factor
        * steel_strength
        * steel_area
    )

    total_capacity_n = (
        concrete_capacity
        + steel_capacity
    )

    # Convert N to kN.
    return total_capacity_n / 1000
