"""Simulation experiment of the study Harvey2018."""

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


class Harvey2018(SimvastatinSimulationExperiment):
    """Simulation experiment of Harvey2018.

    Simvastatin 40 mg po, fasted from 2 h before to 2 h after the dose, alone
    (day 1) and with osimertinib 80 mg once daily (OSI, day 31 after 28 days
    of osimertinib) in patients with advanced non-small cell lung cancer
    (EGFRm NSCLC; 71 % women, 33 % Asian, 60 +- 13 kg; n = 46 and 43). The
    data are geometric means (Fig. 1); the bars of the figure (geometric SD,
    drawn up or down) are not used.
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM", "OSI": "SIM,OSI"}

    #: the mean body weight of the patients [kg]
    bodyweight: ClassVar[float] = 60.0

    #: the line styles of the data
    linestyles: ClassVar[dict[str, str]] = {"control": "solid", "OSI": "dashed"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        fig_id = "Fig1"
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

        Osimertinib does not change the pharmacokinetics of simvastatin in the
        model: it is a weak inducer of CYP3A4 at most, the observed geometric
        mean ratios are 0.91 for the AUC and 0.77 for the Cmax of simvastatin
        and 0.96 for the AUC of the acid. The arm of osimertinib is compared
        with this simulation.
        """
        return {
            self.to_sid("simva_po_control"): Simulation(
                start=0,
                end=40 * 60,
                preinit_changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight),
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
                application_form=ApplicationForm.NR,
                dosing=Dosing.SINGLE,
                health=Health.NSCLC,
                fasting=Fasting.FASTED,
                coadministration=coadministration,
            )

        coadministrations = {
            "control": Coadministration.NONE,
            "OSI": Coadministration.OSIMERTINIB,
        }
        mappings = {}
        for intervention, coadministration in coadministrations.items():
            suffix = "" if intervention == "control" else "_no_interaction"
            for sid, yid in [("simva", "[Cve_simva]"), ("simacid", "[Cve_simacid]")]:
                substance = getattr(self.info, sid).name
                # geometric means without a usable spread: no yid_sd
                mappings[f"fm_{sid}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
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
        """Simvastatin and simvastatin acid, alone and with osimertinib."""
        figures = {}
        for key, intervention_list in {
            "control": ["control"],
            "no_interaction": ["control", "OSI"],
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
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=self.linestyles[intervention],
                        label=f"{self.sid}: {intervention} (geometric mean)",
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
