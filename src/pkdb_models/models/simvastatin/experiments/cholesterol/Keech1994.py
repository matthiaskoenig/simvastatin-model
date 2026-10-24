"""Simulation experiment of the study Keech1994."""

from typing import ClassVar, override

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
    SimvastatinSimulationExperiment,
)

#: the last time of the early response [weeks]: the screening at -8 weeks and the
#: first visit after the randomization at 8 weeks
EARLY_END = 8


class Keech1994(SimvastatinSimulationExperiment):
    """Simulation experiment of Keech1994 (Oxford Cholesterol Study).

    Single centre, randomized, double-blind, 3 years: 621 patients at an
    increased risk of coronary heart disease (prior myocardial infarction,
    angina, vascular disease, treated diabetes or hypertension; total
    cholesterol >= 3.5 mM), 8 weeks of placebo run-in after the screening, then
    simvastatin 40 mg (two 20 mg tablets, n=206), 20 mg (n=208) or placebo
    (n=207) every evening. Non-fasting blood at the screening (-8 weeks, no
    sample at the randomization) and at weeks 8, 20, 32, 44, 56, 68, 80, 104
    and 152 (Fig 1); the doses start at 0 weeks. The data are the intention to
    treat of the patients who attended (including those who stopped the
    treatment, and with a step down to half the dose for adverse events or a
    total cholesterol < 3 mM), which lowers the long term effect compared with
    the simulated full adherence. The model has no time of the day, the evening
    doses are doses every 24 h.
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: intervention of the data, task key of the simulations, dose [mg],
    #: label and number of randomized subjects (the number with results falls
    #: to about half at 3 years)
    group_info: ClassVar[list[tuple[str, str, int, str, int]]] = [
        ("placebo", "placebo", 0, "placebo", 207),
        ("SIM20", "20mg", 20, "SV 20mg", 208),
        ("SIM40", "40mg", 40, "SV 40mg", 206),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                for intervention in df.intervention.unique():
                    key = f"{fig_id}_{substance}_{intervention}"
                    dset_intervention = dset[dset.intervention == intervention]
                    dsets[self.to_sid(key)] = dset_intervention
                    # the early response (screening and 8 weeks) and the long
                    # term effect (20 to 152 weeks) of the fit mappings
                    dsets[self.to_sid(f"{key}_early")] = dset_intervention[
                        dset_intervention.time <= EARLY_END
                    ]
                    dsets[self.to_sid(f"{key}_late")] = dset_intervention[
                        dset_intervention.time > EARLY_END
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM]
        tcs_dict = {
            "simva_po_placebo": (Q(0, "mg"), 4.71643),
            "simva_po_20mg": (Q(20, "mg"), 4.85573),
            "simva_po_40mg": (Q(40, "mg"), 4.77612),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        # 9 weeks before the doses (the screening is at -8 weeks), then a daily
        # dose up to week 152, the last visit
        start = WEEK + 8 * WEEK
        number = 152 * 7 + 1
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=start + number * DAY,
                    dt=DAY / 10,
                    changes=[self.doses(dose, number, start=start)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-start,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of every group (Fig 1).

        The early response (screening and 8 weeks, `fm_ldlc_<group>_early`) and
        the long term effect (20 to 152 weeks, `fm_ldlc_<group>_late`).
        """
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.MULTIPLE,
            health=Health.HEART_DISEASE,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{intervention}_{period}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_ldl-c_{intervention}_{period}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count=count,
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{task_key}_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=metadata,
            )
            for intervention, task_key, _, _, count in self.group_info
            for period in ["early", "late"]
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        for intervention, task_key, dose, label, count in self.group_info:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: {label}",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=task_key),
            )
            dataset = self._datasets[self.to_sid(f"Fig1_ldl-c_{intervention}")]
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

        ax.set_xlim((-12, 160))
        ax.set_ylim((0.0, 10.5))
        ax.tick_params(axis="both", labelsize=18)
        ax.legend(ncol=2, loc="upper center", prop={"size": 11})
        return fig
