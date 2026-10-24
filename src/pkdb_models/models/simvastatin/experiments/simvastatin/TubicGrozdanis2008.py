"""Simulation experiment of the study TubicGrozdanis2008."""

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


class TubicGrozdanis2008(SimvastatinSimulationExperiment):
    """Simulation experiment of TubicGrozdanis2008.

    Single oral doses of 20 mg simvastatin in 7 healthy subjects after a fast
    of at least 10 hr, three formulations in a crossover: Zocor (the immediate
    release reference tablet), an immediate release capsule of a freeze-dried
    gelatin/lecithin powder and a delayed release tablet of the same powder
    (Eudragit RS coat, release in ileum and colon). Plasma, mean and SEM.

    The model describes the immediate release tablet, all formulations are
    compared with its simulation: the capsule raises the exposure of the acid
    1.65-fold over Zocor (a solubilizing formulation, presystemic hydrolysis),
    the delayed release tablet has a lag of about 3 hr and an AUC of simvastatin
    3-fold of Zocor (absorption in the distal intestine with little CYP3A4);
    the model has no regional absorption, both are validation data of its
    limitations.
    """

    #: the formulations: the label and the line style
    formulations: ClassVar[dict[str, tuple[str, str]]] = {
        "SIM_imm_ref": ("Zocor", "solid"),
        "SIM_imm": ("IR capsule", "dashed"),
        "SIM_delayed": ("DR tablet", "dotted"),
    }

    #: the key of the fit mapping and the application form of the formulations
    formulation_mappings: ClassVar[dict[str, tuple[str, ApplicationForm]]] = {
        "SIM_imm_ref": ("immediate_ref", ApplicationForm.TABLET),
        "SIM_imm": ("immediate", ApplicationForm.CAPSULE),
        "SIM_delayed": ("delayed", ApplicationForm.DELAYED_RELEASE_TABLET),
    }

    #: the analytes: the substance, the figure of the data and its selection
    analytes: ClassVar[list[tuple[str, str, str]]] = [
        ("simva", "Fig4", "[Cve_simva]"),
        ("simacid", "Fig5", "[Cve_simacid]"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4", "Fig5"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)

                for intervention in self.formulations:
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 20 mg simvastatin, an immediate release tablet."""
        return {
            "simva_po_control": Simulation(
                start=0,
                end=30 * 60 + 1,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_simva": Q(20, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for intervention, (key, form) in self.formulation_mappings.items():
            for sid, fig_id, yid in self.analytes:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}_{key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"{fig_id}_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task="task_simva_po_control", xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=form,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin and its acid, the immediate and the delayed release forms."""
        figures = {}
        for key, interventions in [
            ("control", ["SIM_imm_ref", "SIM_imm"]),
            ("delayed", ["SIM_imm_ref", "SIM_delayed"]),
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

            for k, (sid, fig_id, yid) in enumerate(self.analytes):
                substance = getattr(self.info, sid).name
                plots[k].add_data(
                    task="task_simva_po_control",
                    xid="time",
                    yid=yid,
                    label="sim: IR tablet",
                    color=self.colors_simva[sid],
                )
                for intervention in interventions:
                    label, linestyle = self.formulations[intervention]
                    plots[k].add_data(
                        dataset=self.to_sid(f"{fig_id}_{substance}_{intervention}"),
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
