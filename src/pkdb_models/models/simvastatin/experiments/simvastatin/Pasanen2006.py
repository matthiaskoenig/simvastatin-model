"""Simulation experiment of the study Pasanen2006."""

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


class Pasanen2006(SimvastatinSimulationExperiment):
    """Simulation experiment of Pasanen2006.

    Single oral dose of 40 mg simvastatin (Zocor) after an overnight fast in 32
    healthy Caucasian volunteers by the SLCO1B1 c.521T>C genotype: TT (n=16,
    68 kg), TC (n=11 of 12, one outlier excluded from the means, 69 kg) and CC
    (n=4, 84 kg), all CYP3A5*3/*3 (non-expressors, the reference of the model).
    Plasma by LC-MS/MS, mean and SEM (the copies hold the SD).

    OATP1B1 (gene SLCO1B1) on the sinusoidal membrane of the hepatocytes takes
    up simvastatin acid, the C allele reduces its activity
    (`slco1b1_activity`, not fitted). The acid AUC was 1.2-fold (TC) and
    3.2-fold (CC) of TT, the lactone was not changed significantly.
    """

    #: the SLCO1B1 c.521T>C genotypes: the genotype of the model, the
    #: genotype of the metadata and the line style
    groups: ClassVar[dict[str, tuple[str, Genotype, str]]] = {
        "c521TT": ("TT", Genotype.SLCO1B1_521TT, "solid"),
        "c521TC": ("TC", Genotype.SLCO1B1_521TC, "dashed"),
        "c521CC": ("CC", Genotype.SLCO1B1_521CC, "dotted"),
    }

    #: the analytes: the substance and its selection
    analytes: ClassVar[list[tuple[str, str]]] = [
        ("simva", "[Cve_simva]"),
        ("simacid", "[Cve_simacid]"),
    ]

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

                for group in self.groups:
                    dsets[self.to_sid(f"{fig_id}_{substance}_{group}")] = dset[
                        dset.group == group
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin in the SLCO1B1 genotypes."""
        simva_po = Q(40, "mg")
        return {
            f"simva_po_{group}": Simulation(
                start=0,
                end=(13 * 60) + 1,
                preinit_changes={
                    **self.slco1b1_changes(genotype),
                    **self.cyp3a5_changes("*3/*3"),
                    "PODOSE_simva": simva_po,
                },
            )
            for group, (genotype, _, _) in self.groups.items()
        }

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
        for sid, yid in self.analytes:
            substance = getattr(self.info, sid).name
            for group, (_, genotype, _) in self.groups.items():
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
                        self, task=f"task_simva_po_{group}", xid="time", yid=yid
                    ),
                    metadata=metadata(genotype),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and its acid in the SLCO1B1 genotypes."""
        figures = {}
        for key, groups in [
            ("control", ["c521TT"]),
            ("genetic_variants", list(self.groups)),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
            plots[1].set_yaxis(self.info.simacid.axis, self.info.simacid.unit)

            for k, (sid, yid) in enumerate(self.analytes):
                substance = getattr(self.info, sid).name
                for group in groups:
                    _, _, linestyle = self.groups[group]
                    plots[k].add_data(
                        task=f"task_simva_po_{group}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {group}",
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
                        label=f"{self.sid}: {group}",
                    )
            figures[f"fig_{key}"] = fig
        return figures
