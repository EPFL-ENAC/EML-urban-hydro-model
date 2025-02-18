import pandera as pa
from pandera.typing import Series


class ModelOutput(pa.DataFrameModel):
    """DataFrame model for the model's output data."""

    time: Series[pa.DateTime] = pa.Field(description="Date and time.")
    Qout: Series[float] = pa.Field(description="Total outflow (m³/s).")
    Qout: Series[float] = pa.Field(description="Total outflow (m³/s).")
    Qroad: Series[float] = pa.Field(description="Runoff from roads (m³/s).")
    Qroof: Series[float] = pa.Field(description="Runoff from roofs (m³/s).")
    Qsoil: Series[float] = pa.Field(description="Water infiltrated into the soil (m³/s).")
    Qtank: Series[float] = pa.Field(description="Overflow from the tank (m³/s).")
    Qirr: Series[float] = pa.Field(description="Water used for irrigation (m³/s).")
    Vflush: Series[float] = pa.Field(description="Water volume flushed from the tank (m³).")
    soil_mois: Series[float] = pa.Field(description="Soil moisture level (dimensionless, 0 to 1).")
    v_tank: Series[float] = pa.Field(description="Water volume stored in the tank (m³).")
