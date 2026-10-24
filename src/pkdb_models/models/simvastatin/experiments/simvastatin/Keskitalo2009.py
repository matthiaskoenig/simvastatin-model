"""Simulation experiment of the study Keskitalo2009."""

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


class Keskitalo2009(SimvastatinSimulationExperiment):
    """Simulation experiment of Keskitalo2009.

    Simvastatin 40 mg po (Zocor) after an overnight fast, in 32 healthy white
    Finnish volunteers grouped by the ABCG2 c.421C>A genotype: C/C (n=23, the
    reference), C/A (n=4) and A/A (n=5); all CYP3A5 non-expressors. The model
    has no BCRP: the groups differ only in their body weight. The variant
    groups carry SLCO1B1 c.521TC more often (C/C 7/23, C/A 4/4, A/A 4/5), which
    the simulations leave out as well (the c.421A/A raised the AUC of the
    lactone by 111 %, of the acid not significantly).
    """

    #: the groups and their names in the data, c.421C/C is the wildtype
    groups: ClassVar[dict[str, str]] = {
        "c421A_A": "c.421A/A",
        "c421C_C": "c.421C/C",
        "c421C_A": "c.421C/A",
    }

    #: the genotype of the groups
    genotypes: ClassVar[dict[str, Genotype]] = {
        "c421A_A": Genotype.ABCG2_421AA,
        "c421C_C": Genotype.ABCG2_421CC,
        "c421C_A": Genotype.ABCG2_421CA,
    }

    #: body weight of the groups [kg]
    bodyweight: ClassVar[dict[str, float]] = {
        "c421A_A": 56.0,
        "c421C_C": 68.0,
        "c421C_A": 73.0,
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
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)

                for group, group_str in self.groups.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{group}")] = dset[
                        dset.group == group_str
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulations of simvastatin 40 mg po, one per group (body weight)."""
        simva_po = Q(40, "mg")

        simulations = {}
        for group in self.groups:
            simulations[f"simva_po_{group}"] = Simulation(
                start=0,
                end=(12 * 60) + 1,
                preinit_changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight[group]),
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
                fasting=Fasting.FASTED,
                genotype=genotype,
            )

        mappings = {}
        for group in self.groups:
            for sid in ["simva", "simacid"]:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}_{group}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{substance}_{group}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_simva_po_{group}",
                        xid="time",
                        yid=f"[Cve_{sid}]",
                    ),
                    metadata=metadata(genotype=self.genotypes[group]),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and simvastatin acid of the ABCG2 genotypes."""
        fig_control = Figure(
            experiment=self,
            sid="Fig_control",
            num_rows=2,
            num_cols=1,
            **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
        )
        plots = fig_control.create_plots(
            xaxis=Axis("Time", unit=self.info.time.unit), legend=True
        )
        plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
        plots[1].set_yaxis(self.info.simacid.axis, self.info.simacid.unit)

        # simulation and data, the line style and the label of the groups
        group_styles = {
            "c421A_A": ("dashed", "c421A/A"),
            "c421C_A": ("dotted", "c421C/A"),
            "c421C_C": ("solid", "c421C/C"),
        }
        for group in self.groups:
            linestyle, group_label = group_styles[group]
            for k, sid in enumerate(["simva", "simacid"]):
                substance = getattr(self.info, sid).name
                plots[k].add_data(
                    task=f"task_simva_po_{group}",
                    xid="time",
                    yid=f"[Cve_{sid}]",
                    label=f"sim: {group_label} ({self.bodyweight[group]:.0f} kg)",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                )
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig1_{substance}_{group}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                    label=f"{self.sid}: ABCG2 {group_label}",
                )

        return {
            "fig_control": fig_control,
        }
