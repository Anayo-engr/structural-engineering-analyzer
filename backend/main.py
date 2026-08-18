from fastapi import FastAPI
from calculations.beams.beam_calculator import calculate_beam

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
    beam_width: float,
    overall_depth: float,
    concrete_cover: float,
    main_bar_diameter: float,
    dead_load: float,
    live_load: float,
    span: float,
    concrete_strength: float = 25,
    steel_strength: float = 500,
    link_diameter: float = 8
):
    """
    Calculate preliminary reinforced-concrete beam design.
    """

    result = calculate_beam(
        beam_width=beam_width,
        overall_depth=overall_depth,
        concrete_cover=concrete_cover,
        main_bar_diameter=main_bar_diameter,
        dead_load=dead_load,
        live_load=live_load,
        span=span,
        concrete_strength=concrete_strength,
        steel_strength=steel_strength,
        link_diameter=link_diameter
    )

    return result
