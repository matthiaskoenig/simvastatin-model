"""Simulation experiment of the study Kim2007."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Dosing,
    Fasting,
    Genotype,
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


class Kim2007(SimvastatinSimulationExperiment):
    """Simulation experiment of Kim2007.

    Simvastatin 20 mg po (Zocor) in 22 healthy Korean men grouped by the
    CYP3A5 genotype *3/*3 (n=10, the reference of the model), *1/*3 (n=8) and
    *1/*1 (n=4); simvastatin lactone only. The genotypes are simulated with
    the functional CYP3A5 (`cyp3a5_changes`, not fitted), the variant groups
    validate it (AUC0-inf of *1/*1 0.30-fold of *3/*3).

    The error bars of Fig 1 are the SEM although the caption says SD: at the
    peak they are 0.31, 0.48 and 0.54 ng/ml (*3/*3, *1/*3, *1/*1), the SD of
    Cmax in Table II 1.23, 1.25 and 0.84 ng/ml, the ratios 3.9, 2.6 and 1.6
    are close to sqrt(n) = 3.2, 2.8 and 2.0. The copy of the data has
    sd = bar * sqrt(n).
    """

    #: the groups in the data and their names in the dataset ids
    groups: ClassVar[dict[str, str]] = {
        "CYP3A5*3/*3": "CYP3A5*3*3",
        "CYP3A5*1/*3": "CYP3A5*1*3",
        "CYP3A5*1/*1": "CYP3A5*1*1",
    }

    #: the CYP3A5 genotype of the groups (a key of `cyp3a5_activity`)
    cyp3a5_genotypes: ClassVar[dict[str, str]] = {
        "CYP3A5*3/*3": "*3/*3",
        "CYP3A5*1/*3": "*1/*3",
        "CYP3A5*1/*1": "*1/*1",
    }

    #: the genotype of the groups in the metadata
    genotypes: ClassVar[dict[str, Genotype]] = {
        "CYP3A5*3/*3": Genotype.CYP3A5_3_3,
        "CYP3A5*1/*3": Genotype.CYP3A5_1_3,
        "CYP3A5*1/*1": Genotype.CYP3A5_1_1,
    }

    #: body weight of the groups [kg]
    bodyweight: ClassVar[dict[str, float]] = {
        "CYP3A5*3/*3": 71.0,
        "CYP3A5*1/*3": 68.4,
        "CYP3A5*1/*1": 68.8,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)

                for group, group_str in self.groups.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{group_str}")] = dset[
                        dset.group == group
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulations of simvastatin 20 mg po, one per CYP3A5 genotype."""
        simva_po = Q(20, "mg")
        simulations = {}
        for group, group_str in self.groups.items():
            simulations[self.to_sid(f"simva_po_{group_str}")] = Simulation(
                start=0,
                end=(12 * 60) + 1,
                preinit_changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight[group]),
                    **self.cyp3a5_changes(self.cyp3a5_genotypes[group]),
                    "PODOSE_simva": simva_po,
                },
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(genotype: Genotype) -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.NR,
                genotype=genotype,
            )

        mappings = {}
        for group, group_str in self.groups.items():
            mappings[self.to_sid(f"fm_simva_{group_str}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_simvastatin_{group_str}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{group_str}"),
                    xid="time",
                    yid="[Cve_simva]",
                ),
                metadata=metadata(genotype=self.genotypes[group]),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin of the CYP3A5 genotypes."""
        fig_control = Figure(
            experiment=self,
            sid="Fig_control",
            num_rows=1,
            num_cols=1,
            **SimvastatinSimulationExperiment.figuresize_kwargs_one_panel,
        )
        plots = fig_control.create_plots(
            xaxis=Axis("Time", unit=self.info.time.unit), legend=True
        )
        plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)

        # simulation and data, the line style and the marker of the groups
        styles = {
            "CYP3A5*3/*3": ("solid", "s"),
            "CYP3A5*1/*3": ("dashed", "o"),
            "CYP3A5*1/*1": ("dotted", "x"),
        }
        substance = self.info.simva.name
        for group, group_str in self.groups.items():
            linestyle, marker = styles[group]
            plots[0].add_data(
                task=self.to_sid(f"task_simva_po_{group_str}"),
                xid="time",
                yid="[Cve_simva]",
                label=f"sim: {group}",
                color=self.colors_simva["simva"],
                linestyle=linestyle,
            )
            plots[0].add_data(
                dataset=self.to_sid(f"Fig1_{substance}_{group_str}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                color=self.colors_simva["simva"],
                marker=marker,
                linestyle=linestyle,
                label=f"{self.sid}: {group}",
            )

        return {"fig_control": fig_control}
