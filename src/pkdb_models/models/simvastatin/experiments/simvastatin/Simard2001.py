"""Simulation experiment of the study Simard2001."""

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


class Simard2001(SimvastatinSimulationExperiment):
    """Simulation experiment of Simard2001.

    Oral doses of 20 mg simvastatin (Zocor tablets) every 12 hr in 11 healthy
    men, in a fixed sequence: cisapride 10 mg every 8 hr on days 1 - 3, then
    simvastatin with cisapride from the night of day 3 to the morning of day 7
    (8 doses), then simvastatin alone to the morning of day 11 (8 more doses,
    16 in all). Plasma 0 - 12 hr after the morning dose of day 7 (cisapride)
    and of day 11 (control), after an overnight fast. Mean and SD.

    Cisapride does not inhibit CYP3A4 here: simvastatin is unchanged (AUC 1.04
    of the control) and simvastatin acid decreased by a third (AUC 0.67), which
    the authors explain by a faster gastrointestinal transit and less
    enterohepatic reabsorption of the acid; the model has neither, the arm is
    simulated as the control (validation of a limitation).
    """

    #: the arms: the intervention of the data, the number of doses, the label
    #: and the line style
    arms: ClassVar[dict[str, tuple[str, int, str, str]]] = {
        "control": ("SIM", 16, "control (day 11)", "solid"),
        "cisapride": ("SIM,CIS", 8, "cisapride (day 7)", "dashed"),
    }

    #: the dosing interval [min]
    interval: ClassVar[float] = 12 * 60

    #: the analytes: the substance and its selection
    analytes: ClassVar[list[tuple[str, str]]] = [
        ("simva", "[Cve_simva]"),
        ("simacid", "[Cve_simacid]"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)

                for arm, (intervention, _, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Oral doses of 20 mg simvastatin every 12 hr, the last dose at time 0.

        The cisapride arm has no changes, see the class.
        """
        return {
            f"simva_po_{arm}": self.multiple_doses(
                dose=Q(20, "mg"),
                number=number,
                interval=self.interval,
                time_shift=-(number - 1) * self.interval,
                changes=self.default_changes(),
            )
            for arm, (_, number, _, _) in self.arms.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        coadministrations = {
            "control": Coadministration.NONE,
            "cisapride": Coadministration.CISAPRIDE,
        }
        mappings = {}
        for arm, coadministration in coadministrations.items():
            suffix = "" if arm == "control" else f"_{arm}"
            for sid, yid in self.analytes:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig2_{substance}_{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_simva_po_{arm}", xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=coadministration,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin and its acid after the last dose, alone and with cisapride."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("cisapride", ["control", "cisapride"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit, min=-1, max=13),
                legend=True,
            )
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
            plots[1].set_yaxis(self.info.simacid.axis, self.info.simacid.unit)

            for arm in arms:
                _, _, label, linestyle = self.arms[arm]
                for k, (sid, yid) in enumerate(self.analytes):
                    substance = getattr(self.info, sid).name
                    plots[k].add_data(
                        task=f"task_simva_po_{arm}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {label}",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"Fig2_{substance}_{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        label=f"{self.sid}: {label}",
                    )
            figures[f"fig_{key}"] = fig

        return figures
