"""Simulation experiment of the study Kantola1998."""

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


class Kantola1998(SimvastatinSimulationExperiment):
    """Simulation experiment of Kantola1998.

    Simvastatin 40 mg po (two 20 mg tablets, 2 h fast before the dose, warm
    meal at 4 h), alone (placebo), with verapamil 80 mg (VER) and with
    erythromycin 500 mg (ERY) three times a day for 2 days, in 12 healthy
    volunteers (68 kg). Serum, limit of quantification 2 ng/ml.
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {
        "control": "SIM",
        "VER": "SIM,VER",
        "ERY": "SIM,ERY",
    }

    #: body weight of the subjects [kg]
    bodyweight: ClassVar[float] = 68.0

    #: activity of CYP3A4 (liver and gut) with the inhibitors: erythromycin and
    #: verapamil (and norverapamil) are moderate mechanism based inhibitors of
    #: CYP3A4. The observed ratios of the AUC0-24 of simvastatin are 6.2
    #: (erythromycin, Cmax 3.4) and 4.6 (verapamil, Cmax 2.6), of simvastatin
    #: acid 3.9 and 2.8; 0.22 gives 6.4 and 0.3 gives 4.7 for simvastatin (the
    #: acid 6.0 and 4.5, it rises more than observed). Not fitted, the arms are
    #: validation.
    f_cyp3a4_inhibitor: ClassVar[dict[str, float]] = {
        "ERY": 0.22,
        "VER": 0.3,
    }

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

                # a mean of 0 after the dose is below the limit of quantification
                # (2 ng/ml), not a concentration
                dset = dset[~((dset.time > 0) & (dset["mean"] == 0))]
                for intervention, intervention_str in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention_str
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulations of simvastatin 40 mg po, alone and with the inhibitors."""
        simva_po = Q(40, "mg")
        simulations = {}
        simulations["simva_po_control"] = Simulation(
            start=0,
            end=(24 * 60) + 1,
            preinit_changes={
                **self.default_changes(),
                **self.bodyweight_changes(self.bodyweight),
                "PODOSE_simva": simva_po,
            },
        )
        for intervention, f_cyp3a4 in self.f_cyp3a4_inhibitor.items():
            simulations[f"simva_po_inhibitor_{intervention}"] = Simulation(
                start=0,
                end=(24 * 60) + 1,
                preinit_changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight),
                    **self.cyp3a4_changes(f_cyp3a4),
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
                tissue=Tissue.SERUM,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                # fasted 2 h before the dose, warm meal 4 h after it
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
            "fm_simva_inhi_VER": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_VER",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_inhibitor_VER",
                    xid="time",
                    yid="[Cve_simva]",
                ),
                metadata=metadata(coadministration=Coadministration.VERAPAMIL),
            ),
            "fm_simacid_inhi_VER": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_acid_VER",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_inhibitor_VER",
                    xid="time",
                    yid="[Cve_simacid]",
                ),
                metadata=metadata(coadministration=Coadministration.VERAPAMIL),
            ),
            "fm_simva_inhi_ERY": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_ERY",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_inhibitor_ERY",
                    xid="time",
                    yid="[Cve_simva]",
                ),
                metadata=metadata(coadministration=Coadministration.ERYTHROMYCIN),
            ),
            "fm_simacid_inhi_ERY": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_acid_ERY",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_inhibitor_ERY",
                    xid="time",
                    yid="[Cve_simacid]",
                ),
                metadata=metadata(coadministration=Coadministration.ERYTHROMYCIN),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and simvastatin acid, alone, with erythromycin and verapamil."""
        # the interventions of the data in the figures
        figure_interventions = {
            "control": ["control"],
            "inhibitor_ERY": ["control", "ERY"],
            "inhibitor_VER": ["control", "VER"],
        }

        figures = {}
        for key, intervention_list in figure_interventions.items():
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

            # simulation and data of the interventions
            for intervention in intervention_list:
                condition = "control" if intervention == "control" else "inhibitor"
                task_id = (
                    "task_simva_po_control"
                    if intervention == "control"
                    else f"task_simva_po_inhibitor_{intervention}"
                )
                linestyle = self.simtype_linestyle[condition]
                for k, sid in enumerate(["simva", "simacid"]):
                    substance = getattr(self.info, sid).name
                    label = (
                        condition
                        if condition == "control"
                        else f"{condition} ({intervention})"
                    )
                    plots[k].add_data(
                        task=self.to_sid(task_id),
                        xid="time",
                        yid=f"[Cve_{sid}]",
                        label=f"sim: {label}",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        label=f"{self.sid}: {label}",
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
