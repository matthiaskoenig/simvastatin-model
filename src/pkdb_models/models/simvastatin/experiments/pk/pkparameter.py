"""Calculation of the pharmacokinetic parameters of simvastatin, illustrated."""

from typing import ClassVar, override

from matplotlib import pyplot as plt
from matplotlib.figure import Figure as FigureMPL
from pkpdutils import nca_single
from pkpdutils.plot import plot_nca
from sbmlsim import Q
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.simvastatin_pk import SUBSTANCES, pk_timecourse


class PKParameter(SimvastatinSimulationExperiment):
    """Non-compartmental analysis of simvastatin and simvastatin acid.

    A single oral dose of 40 mg simvastatin with a sample every 15 min for
    12 hr; the figure shows the analysis of the concentrations in venous
    plasma (see `simvastatin_pk`) on a linear and a logarithmic scale with the
    diagnostic panels of `pkpdutils`: the area to the last sample
    (`auc_last`), the extrapolated area (`auc_inf_obs`), the terminal
    regression (`lambda_z`, `thalf`) with the points it used and the peak
    (`cmax`, `tmax`), and the table of the parameters. The values are in the
    table only: the annotations of `pkpdutils` in the panels overlap each
    other at a short terminal window. The simulation ends after 12 hr, before
    the terminal phase of simvastatin, so the regression windows span less
    than a half-life (`SPAN_LOW`); see `PKScanExperiment` for 48 hr.
    Simvastatin acid has no dose of its own, so it has no apparent clearance
    and volume. The selections are those of the base experiment.
    """

    #: the substances of the figure, keys of `simvastatin_pk.SUBSTANCES`
    substances: ClassVar[tuple[str, ...]] = ("simva", "simacid")
    #: the oral dose of simvastatin
    dose: ClassVar[Quantity] = Q(40, "mg")

    @override
    def simulations(self) -> dict[str, Simulation]:
        """Single oral dose of simvastatin, a sample every 15 min for 12 hr."""
        return {
            "simva_po": Simulation(
                start=0,
                end=12 * 60,
                # one simulation in a run over the draws of the fitted
                # parameters, the analysis of one timecourse
                preinit_changes={
                    **self.default_changes(),
                    **self.fitted_changes(),
                    "PODOSE_simva": self.dose,
                },
            )
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        """Non-compartmental analysis of the simulation."""
        xres = self.results["task_simva_po"]

        fig, axes = plt.subplots(
            nrows=len(self.substances),
            ncols=3,
            figsize=(15, 4.8 * len(self.substances)),
            width_ratios=(1, 1, 0.6),
            layout="constrained",
        )
        fig.suptitle(
            f"Pharmacokinetic parameters, simvastatin {self.dose:~P} oral",
            fontsize=14,
            fontweight="bold",
        )
        for row, sid in enumerate(self.substances):
            timecourse = pk_timecourse(xres, sid, self.Mr.simva)
            plot_nca(
                timecourse,
                nca_single(timecourse),
                title=f"{SUBSTANCES[sid]} (venous plasma)",
                annotate=False,
                axes=axes[row],
            )
        return {"fig_pkparameter": fig}
