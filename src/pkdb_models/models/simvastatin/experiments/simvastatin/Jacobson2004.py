"""Simulation experiment of the study Jacobson2004."""

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
    DAY,
    SimvastatinSimulationExperiment,
)


class Jacobson2004(SimvastatinSimulationExperiment):
    """Simulation experiment of Jacobson2004.

    Simvastatin 40 mg po in two of the four studies, healthy subjects, serum,
    body weight not reported. Study 1: a single dose on day 1 (alone) and on
    day 5 after verapamil (VER, 120 mg immediate release on day 2, then 480 mg
    extended release on the evenings of days 2 to 4), 15 men of whom 3
    discontinued (n = 12), food not reported. Study 2: once daily after
    breakfast on days 1 to 7 (alone, day 7) and 10 to 17 with clarithromycin
    500 mg twice daily on days 10 to 18 (CLA, day 17), n = 15; the profiles
    are of the last dose, the doses are at 0 h.
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {
        "control_1": "SIM1",
        "control_2": "SIM2",
        "VER": "SIM1,VER",
        "CLA": "SIM2,CLA",
    }

    #: activity of CYP3A4 (liver and gut) with verapamil 480 mg daily, a
    #: moderate mechanism based inhibitor of CYP3A4 (verapamil and
    #: norverapamil). The observed AUC of simvastatin is 4.2-fold of the
    #: control (geometric means 135 vs 32 ng*h/ml, Cmax 5-fold), of the acid
    #: 4.1-fold; 0.3 gives 4.7-fold, the factor of verapamil in Kantola1998
    #: (4.6-fold). Not fitted, the arm is validation.
    f_cyp3a4_verapamil: ClassVar[float] = 0.3

    #: activity of CYP3A4 (liver and gut) with clarithromycin 500 mg twice
    #: daily, a strong mechanism based inhibitor of CYP3A4. The observed AUC
    #: of simvastatin at steady state is 10-fold of the control (geometric
    #: means 219 vs 22 ng*h/ml, Cmax 7-fold), of the acid 12-fold; 0.12 gives
    #: about 10-fold. Not fitted, the arm is validation.
    f_cyp3a4_clarithromycin: ClassVar[float] = 0.12

    #: the simulation of the interventions
    task_ids: ClassVar[dict[str, str]] = {
        "control_1": "task_simva_po_study1_control",
        "VER": "task_simva_po_study1_inhibitor",
        "control_2": "task_simva_po_study2_control",
        "CLA": "task_simva_po_study2_inhibitor",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig4"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                if substance == "simvastatin":
                    dset.unit_conversion("mean", 1 / self.Mr.simva)
                elif substance == "simvastatin acid":
                    dset.unit_conversion("mean", 1 / self.Mr.simacid)
                for intervention, intervention_str in self.interventions.items():
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention_str
                    ]

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Simulations of simvastatin 40 mg po.

        Study 1 is a single dose of simvastatin. Study 2 has 7 doses, the last
        one at 0 h; the arm of clarithromycin is simulated as 7 doses with
        clarithromycin (in the study 8 doses after 7 alone and 2 days without),
        both are at steady state.
        """
        simva_po = Q(40, "mg")
        simulations = {}

        # study 1
        for key, changes in {
            "study1_control": {},
            "study1_inhibitor": self.cyp3a4_changes(self.f_cyp3a4_verapamil),
        }.items():
            simulations[self.to_sid(f"simva_po_{key}")] = Simulation(
                start=0,
                end=24 * 60,
                preinit_changes={
                    **self.default_changes(),
                    **changes,
                    "PODOSE_simva": simva_po,
                },
            )

        # study 2
        num_applications = 7
        for key, changes in {
            "study2_control": {},
            "study2_inhibitor": self.cyp3a4_changes(self.f_cyp3a4_clarithromycin),
        }.items():
            simulations[self.to_sid(f"simva_po_{key}")] = self.multiple_doses(
                dose=simva_po,
                number=num_applications,
                interval=DAY,
                time_shift=-(num_applications - 1) * DAY,
                changes={**self.default_changes(), **changes},
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(
            study: int,
            coadministration: Coadministration = Coadministration.NONE,
        ) -> PKPDMappingMetaData:
            """Metadata of study 1 (single dose) or 2 (multiple doses, fed)."""
            return PKPDMappingMetaData(
                tissue=Tissue.SERUM,
                route=Route.PO,
                application_form=ApplicationForm.NR,
                dosing=Dosing.SINGLE if study == 1 else Dosing.MULTIPLE,
                health=Health.HEALTHY,
                fasting=Fasting.NR if study == 1 else Fasting.FED,
                coadministration=coadministration,
            )

        # the intervention, the figure, the substance and the metadata
        specs: dict[str, tuple[str, str, str, PKPDMappingMetaData]] = {
            "fm_simva_single": ("control_1", "Fig1", "simva", metadata(1)),
            "fm_simacid_single": ("control_1", "Fig1", "simacid", metadata(1)),
            "fm_simva_single_inhi": (
                "VER",
                "Fig1",
                "simva",
                metadata(1, Coadministration.VERAPAMIL),
            ),
            "fm_simacid_single_inhi": (
                "VER",
                "Fig1",
                "simacid",
                metadata(1, Coadministration.VERAPAMIL),
            ),
            "fm_simva_multi": ("control_2", "Fig4", "simva", metadata(2)),
            "fm_simva_multi_inhibitor": (
                "CLA",
                "Fig4",
                "simva",
                metadata(2, Coadministration.CLARITHROMYCIN),
            ),
        }
        observables = {"simva": "[Cve_simva]", "simacid": "[Cve_simacid]"}
        return {
            key: FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(
                        f"{fig_id}_{getattr(self.info, sid).name}_{intervention}"
                    ),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.task_ids[intervention],
                    xid="time",
                    yid=observables[sid],
                ),
                metadata=metadata_,
            )
            for key, (intervention, fig_id, sid, metadata_) in specs.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Single dose (study 1) and multiple doses (study 2) of simvastatin."""
        # the figure of the data, the substances and the interventions
        figure_specs: dict[str, tuple[str, list[str], list[str]]] = {
            "control_singledose": ("Fig1", ["simva", "simacid"], ["control_1"]),
            "inhibitor_singledose": (
                "Fig1",
                ["simva", "simacid"],
                ["control_1", "VER"],
            ),
            "control_multipledose": ("Fig4", ["simva"], ["control_2"]),
            "inhibitor_multipledose": ("Fig4", ["simva"], ["control_2", "CLA"]),
        }
        observables = {"simva": "[Cve_simva]", "simacid": "[Cve_simacid]"}
        figures = {}
        for key, (fig_id, sids, intervention_list) in figure_specs.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_{key}"),
                num_rows=len(sids),
                num_cols=1,
                **(
                    SimvastatinSimulationExperiment.figuresize_kwargs_two_panel
                    if len(sids) == 2
                    else SimvastatinSimulationExperiment.figuresize_kwargs_one_panel
                ),
            )
            # the dosing interval of the last dose
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit, min=-1, max=25),
                legend=True,
            )
            for k, sid in enumerate(sids):
                info = getattr(self.info, sid)
                plots[k].set_yaxis(info.axis, info.unit)

            for intervention in intervention_list:
                condition = (
                    "control" if intervention.startswith("control") else "inhibitor"
                )
                label = (
                    condition
                    if condition == "control"
                    else f"{condition} ({intervention})"
                )
                linestyle = self.simtype_linestyle[condition]
                for k, sid in enumerate(sids):
                    plots[k].add_data(
                        task=self.task_ids[intervention],
                        xid="time",
                        yid=observables[sid],
                        label=f"sim: {label}",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(
                            f"{fig_id}_{getattr(self.info, sid).name}_{intervention}"
                        ),
                        xid="time",
                        yid="mean",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        label=f"{self.sid}: {label}",
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
