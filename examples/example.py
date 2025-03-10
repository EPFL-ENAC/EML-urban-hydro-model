import os

import eml_urban_hydro_model as uhm
import pandas as pd


# Input data

filepath = os.path.join(os.path.dirname(__file__), "pluvio.pkl")
df = pd.read_pickle(filepath)

# Preprocess data

df = uhm.preprocess(df)


# Catchment area

area_params = uhm.area_params["swisstech01"]
# Alternatively define parameters manually
# area_params = uhm.AreaParameters(omegaSoil=3938, omegaRoad=12104, omegaRoof=12262)


# Soil characteristics

soil_params = uhm.soil_params["loamy sand"]
# Alternatively define parameters manually
# soil_params = uhm.SoilParameters(Ks=100, n=0.42, beta=12.7, sh=0.08, sw=0.11, ss=0.31, sfc=0.52)


# Vegetation parameters

vegetation_params = uhm.vegetation_params["grass"]
# Alternatively define parameters manually
# vegetation_params = uhm.VegetationParameters(Z_root=140)


# Run model

df_out = uhm.model_st(
    df,
    uhm.ModelParameters(
        k=90,
        lag=0,
        soil_params=soil_params,
        area_params=area_params,
    ),
)
print(df_out)
