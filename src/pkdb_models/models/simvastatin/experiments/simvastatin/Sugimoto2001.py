"""Simulation experiment of the study Sugimoto2001."""

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


class Sugimoto2001(SimvastatinSimulationExperiment):
    """Simulation experiment of Sugimoto2001.

    Single oral dose of 10 mg simvastatin (two 5 mg tablets) in 8 healthy
    Japanese men after an overnight fast, on day 14 of placebo (control) or of
    St John's wort extract (300 mg three times daily), an inducer of CYP3A4.
    Plasma, mean and SE. The sampling times are 0, 0.5, 1, 2, 3, 4, 6, 8, 12
    and 24 hr; the axis of Figure 1 is not linear (the copy of the data has the
    nominal times, the digitization read the axis as linear).
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "placebo", "solid"),
        "stjohnswort": ("SIM,STJ", "St John's wort", "dotted"),
    }

    #: St John's wort (hyperforin) induces the hepatic and the intestinal
    #: CYP3A4 (PXR). 14 days decreased the AUC(0-24) of simvastatin to 0.52 and
    #: of simvastatin acid to 0.38 of placebo (ratio of the means; the mean of
    #: the individual ratios 0.66 and 0.48), the Cmax of the acid to 0.72. An
    #: activity of 1.5 of the reference in liver and gut gives a simvastatin
    #: AUC of 0.53 of the control in the model. Not fitted, the arm is
    #: validation data.
    f_cyp3a4_stjohnswort: ClassVar[float] = 1.5

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
        """Single oral dose of 10 mg simvastatin, alone and with St John's wort."""
        simva_po = Q(10, "mg")
        changes = {
            "control": self.default_changes(),
            "stjohnswort": self.cyp3a4_changes(self.f_cyp3a4_stjohnswort),
        }
        return {
            f"simva_po_{arm}": Simulation(
                start=0,
                end=24 * 60 + 1,
                preinit_changes={**changes[arm], "PODOSE_simva": simva_po},
            )
            for arm in self.arms
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        coadministrations = {
            "control": Coadministration.NONE,
            "stjohnswort": Coadministration.ST_JOHNS_WORT,
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
        """Simvastatin and its acid, alone and with St John's wort."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("stjohnswort", ["control", "stjohnswort"]),
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
