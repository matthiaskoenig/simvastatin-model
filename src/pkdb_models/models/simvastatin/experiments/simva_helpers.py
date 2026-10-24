"""Colors of the simvastatin doses."""

import matplotlib as mpl
import numpy as np

#: the largest dose of simvastatin [mg], the end of the colormap
MAX_DOSE = 160


def colormap_SV_dose(dose: float) -> str | tuple[float, float, float, float]:
    """Get the color of a simvastatin dose [mg], black for placebo.

    The doses are colored on a logarithmic scale of the colormap `plasma_r`.
    """
    if dose == 0:
        return "#000000"
    dose_relative = np.log(dose) / np.log(MAX_DOSE)
    return mpl.colormaps["plasma_r"](dose_relative)
