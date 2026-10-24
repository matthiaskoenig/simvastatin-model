"""Simulation experiment of the study Backman2000."""

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


class Backman2000(SimvastatinSimulationExperiment):
    """Simulation experiment of Backman2000.

    Simvastatin 40 mg po (tablet) after an overnight fast, on day 3 of placebo
    or of gemfibrozil 600 mg twice daily (GEM, the last dose 1 h before
    simvastatin), in 10 healthy volunteers (5 men, 5 women, 41 - 81 kg, mean
    61.9 kg).
    """

    #: the interventions and their names in the data
    interventions: ClassVar[dict[str, str]] = {"control": "SIM", "GEM": "SIM,GEM"}

    #: the mean body weight of the 10 subjects [kg] (individual weights)
    bodyweight: ClassVar[float] = 61.9

    #: activity of OATP1B1 and of the glucuronidation of simvastatin acid
    #: with gemfibrozil 600 mg twice daily: gemfibrozil and its glucuronide
    #: inhibit the hepatic uptake of the acid by OATP1B1 and its
    #: glucuronidation (UGT1A1, UGT1A3) and CYP2C8, not CYP3A4 (no inhibition
    #: in vitro, Backman2000). The observed AUC0-inf of simvastatin acid is
    #: 2.85-fold (Cmax 2.18-fold), of the lactone 1.35-fold; OATP1B1 0.5 and
    #: UGT 0.7 give 2.85-fold for the acid and leave the lactone unchanged.
    #: Not fitted, the arm is validation.
    f_oatp1b1_gemfibrozil: ClassVar[float] = 0.5
    f_ugt_gemfibrozil: ClassVar[float] = 0.7

    #: the line styles of the simulations and the data
    linestyles: ClassVar[dict[str, str]] = {"control": "solid", "GEM": "dashed"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
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
        """Simulations of simvastatin 40 mg po, alone and with gemfibrozil."""
        simva_po = Q(40, "mg")
        changes = {
            "control": {},
            "GEM": {
                **self.oatp1b1_changes(self.f_oatp1b1_gemfibrozil),
                "LI__f_ugt": Q(self.f_ugt_gemfibrozil, "dimensionless"),
            },
        }
        return {
            self.to_sid(f"simva_po_{intervention}"): Simulation(
                start=0,
                end=12 * 60,
                preinit_changes={
                    **self.default_changes(),
                    **self.bodyweight_changes(self.bodyweight),
                    **intervention_changes,
                    "PODOSE_simva": simva_po,
                },
            )
            for intervention, intervention_changes in changes.items()
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
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                coadministration=coadministration,
            )

        coadministrations = {
            "control": Coadministration.NONE,
            "GEM": Coadministration.GEMFIBROZIL,
        }
        mappings = {}
        for intervention, coadministration in coadministrations.items():
            suffix = "" if intervention == "control" else f"_{intervention.lower()}"
            for sid, yid in [("simva", "[Cve_simva]"), ("simacid", "[Cve_simacid]")]:
                substance = getattr(self.info, sid).name
                mappings[f"fm_{sid}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_simva_po_{intervention}"),
                        xid="time",
                        yid=yid,
                    ),
                    metadata=metadata(coadministration=coadministration),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_simva()}

    def figure_simva(self) -> dict[str, Figure]:
        """Simvastatin and simvastatin acid, alone and with gemfibrozil."""
        figures = {}
        for key, intervention_list in {
            "control": ["control"],
            "gemfibrozil": ["control", "GEM"],
        }.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_{key}"),
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
            plots[1].set_yaxis(self.info.simacid.axis, self.info.simacid.unit)

            for intervention in intervention_list:
                linestyle = self.linestyles[intervention]
                for k, (sid, yid) in enumerate(
                    [("simva", "[Cve_simva]"), ("simacid", "[Cve_simacid]")]
                ):
                    substance = getattr(self.info, sid).name
                    plots[k].add_data(
                        task=self.to_sid(f"task_simva_po_{intervention}"),
                        xid="time",
                        yid=yid,
                        label=f"sim: {intervention}",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                    )
                    plots[k].add_data(
                        dataset=self.to_sid(f"Fig1_{substance}_{intervention}"),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                        label=f"{self.sid}: {intervention}",
                    )
            figures[self.to_sid(f"fig_{key}")] = fig

        return figures
