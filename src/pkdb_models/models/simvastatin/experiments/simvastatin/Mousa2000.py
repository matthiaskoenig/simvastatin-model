"""Simulation experiment of the study Mousa2000."""

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


class Mousa2000(SimvastatinSimulationExperiment):
    """Simulation experiment of Mousa2000.

    Single oral dose of 20 mg simvastatin after an overnight fast in 10 healthy
    volunteers, alone (control) or after 2 weeks of diltiazem SR 120 mg twice
    daily, an inhibitor of CYP3A4. Serum, LC-MS/MS (LLOQ 0.5 ng/ml), mean and
    SD; the simvastatin acid of Table 3 has no time course.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "inhibitor": ("SIM,DIL", "diltiazem", "dashed"),
    }

    #: Diltiazem and N-desmethyldiltiazem inactivate CYP3A4 (mechanism based) in
    #: the liver and the gut wall. Diltiazem at steady state (Css 121 ng/ml)
    #: increased the AUCinf of simvastatin 4.8-fold, the Cmax 3.6-fold and the
    #: half-life 2.3-fold. The in vivo Ki of the authors (31.6 ng/ml, from
    #: AUC ratio = 1 + Css/Ki for a hepatic inhibition only) gives an activity
    #: of 1/(1 + 121/31.6) = 0.21; with the intestinal and the hepatic CYP3A4 of
    #: the model an activity of 0.3 in both gives the observed AUC ratio
    #: (4.65-fold, Cmax 4.2-fold; the half-life rises only 1.1-fold). Not
    #: fitted, the arm is validation data.
    f_cyp3a4_diltiazem: ClassVar[float] = 0.3

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.simva)
                for arm, (intervention, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 20 mg simvastatin, alone and with diltiazem."""
        simva_po = Q(20, "mg")
        changes = {
            "control": self.default_changes(),
            "inhibitor": self.cyp3a4_changes(self.f_cyp3a4_diltiazem),
        }
        return {
            f"simva_po_{arm}": Simulation(
                start=0,
                end=24 * 60,
                preinit_changes={**changes[arm], "PODOSE_simva": simva_po},
            )
            for arm in self.arms
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        coadministrations = {
            "control": Coadministration.NONE,
            "inhibitor": Coadministration.DILTIAZEM,
        }
        mappings = {}
        for arm, coadministration in coadministrations.items():
            suffix = "" if arm == "control" else "_inhi"
            mappings[f"fm_simva{suffix}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_simvastatin_{arm}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_simva_po_{arm}", xid="time", yid="[Cve_simva]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=coadministration,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin, alone and with diltiazem."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("inhibitor", ["control", "inhibitor"]),
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
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
            for arm in arms:
                _, label, linestyle = self.arms[arm]
                plots[0].add_data(
                    task=f"task_simva_po_{arm}",
                    xid="time",
                    yid="[Cve_simva]",
                    label=f"sim: {label}",
                    color=self.colors_simva["simva"],
                    linestyle=linestyle,
                )
                plots[0].add_data(
                    dataset=self.to_sid(f"Fig1_simvastatin_{arm}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    color=self.colors_simva["simva"],
                    linestyle=linestyle,
                    label=f"{self.sid}: {label}",
                )
            figures[f"fig_{key}"] = fig

        return figures
