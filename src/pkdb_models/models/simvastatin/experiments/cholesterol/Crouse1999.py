"""Simulation experiment of the study Crouse1999."""

from typing import ClassVar, override

from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Health,
    PKPDData,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.simulation import Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    SimvastatinSimulationExperiment,
)


class Crouse1999(SimvastatinSimulationExperiment):
    """Simulation experiment of Crouse1999.

    Open label, randomized, parallel, 49 centres, 12 weeks: 842 patients with
    hypercholesterolemia (NCEP) on a low fat diet after a run-in of 4 weeks,
    simvastatin 40 mg (n=202) or 80 mg (n=215) (or atorvastatin 20 and 40 mg,
    not simulated) once every evening. Fasting plasma; the baseline LDL
    cholesterol is 212.7 mg/dl (5.5 mM) in every group. The change of the LDL
    cholesterol of Table 1 is the average of the changes at weeks 6 and 12
    (prespecified), the data have it at week 12, where the simulation is
    compared with it (with a plateau of the LDL cholesterol after 6 weeks both
    coincide). The model has no time of the day, the evening doses are doses
    every 24 h.
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    interventions: ClassVar[list[str]] = ["SIM80", "SIM40"]

    #: dose [mg] and number of subjects of the interventions
    dose_count: ClassVar[dict[str, tuple[int, int]]] = {
        "SIM40": (40, 202),
        "SIM80": (80, 215),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                key = "ldl-hdl-c-fraction" if substance == "ldl/hdl-c" else substance
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    if measurement_type == "concentration":
                        if substance == "hdl-c":
                            dset_mtype.unit_conversion("mean", 1 / self.Mr.hdlc)
                        elif substance == "ldl-c":
                            dset_mtype.unit_conversion("mean", 1 / self.Mr.ldlc)
                    for intervention in self.interventions:
                        dsets[self.to_sid(f"{fig_id}_{key}_{intervention}{suffix}")] = (
                            dset_mtype[dset_mtype.intervention == intervention]
                        )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # baseline LDL cholesterol of 212.7 mg/dl [mM], 5.500387897595035
        ldlc_init = 212.7 / self.Mr.ldlc.m * 10
        tcsims: dict[str, Simulation | Scan] = {}
        for dose in [40, 80]:
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{dose}mg_{fh_type_key}")] = self.presim(
                    end=WEEK + (12 * 7 + 1) * DAY,
                    dt=DAY / 25,
                    changes=[self.doses(Q(dose, "mg"), 12 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the simvastatin groups (Table 1, weeks 0 and 12)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.NR,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{intervention}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab1_ldl-c_{intervention}"),
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{dose}mg_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=metadata,
            )
            for intervention, (dose, _) in self.dose_count.items()
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for dose in [40, 80]:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: SV {dose}mg",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=f"{dose}mg"),
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        self._plot_simulations(ax)
        for intervention, (dose, count) in self.dose_count.items():
            dataset = self._datasets[self.to_sid(f"Tab1_ldl-c_{intervention}")]
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                color=color,
                label=f"{self.sid}: SV {dose}mg (n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker="s",
                linestyle="None",
            )
        ax.set_xlim((-0.5, 13))
        ax.set_ylim((0.0, 7))
        ax.legend(ncol=1, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig
