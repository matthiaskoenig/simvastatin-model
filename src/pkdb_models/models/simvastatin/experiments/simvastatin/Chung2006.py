"""Simulation experiment of the study Chung2006."""

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


class Chung2006(SimvastatinSimulationExperiment):
    """Simulation experiment of Chung2006.

    Simvastatin 40 mg po (tablet) after a fast of at least 8 h, alone, on
    day 6 or 9 of ketoconazole 400 mg once daily (KET) and on day 8 or 9 of
    rifampicin 600 mg once daily (RIF), in 19 healthy white volunteers (9 men,
    10 women, 73.4 kg; CYP3A5 *3/*3 in 16, *1/*3 in 3). Only simvastatin (the
    lactone) was measured.
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {
        "control": "SIM",
        "KET": "SIM, KET",
        "RIF": "SIM, RIF",
    }

    #: the mean body weight of the subjects [kg]
    bodyweight: ClassVar[float] = 73.4

    #: activity of CYP3A4 (liver and gut) with ketoconazole 400 mg once
    #: daily, a strong competitive inhibitor of CYP3A4. The observed AUC0-inf
    #: of simvastatin is 12.4-fold of the control (geometric means 364 vs 29
    #: ng*h/ml, Cmax 7.4-fold), 0.09 gives 12-fold. Not fitted, the arm is
    #: validation.
    f_cyp3a4_ketoconazole: ClassVar[float] = 0.09

    #: activity of CYP3A4 (liver and gut) on day 8 or 9 of rifampicin 600 mg
    #: once daily, a strong inducer of CYP3A4 in the intestine and the liver
    #: (PXR). The observed AUC0-inf of simvastatin is 9 % of the control
    #: (geometric means 2.6 vs 29 ng*h/ml, Cmax 15 %), 4 gives 10 %.
    #: Kyrklund2000 (5 days of rifampicin, simvastatin 17 h after the last
    #: dose, 13 % of the control) has 3.5. Not fitted, the arm is validation.
    f_cyp3a4_rifampicin: ClassVar[float] = 4.0

    #: the conditions of the interventions (the simulations, the line styles)
    conditions: ClassVar[dict[str, str]] = {
        "control": "control",
        "KET": "inhibitor",
        "RIF": "inducer",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)

                for intervention, intervention_str in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention_str
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulations of simvastatin 40 mg po, alone, with KET and with RIF."""
        simva_po = Q(40, "mg")
        changes = {
            "control": {},
            "KET": self.cyp3a4_changes(self.f_cyp3a4_ketoconazole),
            "RIF": self.cyp3a4_changes(self.f_cyp3a4_rifampicin),
        }
        return {
            self.to_sid(f"simva_po_{self.conditions[intervention]}"): Simulation(
                start=0,
                end=30 * 60,
                preinit_changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight),
                    **intervention_changes,
                    "PODOSE_simva": simva_po,
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
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=coadministration,
            )

        coadministrations = {
            "control": ("fm_simva", Coadministration.NONE),
            "RIF": ("fm_simva_indu", Coadministration.RIFAMPICIN),
            "KET": ("fm_simva_inhi", Coadministration.KETOCONAZOLE),
        }
        return {
            key: FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig3_simvastatin_{intervention}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{self.conditions[intervention]}"),
                    xid="time",
                    yid="[Cve_simva]",
                ),
                metadata=metadata(coadministration=coadministration),
            )
            for intervention, (key, coadministration) in coadministrations.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin of the control, the inducer and the inhibitor."""
        # the interventions of the figures
        figure_interventions = {
            "control": ["control"],
            "inducer": ["control", "RIF"],
            "inhibitor": ["control", "KET"],
        }

        figures = {}
        for key, intervention_list in figure_interventions.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_{key}"),
                num_rows=1,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_one_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)

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
                    yid="[Cve_simva]",
                    label=f"sim: {label}",
                    color=self.colors_simva["simva"],
                    linestyle=linestyle,
                )
                plots[0].add_data(
                    dataset=self.to_sid(f"Fig3_simvastatin_{intervention}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    color=self.colors_simva["simva"],
                    linestyle=linestyle,
                    label=f"{self.sid}: {label}",
                )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
