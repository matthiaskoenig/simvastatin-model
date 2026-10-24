"""Simulation experiment of the study Lohitnavy2004."""

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


class Lohitnavy2004(SimvastatinSimulationExperiment):
    """Simulation experiment of Lohitnavy2004.

    Bioequivalence study: single oral dose of 40 mg simvastatin (4 tablets of
    10 mg) of a test and a reference formulation in 18 healthy Thai men after an
    overnight fast, a crossover of two periods. Lithium heparin plasma,
    simvastatin and its hydroxy acid (simvastatin acid) by LC-MS/MS, means
    without error bars.
    """

    #: the formulations: the intervention of the data, the key of the mappings,
    #: the label and the line style
    formulations: ClassVar[dict[str, tuple[str, str, str]]] = {
        "SIM_reference": ("ref", "reference", "solid"),
        "SIM_test": ("test", "test", "dashed"),
    }

    #: the analytes: the substance and its selection
    analytes: ClassVar[list[tuple[str, str]]] = [
        ("simva", "[Cve_simva]"),
        ("simacid", "[Cve_simacid]"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        mr = {"simvastatin": self.Mr.simva, "simvastatin acid": self.Mr.simacid}
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                dset.unit_conversion("mean", 1 / mr[substance])
                for intervention in self.formulations:
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin, the formulations are the same."""
        return {
            "simva_po_control": Simulation(
                start=0,
                end=24 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_simva": Q(40, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for intervention, (key, _, _) in self.formulations.items():
            for sid, yid in self.analytes:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}_{key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        count="count",
                    ),
                    observable=FitData(
                        self, task="task_simva_po_control", xid="time", yid=yid
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
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin and its acid, test and reference formulation."""
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

        for k, (sid, yid) in enumerate(self.analytes):
            substance = getattr(self.info, sid).name
            plots[k].add_data(
                task="task_simva_po_control",
                xid="time",
                yid=yid,
                label="sim: 40 mg",
                color=self.colors_simva[sid],
            )
            for intervention, (_, label, linestyle) in self.formulations.items():
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                    label=f"{self.sid}: {label}",
                )

        return {"fig_control": fig}
