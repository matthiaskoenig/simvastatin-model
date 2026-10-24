"""Simulation experiment of the study Saito1991."""

from typing import ClassVar, NamedTuple, override

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


class Arm(NamedTuple):
    """A group of Saito1991."""

    #: intervention of the data
    intervention: str
    #: name of the group in the keys of the datasets and the simulations
    name: str
    #: dose [mg], 0 for placebo
    dose: float
    #: baseline LDL cholesterol [mg/dl] (Table 6, week 0)
    ldlc_init: float
    label: str
    marker: str
    linestyle: str


class Saito1991(SimvastatinSimulationExperiment):
    """Simulation experiment of Saito1991.

    Randomized double-blind placebo-controlled study in Japan, 150 patients with
    hyperlipidemia (15 % heterozygous familial): simvastatin 2.5 or 5 mg once
    daily in the morning or in the evening (double dummy, tablets after the
    morning and the evening meal) or placebo for 12 weeks, then placebo for 4
    weeks. Table 6 gives the LDL cholesterol at weeks 0, 4, 8, 12 and 16. The
    model has no time of the day: the morning and the evening groups differ only
    by their baseline, the doses are given every 24 h (the evening dosing
    lowered the LDL cholesterol 7 - 9 % more, a limitation of the model).
    """

    #: the FH type of the fit mappings, the reduced LDL clearance of a non
    #: familial hypercholesterolemia (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the weeks of the doses, followed by 4 weeks of placebo
    weeks_dosing: ClassVar[int] = 12

    arms: ClassVar[list[Arm]] = [
        Arm(
            "SIM2_5_morning, placebo_at_the_end",
            "2_5mg_morning",
            2.5,
            182.7,
            "SV 2.5mg morning",
            "s",
            "solid",
        ),
        Arm(
            "SIM2_5_evening, placebo_at_the_end",
            "2_5mg_evening",
            2.5,
            195.9,
            "SV 2.5mg evening",
            "o",
            "dashed",
        ),
        Arm(
            "SIM5_morning, placebo_at_the_end",
            "5mg_morning",
            5,
            194.2,
            "SV 5mg morning",
            "s",
            "solid",
        ),
        Arm(
            "SIM5_evening, placebo_at_the_end",
            "5mg_evening",
            5,
            204.3,
            "SV 5mg evening",
            "o",
            "dashed",
        ),
        Arm("placebo_complete", "placebo", 0, 200.2, "placebo", "s", "solid"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        """The LDL cholesterol of the groups.

        `Tab6_ldl-c_<group>` holds all weeks, the doses also the weeks of the
        doses (`_treatment`, weeks 0 to 12) and the week after the withdrawal
        (`_withdrawal`, week 16) on their own.
        """
        dsets = {}
        df = self.load_dataframes_by_substance("Tab6")["ldl-c"]
        dset = self.measurement_dataset(df, "concentration")
        dset.unit_conversion("mean", 1 / self.Mr.ldlc)
        for arm in self.arms:
            dset_arm = dset[dset.intervention == arm.intervention]
            dsets[self.to_sid(f"Tab6_ldl-c_{arm.name}")] = dset_arm
            if arm.dose > 0:
                dsets[self.to_sid(f"Tab6_ldl-c_{arm.name}_treatment")] = dset_arm[
                    dset_arm.time <= self.weeks_dosing
                ]
                dsets[self.to_sid(f"Tab6_ldl-c_{arm.name}_withdrawal")] = dset_arm[
                    dset_arm.time > self.weeks_dosing
                ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        tcsims: dict[str, Simulation | Scan] = {}
        # 12 weeks of daily doses and 4 weeks of withdrawal
        number = self.weeks_dosing * 7
        for arm in self.arms:
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{arm.name}_{fh_type_key}")] = self.presim(
                    end=WEEK + number * DAY + 4 * WEEK,
                    dt=DAY / 25,
                    changes=[self.doses(Q(arm.dose, "mg"), number)],
                    ldlc=arm.ldlc_init / self.Mr.ldlc.m * 10,  # [mM]
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the groups.

        The groups with doses have a mapping of the weeks of the doses
        (`_treatment`) and of the week after the withdrawal (`_withdrawal`).
        """
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.MULTIPLE,
            fasting=Fasting.FED,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        mappings = {}
        for arm in self.arms:
            parts = ["_treatment", "_withdrawal"] if arm.dose > 0 else [""]
            for part in parts:
                dset_key = self.to_sid(f"Tab6_ldl-c_{arm.name}{part}")
                mappings[f"fm_ldlc_{arm.name}{part}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=dset_key,
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        # the smallest number of subjects of the weeks
                        count=int(self._datasets[dset_key]["count"].min()),
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(
                            f"task_simva_po_{arm.name}_{self.fit_fh_type}"
                        ),
                        xid="time",
                        yid="[Cve_ldlc]",
                    ),
                    metadata=metadata,
                )
        return mappings

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data.

        The number of subjects is the one at baseline.
        """
        fig, ax = self.create_cholesterol_plot()
        for arm in self.arms:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: {arm.label}",
                color=arm.dose,
                linestyle=arm.linestyle,
                df=self.create_FH_results(task_key=arm.name),
            )

        for arm in self.arms:
            dataset = self._datasets[self.to_sid(f"Tab6_ldl-c_{arm.name}")]
            count = int(dataset["count"][dataset["time"].idxmin()])
            color = self.colormap_SV_dose(arm.dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                dataset["mean_sd"],
                color=color,
                label=f"{self.sid}: {arm.label} (n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker=arm.marker,
                linestyle="None",
            )

        ax.axvline(self.weeks_dosing, color="grey", linestyle="dotted")
        ax.set_xlim((-0.5, 17))
        ax.set_ylim((0.0, 7.5))
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), prop={"size": 10})
        ax.tick_params(axis="both", labelsize=18)
        return fig
