import os

import eml_urban_hydro_model as uhm
import numpy as np
import pandas as pd


# Input data

filepath = os.path.join(os.path.dirname(__file__), "pluvio.pkl")
df = pd.read_pickle(filepath)


# Catchment area

# [mare foret paturage prairie gazon-fleuri pelouse grille-gazon gravier mineral-compacte]
omegas_st = np.array([0, 0, 0, 2236.43, 1701.78, 0, 0, 0, 0])
# [platform, surface-impermeable]
omega0_st = np.array([5141.19, 6962.80])
# [tank-like roof, roof]
omegat_st = np.array([6225.88, 6035.83])


# Soil characteristics

soil_params = uhm.SoilParameters(Ks=100, n=0.42, beta=12.7, sh=0.08, sw=0.11, ss=0.31, sfc=0.52)
# soil_params = uhm.soil_params["loamy sand"]  # Alternatively get predefined soil parameters


# Run model

df_out = uhm.model_st(
    df,
    uhm.ModelParameters(
        k=90,
        lag=0,
        soil_params=soil_params,
        omegaSoil=sum(omegas_st),
        omegaRoad=sum(omega0_st),
        omegaRoof=sum(omegat_st),
    ),
)
print(df_out)
