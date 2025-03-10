from .type_models.vegetation_parameters import VegetationParameters


vegetation_params: dict[str, VegetationParameters] = {
    "none": VegetationParameters(Z_root=0),
    "grass": VegetationParameters(Z_root=500),
    "shrubs": VegetationParameters(Z_root=750),
    "shallow_rooted_trees": VegetationParameters(Z_root=1500),
    "deep_rooted_trees": VegetationParameters(Z_root=2500),
}
