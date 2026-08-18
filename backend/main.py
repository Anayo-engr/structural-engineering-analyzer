from fastapi import FastAPI

from calculations.beams.beam_calculator import calculate_beam
from calculations.columns.column_calculator import calculate_column

from backend.schemas import (
    BeamCalculationRequest,
    ColumnCalculationRequest
)


app = FastAPI(
    title="Structural Engineering Analyzer API",
    description="API for preliminary structural engineering calculations.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Structural Engineering Analyzer API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/calculate/beam")
def calculate_beam_endpoint(
    request: BeamCalculationRequest
):
    """
    Calculate preliminary reinforced-concrete beam design.
    """

    result = calculate_beam(
        beam_width=request.beam_width,
        overall_depth=request.overall_depth,
        concrete_cover=request.concrete_cover,
        main_bar_diameter=request.main_bar_diameter,
        dead_load=request.dead_load,
        live_load=request.live_load,
        span=request.span,
        concrete_strength=request.concrete_strength,
        steel_strength=request.steel_strength,
        link_diameter=request.link_diameter
    )

    return result


@app.post("/calculate/column")
def calculate_column_endpoint(
    request: ColumnCalculationRequest
):
    """
    Calculate preliminary reinforced-concrete column design.
    """

    result = calculate_column(
        column_width=request.column_width,
        column_depth=request.column_depth,
        dead_load=request.dead_load,
        live_load=request.live_load,
        concrete_strength=request.concrete_strength,
        steel_strength=request.steel_strength,
        preferred_bar_diameter=request.preferred_bar_diameter
    )

    return result
