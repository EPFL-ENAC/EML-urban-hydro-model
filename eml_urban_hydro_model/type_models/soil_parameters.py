from pydantic import BaseModel


class SoilParameters(BaseModel):
    """Container for soil parameters."""

    Ks: float
    n: float
    beta: float
    sh: float
    sw: float
    ss: float
    sfc: float
