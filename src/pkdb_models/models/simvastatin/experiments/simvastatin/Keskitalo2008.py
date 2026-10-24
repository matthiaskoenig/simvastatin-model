"""Simulation experiment of the study Keskitalo2008."""

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


class Keskitalo2008(SimvastatinSimulationExperiment):
    """Simulation experiment of Keskitalo2008.

    Simvastatin 20 mg po (Zocor) after an overnight fast, in 24 healthy white
    Finnish volunteers grouped by the ABCB1 c.1236C>T-c.2677G>T-c.3435C>T
    genotype CGC/CGC and TTT/TTT (12 each, 68 and 66 kg; all CYP3A5*3/*3,
    7/24 SLCO1B1 c.521TC). The model has no P-glycoprotein: both groups are
    simulated alike, the two groups of equal size bracket the population
    (TTT/TTT raised the acid AUC0-12 by 60 %, the lactone not).
    """

    #: the groups and their names in the data
    groups: ClassVar[dict[str, str]] = {"CGC_CGC": "CGC/CGC", "TTT_TTT": "TTT/TTT"}

    #: body weight of the subjects [kg], the mean of the groups (68 and 66 kg)
    bodyweight: ClassVar[float] = 67.0

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
        """Simulation of simvastatin 20 mg po."""
        simva_po = Q(20, "mg")

        simulations = {}
        simulations["simva_po_control"] = Simulation(
            start=0,
            end=(12 * 60) + 1,
            preinit_changes={
                **self.default_changes(),
                **self.bodyweight_changes(self.bodyweight),
                "PODOSE_simva": simva_po,
            },
        )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(
            genotype: Genotype = Genotype.NR,
        ) -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                genotype=genotype,
            )

        return {
            "fm_simva_CGC_CGC": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_CGC_CGC",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_control", xid="time", yid="[Cve_simva]"
                ),
                metadata=metadata(genotype=Genotype.ABCB1_CGC_CGC),
            ),
            "fm_simacid_CGC_CGC": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_acid_CGC_CGC",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_control", xid="time", yid="[Cve_simacid]"
                ),
                metadata=metadata(genotype=Genotype.ABCB1_CGC_CGC),
            ),
            "fm_simva_TTT_TTT": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_TTT_TTT",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_control", xid="time", yid="[Cve_simva]"
                ),
                metadata=metadata(genotype=Genotype.ABCB1_TTT_TTT),
            ),
            "fm_simacid_TTT_TTT": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_acid_TTT_TTT",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_simva_po_control", xid="time", yid="[Cve_simacid]"
                ),
                metadata=metadata(genotype=Genotype.ABCB1_TTT_TTT),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and simvastatin acid of the ABCB1 genotypes."""
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

        # simulation
        for k, sid in enumerate(["simva", "simacid"]):
            plots[k].add_data(
                task="task_simva_po_control",
                xid="time",
                yid=f"[Cve_{sid}]",
                label="sim: control",
                color=self.colors_simva[sid],
                linestyle=self.simtype_linestyle["control"],
            )

        # data
        for group, group_str in self.groups.items():
            linestyle = "dotted" if group == "CGC_CGC" else "dashed"
            for k, sid in enumerate(["simva", "simacid"]):
                substance = getattr(self.info, sid).name
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig1_{substance}_{group}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                    label=f"{self.sid}: ABCB1 genotype {group_str}",
                )

        return {
            "fig_control": fig_control,
        }
