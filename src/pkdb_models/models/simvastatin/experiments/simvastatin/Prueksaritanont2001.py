"""Simulation experiment of the study Prueksaritanont2001."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    SimvastatinSimulationExperiment,
)


class Arm(NamedTuple):
    """An arm of the two studies."""

    #: the figure of the data
    fig_id: str
    #: the intervention of the data
    intervention: str
    #: the daily dose of simvastatin [mg]
    dose: float
    #: the coadministered substance
    coadministration: Coadministration
    #: the label and the line style
    label: str
    linestyle: str
    #: the suffix of the keys of the fit mappings
    suffix: str


class Prueksaritanont2001(SimvastatinSimulationExperiment):
    """Simulation experiment of Prueksaritanont2001.

    Two randomized crossover studies in 12 healthy volunteers each, every dose
    at 8:00 with a standard breakfast. Study 1 (51 - 89 kg): simvastatin 40 mg
    once daily for 10 days alone (control), or on days 15 - 24 of troglitazone
    400 mg/day. Study 2 (64 - 93 kg): simvastatin 80 mg once daily for 10 days
    alone (control), or on days 15 - 24 of pioglitazone 45 mg/day. Plasma on
    the last day of simvastatin, HMG-CoA reductase inhibitors by an enzymatic
    assay before (active inhibitors) and after a base hydrolysis (total
    inhibitors), mean and SD. Time 0 is the last dose.
    """

    #: the arms of the studies
    arms: ClassVar[dict[str, Arm]] = {
        "study1_control": Arm(
            "Fig1", "SIM_1", 40, Coadministration.NONE, "40 mg", "solid", "1"
        ),
        "study1_troglitazone": Arm(
            "Fig1",
            "SIM_1,TRO",
            40,
            Coadministration.TROGLITAZONE,
            "40 mg, troglitazone",
            "dotted",
            "1_indu",
        ),
        "study2_control": Arm(
            "Fig3", "SIM_2", 80, Coadministration.NONE, "80 mg", "solid", "2"
        ),
        "study2_pioglitazone": Arm(
            "Fig3",
            "SIM_2,PIO",
            80,
            Coadministration.PIOGLITAZONE,
            "80 mg, pioglitazone",
            "dashdotdotted",
            "2_no_interaction",
        ),
    }

    #: Troglitazone induces CYP3A4 (PXR). 400 mg/day for 24 days decreased the
    #: AUC of the active inhibitors to 0.62 and of the total inhibitors to 0.59
    #: of the control (Cmax 0.70 and 0.71); the lactone was not measured. It
    #: decreases terfenadine, a substrate of CYP3A4 with a high first pass, by
    #: 50 - 70 % (Rezulin label). An activity of 1.8 of the reference in liver
    #: and gut gives simvastatin 0.40-fold in the model; the inhibitors react
    #: weaker in the model (total 0.80-fold, the lumped metabolites are products
    #: of CYP3A4). Not fitted, the arm is validation data.
    f_cyp3a4_troglitazone: ClassVar[float] = 1.8

    #: the number of daily doses of simvastatin
    number: ClassVar[int] = 10

    #: the inhibitors: the substance of the data, the selection and the color
    analytes: ClassVar[list[tuple[str, str, str]]] = [
        ("active simva inhibitors", "Cve_active_inhibitors", "activesimvainhibitors"),
        ("total simva inhibitors", "Cve_total_inhibitors", "totalsimvainhibitors"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "active simva inhibitors":
                    dset.unit_conversion("mean", 1 / self.Mr.ActiveInh)
                elif substance == "total simva inhibitors":
                    dset.unit_conversion("mean", 1 / self.Mr.TotalInh)

                for key, arm in self.arms.items():
                    if arm.fig_id == fig_id:
                        dsets[self.to_sid(f"{fig_id}_{substance}_{key}")] = dset[
                            dset.intervention == arm.intervention
                        ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Daily oral doses of 40 mg (study 1) and 80 mg (study 2) simvastatin.

        The last dose at time 0. Pioglitazone does not interact (ratios 0.91 -
        1.03), its arm has the changes of the control.
        """
        changes = {
            Coadministration.NONE: self.default_changes(),
            Coadministration.TROGLITAZONE: self.cyp3a4_changes(
                self.f_cyp3a4_troglitazone
            ),
            Coadministration.PIOGLITAZONE: self.default_changes(),
        }
        return {
            f"simva_po_{key}": self.multiple_doses(
                dose=Q(arm.dose, "mg"),
                number=self.number,
                interval=DAY,
                time_shift=-(self.number - 1) * DAY,
                changes=changes[arm.coadministration],
            )
            for key, arm in self.arms.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(coadministration: Coadministration) -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.MULTIPLE,
                health=Health.HEALTHY,
                fasting=Fasting.FED,
                coadministration=coadministration,
            )

        mappings = {}
        for key, arm in self.arms.items():
            for substance, yid, _ in self.analytes:
                prefix = (
                    "activeInhibitors" if "active" in substance else "totalInhibitors"
                )
                mappings[f"fm_{prefix}{arm.suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{arm.fig_id}_{substance}_{key}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_simva_po_{key}", xid="time", yid=yid
                    ),
                    metadata=metadata(arm.coadministration),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Active and total simvastatin inhibitors of the two studies."""
        figures = {}
        for key, arms in [
            ("control_study1", ["study1_control"]),
            ("troglitazone_study1", ["study1_control", "study1_troglitazone"]),
            ("control_study2", ["study2_control"]),
            ("pioglitazone_study2", ["study2_control", "study2_pioglitazone"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(
                self.info.activesimvainhibitors.axis,
                self.info.activesimvainhibitors.unit,
            )
            plots[1].set_yaxis(
                self.info.totalsimvainhibitors.axis, self.info.totalsimvainhibitors.unit
            )

            for k, (substance, yid, color_key) in enumerate(self.analytes):
                for arm_key in arms:
                    arm = self.arms[arm_key]
                    plots[k].add_data(
                        task=f"task_simva_po_{arm_key}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {arm.label}",
                        color=self.colors_simva[color_key],
                        linestyle=arm.linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"{arm.fig_id}_{substance}_{arm_key}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[color_key],
                        linestyle=arm.linestyle,
                        label=f"{self.sid}: {arm.label}",
                    )
            for plot in plots:
                xaxis = plot.xaxis
                if xaxis is not None:  # set by `create_plots`
                    xaxis.min = -2
                    xaxis.max = 25
            figures[f"fig_{key}"] = fig
        return figures
