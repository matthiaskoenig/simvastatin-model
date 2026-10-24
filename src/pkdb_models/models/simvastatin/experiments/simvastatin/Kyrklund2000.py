"""Simulation experiment of the study Kyrklund2000."""

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


class Kyrklund2000(SimvastatinSimulationExperiment):
    """Simulation experiment of Kyrklund2000.

    Simvastatin 40 mg po after an overnight fast, alone (placebo) and 17 h
    after the last of five daily doses of rifampicin 600 mg (RIF), in 10
    healthy men (59 - 81 kg, the mean is not reported).
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM", "RIF": "SIM,RIF"}

    #: activity of CYP3A4 (liver and gut) after rifampicin 600 mg daily for
    #: 5 days: rifampicin induces CYP3A4 in the intestine and the liver (PXR);
    #: 17 h after the last dose its inhibition of OATP1B1 is gone. The
    #: observed AUC0-inf of simvastatin is 13.1 % of the control (Cmax 9.5 %),
    #: of simvastatin acid 6.8 % (Cmax 10 %) with an unchanged half-life, a
    #: first pass effect; 3.5 gives 13 % for simvastatin (the acid 12 %). Not
    #: fitted, the arm is validation.
    f_cyp3a4_rifampicin: ClassVar[float] = 3.5

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
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
        """Simulations of simvastatin 40 mg po, alone and with rifampicin."""
        simva_po = Q(40, "mg")
        simulations = {}
        simulations["simva_po_control"] = Simulation(
            start=0,
            end=(12 * 60) + 1,
            preinit_changes={**self.default_changes(), "PODOSE_simva": simva_po},
        )
        simulations["simva_po_inducer"] = Simulation(
            start=0,
            end=(12 * 60) + 1,
            preinit_changes={
                **self.default_changes(),
                **self.cyp3a4_changes(self.f_cyp3a4_rifampicin),
                "PODOSE_simva": simva_po,
            },
        )
        return simulations

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

        return {
            "fm_simva": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_control",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_control", xid="time", yid="[Cve_simva]"
                ),
                metadata=metadata(),
            ),
            "fm_simacid": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_acid_control",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_control", xid="time", yid="[Cve_simacid]"
                ),
                metadata=metadata(),
            ),
            "fm_simva_indu": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_RIF",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_inducer", xid="time", yid="[Cve_simva]"
                ),
                metadata=metadata(coadministration=Coadministration.RIFAMPICIN),
            ),
            "fm_simacid_indu": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_acid_RIF",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_inducer", xid="time", yid="[Cve_simacid]"
                ),
                metadata=metadata(
                    coadministration=Coadministration.RIFAMPICIN,
                ),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and simvastatin acid of the control and the inducer."""
        figures = {}
        for key in ["control", "inducer"]:
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

            # simulation
            condition_list = ["control"]
            if key != "control":
                condition_list.append(key)

            for condition in condition_list:
                linestyle = self.simtype_linestyle[condition]
                task_id = f"task_simva_po_{condition}"
                label = (
                    "sim: control"
                    if condition == "control"
                    else f"sim: {condition} (RIF)"
                )
                plots[0].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid="[Cve_simva]",
                    label=label,
                    color=self.colors_simva["simva"],
                    linestyle=linestyle,
                )
                plots[1].add_data(
                    task=self.to_sid(task_id),
                    xid="time",
                    yid="[Cve_simacid]",
                    label=label,
                    color=self.colors_simva["simacid"],
                    linestyle=linestyle,
                )

            # data
            intervention_list = (
                ["control"] if key == "control" else list(self.interventions)
            )
            for intervention in intervention_list:
                condition = "inducer" if intervention == "RIF" else "control"
                linestyle = self.simtype_linestyle[condition]
                for k, sid in enumerate(["simva", "simacid"]):
                    substance = getattr(self.info, sid).name
                    label = (
                        f"{self.sid}: {condition}"
                        if condition == "control"
                        else f"{self.sid}: {condition} ({intervention})"
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        label=label,
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
