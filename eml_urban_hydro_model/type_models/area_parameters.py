from pydantic import BaseModel, Field


class AreaParameters(BaseModel):
    """Container for area parameters."""

    omegaSoil: float = Field(..., description="Catchment area for soil infiltration (m²).")
    omegaRoad: float = Field(..., description="Catchment area for road runoff (m²).")
    omegaRoof: float = Field(..., description="Catchment area for roof runoff (m²).")
