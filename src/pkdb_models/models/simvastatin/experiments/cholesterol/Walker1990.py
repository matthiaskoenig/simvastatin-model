"""Simulation experiment of the study Walker1990."""

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


class Walker1990(SimvastatinSimulationExperiment):
    """Simulation experiment of Walker1990.

    Randomized double-blind placebo-controlled study, 4 weeks, 160 elderly
    patients (62 - 82 years) with type II hyperlipidemia and atherosclerosis:
    placebo or simvastatin 2.5, 5, 10 or 20 mg once daily in the evening. Table
    3 gives the LDL cholesterol at baseline and at week 4. The model has no time
    of the day and no effect of age, the evening doses are doses every 24 h.
    """

    #: the FH type of the fit mappings, the reduced LDL clearance of a non
    #: familial hypercholesterolemia (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: intervention of the data, task key of the simulations, dose [mg]
    #: and label
    group_info: ClassVar[list[tuple[str, str, float, str]]] = [
        ("SIM0", "0mg", 0, "placebo"),
        ("SIM2_5", "2_5mg", 2.5, "SV 2.5mg"),
        ("SIM5", "5mg", 5, "SV 5mg"),
        ("SIM10", "10mg", 10, "SV 10mg"),
        ("SIM20", "20mg", 20, "SV 20mg"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab2", "Tab3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "cholesterol" and fig_id == "Tab2":
                    dset.unit_conversion("mean", 1 / self.Mr.cho)
                elif substance == "ldl-c" and fig_id == "Tab3":
                    dset.unit_conversion("mean", 1 / self.Mr.ldlc)
                for label in df.label.unique():
                    dsets[self.to_sid(f"{fig_id}_{label}")] = dset[dset.label == label]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM]
        tcs_dict = {
            "simva_po_0mg": (Q(0, "mg"), 232.1 / self.Mr.ldlc.m * 10),
            "simva_po_2_5mg": (Q(2.5, "mg"), 226.9 / self.Mr.ldlc.m * 10),
            "simva_po_5mg": (Q(5, "mg"), 227.4 / self.Mr.ldlc.m * 10),
            "simva_po_10mg": (Q(10, "mg"), 224.8 / self.Mr.ldlc.m * 10),
            "simva_po_20mg": (Q(20, "mg"), 230.9 / self.Mr.ldlc.m * 10),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + (4 * 7 + 1) * DAY,
                    dt=DAY / 100,
                    changes=[self.doses(dose, 4 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of every group (Table 3, weeks 0 and 4)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.SERUM,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{intervention}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab3_ldl-c_{intervention}"),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{task_key}_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=metadata,
            )
            for intervention, task_key, _, _ in self.group_info
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        figures = {"fig_cho": self._figure_cho()}
        if self.show_all_cho_data:
            figures["fig_all"] = self._figure_all()
        return figures

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for _, task_key, dose, label in self.group_info:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: {label}",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=task_key),
            )

    def _plot_data(
        self, ax: Axes, dset_prefix: str, count_separator: str = "\n"
    ) -> None:
        """Plot the data of the groups.

        The number of subjects is the one of the last time point.
        """
        for intervention, _, dose, label in self.group_info:
            dataset = self._datasets[self.to_sid(f"{dset_prefix}_{intervention}")]
            count = int(dataset["count"][dataset["time"].idxmax()])
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                color=color,
                label=f"{self.sid}: {label}{count_separator}(n={count})",
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
        self._plot_data(ax, "Tab3_ldl-c", count_separator=" ")
        ax.set_xlim((-0.5, 5))
        ax.set_ylim((0.0, 7))
        ax.legend(ncol=2, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _figure_all(self) -> FigureMPL:
        """The total and LDL cholesterol of the data and the simulations."""
        kwargs: FontKwargs = {"weight": "bold", "size": 16}
        fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=2, sharex="col", figsize=(15, 6))
        fig.subplots_adjust(bottom=0.12, top=0.925, left=0.07, right=0.95, hspace=0.05)
        ax1.set_xlabel("Time [weeks]", **kwargs)
        ax2.set_xlabel("Time [weeks]", **kwargs)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("Total cholesterol [mM]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "Tab3_ldl-c")
        self._plot_data(ax2, "Tab2_cholesterol")

        for ax in [ax1, ax2]:
            ax.set_xlim((-0.5, 5))
            ax.legend(loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 7))
        ax2.set_ylim((0.0, 15))
        return fig
