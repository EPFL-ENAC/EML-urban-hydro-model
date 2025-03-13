from .type_models.vegetation_parameters import VegetationParameters


vegetation_params: dict[str, VegetationParameters] = {
    "none": VegetationParameters(Z_root=0),
    "grass": VegetationParameters(Z_root=50),
    "shrubs": VegetationParameters(Z_root=75),
    "shallow_rooted_trees": VegetationParameters(Z_root=150),
    "deep_rooted_trees": VegetationParameters(Z_root=250),
}
