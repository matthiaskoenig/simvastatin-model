"""Simulation experiment of the study Zhou2013."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
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


class Zhou2013(SimvastatinSimulationExperiment):
    """Simulation experiment of Zhou2013.

    Single oral dose of 40 mg simvastatin (tablet) in 17 healthy Chinese Han men
    after a fast of 12 hr. Plasma simvastatin, mean and SD. The genotypes
    (SLCO1B1, ABCG2, ABCB1, CYP3A5) are mixed and had no effect on the
    pharmacokinetics (genotype not reported).
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                for intervention, intervention_str in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention_str
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin."""
        return {
            "simva_po_control": Simulation(
                start=0,
                end=24 * 60 + 1,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_simva": Q(40, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
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
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )
        }

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin."""
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=1,
            num_cols=1,
            **SimvastatinSimulationExperiment.figuresize_kwargs_one_panel,
        )
        plots = fig.create_plots(
            xaxis=Axis("Time", unit=self.info.time.unit), legend=True
        )
        plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
        plots[0].add_data(
            task="task_simva_po_control",
            xid="time",
            yid="[Cve_simva]",
            label="sim: control",
            color=self.colors_simva["simva"],
        )
        plots[0].add_data(
            dataset=self.to_sid(f"Fig1_{self.info.simva.name}_control"),
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            color=self.colors_simva["simva"],
            linestyle="solid",
            label=f"{self.sid}: control",
        )

        return {"fig_control": fig}
