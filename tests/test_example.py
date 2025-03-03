import os

import pandas as pd

import eml_urban_hydro_model as uhm


def test_example():
    """Test running the example."""

    filepath = os.path.join(os.path.dirname(__file__), "..", "examples", "pluvio.pkl")
    df = pd.read_pickle(filepath)
    df = uhm.preprocess(df)

    area_params = uhm.area_params["swisstech01"]
    soil_params = uhm.soil_params["loamy sand"]

    df_out = uhm.model_st(
        df,
        uhm.ModelParameters(
            k=90,
            lag=0,
            soil_params=soil_params,
            area_params=area_params,
        ),
    )

    assert isinstance(df_out, pd.DataFrame)
