"""Simulation experiment of the study Moelgaard1988."""

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


class Moelgaard1988(SimvastatinSimulationExperiment):
    """Simulation experiment of Moelgaard1988.

    21 Swedish patients with or at high risk of coronary heart disease on an AHA
    phase 1 diet: 11 with heterozygous familial hypercholesterolemia (FH) and 10
    with polygenic hypercholesterolemia (P-HC, LDL-C > 4.3 mM on diet).
    Simvastatin capsules twice daily, before breakfast and dinner: the FH
    patients 10 mg twice daily in weeks 0 - 8 and 20 mg twice daily in weeks
    8 - 24, the P-HC patients 10 mg twice daily for 24 weeks. Fasting samples
    every 4 weeks, LDL-C by ultracentrifugation and precipitation, mean +- SEM
    (Table 1: FH, Table 2: P-HC; the digitized Fig 1 and Fig 2 show the same
    values less exactly and are not used). The P-HC patients are not familial
    hypercholesterolemia, the presimulation with a FH type gives their baseline
    LDL-C.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: table of the data, task key of the simulations, daily dose of
    #: the color [mg] and label
    group_info: ClassVar[list[tuple[str, str, int, str]]] = [
        ("Tab1", "FH_trial", 40, "SV 10mg, 20mg twice daily, FH"),
        ("Tab2", "PHC_trial", 20, "SV 10mg twice daily, P-HC"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1", "Tab2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                # a table has the data of one group of patients
                assert df.group.nunique() == 1, df.group.unique()
                dsets[self.to_sid(f"{fig_id}_{substance}")] = DataSet.from_df(
                    df, self.ureg
                )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Twice daily doses of simvastatin in the two groups of patients.

        A dose every 12 hr from week 0; the FH patients 10 mg in weeks 0 - 8 and
        20 mg in weeks 8 - 24, the P-HC patients 10 mg in weeks 0 - 24. The
        baseline LDL cholesterol is the one of week 0 (Table 1 and 2).
        """
        interval = DAY / 2
        n_8weeks = 2 * 8 * 7
        n_16weeks = 2 * 16 * 7
        end = WEEK + 24 * WEEK
        regimens = {
            # P-HC: 10 mg twice daily for 24 weeks
            "PHC_trial": (
                4.97,
                [self.doses(Q(10, "mg"), n_8weeks + n_16weeks, interval=interval)],
            ),
            # FH: 10 mg twice daily for 8 weeks, then 20 mg twice daily
            "FH_trial": (
                8.87,
                [
                    self.doses(Q(10, "mg"), n_8weeks, interval=interval),
                    self.doses(
                        Q(20, "mg"),
                        n_16weeks,
                        start=WEEK + 8 * WEEK,
                        interval=interval,
                    ),
                ],
            ),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (ldlc_init, changes) in regimens.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{key}_{fh_type_key}")] = self.presim(
                    end=end,
                    dt=DAY / 50,
                    changes=changes,
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the two groups (Table 1 and 2)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.CAPSULE,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{task_key}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"{fig_id}_ldl-c"),
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
            for fig_id, task_key, _, _ in self.group_info
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
        for fig_id, _, dose, label in self.group_info:
            dataset = self._datasets[self.to_sid(f"{fig_id}_{substance}")]
            count = int(dataset["count"][dataset["time"].idxmax()])
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                dataset["mean_sd"],
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
        self._plot_data(ax, "ldl-c")
        ax.set_xlim((-1, 25))
        ax.set_ylim((0.0, 13))
        ax.legend(ncol=1, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _figure_all(self) -> FigureMPL:
        """The lipids of the data and the LDL cholesterol of the simulations."""
        kwargs: FontKwargs = {"weight": "bold", "size": 16}
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(22, 6))
        fig.subplots_adjust(bottom=0.12, top=0.925, left=0.05, right=0.98)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("Total cholesterol [mM]", **kwargs)
        ax3.set_ylabel("Apolipoprotein B [g/l]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "ldl-c")
        self._plot_data(ax2, "cholesterol")
        self._plot_data(ax3, "apoB100+48")

        for ax in [ax1, ax2, ax3]:
            ax.set_xlabel("Time [weeks]", **kwargs)
            ax.set_xlim((-1, 25))
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 13))
        ax2.set_ylim((0.0, 16))
        ax3.set_ylim((0.0, 3))
        return fig
