"""Simulation experiment of the study Hsyu2001."""

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


class Hsyu2001(SimvastatinSimulationExperiment):
    """Simulation experiment of Hsyu2001.

    Simvastatin 20 mg po (tablet) once daily in the morning with food for
    14 days (day 14, control), then with nelfinavir 1250 mg twice daily on
    days 15 to 28 (day 28, NEL), in 16 healthy volunteers (72 +- 9 kg). The
    enzyme inhibition assay without hydrolysis measures the active inhibitors
    (simvastatin acid and its active metabolites, in simvastatin acid
    equivalents). The profiles are of the last dose, the doses are at 0 h.
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM", "NEL": "SIM,NEL"}

    #: the mean body weight of the subjects of the simvastatin group [kg]
    bodyweight: ClassVar[float] = 72.0

    #: activity of CYP3A4 (liver and gut) with nelfinavir 1250 mg twice daily,
    #: a strong mechanism based inhibitor of CYP3A4, comparable to
    #: clarithromycin (Jacobson2004, 0.12). The observed AUC0-24 of the active
    #: inhibitors at steady state is 6.05-fold of the control (Cmax 6.2-fold);
    #: the active inhibitors of the model react weaker than simvastatin and
    #: its acid (the lumped metabolites are CYP3A4 products), 0.12 gives about
    #: 4-fold. Not fitted, the arm is validation.
    f_cyp3a4_nelfinavir: ClassVar[float] = 0.12

    #: the conditions of the interventions (the simulations, the line styles)
    conditions: ClassVar[dict[str, str]] = {"control": "control", "NEL": "inhibitor"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        fig_id = "Fig2"
        dframes = self.load_dataframes_by_substance(fig_id)
        for substance, df in dframes.items():
            dset = DataSet.from_df(df, ureg=self.ureg)
            if substance == "active simva inhibitors":
                dset.unit_conversion("mean", 1 / self.Mr.ActiveInh)
            elif substance == "total simva inhibitors":
                dset.unit_conversion("mean", 1 / self.Mr.TotalInh)

            for intervention, intervention_str in self.interventions.items():
                dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                    dset.intervention == intervention_str
                ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulations of simvastatin 20 mg po once daily for 14 days.

        The last dose is at 0 h. The arm of nelfinavir is simulated as 14 doses
        with nelfinavir (in the study the 14 doses with nelfinavir followed 14
        doses alone), both are at steady state.
        """
        num_applications = 14
        changes = {
            "control": {},
            "NEL": self.cyp3a4_changes(self.f_cyp3a4_nelfinavir),
        }
        return {
            self.to_sid(
                f"simva_po_{self.conditions[intervention]}"
            ): self.multiple_doses(
                dose=Q(20, "mg"),
                number=num_applications,
                interval=DAY,
                time_shift=-(num_applications - 1) * DAY,
                changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight),
                    **intervention_changes,
                },
            )
            for intervention, intervention_changes in changes.items()
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
            "control": ("fm_active_inhibitors", Coadministration.NONE),
            "NEL": ("fm_active_inhibitors_inhi", Coadministration.NELFINAVIR),
        }
        return {
            key: FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(
                        f"Fig2_{self.info.activesimvainhibitors.name}_{intervention}"
                    ),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{self.conditions[intervention]}"),
                    xid="time",
                    yid="Cve_active_inhibitors",
                ),
                metadata=metadata(coadministration=coadministration),
            )
            for intervention, (key, coadministration) in coadministrations.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Active simvastatin inhibitors, alone and with nelfinavir."""
        figures = {}
        for key, intervention_list in {
            "control": ["control"],
            "inhibitor": ["control", "NEL"],
        }.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_{key}"),
                num_rows=1,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_one_panel,
            )
            # the dosing interval of the last dose
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit, min=-1, max=25),
                legend=True,
            )
            plots[0].set_yaxis(
                self.info.activesimvainhibitors.axis,
                self.info.activesimvainhibitors.unit,
            )
            sid = "activesimvainhibitors"
            for intervention in intervention_list:
                condition = self.conditions[intervention]
                linestyle = self.simtype_linestyle[condition]
                label = (
                    condition
                    if condition == "control"
                    else f"{condition} ({intervention})"
                )
                plots[0].add_data(
                    task=self.to_sid(f"task_simva_po_{condition}"),
                    xid="time",
                    yid="Cve_active_inhibitors",
                    label=f"sim: {label}",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                )
                plots[0].add_data(
                    dataset=self.to_sid(
                        f"Fig2_{self.info.activesimvainhibitors.name}_{intervention}"
                    ),
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
