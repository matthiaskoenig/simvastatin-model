"""Simulation experiment of the study Loria1993."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Fasting,
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
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)


class Loria1993(SimvastatinSimulationExperiment):
    """Simulation experiment of Loria1993.

    5 normolipidemic patients (LDL-C 97 mg/dl, 2.5 mM) 7 days after an elective
    cholecystectomy with a T-tube; the enterohepatic circulation was interrupted
    (bile drained) the night before, after a 12 h fast, and the patients fasted
    until 12 h after a single oral dose of 80 mg simvastatin (4 x 20 mg tablets)
    with intravenous fructose and saline. Plasma lipids at 0, 8 and 18 h, LDL-C
    by ultracentrifugation (LDL + IDL), mean +- SD (Table 2). The acute fall of
    the LDL-C (-20 % at 8 h) under the biliary diversion, the surgery and the
    fasting is outside the model (no biliary diversion, no coupling of the bile
    acid synthesis): the data are a validation of a limitation of the model.
    """

    #: the FH type of the fit mappings: the populations of the cholesterol
    #: studies are mostly not familial; the reduced internalization of LDL by
    #: the LDL receptor (FH_type4) stands for a reduced hepatic LDL clearance,
    #: its presimulation meets the baseline LDL cholesterol (FH_type1 is 1.5 %
    #: above it) and its response lies in the middle of the FH types
    fit_fh_type: ClassVar[str] = "FH_type4"

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab2", "Tab3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "cholesterol":
                    if fig_id == "Tab2":
                        dset.unit_conversion("mean", 1 / self.Mr.cho)
                elif substance == "vldl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.vldlc)
                elif substance == "hdl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.hdlc)
                elif substance == "ldl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.ldlc)
                # a frame of a substance has a single intervention
                assert df.intervention.nunique() == 1, df.intervention.unique()
                dsets[self.to_sid(f"{fig_id}_{substance}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        ldlc_init = 97 / self.Mr.ldlc.m * 10  # [mM]
        tcsims: dict[str, Simulation | Scan] = {}
        # a single dose of 80 mg, the samples up to 18 hr
        for fh_type_key in self.fh_types:
            tcsims[self.to_sid(f"simva_po_80mg_{fh_type_key}")] = self.presim(
                end=WEEK + 20 * 60,
                dt=20 * 60 / 50,
                changes=[self.doses(Q(80, "mg"), 1)],
                ldlc=ldlc_init,
                FH_type=fh_type_key,
                time_shift=-WEEK,
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol after the single dose (Table 2)."""
        return {
            "fm_ldlc_SIM80": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid("Tab2_ldl-c"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_80mg_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.CHOLECYSTECTOMY,
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
        """Plot the LDL cholesterol of the simulations over the time [hr]."""
        df = self.create_FH_results(task_key="80mg")
        df["time"] = df["time"] * 24 * 7  # convert from weeks to hours
        self.plot_FH_results(
            ax=ax, label="sim: SV 80mg", color=80, linestyle="solid", df=df
        )

    def _plot_data(self, ax: Axes, substance: str) -> None:
        """Plot the data of a substance.

        The number of subjects is the one of the last time point.
        """
        dataset = self._datasets[self.to_sid(f"Tab2_{substance}")]
        count = dataset["count"][dataset["time"].idxmax()]
        color = self.colormap_SV_dose(80)
        ax.errorbar(
            dataset["time"],
            dataset["mean"],
            dataset["mean_sd"],
            color=color,
            label=f"{self.sid}: SV 80mg (n={count})",
            markerfacecolor=color,
            markeredgecolor="black",
            markersize=8,
            marker="s",
            linestyle="None",
        )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        kwargs: FontKwargs = {"weight": "bold", "size": 20}
        fig, ax = self.create_cholesterol_plot()
        ax.set_xlabel("Time [hrs]", **kwargs)
        self._plot_simulations(ax)
        self._plot_data(ax, "ldl-c")
        ax.set_xlim((-1, 19))
        ax.set_ylim((0.0, 5))
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
        ax3.set_xlabel("Time [hrs]", **kwargs)
        ax4.set_xlabel("Time [hrs]", **kwargs)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("HDL-C [mM]", **kwargs)
        ax3.set_ylabel("Total cholesterol [mM]", **kwargs)
        ax4.set_ylabel("VLDL-C [mM]", **kwargs)

        self._plot_simulations(ax1)
        self._plot_data(ax1, "ldl-c")
        self._plot_data(ax3, "cholesterol")
        self._plot_data(ax2, "hdl-c")
        self._plot_data(ax4, "vldl-c")

        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_xlim((-1, 20))
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 8))
        ax2.set_ylim((0.0, 2))
        ax3.set_ylim((0.0, 11))
        ax4.set_ylim((0.0, 1))
        return fig
