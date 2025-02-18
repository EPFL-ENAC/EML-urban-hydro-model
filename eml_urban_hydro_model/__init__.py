from importlib.metadata import version, PackageNotFoundError

from .model import model_st
from .soil_parameters import soil_params
from .type_models.model_input import ModelInput
from .type_models.model_output import ModelOutput
from .type_models.model_parameters import ModelParameters
from .type_models.soil_parameters import SoilParameters


__all__ = [
    "model_st",
    "soil_params",
    "ModelInput",
    "ModelOutput",
    "ModelParameters",
    "SoilParameters",
]


try:
    __version__ = version("eml_urban_hydro_model")
except PackageNotFoundError:
    pass
