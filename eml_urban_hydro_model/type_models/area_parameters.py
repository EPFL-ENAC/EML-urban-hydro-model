from pydantic import BaseModel, Field


class AreaParameters(BaseModel):
    """Container for area parameters."""

    omegaSoil: float = Field(..., gt=0, description="Catchment area for soil infiltration (m²).")
    omegaRoad: float = Field(..., ge=0, description="Catchment area for road runoff (m²).")
    omegaRoof: float = Field(..., ge=0, description="Catchment area for roof runoff (m²).")
    runoff_coeff_soil: float = Field(0.5, ge=0, le=1, description="Runoff coefficient for permeable soil area.")
    runoff_coeff_roads: float = Field(
        0.9, ge=0, le=1, description="Runoff coefficient for roads (impervious, but not 100%)."
    )
    runoff_coeff_roofs: float = Field(
        0.95, ge=0, le=1, description="Runoff coefficient for roofs (impervious, but not 100%)."
    )


def get_percent_paved(params: AreaParameters) -> float:
    """Calculates the percentage of paved area based on the area parameters.

    Args:
        params (AreaParameters): The area parameters containing omega values.

    Returns:
        float: The percentage of paved area (0-100).
    """

    total_area = params.omegaSoil + params.omegaRoad + params.omegaRoof
    if total_area == 0:
        return 0.0

    paved_area = params.omegaRoad + params.omegaRoof
    percent_paved = (paved_area / total_area) * 100

    return percent_paved


def set_percent_paved(params: AreaParameters, percent_paved: float) -> AreaParameters:
    """Adjusts the omega* parameters based on the percent_paved value.

    Args:
        params (AreaParameters): The original area parameters.
        percent_paved (float): The desired percentage of paved area (0-100).

    Returns:
        AreaParameters: Updated area parameters with adjusted omega values.
    """

    total_area = params.omegaSoil + params.omegaRoad + params.omegaRoof
    previous_paved_area = params.omegaRoad + params.omegaRoof
    new_paved_area = (percent_paved / 100) * total_area

    new_params_dict = params.model_dump()
    new_params_dict["omegaSoil"] = total_area - new_paved_area
    new_params_dict["omegaRoad"] = (
        (params.omegaRoad / previous_paved_area) * new_paved_area if previous_paved_area > 0 else 0
    )
    new_params_dict["omegaRoof"] = (
        (params.omegaRoof / previous_paved_area) * new_paved_area if previous_paved_area > 0 else 0
    )

    return AreaParameters(**new_params_dict)
