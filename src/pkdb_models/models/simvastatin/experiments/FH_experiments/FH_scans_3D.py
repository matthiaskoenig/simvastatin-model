"""Scan of two FH types combined: the LDL-C in steady state as a surface."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from sbmlsim import Q
from sbmlsim.data import Data
from sbmlsim.simulation import Dimension, Scan

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    WEEK,
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.experiments.FH_experiments.readout_dict_FH_scans import (
    time_FH_steadystate,
)


class FH_scans_3D(SimvastatinSimulationExperiment):
    """Simulate timecourse of simvastatin therapy under varying FH strength.

    The FH strength of the combined FH types 1 and 2 & 6 (the synthesis and
    the membrane transport of the LDLR) is scanned for 3D scans.
    """

    #: the time to the steady state of the FH types [weeks]
    time_FH_steadystate: ClassVar[int] = time_FH_steadystate

    #: the factors of the scan, log10 from `scanspace_start` to `scanspace_stop`
    scanspace_start: ClassVar[int] = -2
    scanspace_stop: ClassVar[int] = 2
    scanspace_num: ClassVar[int] = 11  # FIXME change to 21!

    @override
    def data(self) -> dict[str, Data]:
        # the plasma LDL-C of the figure
        self.add_selections_data(selections=["time", "[Cve_ldlc]"])
        return {}

    @override
    def simulations(self) -> dict[str, Scan]:
        return {
            **self.simulation_cho(),
        }

    def simulation_cho(self) -> dict[str, Scan]:
        """Scan of the factors of the FH types 1 and 2 & 6 into the steady state."""
        tcscans = {}
        values = Q(
            np.logspace(
                self.scanspace_start, self.scanspace_stop, num=self.scanspace_num
            ),
            "dimensionless",
        )
        # steady state for the parameter changes (FH types) from 0
        tcscans["FH_scan_1vs2_6"] = Scan(
            simulation=self.presim(
                end=WEEK + self.time_FH_steadystate * WEEK,
                dt=WEEK,
                ldlc=3,
                # one simulation in a run over the draws of the fitted
                # parameters, which have no effect without simvastatin
                preinit_changes=self.fitted_changes(),
            ),
            dimensions=[
                Dimension(
                    "dim_fh1", values={"LI__SYNTHESIS_LDLR_Vmax_f": values}, at=0
                ),
                Dimension(
                    "dim_fh2_6", values={"LI__LDLRMEMBRANE_Kcat_f": values}, at=0
                ),
            ],
        )
        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {**self.figure_mpl1()}

    def figure_mpl1(self) -> dict[str, FigureMPL]:
        """Plasma LDL-C at the end of the scan over the factors of the FH types."""
        figures: dict[str, FigureMPL] = {}

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        # the factors of the FH types
        xdata = np.logspace(
            start=self.scanspace_start, stop=self.scanspace_stop, num=self.scanspace_num
        )
        ydata = xdata

        xres = self.results["task_FH_scan_1vs2_6"]

        # the plasma LDL-C at the last time over the factors of the FH types
        zdata = xres["[Cve_ldlc]"].isel(time=-1).values
        x_grid, y_grid = np.meshgrid(xdata, ydata, indexing="ij")
        ax.plot_surface(x_grid, y_grid, zdata, cmap="Greens")

        figures["fig_3d"] = fig
        return figures
