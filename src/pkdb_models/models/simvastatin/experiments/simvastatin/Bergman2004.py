"""Simulation experiment of the study Bergman2004."""

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
    DAY,
    SimvastatinSimulationExperiment,
)


class Bergman2004(SimvastatinSimulationExperiment):
    """Simulation experiment of Bergman2004.

    Simvastatin 80 mg po (tablet) once daily for 7 days, 20 min after a
    standardized breakfast, alone (treatment A) and on days 8 to 14 of
    fenofibrate 160 mg once daily (FEN, treatment B), in 12 healthy subjects
    (9 men, 3 women, body weight not reported). The profiles are of the last
    dose (day 7 and day 14), the doses are at 0 h.
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM", "FEN": "SIM,FEN"}

    #: the line styles of the data
    linestyles: ClassVar[dict[str, str]] = {"control": "solid", "FEN": "dashed"}

    #: the substances of the data: the figure, the observable and the
    #: molecular weight of the unit conversion
    substances: ClassVar[dict[str, tuple[str, str]]] = {
        "simva": ("Fig2", "[Cve_simva]"),
        "simacid": ("Fig2", "[Cve_simacid]"),
        "activesimvainhibitors": ("Fig1", "Cve_active_inhibitors"),
        "totalsimvainhibitors": ("Fig1", "Cve_total_inhibitors"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)
                elif substance == "total simva inhibitors":
                    dset.unit_conversion("mean", 1 / self.Mr.TotalInh)
                elif substance == "active simva inhibitors":
                    dset.unit_conversion("mean", 1 / self.Mr.ActiveInh)

                for intervention, intervention_str in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention_str
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulation of 80 mg simvastatin once daily for 7 days.

        The last dose is at 0 h. Fenofibrate does not change the
        pharmacokinetics of simvastatin in the model (no CYP3A4 interaction;
        the observed geometric mean ratios are 0.89 for the AUC of simvastatin,
        0.64 for the acid and 0.88 for the active inhibitors), the arm of
        fenofibrate is compared with this simulation.
        """
        num_applications = 7
        return {
            self.to_sid("simva_po_control"): self.multiple_doses(
                dose=Q(80, "mg"),
                number=num_applications,
                interval=DAY,
                time_shift=-(num_applications - 1) * DAY,
                changes=self.default_changes(),
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(
            coadministration: Coadministration = Coadministration.NONE,
        ) -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.MULTIPLE,
                health=Health.HEALTHY,
                fasting=Fasting.FED,
                coadministration=coadministration,
            )

        coadministrations = {
            "control": Coadministration.NONE,
            "FEN": Coadministration.FENOFIBRATE,
        }
        keys = {
            "simva": "simva",
            "simacid": "simacid",
            "activesimvainhibitors": "active_inhibitors",
            "totalsimvainhibitors": "total_inhibitors",
        }
        mappings = {}
        for intervention, coadministration in coadministrations.items():
            suffix = "" if intervention == "control" else "_no_interaction"
            for sid, (fig_id, yid) in self.substances.items():
                substance = getattr(self.info, sid).name
                mappings[f"fm_{keys[sid]}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{fig_id}_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        count="count",
                    ),
                    observable=FitData(
                        self, task="task_simva_po_control", xid="time", yid=yid
                    ),
                    metadata=metadata(coadministration=coadministration),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin, simvastatin acid and the inhibitors after the last dose."""
        figures = {}
        for key, intervention_list in {
            "control": ["control"],
            "fenofibrate": ["control", "FEN"],
        }.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_{key}"),
                num_rows=2,
                num_cols=2,
                **SimvastatinSimulationExperiment.figuresize_kwargs_four_panel,
            )
            # the dosing interval of the last dose
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit, min=-1, max=25),
                legend=True,
            )
            for k, sid in enumerate(self.substances):
                info = getattr(self.info, sid)
                plots[k].set_yaxis(info.axis, info.unit)

            for k, (sid, (fig_id, yid)) in enumerate(self.substances.items()):
                substance = getattr(self.info, sid).name
                plots[k].add_data(
                    task="task_simva_po_control",
                    xid="time",
                    yid=yid,
                    label="sim: control",
                    color=self.colors_simva[sid],
                )
                for intervention in intervention_list:
                    plots[k].add_data(
                        dataset=self.to_sid(f"{fig_id}_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=self.linestyles[intervention],
                        label=f"{self.sid}: {intervention}",
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
