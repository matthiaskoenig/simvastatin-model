"""Simulation experiment of the study Pietro1989."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Health,
    PKPDData,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.simulation import Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)


class Pietro1989(SimvastatinSimulationExperiment):
    """Simulation experiment of Pietro1989.

    Randomized double-blind parallel study, 12 weeks, 243 patients with primary
    hypercholesterolemia (55 % familial): simvastatin 20 or 40 mg once daily in
    the evening or probucol 500 mg twice daily (not simulated). Fig 1 shows the
    mean percent change of the LDL cholesterol at weeks 2, 6, 10 and 12; the
    concentrations of the data are derived from it with the baseline of all
    patients of Table II (251 mg/dl, no baseline per group is reported), which
    is the baseline of the simulations. The model has no time of the day, the
    evening doses are doses every 24 h.
    """

    #: the doses [mg]
    doses_mg: ClassVar[list[int]] = [20, 40]

    #: the FH type of the fit mappings, the reduced LDL clearance of a non
    #: familial hypercholesterolemia (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the lipids in mg/dl which are converted to mM with the lipid conversion
    #: factor; the triglycerides and apoB stay in mg/dl
    cholesterol_substances: ClassVar[set[str]] = {"cholesterol", "hdl-c", "ldl-c"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        # the changes of the LDL cholesterol of the subgroups (Tab3) are not used
        for fig_id in ["Fig1", "Tab2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    if not (df["measurement_type"] == measurement_type).any():
                        continue
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    if (
                        measurement_type == "concentration"
                        and substance in self.cholesterol_substances
                    ):
                        dset_mtype.unit_conversion("mean", 1 / self.Mr.cho)
                    for intervention in df.intervention.unique():
                        dsets[
                            self.to_sid(f"{fig_id}_{substance}_{intervention}{suffix}")
                        ] = dset_mtype[dset_mtype.intervention == intervention]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        ldlc_init = 251 / self.Mr.ldlc.m * 10  # [mM]
        tcsims: dict[str, Simulation | Scan] = {}
        for dose in self.doses_mg:
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{dose}mg_{fh_type_key}")] = self.presim(
                    end=WEEK + (12 * 7 + 1) * DAY,
                    dt=DAY / 100,
                    changes=[self.doses(Q(dose, "mg"), 12 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the doses (Fig 1, weeks 0 to 12)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_SIM{dose}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_ldl-c_SIM{dose}"),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{dose}mg_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=metadata,
            )
            for dose in self.doses_mg
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        figures = {"fig_cho": self._figure_cho()}
        if self.show_all_cho_data:
            figures["fig_all"] = self._figure_all()
        return figures

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for dose in self.doses_mg:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: SV {dose}mg",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=f"{dose}mg"),
            )

    def _plot_data(self, ax: Axes, dset_prefix: str, suffix: str = "") -> None:
        """Plot the data of the doses.

        The number of subjects is the one of the last time point.
        """
        for dose in self.doses_mg:
            dataset = self._datasets[self.to_sid(f"{dset_prefix}_SIM{dose}{suffix}")]
            count = int(dataset["count"][dataset["time"].idxmax()])
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                color=color,
                label=f"{self.sid}: SV {dose}mg (n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker="s",
                linestyle="None",
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        self._plot_simulations(ax)
        self._plot_data(ax, "Fig1_ldl-c")
        ax.set_xlim((-1, 13))
        ax.set_ylim((0.0, 9))
        ax.legend(ncol=1, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _figure_all(self) -> FigureMPL:
        """The lipids of the data and the LDL cholesterol of the simulations."""
        kwargs: FontKwargs = {"weight": "bold", "size": 16}
        fig, [[ax1, ax2], [ax3, ax4], [ax5, ax6]] = plt.subplots(
            nrows=3, ncols=2, sharex="col", figsize=(15, 12)
        )
        fig.subplots_adjust(bottom=0.12, top=0.925, left=0.07, right=0.95, hspace=0.05)
        ax5.set_xlabel("Time [weeks]", **kwargs)
        ax6.set_xlabel("Time [weeks]", **kwargs)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("HDL-C [mM]", **kwargs)
        ax3.set_ylabel("Total cholesterol [mM]", **kwargs)
        ax4.set_ylabel("LDL-C change [%]", **kwargs)
        ax5.set_ylabel("Triglycerides [mg/dl]", **kwargs)
        ax6.set_ylabel("ApoB100+48 [mg/dl]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "Fig1_ldl-c")
        self._plot_data(ax3, "Tab2_cholesterol")
        self._plot_data(ax2, "Tab2_hdl-c")
        self._plot_data(ax5, "Tab2_triglyceride")
        self._plot_data(ax6, "Tab2_apoB100+48")
        self._plot_data(ax4, "Fig1_ldl-c", suffix="_relative_change")

        for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
            ax.set_xlim((-1, 13))
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 9))
        ax2.set_ylim((0.0, 2.5))
        ax3.set_ylim((0.0, 11))
        ax4.set_ylim((-50, 5))
        ax5.set_ylim((0.0, 200))
        ax6.set_ylim((0.0, 270))
        return fig
