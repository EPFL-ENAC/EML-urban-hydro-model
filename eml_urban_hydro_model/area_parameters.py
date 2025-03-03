from .type_models.area_parameters import AreaParameters


area_params: dict[str, AreaParameters] = {
    "centre01": AreaParameters(omegaSoil=14158, omegaRoad=78849, omegaRoof=44754),
    "co01": AreaParameters(omegaSoil=10853, omegaRoad=35364, omegaRoof=21048),
    "colladon01": AreaParameters(omegaSoil=501, omegaRoad=4296, omegaRoof=0),
    "nord_est01": AreaParameters(omegaSoil=64, omegaRoad=4594, omegaRoof=4598),
    "nord_est02": AreaParameters(omegaSoil=533, omegaRoad=6213, omegaRoof=2121),
    "nord_est03": AreaParameters(omegaSoil=1956, omegaRoad=23966, omegaRoof=17329),
    "rlc01": AreaParameters(omegaSoil=17683, omegaRoad=14361, omegaRoof=15940),
    "sud-ouest01": AreaParameters(omegaSoil=2831, omegaRoad=19578, omegaRoof=21494),
    "sud-ouest02": AreaParameters(omegaSoil=1774, omegaRoad=6484, omegaRoof=2994),
    "sud-ouest03": AreaParameters(omegaSoil=1026, omegaRoad=12055, omegaRoof=5105),
    "swisstech01": AreaParameters(omegaSoil=3938, omegaRoad=12104, omegaRoof=12262),
    "tf01": AreaParameters(omegaSoil=328, omegaRoad=6796, omegaRoof=0),
}
