import numpy as np

from .type_models.rho_parameters import RhoParameters


def rho(s: np.ndarray, params: RhoParameters) -> np.ndarray | float:
    Z_soil = params.n * params.model_params.vegetation_params.Z_root  # grass root depth[cm]
    eta_w = params.model_params.E_w / Z_soil  # normalized maximum evapotranspiration [-/day]
    eta = params.model_params.E_max / Z_soil
    m = (
        params.Ks / (Z_soil * (np.exp(params.beta * (1 - params.s_fc)) - 1))
        if (params.s_fc != 1)
        else params.Ks / Z_soil
    )

    if s <= params.s_h:
        return 0
    elif params.s_h < s <= params.s_w:
        return eta_w * (s - params.s_h) / (params.s_w - params.s_h)
    elif params.s_w < s <= params.s_s:
        return eta_w + (eta - eta_w) * (s - params.s_w) / (params.s_s - params.s_w)
    elif params.s_s < s <= params.s_fc:
        return eta
    else:
        return eta + m * (np.exp(params.beta * (s - params.s_fc)) - 1)
        # return eta + heavy/Z_soil
