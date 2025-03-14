import numpy as np
import pandas as pd
from pandera.typing import DataFrame

from .type_models.model_input import ModelInput
from .type_models.preprocessing_parameters import PreprocessingParameters


def preprocess(
    original_rainfall: DataFrame[ModelInput],
    params: PreprocessingParameters = PreprocessingParameters(),
) -> DataFrame[ModelInput]:
    """Modify rainfall intensity using a memory term with heavyside equation."""

    T_steps = params.T // params.resolution  # Memory duration in terms of time steps
    alpha = 0.7
    # Initialize modified rainfall array
    results = np.zeros_like(original_rainfall["precp"])

    for t in range(len(original_rainfall)):
        # First term
        if original_rainfall["precp"].iloc[t] > params.ic:
            direct_contribution = original_rainfall["precp"].iloc[t]
        else:
            direct_contribution = 0

        # Second term
        memory_contribution = 0
        for tau in range(T_steps):
            if t - tau >= 0:  # Ensure valid index
                past_rainfall = original_rainfall["precp"].iloc[t - tau]
                if past_rainfall <= params.ic:  # Only consider rainfall below ic
                    memory_contribution += past_rainfall * alpha * (tau / T_steps) * np.exp((tau - T_steps) / T_steps)

        memory_contribution /= T_steps

        # Combine contributions
        results[t] = direct_contribution + memory_contribution

    # Create a new DataFrame with the modified rainfall
    modified_rainfall = pd.DataFrame(
        {"time": original_rainfall["time"], "precp": results}, index=original_rainfall.index
    )

    return modified_rainfall
