"""Simulation experiment of the study Gehin2015."""

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


class Gehin2015(SimvastatinSimulationExperiment):
    """Simulation experiment of Gehin2015.

    Simvastatin 40 mg po (tablet) after an overnight fast, alone (period A)
    and 1 h after setipiprant 1000 mg on the 9th day of setipiprant 1000 mg
    twice daily (SET, period C), in 22 healthy men (BMI 26.2, body weight not
    reported).
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM", "SET": "SIM,SET"}

    #: the line styles of the data
    linestyles: ClassVar[dict[str, str]] = {"control": "solid", "SET": "dashed"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)

                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)

                for intervention, intervention_str in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention_str
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulation of simvastatin 40 mg po.

        Setipiprant does not change the pharmacokinetics of simvastatin in the
        model: the observed geometric mean ratios are 0.84 for the AUC and 0.91
        for the Cmax of simvastatin and 0.96 for the AUC of the acid, no
        interaction via CYP3A4 (the 2.7-fold Cmax of the acid is attributed to a
        faster appearance by an intestinal transporter, Gehin2015). The arm of
        setipiprant is compared with this simulation.
        """
        return {
            self.to_sid("simva_po_control"): Simulation(
                start=0,
                end=24 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_simva": Q(40, "mg"),
                },
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
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=coadministration,
            )

        coadministrations = {
            "control": Coadministration.NONE,
            "SET": Coadministration.SETIPIPRANT,
        }
        mappings = {}
        for intervention, coadministration in coadministrations.items():
            suffix = "" if intervention == "control" else "_no_interaction"
            for sid, yid in [("simva", "[Cve_simva]"), ("simacid", "[Cve_simacid]")]:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig3_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
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
        """Simvastatin and simvastatin acid, alone and with setipiprant."""
        figures = {}
        for key, intervention_list in {
            "control": ["control"],
            "no_interaction": ["control", "SET"],
        }.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_{key}"),
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
            plots[1].set_yaxis(self.info.simacid.axis, self.info.simacid.unit)

            for k, (sid, yid) in enumerate(
                [("simva", "[Cve_simva]"), ("simacid", "[Cve_simacid]")]
            ):
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
                        dataset=self.to_sid(f"Fig3_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=self.linestyles[intervention],
                        label=f"{self.sid}: {intervention}",
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
