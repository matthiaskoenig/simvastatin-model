"""Simulation experiment of the study Lilja2000."""

import math
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
from sbmlsim.units import Quantity

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)


class Lilja2000(SimvastatinSimulationExperiment):
    """Simulation experiment of Lilja2000.

    Single oral dose of 40 mg simvastatin (Zocor tablet) in 10 healthy
    volunteers with water (control), with double strength grapefruit juice
    (200 ml three times daily for 2 days, on day 3 200 ml with the dose and 0.5
    and 1.5 hr after it), and with water 1, 3 and 7 days after the last
    grapefruit juice (200 ml double strength three times daily for 3 days). A
    meal 3 hr after the dose, the fast before it is not reported
    (`Fasting.NR`). Serum, LC-MS/MS, the means of the figure have no error bars.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "intestinal_inhibitor": ("SIM,GRA", "grapefruit juice", "dashdot"),
        "gfj_1d": ("SIM1D,GRA", "1 day after grapefruit juice", "dashed"),
        "gfj_3d": ("SIM3D,GRA", "3 days after grapefruit juice", "dotted"),
        "gfj_7d": ("SIM7D,GRA", "7 days after grapefruit juice", "dashdotdotted"),
    }

    #: Double strength grapefruit juice three times daily: the furanocoumarins
    #: inactivate the intestinal CYP3A4 (mechanism based), the AUCinf of
    #: simvastatin was 13.5-fold and the Cmax 12.0-fold of the control, of
    #: simvastatin acid 4.5-fold and 5.0-fold. The intestinal CYP3A4 is fully
    #: inhibited (0). The gut availability of the model (0.28) limits an
    #: intestinal effect to 3.6-fold, so the hepatic CYP3A4 is inhibited as well
    #: (0.12, as in Lilja1998 with the same regimen), which gives a simvastatin
    #: AUC of 14.0-fold of the control. Not fitted, the arm is validation data.
    f_cyp3a4_gu_grapefruit: ClassVar[float] = 0.0
    f_cyp3a4_li_grapefruit: ClassVar[float] = 0.12

    #: After the last grapefruit juice the hepatic CYP3A4 is not inhibited (the
    #: furanocoumarins are cleared within hours) and the inactivated intestinal
    #: CYP3A4 recovers by its resynthesis, a first order recovery from 0 with
    #: a half-life of 52 hr. The half-life gives the simvastatin AUC of the
    #: arm 1 day after the grapefruit juice (2.06-fold of the control, activity
    #: 0.27); the arms 3 and 7 days after are predicted (activity 0.62 and
    #: 0.89: AUC 1.37 and 1.08-fold simulated, 1.37 and 1.06-fold observed).
    #: Not fitted, the arms are validation data of the duration of the effect.
    gfj_recovery_half_life: ClassVar[float] = 52.0  # [hr]
    gfj_days: ClassVar[dict[str, float]] = {"gfj_1d": 1, "gfj_3d": 3, "gfj_7d": 7}

    #: the markers of the data of the arms
    markers: ClassVar[dict[str, str]] = {
        "control": "s",
        "intestinal_inhibitor": "o",
        "gfj_1d": "o",
        "gfj_3d": "^",
        "gfj_7d": "v",
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
                for arm, (intervention, _, _) in self.arms.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    def gfj_recovery_changes(self, days: float) -> dict[str, Quantity]:
        """Changes of the intestinal CYP3A4 `days` after the last grapefruit juice."""
        f_cyp3a4_gu = 1.0 - math.exp(
            -math.log(2) * days * 24 / self.gfj_recovery_half_life
        )
        return self.cyp3a4_changes(1.0, f_cyp3a4_gu=f_cyp3a4_gu)

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin, the arms of the grapefruit juice."""
        simva_po = Q(40, "mg")
        changes = {
            "control": self.default_changes(),
            "intestinal_inhibitor": self.cyp3a4_changes(
                self.f_cyp3a4_li_grapefruit,
                f_cyp3a4_gu=self.f_cyp3a4_gu_grapefruit,
            ),
            **{
                arm: self.gfj_recovery_changes(days)
                for arm, days in self.gfj_days.items()
            },
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
        suffixes = {
            "control": "",
            "intestinal_inhibitor": "_inhi",
            "gfj_1d": "_gfj1d",
            "gfj_3d": "_gfj3d",
            "gfj_7d": "_gfj7d",
        }
        mappings = {}
        for arm, suffix in suffixes.items():
            coadministration = (
                Coadministration.NONE
                if arm == "control"
                else Coadministration.GRAPEFRUIT_JUICE
            )
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
                        self, task=f"task_simva_po_{arm}", xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.SERUM,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=coadministration,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin and its acid, control and the arms of the grapefruit juice."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("intestinal_inhibitor", ["control", "intestinal_inhibitor"]),
            ("after_grapefruit_juice", ["control", "gfj_1d", "gfj_3d", "gfj_7d"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
                settings={"legend_scope": "row"},
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
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        marker=self.markers[arm],
                        label=f"{self.sid}: {label}",
                    )
            figures[f"fig_{key}"] = fig

        return figures
