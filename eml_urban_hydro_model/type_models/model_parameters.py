from pydantic import BaseModel, Field

from .area_parameters import AreaParameters
from .soil_parameters import SoilParameters
from ..vegetation_parameters import VegetationParameters
from ..soil_parameters import soil_params


class ModelParameters(BaseModel):
    """Container for model's parameters."""

    k: float = Field(84, description="Runoff coefficient for roads and roofs.")
    frac_rt2s: float = Field(0.5, description="Fraction of roof runoff directed to soil.")
    frac_rt2tk: float = Field(0.5, description="Fraction of roof runoff directed to tank.")
    vegetation_params: VegetationParameters = Field(
        VegetationParameters(Z_root=140), description="Vegetation parameters."
    )
    E_max: float = Field(0.5, description="Maximum evapotranspiration rate (mm/day).")
    E_w: float = Field(0.0625, description="Minimum evapotranspiration rate (mm/day).")
    heavy: float = Field(55 / 600000, description="Threshold for intense rainfall (m/s).")
    soil_params: SoilParameters = Field(
        soil_params["loamy sand"], description='Soil parameters. Defaults to "loamy sand" parameters.'
    )
    area_params: AreaParameters = Field(..., description="Catchment areas.")
    Vmax: float = Field(10, description="Maximum tank capacity (m³).")
    lag: int = Field(0, description="Time lag for precipitation effect.")
    resolution: int = Field(5, description="Time step resolution (minutes).")
    Qirr: float | None = Field(
        None, description="Irrigation flow rate (m³/s). Defaults to omegaSoil*E_max/(100*86400)."
    )
    flushing_frequency: float = Field(2, description="Tank flushing frequency (per hour).")
