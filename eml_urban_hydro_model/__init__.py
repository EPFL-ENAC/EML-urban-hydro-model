from importlib.metadata import version, PackageNotFoundError

from .area_parameters import area_params
from .model import model_st
from .preprocessing import preprocess
from .soil_parameters import soil_params
from .type_models.model_input import ModelInput
from .type_models.model_output import ModelOutput
from .type_models.area_parameters import AreaParameters
from .type_models.preprocessing_parameters import PreprocessingParameters
from .type_models.model_parameters import ModelParameters
from .type_models.soil_parameters import SoilParameters


__all__ = [
    "area_params",
    "preprocess",
    "model_st",
    "soil_params",
    "AreaParameters",
    "PreprocessingParameters",
    "ModelInput",
    "ModelOutput",
    "ModelParameters",
    "SoilParameters",
]


try:
    __version__ = version("eml_urban_hydro_model")
except PackageNotFoundError:
    pass
