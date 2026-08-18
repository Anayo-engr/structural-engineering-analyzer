from pydantic import BaseModel, Field


class BeamCalculationRequest(BaseModel):
    """Input model for preliminary beam calculations."""

    beam_width: float = Field(gt=0)
    overall_depth: float = Field(gt=0)
    concrete_cover: float = Field(gt=0)
    main_bar_diameter: float = Field(gt=0)
    dead_load: float = Field(ge=0)
    live_load: float = Field(ge=0)
    span: float = Field(gt=0)
    concrete_strength: float = Field(default=25, gt=0)
    steel_strength: float = Field(default=500, gt=0)
    link_diameter: float = Field(default=8, gt=0)


class ColumnCalculationRequest(BaseModel):
    """Input model for preliminary column calculations."""

    column_width: float = Field(gt=0)
    column_depth: float = Field(gt=0)
    dead_load: float = Field(ge=0)
    live_load: float = Field(ge=0)
    concrete_strength: float = Field(default=25, gt=0)
    steel_strength: float = Field(default=500, gt=0)
    preferred_bar_diameter: float = Field(default=16, gt=0)
