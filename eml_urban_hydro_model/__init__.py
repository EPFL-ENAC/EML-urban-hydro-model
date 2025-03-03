from importlib.metadata import version, PackageNotFoundError

from .area_parameters import area_params
from .model import model_st
from .soil_parameters import soil_params
from .type_models.model_input import ModelInput
from .type_models.model_output import ModelOutput
from .type_models.area_parameters import AreaParameters
from .type_models.model_parameters import ModelParameters
from .type_models.soil_parameters import SoilParameters


__all__ = [
    "model_st",
    "area_params",
    "soil_params",
    "AreaParameters",
    "ModelInput",
    "ModelOutput",
    "ModelParameters",
    "SoilParameters",
]


try:
    __version__ = version("eml_urban_hydro_model")
except PackageNotFoundError:
    pass
