"""Simulation experiment of the study Lilja1998."""

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


class Lilja1998(SimvastatinSimulationExperiment):
    """Simulation experiment of Lilja1998.

    Single oral dose of 60 mg simvastatin (3 Zocor tablets of 20 mg) in 10
    healthy volunteers, with water (control) or with double strength grapefruit
    juice (200 ml three times daily for 2 days, on day 3 200 ml with the dose
    and 0.5 and 1.5 hr after it), an inhibitor of the intestinal CYP3A4. No food
    from 1 hr before to 4 hr after the dose (`Fasting.FASTED`). Serum, mean and
    SEM; simvastatin and its acid by LC-MS/MS, the active and the total
    HMG-CoA reductase inhibitors (the latter after the hydrolysis of the
    lactones) by a radioenzyme inhibition assay.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "intestinal_inhibitor": ("SIM,GRA", "grapefruit juice", "dashdot"),
    }

    #: Double strength grapefruit juice three times daily: the furanocoumarins
    #: inactivate the intestinal CYP3A4 (mechanism based), the AUCinf of
    #: simvastatin was 16.1-fold and the Cmax 9.4-fold of the control, of
    #: simvastatin acid 6.8-fold and 6.5-fold, the half-lives unchanged. The
    #: intestinal CYP3A4 is fully inhibited (0). The gut availability of the
    #: model (0.28) limits an intestinal effect to 3.6-fold, so the hepatic
    #: CYP3A4 is inhibited as well (0.12, the same regimen as the grapefruit
    #: juice arm of Lilja2000), which gives a simvastatin AUC of 14.9-fold of
    #: the control at 60 mg (Lilja2000 at 40 mg: 13.5-fold observed, 14.0-fold
    #: simulated). Not fitted, the arm is validation data.
    f_cyp3a4_gu_grapefruit: ClassVar[float] = 0.0
    f_cyp3a4_li_grapefruit: ClassVar[float] = 0.12

    #: the analytes: the data set, the substance of the data, the key of the
    #: mapping, the selection and the key of the colors and labels
    analytes: ClassVar[list[tuple[str, str, str, str, str]]] = [
        ("Fig1", "simvastatin", "simva", "[Cve_simva]", "simva"),
        ("Fig1", "simvastatin acid", "simacid", "[Cve_simacid]", "simacid"),
        (
            "Fig2a",
            "active simva inhibitors",
            "active_inhibitors",
            "Cve_active_inhibitors",
            "activesimvainhibitors",
        ),
        (
            "Fig2b",
            "total simva inhibitors",
            "total_inhibitors",
            "Cve_total_inhibitors",
            "totalsimvainhibitors",
        ),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        mr = {
            "simvastatin": self.Mr.simva,
            "simvastatin acid": self.Mr.simacid,
            "active simva inhibitors": self.Mr.ActiveInh,
            "total simva inhibitors": self.Mr.TotalInh,
        }
        dsets = {}
        for fig_id in ["Fig1", "Fig2a", "Fig2b"]:
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
        """Single oral dose of 60 mg simvastatin, control and grapefruit juice."""
        simva_po = Q(60, "mg")
        changes = {
            "control": self.default_changes(),
            "intestinal_inhibitor": self.cyp3a4_changes(
                self.f_cyp3a4_li_grapefruit,
                f_cyp3a4_gu=self.f_cyp3a4_gu_grapefruit,
            ),
        }
        return {
            f"simva_po_{arm}": Simulation(
                start=0,
                end=12 * 60,
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
            for fig_id, substance, key, yid, _ in self.analytes:
                mappings[f"fm_{key}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{fig_id}_{substance}_{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_simva_po_{arm}", xid="time", yid=yid
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
        """Simvastatin, its acid and the inhibitors, control and grapefruit juice."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("intestinal_inhibitor", ["control", "intestinal_inhibitor"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=2,
                num_cols=2,
                **SimvastatinSimulationExperiment.figuresize_kwargs_four_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            for k, (_, _, _, _, info_key) in enumerate(self.analytes):
                info = getattr(self.info, info_key)
                plots[k].set_yaxis(info.axis, info.unit)
                if k < 2:
                    xaxis = plots[k].xaxis
                    if xaxis is not None:  # set by `create_plots`
                        xaxis.label_visible = False

            for arm in arms:
                _, label, linestyle = self.arms[arm]
                for k, (fig_id, substance, _, yid, info_key) in enumerate(
                    self.analytes
                ):
                    plots[k].add_data(
                        task=f"task_simva_po_{arm}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {label}",
                        color=self.colors_simva[info_key],
                        linestyle=linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"{fig_id}_{substance}_{arm}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[info_key],
                        linestyle=linestyle,
                        label=f"{self.sid}: {label}",
                    )
            figures[f"fig_{key}"] = fig

        return figures
