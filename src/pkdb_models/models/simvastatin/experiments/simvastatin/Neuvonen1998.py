"""Simulation experiment of the study Neuvonen1998."""

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


class Neuvonen1998(SimvastatinSimulationExperiment):
    """Simulation experiment of Neuvonen1998.

    Single oral dose of 40 mg simvastatin (Zocor tablet) in 10 healthy
    volunteers (study I, 69 kg) on day 4 of itraconazole 200 mg/day or placebo,
    a crossover; fasted 2 hr before the dose, a meal 4 hr after it. Serum, mean
    and SEM (the copies hold the SD). Simvastatin (the lactone) by HPLC, limit
    of detection 10 ng/ml, below it in the placebo phase; the total simvastatin
    acid (the acid and the lactone after its hydrolysis to the acid) by GC-MS
    in ng of the acid; the HMG-CoA reductase inhibitors after a base hydrolysis
    (the total inhibitors) by a radioenzyme assay, in ng-eq of simvastatin acid.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "itraconazole": ("SIM,ITR", "itraconazole", "dashed"),
    }

    #: Itraconazole is a strong inhibitor of CYP3A4 in liver and gut. 200
    #: mg/day for 4 days increased the AUC of the total simvastatin acid
    #: 19-fold (Cmax 17-fold), the simvastatin lactone at least 10-fold (not
    #: detectable without itraconazole) and the total inhibitors 5.2-fold. An
    #: activity of 0.02 of the reference in liver and gut gives 18-fold
    #: simvastatin and simvastatin acid (sum of the masses) and 6.7-fold total
    #: inhibitors in the model. Not fitted, the arm is validation data.
    f_cyp3a4_itraconazole: ClassVar[float] = 0.02

    #: the limits of quantification (detection) of the assays [ng/ml]: a mean
    #: below half of the limit after the dose is mostly values below the limit,
    #: which the study set to 0, not a concentration
    loq: ClassVar[dict[str, float]] = {
        "simvastatin": 10.0,
        "simva+simacid": 0.5,
        "total simva inhibitors": 2.0,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                if substance not in self.loq:
                    continue
                df = df[(df.time == 0) | (df["mean"] >= 0.5 * self.loq[substance])]
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simva+simacid":
                    # the lactone is measured as the acid after its hydrolysis
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)
                elif substance == "total simva inhibitors":
                    dset.unit_conversion("mean", 1 / self.Mr.TotalInh)

                for arm, (intervention, _, _) in self.arms.items():
                    selection = dset[dset.intervention == intervention]
                    if not selection.empty:
                        dsets[self.to_sid(f"{fig_id}_{substance}_{arm}")] = selection
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin, alone and with itraconazole."""
        simva_po = Q(40, "mg")
        changes = {
            "control": self.default_changes(),
            "itraconazole": self.cyp3a4_changes(self.f_cyp3a4_itraconazole),
        }
        return {
            f"simva_po_{arm}": Simulation(
                start=0,
                end=(24 * 60) + 1,
                preinit_changes={**changes[arm], "PODOSE_simva": simva_po},
            )
            for arm in self.arms
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(
            coadministration: Coadministration = Coadministration.NONE,
        ) -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=Tissue.SERUM,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=coadministration,
            )

        itraconazole = metadata(coadministration=Coadministration.ITRACONAZOLE)
        # key: dataset, task, observable and metadata
        fit_dict: dict[str, tuple[str, str, str, PKPDMappingMetaData]] = {
            "fm_simva_and_simacid": (
                "Fig1_simva+simacid_control",
                "task_simva_po_control",
                "Cve_simva_and_simacid",
                metadata(),
            ),
            "fm_total_inhibitors": (
                "Fig1_total simva inhibitors_control",
                "task_simva_po_control",
                "Cve_total_inhibitors",
                metadata(),
            ),
            "fm_simva_inhi": (
                "Fig1_simvastatin_itraconazole",
                "task_simva_po_itraconazole",
                "[Cve_simva]",
                itraconazole,
            ),
            "fm_simva_and_simacid_inhi": (
                "Fig1_simva+simacid_itraconazole",
                "task_simva_po_itraconazole",
                "Cve_simva_and_simacid",
                itraconazole,
            ),
            "fm_total_inhibitors_inhi": (
                "Fig1_total simva inhibitors_itraconazole",
                "task_simva_po_itraconazole",
                "Cve_total_inhibitors",
                itraconazole,
            ),
        }
        return {
            key: FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(dataset),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=task, xid="time", yid=yid),
                metadata=md,
            )
            for key, (dataset, task, yid, md) in fit_dict.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Inhibitors and simvastatin, alone and with itraconazole."""
        fig_control = Figure(
            experiment=self,
            sid="Fig_control",
            num_rows=2,
            num_cols=1,
            **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
        )
        fig_itraconazole = Figure(
            experiment=self,
            sid="Fig_itraconazole",
            num_rows=3,
            num_cols=1,
            **SimvastatinSimulationExperiment.figuresize_kwargs_three_panel,
        )
        # the panels: the data, the selection and the color
        panels = [
            ("total simva inhibitors", "Cve_total_inhibitors", "totalsimvainhibitors"),
            ("simva+simacid", "Cve_simva_and_simacid", "simva_and_simacid"),
            ("simvastatin", "[Cve_simva]", "simva"),
        ]

        figures = {
            "control": (fig_control, ["control"]),
            "itraconazole": (fig_itraconazole, ["control", "itraconazole"]),
        }
        for fig, arms in figures.values():
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(
                self.info.totalsimvainhibitors.axis, self.info.totalsimvainhibitors.unit
            )
            plots[1].set_yaxis(
                self.info.simva_and_simacid.axis, self.info.simva_and_simacid.unit
            )
            if len(plots) > 2:
                plots[2].set_yaxis(self.info.simva.axis, self.info.simva.unit)

            for k, plot in enumerate(plots):
                substance, yid, color_key = panels[k]
                for arm in arms:
                    _, label, linestyle = self.arms[arm]
                    plot.add_data(
                        task=f"task_simva_po_{arm}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {label}",
                        color=self.colors_simva[color_key],
                        linestyle=linestyle,
                    )
                    # the lactone is below the limit of detection in the control
                    if substance != "simvastatin" or arm != "control":
                        plot.add_data(
                            dataset=self.to_sid(f"Fig1_{substance}_{arm}"),
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                            color=self.colors_simva[color_key],
                            linestyle=linestyle,
                            label=f"{self.sid}: {label}",
                        )

        return {"fig_control": fig_control, "fig_itraconazole": fig_itraconazole}
