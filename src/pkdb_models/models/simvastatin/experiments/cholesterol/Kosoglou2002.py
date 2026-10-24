"""Simulation experiment of the study Kosoglou2002."""

from typing import ClassVar, override

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
    DAY,
    WEEK,
    SimvastatinSimulationExperiment,
)


class Kosoglou2002(SimvastatinSimulationExperiment):
    """Simulation experiment of Kosoglou2002.

    Two single centre, randomized, evaluator-blind, parallel studies in 82
    otherwise healthy hypercholesterolemic men (LDL-C >= 130 mg/dl) on the NCEP
    step I diet, inpatients for 16 days: study 1 placebo (n=11) or simvastatin
    10 mg (n=12) (or with ezetimibe 0.25, 1 or 10 mg), study 2 simvastatin
    20 mg (n=8) (or ezetimibe 10 mg, alone or with simvastatin), once daily in
    the morning after a fast of >= 10 h, days 1 to 14. The serum lipids were
    taken before the dose of days 1 (baseline), 7, 14 and 15; the day 14 sample
    of Table 4 is before the 14th dose, 13 days after the first dose. The
    arms with ezetimibe are not simulated (no inhibition of the cholesterol
    absorption in the model). Table 3 has the steady state pharmacokinetics of
    simvastatin and its acid at day 14 (10 mg), not used.
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: intervention of the data, task key of the simulations, dose [mg]
    #: and label
    group_info: ClassVar[list[tuple[str, str, int, str]]] = [
        ("placebo", "placebo", 0, "placebo"),
        ("SIM10", "10mg", 10, "SV 10mg"),
        ("SIM20", "20mg", 20, "SV 20mg"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab4"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "cholesterol":
                    dset.unit_conversion("mean", 1 / self.Mr.cho)
                elif substance == "hdl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.hdlc)
                elif substance == "ldl-c":
                    dset.unit_conversion("mean", 1 / self.Mr.ldlc)
                for intervention in df.intervention.unique():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM]
        tcs_dict = {
            "simva_po_placebo": (Q(0, "mg"), 164 / self.Mr.ldlc.m * 10),
            "simva_po_10mg": (Q(10, "mg"), 167.5 / self.Mr.ldlc.m * 10),
            "simva_po_20mg": (Q(20, "mg"), 157.8 / self.Mr.ldlc.m * 10),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + 14 * DAY,
                    dt=DAY / 50,
                    changes=[self.doses(dose, 14)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of placebo and simvastatin alone (Table 4, days 0 and 13)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.SERUM,
            route=Route.PO,
            application_form=ApplicationForm.NR,
            dosing=Dosing.MULTIPLE,
            fasting=Fasting.FASTED,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{intervention}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab4_ldl-c_{intervention}"),
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
            for intervention, task_key, _, _ in self.group_info
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

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
        """Plot the data of a substance of the groups over the time [weeks].

        The number of subjects is the one of the last time point.
        """
        for intervention, _, dose, label in self.group_info:
            dataset = self._datasets[self.to_sid(f"Tab4_{substance}_{intervention}")]
            count = dataset["count"][dataset["time"].idxmax()]
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"] / 7,
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
        ax.set_xlim((-0.1, 2.2))
        ax.set_ylim((0.0, 6))
        ax.legend(ncol=2, loc="lower left", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig
