from pydantic import BaseModel, Field


class PreprocessingParameters(BaseModel):
    """Container for preprocess function parameters."""

    ic: float = Field(0.2, description="Critical intensity threshold (mm).")
    T: int = Field(50, description="Memory duration (minutes).")
    resolution: int = Field(5, description="Time resolution of the rainfall data (minutes).")
