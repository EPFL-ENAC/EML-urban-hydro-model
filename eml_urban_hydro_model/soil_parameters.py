from .type_models.soil_parameters import SoilParameters


soil_params: dict[str, SoilParameters] = {
    "sand": SoilParameters(Ks=500, n=0.35, beta=12.1, sh=0.08, sw=0.11, ss=0.33, sfc=0.35),
    "loamy sand": SoilParameters(Ks=100, n=0.42, beta=12.7, sh=0.08, sw=0.11, ss=0.31, sfc=0.52),
    "sandy loam": SoilParameters(Ks=80, n=0.43, beta=13.8, sh=0.14, sw=0.18, ss=0.46, sfc=0.56),
    "loam": SoilParameters(Ks=20, n=0.45, beta=14.8, sh=0.19, sw=0.24, ss=0.57, sfc=0.65),
    "clay": SoilParameters(Ks=1, n=0.5, beta=26.8, sh=0.47, sw=0.52, ss=0.78, sfc=0.99),
}
