import pandera as pa
from pandera import Series


class ModelInput(pa.DataFrameModel):
    """DataFrame model for the model's input data."""

    time: Series[pa.DateTime] = pa.Field(description="Date and time.")
    precp: Series[float] = pa.Field(
        description="Precipitation (mm/5min). The 5min depends on the resolution of the data."
    )
