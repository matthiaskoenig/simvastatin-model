"""Simulation experiment of the study OBrien2003."""

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


class OBrien2003(SimvastatinSimulationExperiment):
    """Simulation experiment of OBrien2003.

    Single oral dose of 40 mg simvastatin (tablet) in 20 patients with chronic
    myeloid leukaemia (53 - 111 kg), open label in one sequence: simvastatin
    alone on day 1 (control), imatinib 400 mg/day on days 2 - 8 with
    simvastatin on day 8. Simvastatin directly after a low fat breakfast.
    Plasma by LC-MS/MS, mean and SD.
    """

    #: the arms: the intervention of the data, the label and the line style
    arms: ClassVar[dict[str, tuple[str, str, str]]] = {
        "control": ("SIM", "control", "solid"),
        "imatinib": ("SIM,IMA", "imatinib", "dashed"),
    }

    #: Imatinib is a competitive and mechanism based inhibitor of CYP3A4
    #: (moderate). 400 mg/day for 7 days increased the AUCinf of simvastatin
    #: 2.9-fold (Cmax 1.8-fold) and of simvastatin acid 2.3-fold (Cmax
    #: 1.7-fold). An activity of 0.45 of the reference in liver and gut gives
    #: 3.0-fold simvastatin and 2.9-fold simvastatin acid in the model. Not
    #: fitted, the arm is validation data.
    f_cyp3a4_imatinib: ClassVar[float] = 0.45

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
        """Single oral dose of 40 mg simvastatin, alone and with imatinib."""
        simva_po = Q(40, "mg")
        changes = {
            "control": self.default_changes(),
            "imatinib": self.cyp3a4_changes(self.f_cyp3a4_imatinib),
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
                tissue=Tissue.PLASMA,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.CML,
                fasting=Fasting.FED,
                coadministration=coadministration,
            )

        coadministrations = {
            "control": Coadministration.NONE,
            "imatinib": Coadministration.IMATINIB,
        }
        # the keys of the mappings of the arms
        suffixes = {"control": "", "imatinib": "_inhi"}
        mappings = {}
        for arm in self.arms:
            for sid, yid in self.analytes:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}{suffixes[arm]}"] = FitMapping(
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
                    metadata=metadata(coadministrations[arm]),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and its acid, alone and with imatinib."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("imatinib", ["control", "imatinib"]),
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

            for k, (sid, yid) in enumerate(self.analytes):
                substance = getattr(self.info, sid).name
                for arm in arms:
                    _, label, linestyle = self.arms[arm]
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
