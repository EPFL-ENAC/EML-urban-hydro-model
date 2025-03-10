from pydantic import BaseModel, Field


class VegetationParameters(BaseModel):
    """Container for vegetation parameters."""

    Z_root: float = Field(..., description="Root zone depth (mm).")
