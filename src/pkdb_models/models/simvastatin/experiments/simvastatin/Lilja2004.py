"""Simulation experiment of the study Lilja2004."""

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


class Lilja2004(SimvastatinSimulationExperiment):
    """Simulation experiment of Lilja2004.

    Single oral dose of 40 mg simvastatin (Zocor tablet) in 10 healthy men after
    an overnight fast, with water (control) or with 200 ml of normal strength
    grapefruit juice (once daily for 2 days and with the dose), an inhibitor of
    the intestinal CYP3A4. Plasma, LC-MS/MS, mean and SEM (the bars of Fig. 1
    are the SD of Table 1 over the square root of 10).
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "intestinal_inhibitor": ("SIM,GRA", "grapefruit juice", "dashdot"),
    }

    #: One glass of normal strength grapefruit juice daily: the furanocoumarins
    #: inactivate the intestinal CYP3A4 (mechanism based), the hepatic CYP3A4
    #: is not affected (half-life 2.7 and 2.0 hr). The AUC0-24 of simvastatin
    #: was 3.55-fold and the Cmax 3.93-fold of the control, of simvastatin acid
    #: 3.35-fold and 4.32-fold. A full inhibition of the intestinal CYP3A4 (0)
    #: gives a simvastatin AUC of 3.57-fold of the control in the model. Not
    #: fitted, the arm is validation data.
    f_cyp3a4_gu_grapefruit: ClassVar[float] = 0.0

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
                for arm, (intervention, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin, control and grapefruit juice."""
        simva_po = Q(40, "mg")
        changes = {
            "control": self.default_changes(),
            "intestinal_inhibitor": self.cyp3a4_changes(
                1.0, f_cyp3a4_gu=self.f_cyp3a4_gu_grapefruit
            ),
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
            "intestinal_inhibitor": Coadministration.GRAPEFRUIT_JUICE,
        }
        mappings = {}
        for arm, coadministration in coadministrations.items():
            suffix = "" if arm == "control" else "_inhi"
            for sid, yid in self.analytes:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{substance}_{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_simva_po_{arm}", xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
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
        """Simvastatin and its acid, control and grapefruit juice."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("intestinal_inhibitor", ["control", "intestinal_inhibitor"]),
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

            for arm in arms:
                _, label, linestyle = self.arms[arm]
                for k, (sid, yid) in enumerate(self.analytes):
                    substance = getattr(self.info, sid).name
                    plots[k].add_data(
                        task=f"task_simva_po_{arm}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {label}",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"Fig1_{substance}_{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        label=f"{self.sid}: {label}",
                    )
            figures[f"fig_{key}"] = fig

        return figures
