"""Simulation experiment of the study Mol1988."""

from typing import ClassVar, override

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
    SimvastatinSimulationExperiment,
)


class Mol1988(SimvastatinSimulationExperiment):
    """Simulation experiment of Mol1988.

    Open 24-week extension of Mol1986: 38 patients with heterozygous familial
    hypercholesterolemia (FH) on a diet, 2 - 4 weeks without therapy, then
    simvastatin 10 mg twice daily in weeks 0 - 8 and 20 mg twice daily in weeks
    8 - 16; group 1 (n = 10) 20 mg twice daily until week 24, group 2 (n = 20)
    40 mg once daily before the evening meal in weeks 16 - 24, group 3 (n = 8)
    20 mg twice daily until week 20 and 40 mg once daily in weeks 20 - 24.
    Fasting samples every 4 weeks, LDL-C by the Friedewald formula, mean +- SD;
    the baseline is the one of the dose-finding study (Mol1986). Table 1 has
    all patients (n = 38), weeks 0 - 24; the patients have the same regimen until
    week 16, the data of weeks 0 - 16 are simulated with the baseline of all
    patients. Table 2 has the groups at weeks 0, 12, 16, 20 and 24, each group is
    simulated with its baseline.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: baseline LDL-C [mM] (Table 1 and 2), end of the simulation
    #: [weeks], label, color and marker
    group_info: ClassVar[dict[str, tuple[float, int, str, str, str]]] = {
        "all": (
            9.70,
            16,
            "all: SV 10mg twice daily (weeks 0-8),\n20mg twice daily (weeks 8-16)",
            "black",
            "o",
        ),
        "group1": (
            10.03,
            24,
            "group 1: SV 20mg twice daily (weeks 16-24)",
            "tab:blue",
            "D",
        ),
        "group2": (
            9.39,
            24,
            "group 2: SV 40mg once daily (weeks 16-24)",
            "tab:orange",
            "s",
        ),
        "group3": (
            10.05,
            24,
            "group 3: SV 20mg twice daily (weeks 16-20),\n40mg once daily (weeks 20-24)",
            "tab:green",
            "^",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        # the patients of Table 1 have a common regimen until week 16
        for substance, df in self.load_dataframes_by_substance("Tab1").items():
            dset = DataSet.from_df(df, self.ureg)
            dsets[self.to_sid(f"Tab1_{substance}_all")] = dset[dset.time <= 16]
        for substance, df in self.load_dataframes_by_substance("Tab2").items():
            dset = DataSet.from_df(df, self.ureg)
            for group in df.group.unique():
                dsets[self.to_sid(f"Tab2_{substance}_{group}")] = dset[
                    dset.group == group
                ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """The regimens of all patients until week 16 and of the groups."""
        bid = DAY / 2
        n_4weeks_bid = 2 * 4 * 7
        n_4weeks_qd = 4 * 7

        def common() -> list[Change]:
            """10 mg twice daily in weeks 0 - 8, 20 mg twice daily in weeks 8 - 16."""
            return [
                self.doses(Q(10, "mg"), 2 * n_4weeks_bid, interval=bid),
                self.doses(
                    Q(20, "mg"), 2 * n_4weeks_bid, start=WEEK + 8 * WEEK, interval=bid
                ),
            ]

        week16 = WEEK + 16 * WEEK
        week20 = WEEK + 20 * WEEK
        regimens: dict[str, list[Change]] = {
            "all": common(),
            "group1": [
                *common(),
                self.doses(Q(20, "mg"), 2 * n_4weeks_bid, start=week16, interval=bid),
            ],
            "group2": [
                *common(),
                self.doses(Q(40, "mg"), 2 * n_4weeks_qd, start=week16, interval=DAY),
            ],
            "group3": [
                *common(),
                self.doses(Q(20, "mg"), n_4weeks_bid, start=week16, interval=bid),
                self.doses(Q(40, "mg"), n_4weeks_qd, start=week20, interval=DAY),
            ],
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for group, changes in regimens.items():
            ldlc_init, end_weeks, *_ = self.group_info[group]
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{group}_{fh_type_key}")] = self.presim(
                    end=WEEK + end_weeks * WEEK,
                    dt=DAY / 50,
                    changes=changes,
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of all patients (Table 1) and of the groups (Table 2)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.SERUM,
            route=Route.PO,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{group}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(
                        f"Tab1_ldl-c_{group}"
                        if group == "all"
                        else f"Tab2_ldl-c_{group}"
                    ),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{group}_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=metadata,
            )
            for group in self.group_info
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _plot_group(self, ax: Axes, group: str) -> None:
        """Plot the simulation (mean and range of the FH types) and the data."""
        _, _, label, color, marker = self.group_info[group]
        df = self.create_FH_results(task_key=group)
        ax.fill_between(df["time"], df["min"], df["max"], facecolor=color, alpha=0.3)
        ax.plot(df["time"], df["mean"], label=f"sim: {label}", color=color)

        fig_id = "Tab1" if group == "all" else "Tab2"
        dataset = self._datasets[self.to_sid(f"{fig_id}_ldl-c_{group}")]
        # the number of subjects of the last time point
        count = int(dataset["count"][dataset["time"].idxmax()])
        ax.errorbar(
            dataset["time"],
            dataset["mean"],
            dataset["mean_sd"],
            color=color,
            label=f"{self.sid} {fig_id}: {label.split(':')[0]} (n={count})",
            markerfacecolor=color,
            markeredgecolor="black",
            markersize=8,
            marker=marker,
            linestyle="None",
        )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        fig.set_size_inches(14, 6)
        for group in self.group_info:
            self._plot_group(ax, group)
        ax.set_xlim((-1, 25))
        ax.set_ylim((0.0, 14))
        ax.legend(
            ncol=1, loc="upper left", bbox_to_anchor=(1.01, 1.0), prop={"size": 10}
        )
        ax.tick_params(axis="both", labelsize=18)
        fig.tight_layout()
        return fig
