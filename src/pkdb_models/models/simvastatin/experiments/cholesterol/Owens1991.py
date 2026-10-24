"""Simulation experiment of the study Owens1991."""

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
from sbmlsim.simulation import Change, Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)


class Owens1991(SimvastatinSimulationExperiment):
    """Simulation experiment of Owens1991.

    27 patients with primary hypercholesterolemia (total cholesterol > 6.5 mM,
    triglycerides < 2.0 mM, no familial hypercholesterolemia) after a 4-week
    placebo run-in, randomized to simvastatin (n = 12), pravastatin (n = 10) or
    placebo (n = 5) for 12 weeks. Simvastatin 10 mg/day, raised to 20 mg/day
    after 4 weeks and to 40 mg/day after 8 weeks if the total cholesterol stayed
    above 5.2 mM. Fig 1 shows the LDL-C of the patients by their final dose
    (20 mg/day n = 6, 40 mg/day n = 4; the text: 7 x 20 and 4 x 40 mg) and of
    placebo, every 4 weeks, without error bars. The groups are defined by the
    response (the 40 mg/day patients are the ones whose cholesterol fell less),
    the difference between the groups is not a dose response. The simulations
    titrate as the groups: 10 mg/day in weeks 0 - 4 and 20 mg/day in weeks
    4 - 12, or 10, 20 and 40 mg/day in weeks 0 - 4, 4 - 8 and 8 - 12. The
    patients are not familial hypercholesterolemia, the presimulation with a FH
    type gives their baseline LDL-C.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    interventions: ClassVar[list[str]] = ["SIM20", "SIM40", "placebo"]

    #: the groups: intervention of the data, task key of the simulations, dose [mg]
    #: and label of the data
    group_info: ClassVar[list[tuple[str, str, int, str]]] = [
        ("placebo", "placebo", 0, "placebo"),
        ("SIM20", "20mg", 20, "SV 10mg, from week 4 20mg"),
        ("SIM40", "40mg", 40, "SV 10mg, from week 4 20mg,\nfrom week 8 40mg"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                for intervention in self.interventions:
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Daily doses for 12 weeks, the dose raised every 4 weeks."""
        n_4weeks = 4 * 7

        def phases(*doses_mg: float) -> list[Change]:
            """Daily doses [mg] of the 4-week phases from week 0."""
            return [
                self.doses(Q(dose, "mg"), n_4weeks, start=WEEK + k * 4 * WEEK)
                for k, dose in enumerate(doses_mg)
            ]

        # regimen and baseline LDL cholesterol [mM] (Fig 1)
        regimens: dict[str, tuple[list[Change], float]] = {
            "placebo": ([], 5.0182643),
            "20mg": (phases(10, 20, 20), 5.900709),
            "40mg": (phases(10, 20, 40), 6.440729),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (changes, ldlc_init) in regimens.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + 12 * WEEK,
                    dt=DAY / 100,
                    changes=changes,
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the groups (Fig 1, no error bars)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.SERUM,
            route=Route.PO,
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

    def _plot_data(self, ax: Axes, substance: str) -> None:
        """Plot the data of a substance of the groups.

        The number of subjects is the one of the last time point.
        """
        for intervention, _, dose, label in self.group_info:
            dataset = self._datasets[self.to_sid(f"Fig1_{substance}_{intervention}")]
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
        fig.set_size_inches(14, 6)
        self._plot_simulations(ax)
        self._plot_data(ax, "ldl-c")
        ax.set_xlim((-1, 13))
        ax.set_ylim((0.0, 8))
        ax.legend(
            ncol=1, loc="upper left", bbox_to_anchor=(1.01, 1.0), prop={"size": 11}
        )
        ax.tick_params(axis="both", labelsize=18)
        fig.tight_layout()
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
        self._plot_data(ax1, "ldl-c")
        self._plot_data(ax2, "cholesterol")

        for ax in [ax1, ax2]:
            ax.set_xlim((-1, 15))
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 9))
        ax2.set_ylim((0.0, 11))
        return fig
