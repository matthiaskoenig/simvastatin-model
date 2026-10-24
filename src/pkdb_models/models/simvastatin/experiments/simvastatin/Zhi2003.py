"""Simulation experiment of the study Zhi2003."""

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


class Zhi2003(SimvastatinSimulationExperiment):
    """Simulation experiment of Zhi2003.

    Single oral dose of 80 mg simvastatin with breakfast in 29 healthy subjects,
    on day 4 - 6 of orlistat (120 mg three times daily with the meals) or
    placebo (control). Plasma, means without error bars. Orlistat does not
    change the pharmacokinetics (ratios of Cmax and AUC 0.92 - 1.02), both arms
    are simulated as the control.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "placebo", "solid"),
        "orlistat": ("SIM,ORL", "orlistat", "dashed"),
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
                for arm, (intervention, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 80 mg simvastatin, orlistat does not interact."""
        return {
            "simva_po_control": Simulation(
                start=0,
                end=24 * 60 + 1,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_simva": Q(80, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        coadministrations = {
            "control": Coadministration.NONE,
            "orlistat": Coadministration.ORLISTAT,
        }
        mappings = {}
        for arm, coadministration in coadministrations.items():
            suffix = "" if arm == "control" else f"_{arm}"
            for sid, yid in self.analytes:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{substance}_{arm}"),
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
                        fasting=Fasting.FED,
                        coadministration=coadministration,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin and its acid, with placebo and with orlistat."""
        fig = Figure(
            experiment=self,
            sid="Fig_control",
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
                label="sim: control",
                color=self.colors_simva[sid],
            )
            for arm, (_, label, linestyle) in self.arms.items():
                plots[k].add_data(
                    dataset=self.to_sid(f"Fig1_{substance}_{arm}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    color=self.colors_simva[sid],
                    linestyle=linestyle,
                    label=f"{self.sid}: {label}",
                )

        return {"fig_control": fig}
