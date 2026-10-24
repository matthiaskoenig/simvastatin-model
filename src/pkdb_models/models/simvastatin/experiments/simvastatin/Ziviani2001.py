"""Simulation experiment of the study Ziviani2001."""

from typing import ClassVar, override

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
    SimvastatinSimulationExperiment,
)


class Ziviani2001(SimvastatinSimulationExperiment):
    """Simulation experiment of Ziviani2001.

    Oral doses of 40 mg simvastatin once daily in the morning for 8 days in 18
    healthy subjects (17 completed), alone (control) or with lacidipine 4 mg
    once daily, a crossover. On day 8 the dose after a fast of 10 hr, plasma
    0 - 24 hr after it. The assay measures the total simvastatin acid, the acid
    and the lactone after alkaline hydrolysis (`Cve_simva_and_simacid`, the
    data converted with the molecular weight of the acid). Mean and SD.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "lacidipine": ("SIM,LAC", "lacidipine", "dashed"),
    }

    #: Lacidipine is a weak inhibitor of CYP3A4 and a substrate of it with an
    #: extensive first pass; at 4 mg its plasma concentrations are low (a few
    #: ng/ml), the inhibition is intestinal. It increased the AUC(0-24) of the
    #: total acid to 1.35 and its Cmax to 1.69 of the control (geometric means,
    #: the half-life unchanged: a first pass effect). An intestinal CYP3A4
    #: activity of 0.65 gives an AUC of 1.32 of the control in the model (the
    #: Cmax as well, the model has the same ratio for both). Not fitted, the
    #: arm is validation data.
    f_cyp3a4_gu_lacidipine: ClassVar[float] = 0.65

    #: the number of doses and the dosing interval [min]
    number: ClassVar[int] = 8
    interval: ClassVar[float] = 24 * 60

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simva+simacid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)

                for arm, (intervention, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Oral doses of 40 mg simvastatin once daily, the last dose at time 0."""
        changes = {
            "control": self.default_changes(),
            "lacidipine": self.cyp3a4_changes(
                1.0, f_cyp3a4_gu=self.f_cyp3a4_gu_lacidipine
            ),
        }
        return {
            f"simva_po_{arm}": self.multiple_doses(
                dose=Q(40, "mg"),
                number=self.number,
                interval=self.interval,
                time_shift=-(self.number - 1) * self.interval,
                changes=changes[arm],
            )
            for arm in self.arms
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        coadministrations = {
            "control": Coadministration.NONE,
            "lacidipine": Coadministration.LACIDIPINE,
        }
        mappings = {}
        for arm, coadministration in coadministrations.items():
            suffix = "" if arm == "control" else f"_{arm}"
            mappings[f"fm_simva_and_simacid{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig2_simva+simacid_{arm}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_simva_po_{arm}",
                    xid="time",
                    yid="Cve_simva_and_simacid",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministration,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """The total acid after the last dose, alone and with lacidipine."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("lacidipine", ["control", "lacidipine"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=1,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_one_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit, min=-1, max=25),
                legend=True,
            )
            plots[0].set_yaxis(
                self.info.simva_and_simacid.axis, self.info.simva_and_simacid.unit
            )
            for arm in arms:
                _, label, linestyle = self.arms[arm]
                plots[0].add_data(
                    task=f"task_simva_po_{arm}",
                    xid="time",
                    yid="Cve_simva_and_simacid",
                    label=f"sim: {label}",
                    color=self.colors_simva["simva_and_simacid"],
                    linestyle=linestyle,
                )
                plots[0].add_data(
                    dataset=self.to_sid(f"Fig2_simva+simacid_{arm}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    color=self.colors_simva["simva_and_simacid"],
                    linestyle=linestyle,
                    label=f"{self.sid}: {label}",
                )
            figures[f"fig_{key}"] = fig

        return figures
