# Urban Hydrological Model

_A Python library to simulate urban hydrological systems._


# 🔍 Overview

This library provides a function `model_st` that simulates an urban hydrological system, modeling water movement through different reservoirs:
- **Soil**
- **Roads**
- **Roofs**
- **Rainwater Tank**

It accounts for rainfall infiltration, runoff, tank storage, and irrigation, incorporating soil parameters and hydrological properties.


## Input Data

The function expects a **Pandas DataFrame (`df`)** with at least one required column:
- `precp`: Precipitation (mm/5min) the 5min depends on the resolution of the data. The column must be named `precp`
-  If you have a different resolution, you'll need to put in input of the model when running it. See the "Usage" section for more details.

Additionally, the DataFrame must include a **datetime column (`time`)**, from which the function extracts the month to determine seasonal irrigation demand. The column should be named `time`.

You can also provide the soil parameters and the area of the catchment.


## Function Parameters

| Parameter     | Description                                           | Default  |
|---------------|-------------------------------------------------------|----------|
| `df`          | Input DataFrame containing precipitation data         | Required |
| `k`           | Runoff coefficient for roads and roofs                | `90` |
| `frac_rt2s`   | Fraction of roof runoff directed to soil              | `0.5` |
| `frac_rt2tk`  | Fraction of roof runoff directed to tank              | `0.5` |
| `Z_root`      | Root zone depth (cm)                                  | `140` |
| `E_max`       | Maximum evapotranspiration rate (mm/day)              | `0.5` |
| `E_w`         | Minimum evapotranspiration rate (mm/day)              | `0.0625` |
| `heavy`       | Threshold for intense rainfall (m/s)                  | `55/600000` |
| `soil_params` | Soil parameters                                       | `"loamy sand"` parameters |
| `area_params` | Catchment areas (soil infiltration, road/roof runoff) | `"swisstech01"` parameters |
| `Vmax`        | Maximum tank capacity (m³)                            | `10` |
| `lag`         | Time lag for precipitation effect                     | `0` |
| `resolution`  | Time step resolution (minutes)                        | `5` |
| `Qirr`        | Irrigation flow rate (m³/s)                           | `omegaSoil * E_max / (100 * 86400)` |
| `flushing_frequency` | Tank flushing frequency (per hour)             | `2` |


## Outputs

The function returns a **DataFrame** with the following computed hydrological variables:

| Column        | Description                                      |
|--------------|--------------------------------------------------|
| `Qout`      | Total outflow (m³/s)                              |
| `Qroad`     | Runoff from roads (m³/s)                          |
| `Qroof`     | Runoff from roofs (m³/s)                          |
| `Qsoil`     | Water infiltrated into the soil (m³/s)            |
| `Qtank`     | Overflow from the tank (m³/s)                     |
| `Qirr`      | Water used for irrigation (m³/s)                  |
| `Vflush`    | Water volume flushed from the tank (m³)           |
| `soil_mois` | Soil moisture level (dimensionless, 0 to 1)       |
| `v_tank`    | Water volume stored in the tank (m³)              |


## Assumptions & Notes

- The function assumes `soil` is a predefined dictionary containing soil parameters (`Ks`, `n`, `beta`, etc.).
- The function incorporates irrigation (`Qirr`) only when there is no rainfall and soil moisture is below field capacity.
- The model uses **Poisson-distributed flushing events** to simulate real-world variability in tank flushing.


# 🐇 Quick start

## Requirements

- Python 3.10 or higher


## Installation

We recommend you install this library inside a Python virtual environment, for example using [uv](https://github.com/astral-sh/uv) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). To install, run the following command in your terminal:
```bash
pip install git+https://github.com/EPFL-ENAC/EML-urban-hydro-model.git
```

## Usage

See `examples/example.py` for a simple example of how to use the library.

```python
import eml_urban_hydro_model as uhm

df = uhm.preprocess(df)
area_params = uhm.area_params["swisstech01"]
df_out = uhm.model_st(
    df,
    uhm.ModelParameters(area_params=area_params, resolution=5),
)
```


# 💾 Installation for development

```bash
git clone https://github.com/EPFL-ENAC/EML-urban-hydro-model.git
cd EML-urban-hydro-model
make install
```

Use [uv](https://github.com/astral-sh/uv) to add dependencies to the `pyproject.toml`:

```bash
uv add <package-name>
```


# ✅ Running tests

```bash
make test
```
