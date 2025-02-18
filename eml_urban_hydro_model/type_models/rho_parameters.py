from pydantic import BaseModel

from .model_parameters import ModelParameters


class RhoParameters(BaseModel):
    """Container for rho function's parameters."""

    n: float
    model_params: ModelParameters
    beta: float
    s_h: float
    s_w: float
    s_s: float
    s_fc: float
    Ks: float
