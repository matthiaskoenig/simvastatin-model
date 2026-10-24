"""Simulation experiment of the study Ntanios1999."""

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
from sbmlsim.simulation import Change, Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)


class Ntanios1999(SimvastatinSimulationExperiment):
    """Simulation experiment of Ntanios1999.

    18 hypercholesterolemic subjects (LDL-C > 4.16 mM, homozygous familial
    hypercholesterolemia excluded) after a 4-week washout on a NCEP step 1 diet,
    simvastatin 40 mg/day (n = 7) or 80 mg/day (n = 11) for 24 weeks; the
    subjects whose total cholesterol did not fall to a desirable value with
    40 mg/day were changed to 80 mg/day. The time of the change is not reported,
    the simulations assume the first visit, week 6. Samples every 6 weeks, LDL-C
    by the Friedewald formula, mean +- SD. Per dose only the baseline is reported
    (Table 3); Fig 1 shows all subjects (n = 18), they are simulated with the
    baseline of Table 5 (7.91 mM), 40 mg/day until week 6 and the mean daily dose
    of the subjects afterwards ((7 x 40 + 11 x 80) / 18 mg). The subjects are
    not familial hypercholesterolemia, the presimulation with a FH type gives
    their baseline LDL-C.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the number of subjects of the doses
    counts: ClassVar[dict[int, int]] = {40: 7, 80: 11}

    #: the change from 40 to 80 mg/day [weeks], assumed at the first visit
    titration_week: ClassVar[int] = 6

    #: the groups: task key, baseline LDL-C [mM], daily dose of the color [mg]
    #: and label
    group_info: ClassVar[list[tuple[str, float, float, str]]] = [
        ("40mg", 7.69, 40, "SV 40mg"),
        ("80mg", 8.12, 80, "SV 40mg (weeks 0-6), 80mg"),
        ("all", 7.91, 60, "all: SV 40mg (weeks 0-6), 40mg or 80mg"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for substance, df in self.load_dataframes_by_substance("Fig1").items():
            # a frame of a substance has a single intervention
            assert df.intervention.nunique() == 1, df.intervention.unique()
            dsets[self.to_sid(f"Fig1_{substance}")] = DataSet.from_df(df, self.ureg)
        for substance, df in self.load_dataframes_by_substance("Tab3").items():
            dset = DataSet.from_df(df, self.ureg)
            for group in df.group.unique():
                dsets[self.to_sid(f"Tab3_{substance}_{group}")] = dset[
                    dset.group == group
                ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Daily doses for 24 weeks, the change to 80 mg at week 6."""
        n_40 = self.titration_week * 7
        n_rest = (24 - self.titration_week) * 7
        start_rest = WEEK + self.titration_week * WEEK
        dose_all = sum(dose * count for dose, count in self.counts.items()) / sum(
            self.counts.values()
        )
        regimens: dict[str, list[Change]] = {
            "40mg": [self.doses(Q(40, "mg"), n_40 + n_rest)],
            "80mg": [
                self.doses(Q(40, "mg"), n_40),
                self.doses(Q(80, "mg"), n_rest, start=start_rest),
            ],
            "all": [
                self.doses(Q(40, "mg"), n_40),
                self.doses(Q(dose_all, "mg"), n_rest, start=start_rest),
            ],
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, ldlc_init, _, _ in self.group_info:
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + 24 * WEEK,
                    dt=DAY / 50,
                    changes=regimens[key],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of all subjects (Fig 1)."""
        return {
            "fm_ldlc_all": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid("Fig1_ldl-c"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_all_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.MULTIPLE,
                    health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
                    data=PKPDData.PD,
                    data_type=DataType.MEAN,
                ),
            )
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        figures = {"fig_cho": self._figure_cho()}
        if self.show_all_cho_data:
            figures["fig_all"] = self._figure_all()
        return figures

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for key, _, dose, label in self.group_info:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: {label}",
                color=dose,
                linestyle="dashed" if key == "all" else "solid",
                df=self.create_FH_results(task_key=key),
            )

    def _plot_data(self, ax: Axes, substance: str) -> None:
        """Plot the data of a substance: all subjects (Fig 1), the baselines (Table 3)."""
        dataset = self._datasets[self.to_sid(f"Fig1_{substance}")]
        count = int(dataset["count"][dataset["time"].idxmax()])
        color = self.colormap_SV_dose(60)
        ax.errorbar(
            dataset["time"],
            dataset["mean"],
            dataset["mean_sd"],
            color=color,
            label=f"{self.sid} Fig1: all (n={count})",
            markerfacecolor=color,
            markeredgecolor="black",
            markersize=8,
            marker="o",
            linestyle="None",
        )
        for dose, count in self.counts.items():
            dataset = self._datasets[self.to_sid(f"Tab3_{substance}_SIM{dose}")]
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                dataset["mean_sd"],
                color=color,
                label=f"{self.sid} Tab3: SV {dose}mg, baseline (n={count})",
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
        ax.legend(ncol=1, loc="best", prop={"size": 10})
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
        self._plot_data(ax1, "ldl-c")
        self._plot_data(ax2, "hdl-c")
        self._plot_data(ax3, "cholesterol")
        self._plot_data(ax4, "triglyceride")

        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim((-1, 25))
            ax.legend(ncol=1, loc="best", prop={"size": 10})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 13))
        ax2.set_ylim((0.0, 4.5))
        ax3.set_ylim((0.0, 13))
        ax4.set_ylim((0.0, 4.5))
        return fig
