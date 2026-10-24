"""Simulation experiment of the study Najib2003."""

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


class Najib2003(SimvastatinSimulationExperiment):
    """Simulation experiment of Najib2003.

    Bioequivalence of two formulations of 40 mg simvastatin (Zocor, the
    reference, and Simvast, the test), a single oral dose in a crossover of 24
    healthy Jordanian men after an overnight fast; plasma by LC-MS/MS, mean and
    SEM (the copies hold the SD). The data are 55 - 70 % below the simulations
    and 2.3-fold below Pasanen2006 at the same dose and formulation (simvastatin
    AUCinf 11.7 vs 26.4 ng*hr/ml, simvastatin acid 7.2 vs 16.4), which neither
    the assay nor the population explains: the mappings are outliers.
    """

    #: the formulations, as named in the data
    interventions: ClassVar[list[str]] = ["zocor", "simvast"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)

                for intervention in self.interventions:
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin."""
        simva_po = Q(40, "mg")
        return {
            "simva_po_control": Simulation(
                start=0,
                end=(12 * 60) + 1,
                preinit_changes={**self.default_changes(), "PODOSE_simva": simva_po},
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata() -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
            )

        return {
            "fm_simva_zocor": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_zocor",
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
            "fm_simacid_zocor": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig2_simvastatin_acid_zocor",
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
            "fm_simva_simvast": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_simvastatin_simvast",
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
            "fm_simacid_simvast": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig2_simvastatin_acid_simvast",
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
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and its acid, the two formulations."""
        fig = Figure(
            experiment=self,
            sid="Fig1",
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
        for k, (sid, yid) in enumerate(
            [("simva", "[Cve_simva]"), ("simacid", "[Cve_simacid]")]
        ):
            plots[k].add_data(
                task="task_simva_po_control",
                xid="time",
                yid=yid,
                label="sim: control",
                color=self.colors_simva[sid],
                linestyle=self.simtype_linestyle["control"],
            )

        # data
        for intervention in self.interventions:
            for k, sid in enumerate(["simva", "simacid"]):
                substance = getattr(self.info, sid).name
                fig_id = "Fig1" if (substance == "simvastatin") else "Fig2"
                dset_id = f"{fig_id}_{substance}_{intervention}"
                linestyle = "solid" if (intervention == "zocor") else "dashed"
                plots[k].add_data(
                    dataset=self.to_sid(dset_id),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                    label=f"{self.sid}: {intervention}",
                )

        return {"fig_control": fig}
