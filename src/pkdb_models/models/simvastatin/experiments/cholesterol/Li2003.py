"""Simulation experiment of the study Li2003."""

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


class Li2003(SimvastatinSimulationExperiment):
    """Simulation experiment of Li2003.

    42 Chinese patients with mixed hypercholesterolemia (LDL-C >= 160 mg/dl,
    TG <= 300 mg/dl), many with coronary heart disease and comedication (calcium
    channel blockers, nitrates), on an AHA step I diet, randomized to simvastatin
    20 or 40 mg once daily (tablets, n = 21 each) for 2 weeks. Fasting blood
    samples at day 0 and day 14, 8 - 12 h after the evening dose; LDL-C by the
    Friedewald formula, mean +- SD (Table 2). The 14 doses are given at days 0 to
    13, the sample of day 14 is before the next dose. The patients are not
    familial hypercholesterolemia, the presimulation with a FH type gives their
    baseline LDL-C.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the interventions of the datasets and their name in the data
    interventions: ClassVar[dict[str, str]] = {
        "SIM20": "SIM_20mg",
        "SIM40": "SIM_40mg",
    }

    #: the doses [mg]
    doses_mg: ClassVar[list[int]] = [20, 40]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "hdl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.hdlc)
                elif substance == "ldl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.ldlc)
                elif substance == "cholesterol":
                    dset.unit_conversion("mean", 1 / self.Mr.cho)
                for intervention, name in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == name
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM] (Table 2, 165 and 163 mg/dl)
        tcs_dict = {
            "simva_po_20mg": (Q(20, "mg"), 165 / self.Mr.ldlc.m * 10),
            "simva_po_40mg": (Q(40, "mg"), 163 / self.Mr.ldlc.m * 10),
        }
        # once daily at days 0 to 13, the last sample at day 14
        number = 2 * 7
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + number * DAY,
                    dt=DAY / 50,
                    changes=[self.doses(dose, number)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the doses (Table 2, day 0 and 14)."""
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
            f"fm_ldlc_SIM{dose}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab2_ldl-c_SIM{dose}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
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

    def _plot_data(self, ax: Axes, substance: str) -> None:
        """Plot the data of a substance of the doses over the time [weeks].

        The number of subjects is the one of the last time point.
        """
        for dose in self.doses_mg:
            dataset = self._datasets[self.to_sid(f"Tab2_{substance}_SIM{dose}")]
            count = dataset["count"][dataset["time"].idxmax()]
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"] / 7,
                dataset["mean"],
                dataset["mean_sd"],
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
        self._plot_data(ax, "ldl-c")
        ax.set_xlim((-0.1, 2.5))
        ax.set_ylim((0.0, 8))
        ax.legend(ncol=1, loc="best", prop={"size": 12})
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
        ax2.set_ylabel("Total cholesterol [mM]", **kwargs)
        ax3.set_ylabel("HDL-C [mM]", **kwargs)
        ax4.set_ylabel("Triglycerides [mg/dl]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "ldl-c")
        self._plot_data(ax2, "cholesterol")
        self._plot_data(ax3, "hdl-c")
        self._plot_data(ax4, "triglyceride")

        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim((-0.1, 2.2))
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 6))
        ax2.set_ylim((0.0, 16))
        ax3.set_ylim((0.0, 3))
        ax4.set_ylim((0.0, 203))
        return fig
