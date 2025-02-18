from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("eml_urban_hydro_model")
except PackageNotFoundError:
    pass
