import os

import pandas as pd

import eml_urban_hydro_model as uhm


def test_example():
    """Test running the example."""

    filepath = os.path.join(os.path.dirname(__file__), "..", "examples", "pluvio.pkl")
    df = pd.read_pickle(filepath)
    df = uhm.preprocess(df)

    area_params = uhm.area_params["swisstech01"]
    area_params = uhm.set_percent_paved(area_params, percent_paved=85)
    soil_params = uhm.soil_params["loamy sand"]
    vegetation_params = uhm.vegetation_params["grass"]

    df_out = uhm.model_st(
        df,
        uhm.ModelParameters(
            k=90,
            lag=0,
            area_params=area_params,
            soil_params=soil_params,
            vegetation_params=vegetation_params,
        ),
    )

    assert isinstance(df_out, pd.DataFrame)
