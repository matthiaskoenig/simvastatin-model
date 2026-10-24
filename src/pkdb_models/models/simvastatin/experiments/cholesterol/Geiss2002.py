"""Simulation experiment of the study Geiss2002."""

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


class Geiss2002(SimvastatinSimulationExperiment):
    """Simulation experiment of Geiss2002.

    Heterozygous familial hypercholesterolemia (FH, n=9) and type 2 diabetes
    with a mixed hyperlipoproteinemia (n=8, with antidiabetic and
    antihypertensive drugs), simvastatin 10 - 20 mg daily for 4 weeks (mean
    13.3 +- 5 and 13.8 +- 5 mg) on the NCEP step I diet; the time of the dose is
    not reported. Fasting morning plasma (Table 1). The split into 10 and 20 mg
    is not reported, the groups are simulated with their mean dose (an
    approximation of a nonlinear dose response). The diabetic patients have no
    familial hypercholesterolemia, they are simulated as the FH types with
    their baseline LDL cholesterol as every population of the cholesterol
    studies.
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: task key of the simulations, dose [mg], label, number of
    #: subjects, marker and line style, health
    group_info: ClassVar[dict[str, tuple[str, float, str, int, str, str, Health]]] = {
        "SIM_FH": (
            "FH",
            13.3,
            "FH patients SV 13.3mg",
            9,
            "s",
            "solid",
            Health.PRIMARY_HYPERCHOLESTEROLEMIA,
        ),
        "SIM_diabetics": (
            "diabetics",
            13.8,
            "Diabetic patients SV 13.8mg",
            8,
            "o",
            "dotted",
            Health.T2DM,
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, self.ureg)
                for intervention in self.group_info:
                    dsets[self.to_sid(f"{fig_id}_{substance}_{intervention}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM]
        tcs_dict = {
            "simva_po_FH": (Q(13.3, "mg"), 7.1),
            "simva_po_diabetics": (Q(13.8, "mg"), 4.8),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + (4 * 7 + 1) * DAY,
                    dt=DAY / 100,
                    changes=[self.doses(dose, 4 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of both groups (Table 1, weeks 0 and 4)."""
        return {
            f"fm_ldlc_{intervention}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab1_ldl-c_{intervention}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_simva_po_{task_key}_{self.fit_fh_type}"),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.MULTIPLE,
                    health=health,
                    data=PKPDData.PD,
                    data_type=DataType.MEAN,
                ),
            )
            for intervention, (task_key, *_, health) in self.group_info.items()
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for task_key, dose, _, _, _, linestyle, _ in self.group_info.values():
            self.plot_FH_results(
                ax=ax,
                label=f"sim: SV {task_key}",
                color=dose,
                linestyle=linestyle,
                df=self.create_FH_results(task_key=task_key),
            )

    def _plot_data(self, ax: Axes, substance: str) -> None:
        """Plot the data of a substance of both groups."""
        for intervention, (
            _,
            dose,
            label,
            count,
            marker,
            *_,
        ) in self.group_info.items():
            dataset = self._datasets[self.to_sid(f"Tab1_{substance}_{intervention}")]
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"],
                dataset["mean"],
                dataset["mean_sd"],
                color=color,
                label=f"{self.sid}: {label} (n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker=marker,
                linestyle="None",
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        self._plot_simulations(ax)
        self._plot_data(ax, "ldl-c")
        ax.set_xlim((-0.5, 4.5))
        ax.set_ylim((0.0, 9))
        ax.legend(ncol=1, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig
