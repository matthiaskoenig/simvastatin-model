"""Simulation experiment of the study Mol1986."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import (
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


class Mol1986(SimvastatinSimulationExperiment):
    """Simulation experiment of Mol1986.

    43 patients with heterozygous familial hypercholesterolemia (FH) on a
    low-cholesterol diet, 2 weeks placebo, then double-blind for 4 weeks:
    simvastatin twice daily 1.25, 2.5, 5, 10, 20 or 40 mg or once daily before
    the evening meal 2.5, 10 or 40 mg (n = 4 per regimen, 20 mg twice daily
    n = 3) or placebo (n = 8). Table 2 combines the regimens of the same daily
    dose (once and twice daily did not differ, Table 1): placebo (n = 8), 2.5
    (8), 5 (4), 10 (8), 20 (4), 40 (7) and 80 mg/day (4); LDL-C by the
    Friedewald formula at week 0 (mean of weeks -2 and 0) and week 4, mean +-
    SD. Fig 1 shows the change of the LDL-C of the 10 and 40 mg/day groups at
    weeks 1, 2 and 4 (mean +- SEM), the data are the concentrations of the
    change and the baseline of the group.

    A group is simulated once with its baseline LDL-C (Table 2): the groups of
    one regimen with it, the combined groups of 2.5, 10 and 40 mg/day once
    daily (the model gives about 2 % more lowering for twice daily).
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    interventions: ClassVar[list[str]] = [
        "placebo",
        "SIM2_5_once",
        "SIM2_5_twice",
        "SIM10_once",
        "SIM10_twice",
        "SIM40_once",
        "SIM40_twice",
        "SIM10",
        "SIM40",
    ]

    #: the groups of Table 2: daily dose [mg], marker of the data, task key of
    #: the simulation, dose [mg], doses per day and baseline LDL-C [mM]
    group_info: ClassVar[dict[str, tuple[float, str, str, float, int, float]]] = {
        "placebo": (0, "o", "placebo", 0, 1, 10.13),
        "SIM2_5_once": (2.5, "v", "2_5mg_once", 2.5, 1, 9.89),
        "SIM2_5_twice": (5, "^", "2_5mg_twice", 2.5, 2, 8.8),
        "SIM10_once": (10, "<", "10mg_once", 10, 1, 10.47),
        "SIM10_twice": (20, ">", "10mg_twice", 10, 2, 9.97),
        "SIM40_once": (40, "s", "40mg_once", 40, 1, 8.78),
        "SIM40_twice": (80, "D", "40mg_twice", 40, 2, 8.72),
    }

    #: the groups of Fig 1 and the groups of Table 2 with the same subjects
    fig1_groups: ClassVar[dict[str, str]] = {
        "SIM10": "SIM10_once",
        "SIM40": "SIM40_once",
    }

    #: the labels of the groups in the figure of the LDL cholesterol
    labels_ldlc: ClassVar[dict[str, str]] = {
        "placebo": "placebo",
        "SIM2_5_once": "SV 2.5mg/day (1.25mg twice,\n2.5mg once)",
        "SIM2_5_twice": "SV 2.5mg twice",
        "SIM10_once": "SV 10mg/day (5mg twice,\n10mg once)",
        "SIM10_twice": "SV 10mg twice",
        "SIM40_once": "SV 40mg/day (20mg twice,\n40mg once)",
        "SIM40_twice": "SV 40mg twice",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2", "Tab3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    for intervention in self.interventions:
                        dsets[
                            self.to_sid(f"{fig_id}_{substance}_{intervention}{suffix}")
                        ] = dset_mtype[dset_mtype.intervention == intervention]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Once daily or twice daily (every 12 hr) doses for 4 weeks."""
        tcsims: dict[str, Simulation | Scan] = {}
        for _, _, task_key, dose_mg, per_day, ldlc_init in self.group_info.values():
            interval = DAY / per_day
            number = per_day * 4 * 7
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{task_key}_{fh_type_key}")] = self.presim(
                    end=WEEK + 4 * WEEK,
                    dt=DAY / 100,
                    changes=[self.doses(Q(dose_mg, "mg"), number, interval=interval)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the groups (Table 2) and of Fig 1."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.SERUM,
            route=Route.PO,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )

        def mapping(dataset: str, task_key: str) -> FitMapping:
            return FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(dataset),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
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

        mappings = {
            f"fm_ldlc_{intervention}": mapping(f"Tab2_ldl-c_{intervention}", info[2])
            for intervention, info in self.group_info.items()
        }
        for intervention, group in self.fig1_groups.items():
            mappings[f"fm_ldlc_Fig1_{intervention}"] = mapping(
                f"Fig1_ldl-c_{intervention}", self.group_info[group][2]
            )
        return mappings

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        figures = {"fig_cho": self._figure_cho()}
        if self.show_all_cho_data:
            figures["fig_all"] = self._figure_all()
        return figures

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types.

        The color is the one of the daily dose, twice a day is dashed.
        """
        for intervention, (dose, _, task_key, _, per_day, _) in self.group_info.items():
            self.plot_FH_results(
                ax=ax,
                label=f"sim: {self.labels_ldlc[intervention]}",
                color=dose,
                linestyle="dashed" if per_day == 2 else "solid",
                df=self.create_FH_results(task_key=task_key),
            )

    def _plot_data(
        self,
        ax: Axes,
        dset_prefix: str,
        labels: dict[str, str],
        count_separator: str = "\n",
    ) -> None:
        """Plot the data of the groups.

        The number of subjects is the one of the last time point.
        """
        for intervention, (dose, marker, *_) in self.group_info.items():
            dataset = self._datasets[self.to_sid(f"{dset_prefix}_{intervention}")]
            count = int(dataset["count"][dataset["time"].idxmax()])
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                dataset["mean_sd"],
                marker=marker,
                color=color,
                label=f"{self.sid}: {labels[intervention]}{count_separator}(n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                linestyle="None",
            )

    def _plot_fig1(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of Fig 1, the 10 and 40 mg/day groups."""
        for intervention, group in self.fig1_groups.items():
            dataset = self._datasets[self.to_sid(f"Fig1_ldl-c_{intervention}")]
            count = int(dataset["count"][dataset["time"].idxmax()])
            color = self.colormap_SV_dose(self.group_info[group][0])
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                dataset["mean_sd"],
                marker="o",
                color=color,
                label=f"{self.sid} Fig1: {self.labels_ldlc[group]} (n={count})",
                markerfacecolor="white",
                markeredgecolor=color,
                markersize=8,
                linestyle="None",
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        fig.set_size_inches(14, 6)
        self._plot_simulations(ax)
        self._plot_data(ax, "Tab2_ldl-c", self.labels_ldlc, count_separator=" ")
        self._plot_fig1(ax)
        ax.set_xlim((-0.2, 4.2))
        ax.set_ylim((0.0, 14))
        ax.legend(
            ncol=2, loc="upper left", bbox_to_anchor=(1.01, 1.0), prop={"size": 9}
        )
        fig.tight_layout()
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _figure_all(self) -> FigureMPL:
        """The lipids of the data and the LDL cholesterol of the simulations.

        One legend for the four panels, the groups have the same markers.
        """
        kwargs: FontKwargs = {"weight": "bold", "size": 16}
        fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(
            nrows=2, ncols=2, sharex="col", figsize=(22, 9)
        )
        fig.subplots_adjust(
            bottom=0.1, top=0.95, left=0.06, right=0.72, hspace=0.05, wspace=0.2
        )
        ax3.set_xlabel("Time [weeks]", **kwargs)
        ax4.set_xlabel("Time [weeks]", **kwargs)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("HDL-C [mM]", **kwargs)
        ax3.set_ylabel("Total cholesterol [mM]", **kwargs)
        ax4.set_ylabel("Triglycerides [mM]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "Tab2_ldl-c", self.labels_ldlc, count_separator=" ")
        self._plot_data(ax3, "Tab2_cholesterol", self.labels_ldlc)
        self._plot_data(ax2, "Tab3_hdl-c", self.labels_ldlc)
        self._plot_data(ax4, "Tab3_triglyceride", self.labels_ldlc)

        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim((-0.5, 4.5))
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 16))
        ax2.set_ylim((0.0, 2))
        ax3.set_ylim((0.0, 16))
        ax4.set_ylim((0.0, 6))
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(
            handles, labels, loc="center left", bbox_to_anchor=(0.73, 0.5), fontsize=11
        )
        return fig
