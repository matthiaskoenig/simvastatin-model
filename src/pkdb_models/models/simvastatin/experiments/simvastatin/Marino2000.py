"""Simulation experiment of the study Marino2000."""

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


class Marino2000(SimvastatinSimulationExperiment):
    """Simulation experiment of Marino2000.

    Single oral dose of 40 mg simvastatin (one tablet) after an overnight fast
    in 12 healthy subjects (13 men, 1 woman randomized, 10 black), alone
    (control) or with 300 mg irbesartan, a crossover of two periods. Serum,
    total simvastatin acid (simvastatin and simvastatin acid after the
    conversion of the lactone, `Cve_simva_and_simacid`) by GC/MS, means
    without error bars.

    Irbesartan does not interact with simvastatin (it is metabolized by CYP2C9,
    not CYP3A4): the geometric mean ratio of the AUC was 0.999, of the Cmax
    0.831. The arm with irbesartan is the control simulation, it is validation
    data of the absent interaction.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "IRB": ("SIM,IRB", "irbesartan", "dashed"),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                # simvastatin acid equivalents
                dset.unit_conversion("mean", 1 / self.Mr.simacid)
                for arm, (intervention, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin, irbesartan does not change it."""
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
        coadministrations = {
            "control": Coadministration.NONE,
            "IRB": Coadministration.IRBESARTAN,
        }
        mappings = {}
        for arm, coadministration in coadministrations.items():
            suffix = "" if arm == "control" else "_irb"
            mappings[f"fm_simva_and_simacid{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_simva+simacid_{arm}"),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_simva_po_control",
                    xid="time",
                    yid="Cve_simva_and_simacid",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministration,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Total simvastatin acid, alone and with irbesartan."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("no_interaction", ["control", "IRB"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=1,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_one_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(
                self.info.simva_and_simacid.axis, self.info.simva_and_simacid.unit
            )
            plots[0].add_data(
                task="task_simva_po_control",
                xid="time",
                yid="Cve_simva_and_simacid",
                label="sim: 40 mg",
                color=self.colors_simva["simva_and_simacid"],
            )
            for arm in arms:
                _, label, linestyle = self.arms[arm]
                plots[0].add_data(
                    dataset=self.to_sid(f"Fig1_simva+simacid_{arm}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    color=self.colors_simva["simva_and_simacid"],
                    linestyle=linestyle,
                    label=f"{self.sid}: {label}",
                )
            figures[f"fig_{key}"] = fig

        return figures
