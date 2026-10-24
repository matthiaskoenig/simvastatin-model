"""Simulation experiment of the study Jones1998a."""

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


class Jones1998a(SimvastatinSimulationExperiment):
    """Simulation experiment of Jones1998a (CURVES).

    Multicentre, randomized, open label, parallel, 8 weeks: 518 patients with
    hypercholesterolemia (LDL-C >= 160 mg/dl, TG <= 400 mg/dl) on the NCEP step 1
    diet, among them simvastatin 10, 20 and 40 mg (n 70, 49, 61) once daily as
    recommended (in the evening); the other statins are not simulated. The
    baseline is the mean of weeks -2 and 0 (5.36, 5.95 and 5.66 mM), the data
    are the LDL cholesterol at week 8 and its mean change (SD). The model has
    no time of the day, the evening doses are doses every 24 h.
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the doses [mg]
    doses_mg: ClassVar[list[int]] = [10, 20, 40]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab1_2"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    df_mtype = df.loc[df["measurement_type"] == measurement_type].copy()
                    dset_mtype = DataSet.from_df(df_mtype, self.ureg)
                    # the simvastatin groups, the other statins are not simulated
                    for intervention in [f"SIM{dose}" for dose in self.doses_mg]:
                        dsets[
                            self.to_sid(f"{fig_id}_{substance}_{intervention}{suffix}")
                        ] = dset_mtype[dset_mtype.intervention == intervention]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mM]
        tcs_dict = {
            "simva_po_10mg": (Q(10, "mg"), 5.36),
            "simva_po_20mg": (Q(20, "mg"), 5.95),
            "simva_po_40mg": (Q(40, "mg"), 5.66),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + (8 * 7 + 1) * DAY,
                    dt=DAY / 100,
                    changes=[self.doses(dose, 8 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the simvastatin groups (Tables 1 and 2, weeks 0 and 8)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_SIM{dose}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab1_2_ldl-c_SIM{dose}"),
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
            for dose in self.doses_mg
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for dose in self.doses_mg:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: SV {dose}mg",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=f"{dose}mg"),
            )

    def _plot_data(self, ax: Axes, substance: str, wiggles: dict[int, float]) -> None:
        """Plot the data of a substance of the doses.

        The times of a dose are shifted by its `wiggles` [weeks], so that the
        points do not overlap. The number of subjects is the one of the last
        time point.
        """
        for dose in self.doses_mg:
            dataset = self._datasets[self.to_sid(f"Tab1_2_{substance}_SIM{dose}")]
            count = int(dataset["count"][dataset["time"].idxmax()])
            color = self.colormap_SV_dose(dose)
            ax.errorbar(
                dataset["time"] + wiggles[dose],
                dataset["mean"],
                color=color,
                label=f"{self.sid}: SV {dose}mg (n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker="s",
                linestyle="None",
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        self._plot_simulations(ax)
        self._plot_data(ax, "ldl-c", wiggles={10: -0.1, 20: 0.1, 40: 0.0})
        ax.set_xlim((-1, 9))
        ax.set_ylim((0.0, 7))
        ax.legend(ncol=2, loc="best", prop={"size": 12})
        ax.tick_params(axis="both", labelsize=18)
        return fig
