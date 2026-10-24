"""Simulation experiment of the study Pentikainen1992."""

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


class Pentikainen1992(SimvastatinSimulationExperiment):
    """Simulation experiment of Pentikainen1992.

    Single oral dose of 40 mg simvastatin (two 20 mg tablets) in 12 healthy men
    (74 kg) after a fast, one arm of a crossover with lovastatin and
    pravastatin. Plasma HMG-CoA reductase inhibitors by an enzyme inhibition
    assay with simvastatin acid as the standard, before (active inhibitors) and
    after a base hydrolysis (total inhibitors); means without error bars.
    """

    #: the lower limits of the linear range of the assay [ng/ml]; values below
    #: it were set to 0 and used in the means, a mean below half of the limit
    #: after the dose is mostly such zeros (12 and 24 hr), not a concentration
    loq: ClassVar[dict[str, float]] = {
        "active simva inhibitors": 2.5,
        "total simva inhibitors": 5.0,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            mr = {
                "active simva inhibitors": self.Mr.ActiveInh,
                "total simva inhibitors": self.Mr.TotalInh,
            }
            # the inhibitors of simvastatin, not of lovastatin and pravastatin
            for substance, loq in self.loq.items():
                df = dframes[substance]
                df = df[(df.time == 0) | (df["mean"] >= 0.5 * loq)]
                dset = DataSet.from_df(df, ureg=self.ureg)
                dset.unit_conversion("mean", 1 / mr[substance])
                dsets[self.to_sid(f"{fig_id}_{substance}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin."""
        simva_po = Q(40, "mg")
        return {
            "simva_po_control": Simulation(
                start=0,
                end=(24 * 60) + 1,
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
            "fm_active_inhibitors": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_active_simva_inhibitors",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_control",
                    xid="time",
                    yid="Cve_active_inhibitors",
                ),
                metadata=metadata(),
            ),
            "fm_total_inhibitors": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_total_simva_inhibitors",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_control",
                    xid="time",
                    yid="Cve_total_inhibitors",
                ),
                metadata=metadata(),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Active and total simvastatin inhibitors."""
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
        plots[0].set_yaxis(
            self.info.activesimvainhibitors.axis, self.info.activesimvainhibitors.unit
        )
        plots[1].set_yaxis(
            self.info.totalsimvainhibitors.axis, self.info.totalsimvainhibitors.unit
        )

        linestyle = self.simtype_linestyle["control"]
        for k, (sid, yid) in enumerate(
            [
                ("activesimvainhibitors", "Cve_active_inhibitors"),
                ("totalsimvainhibitors", "Cve_total_inhibitors"),
            ]
        ):
            plots[k].add_data(
                task="task_simva_po_control",
                xid="time",
                yid=yid,
                label="sim: control",
                color=self.colors_simva[sid],
                linestyle=linestyle,
            )

        # data
        for k, sid in enumerate(["activesimvainhibitors", "totalsimvainhibitors"]):
            substance = getattr(self.info, sid).name
            dset_id = f"Fig1_{substance}"
            plots[k].add_data(
                dataset=self.to_sid(dset_id),
                xid="time",
                yid="mean",
                count="count",
                color=self.colors_simva[sid],
                linestyle=linestyle,
                label=f"{self.sid}: control",
            )

        return {"fig_control": fig}
