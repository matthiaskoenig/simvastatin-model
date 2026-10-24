"""Simulation experiment of the study Tuomilehto1995."""

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


class Tuomilehto1995(SimvastatinSimulationExperiment):
    """Simulation experiment of Tuomilehto1995.

    Randomized double-blind placebo-controlled dose response study, 8 weeks,
    166 patients with primary hypercholesterolemia (LDL-C > 4.3 mM on diet):
    placebo or simvastatin 2.5, 5, 10, 20 or 40 mg once daily in the evening
    (one capsule). Fig 1 shows the mean percent change of the LDL cholesterol at
    weeks 2, 4, 6 and 8; the concentrations of the data are derived from it with
    the baseline of the group of Table 2 (0.1 mM resolution), which is the
    baseline of the simulation (`ldlc_init`). The model has no time of the day,
    the evening doses are doses every 24 h.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types (they
    #: differ by less than 3 percentage points at 8 weeks of 40 mg)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: intervention of the data, task key of the simulations, dose [mg]
    #: and label
    group_info: ClassVar[list[tuple[str, str, float, str]]] = [
        ("SIM0", "0mg", 0, "placebo"),
        ("SIM2_5", "2_5mg", 2.5, "SV 2.5mg"),
        ("SIM5", "5mg", 5, "SV 5mg"),
        ("SIM10", "10mg", 10, "SV 10mg"),
        ("SIM20", "20mg", 20, "SV 20mg"),
        ("SIM40", "40mg", 40, "SV 40mg"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    for intervention in df.intervention.unique():
                        dsets[
                            self.to_sid(f"{fig_id}_{substance}_{intervention}{suffix}")
                        ] = dset_mtype[dset_mtype.intervention == intervention]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM]
        tcs_dict = {
            "simva_po_0mg": (Q(0, "mg"), 5.3),
            "simva_po_2_5mg": (Q(2.5, "mg"), 5.1),
            "simva_po_5mg": (Q(5, "mg"), 5),
            "simva_po_10mg": (Q(10, "mg"), 5.2),
            "simva_po_20mg": (Q(20, "mg"), 5.2),
            "simva_po_40mg": (Q(40, "mg"), 5),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + (8 * 7 + 1) * DAY,
                    dt=DAY / 100,
                    changes=[self.doses(dose, 8 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of every group (Fig 1, weeks 0 to 8)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.SERUM,
            route=Route.PO,
            application_form=ApplicationForm.CAPSULE,
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
                    dataset=self.to_sid(f"Fig1_ldl-c_{intervention}"),
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

    def _plot_data(self, ax: Axes, dset_prefix: str) -> None:
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
                label=f"{self.sid}: {label} (n={count})",
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
        ax.set_xlim((-0.3, 9))
        ax.set_ylim((0.0, 11))
        ax.legend(ncol=2, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _figure_all(self) -> FigureMPL:
        """The lipids of the data and the LDL cholesterol of the simulations."""
        kwargs: FontKwargs = {"weight": "bold", "size": 16}
        fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(
            nrows=2, ncols=2, sharex="col", figsize=(15, 8)
        )
        fig.subplots_adjust(bottom=0.12, top=0.925, left=0.07, right=0.95, hspace=0.05)
        ax3.set_xlabel("Time [weeks]", **kwargs)
        ax4.set_xlabel("Time [weeks]", **kwargs)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("HDL-C [mM]", **kwargs)
        ax3.set_ylabel("Total cholesterol [mM]", **kwargs)
        ax4.set_ylabel("Triglycerides [mM]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "Fig1_ldl-c")
        self._plot_data(ax2, "Fig2_hdl-c")
        self._plot_data(ax3, "Fig1_cholesterol")
        self._plot_data(ax4, "Fig2_triglyceride")

        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim((-1, 9))
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 8))
        ax2.set_ylim((0.0, 2))
        ax3.set_ylim((0.0, 11))
        ax4.set_ylim((0.0, 4))
        return fig
