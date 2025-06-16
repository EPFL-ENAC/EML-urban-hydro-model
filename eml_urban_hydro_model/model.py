import numpy as np
import pandera as pa
from pandera.typing import DataFrame

from .rho import rho
from .type_models.model_input import ModelInput
from .type_models.model_parameters import ModelParameters
from .type_models.model_output import ModelOutput
from .type_models.rho_parameters import RhoParameters


@pa.check_types
def model_st(df: DataFrame[ModelInput], params: ModelParameters) -> DataFrame[ModelOutput]:
    Qirr = params.Qirr if params.Qirr is not None else (params.area_params.omegaSoil * params.E_max / (100 * 86400))

    rain = df["precp"].copy().fillna(0)
    rain_lag = rain if params.lag == 0 else np.concatenate((np.zeros(params.lag), rain.iloc[: -params.lag]))
    Kc = df["time"].dt.month.apply(lambda x: 1 if x in [12, 1, 2, 9, 10, 11] else 2)

    # Soil parameters
    Ks = params.soil_params.Ks
    n = params.soil_params.n
    beta = params.soil_params.beta
    s_h = params.soil_params.sh / params.soil_params.sfc
    s_w = params.soil_params.sw / params.soil_params.sfc
    s_s = params.soil_params.ss / params.soil_params.sfc
    s_fc = params.soil_params.sfc / params.soil_params.sfc

    # Initialization

    y0 = [0, s_s, 0, 0]
    y_result = np.zeros(
        (df.shape[0], 4)
    )  # increased to 4 for roof vector (index: 0 for Road, 1 for Soil, 2 for Roof, 3 for Tank)
    y_result[0] = y0
    dydt = np.zeros(4)  # increased to 4 for roof vector
    Qsoil = np.zeros(df.shape[0])
    Qpolicy_irr = np.zeros(df.shape[0])
    Vpolicy_flush = np.zeros(df.shape[0])

    Qout = np.zeros(df.shape[0])
    Qroad = np.zeros(df.shape[0])
    Qroof = np.zeros(df.shape[0])
    Qtank = np.zeros(df.shape[0])
    Vroad = np.zeros(df.shape[0])
    Vroof = np.zeros(df.shape[0])
    # Vtank = np.zeros(df.shape[0])  # Not used

    steps_per_hour = 60 / params.resolution  # Number of time steps per hour
    lam = params.flushing_frequency / steps_per_hour  # Poisson mean

    for i in range(df.shape[0] - 1):
        p = rain_lag.iloc[i] / (1000 * 60 * params.resolution)  # Convert from mm/5min to m/s
        pm = p  # Modeled precipitation

        # Sample from a Poisson distribution (flush count per time step)
        flushing = np.random.poisson(lam)

        # ============ Qsoil ===============#
        if y_result[i, 1] >= s_fc:
            Qsoil[i] = p * params.area_params.omegaSoil
        elif p > params.heavy:
            Qsoil[i] = (p - params.heavy) * params.area_params.omegaSoil
        else:
            Qsoil[i] = 0

        p_eff = (
            p * params.area_params.omegaSoil - Qsoil[i]
        ) / params.area_params.omegaSoil  # Precipitation that goes into the soil

        # ============ Qroad ===============#
        Qroad[i] = (
            params.k * y_result[i, 0] * params.area_params.omegaRoad / 86400
        )  # Water flow at time point i the k should be different in roads and roofs
        Vroad[i] = y_result[i, 0] * params.area_params.omegaRoad  # Water volume of Road reservoir at time point i
        # Qroad[i] = k * V_runoff[i]  # Turn k [/day] to k [/s]

        # ============ Qroof ===============#
        Vroof[i] = y_result[i, 2] * (1 - params.frac_rt2tk) * params.area_params.omegaRoof
        Qroof[i] = (
            params.k * y_result[i, 2] * (1 - params.frac_rt2tk) * params.area_params.omegaRoof / 86400
        )  # Water flow at time point i

        # ==============Road reservoir==========#
        dydt[0] = pm - Qroad[i] / params.area_params.omegaRoad  # roof, tank and roads use pm (modeled precipitation)

        y_result[i + 1, 0] = y_result[i, 0] + dydt[0] * 60 * params.resolution
        if y_result[i + 1, 0] < 0:
            y_result[i + 1, 0] = 0

        # ==============Tank reservoir==========#
        Qpolicy_irr[i] = (
            Kc.iloc[i] * Qirr
            if (
                pm == 0 and y_result[i, 1] < s_fc - 0.1 and y_result[i, 3] >= Kc.iloc[i] * Qirr * params.resolution * 60
            )
            else 0
        )
        Vpolicy_flush[i] = (
            flushing * 0.02 if (y_result[i, 3] > 0.02 * flushing) else y_result[i, 3]
        )  # multiply by random 0 or 1

        if params.frac_rt2tk != 0:
            # Calculate inflow and outflows
            dydt[3] = pm * (params.frac_rt2tk * params.area_params.omegaRoof) - (Qtank[i] + Qpolicy_irr[i])
            y_result[i + 1, 3] = y_result[i, 3] - Vpolicy_flush[i] + dydt[3] * 60 * params.resolution

            # Ensure tank volume is non-negative
            if y_result[i + 1, 3] < 0:
                y_result[i + 1, 3] = 0

            # Check for overflow
            if y_result[i + 1, 3] >= params.Vmax:
                Qtank[i] = (y_result[i + 1, 3] - params.Vmax) / (60 * params.resolution)  # Overflow rate
                y_result[i + 1, 3] = params.Vmax
            else:
                Qtank[i] = 0
        else:
            dydt[3] = 0
            y_result[:, 3] = 0

        # ==============Roof reservoir==========#
        dydt[2] = (
            pm - Qroof[i] / ((1 - params.frac_rt2tk) * params.area_params.omegaRoof) if params.frac_rt2tk != 1 else 0
        )  # roof, tank and roads use pm (modeled precipitation)

        y_result[i + 1, 2] = y_result[i, 2] + dydt[2] * 60 * params.resolution
        if y_result[i + 1, 2] < 0:
            y_result[i + 1, 2] = 0

        # ==============Soil reservoir==========#
        Z_soil = n * params.vegetation_params.Z_root
        rho_params = RhoParameters(n=n, model_params=params, beta=beta, s_h=s_h, s_w=s_w, s_s=s_s, s_fc=s_fc, Ks=Ks)
        dydt[1] = (p_eff + Qpolicy_irr[i] / params.area_params.omegaSoil) / (Z_soil / 100) - rho(
            y_result[i, 1], rho_params
        ) / 86400  # (1+(1-frac_rt2tk)*frac_rt2s*omegat/omegas)

        y_result[i + 1, 1] = y_result[i, 1] + dydt[1] * 60 * params.resolution
        if y_result[i + 1, 1] >= 1:
            y_result[i + 1, 1] = 1

        # ============ Qout ===============#
        Qout[i] = Qroad[i] + Qroof[i] + Qtank[i] + Qsoil[i]  # Total outflow at time point i

    df_return = df[["time", "precp"]].copy()
    df_return["Qout"] = Qout
    df_return["Qroad"] = Qroad
    df_return["Qroof"] = Qroof
    df_return["Qsoil"] = Qsoil
    df_return["Qtank"] = Qtank
    df_return["Qirr"] = Qpolicy_irr
    df_return["Vflush"] = Vpolicy_flush
    df_return["soil_mois"] = y_result[:, 1]
    df_return["v_tank"] = y_result[:, 3]

    return df_return
