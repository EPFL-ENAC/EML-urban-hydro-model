from pydantic import BaseModel, Field

from .soil_parameters import SoilParameters
from ..soil_parameters import soil_params


class ModelParameters(BaseModel):
    """Container for model's parameters."""

    k: float | None = Field(90, description="Runoff coefficient for roads and roofs.")
    frac_rt2s: float | None = Field(0.5, description="Fraction of roof runoff directed to soil.")
    frac_rt2tk: float | None = Field(0.5, description="Fraction of roof runoff directed to tank.")
    Z_root: float | None = Field(140, description="Root zone depth (mm).")
    E_max: float | None = Field(0.5, description="Maximum evapotranspiration rate (mm/day).")
    E_w: float | None = Field(0.0625, description="Minimum evapotranspiration rate (mm/day).")
    heavy: float | None = Field(55 / 600000, description="Threshold for intense rainfall (m/s).")
    soil_params: SoilParameters | None = Field(
        soil_params["loamy sand"], description='Soil parameters. Defaults to "loamy sand" parameters.'
    )
    omegaSoil: float = Field(..., description="Catchment area for soil infiltration.")
    omegaRoad: float = Field(..., description="Catchment area for road runoff.")
    omegaRoof: float = Field(..., description="Catchment area for roof runoff.")
    Vmax: float | None = Field(10, description="Maximum tank capacity (m³).")
    lag: int | None = Field(0, description="Time lag for precipitation effect.")
    resolution: int | None = Field(5, description="Time step resolution (minutes).")
    Qirr: float | None = Field(
        None, description="Irrigation flow rate (m³/s). Defaults to omegaSoil*E_max/(100*86400)."
    )
    flushing_frequency: float | None = Field(2, description="Tank flushing frequency (per hour).")
