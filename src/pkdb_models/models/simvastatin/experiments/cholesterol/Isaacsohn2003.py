"""Simulation experiment of the study Isaacsohn2003."""

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


class Isaacsohn2003(SimvastatinSimulationExperiment):
    """Simulation experiment of Isaacsohn2003.

    Randomized, double-blind, placebo controlled, parallel, multicentre, 6
    weeks: 195 patients with hypertriglyceridemia (fasting TG 300 - 900 mg/dl,
    LDL-C >= 75 mg/dl; about 60 % type IV hyperlipidemia with LDL-C < 130 mg/dl,
    16 % type 2 diabetes) on the AHA step 1 diet after a placebo run-in of 4
    weeks, placebo or simvastatin 20, 40 or 80 mg orally once daily in the
    evening (n 49, 47, 46, 47). LDL cholesterol by ultracentrifugation in
    fasting samples (Table 3). The patients have no familial
    hypercholesterolemia, they are simulated as the FH types with their
    baseline LDL cholesterol as every population of the cholesterol studies;
    the response of hypertriglyceridemia is flatter in the dose than the one of
    hypercholesterolemia. The model has no time of the day, the evening doses
    are doses every 24 h.
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the groups: intervention of the data, task key of the simulations, dose [mg]
    #: and label
    group_info: ClassVar[list[tuple[str, str, int, str]]] = [
        ("placebo", "placebo", 0, "placebo"),
        ("SIM20", "20mg", 20, "SV 20mg"),
        ("SIM40", "40mg", 40, "SV 40mg"),
        ("SIM80", "80mg", 80, "SV 80mg"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab3"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    if measurement_type == "concentration":
                        if substance == "cholesterol":
                            dset_mtype.unit_conversion("mean", 1 / self.Mr.cho)
                        elif substance == "hdl-c":
                            dset_mtype.unit_conversion("mean", 1 / self.Mr.hdlc)
                        elif substance == "ldl-c":
                            dset_mtype.unit_conversion("mean", 1 / self.Mr.ldlc)
                    for intervention in df.intervention.unique():
                        dsets[
                            self.to_sid(f"{fig_id}_{substance}_{intervention}{suffix}")
                        ] = dset_mtype[dset_mtype.intervention == intervention]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        # dose and baseline LDL cholesterol [mg/dl] / Mr = [mM]
        tcs_dict = {
            "simva_po_placebo": (Q(0, "mg"), 130 / self.Mr.ldlc.m * 10),
            "simva_po_20mg": (Q(20, "mg"), 127 / self.Mr.ldlc.m * 10),
            "simva_po_40mg": (Q(40, "mg"), 116 / self.Mr.ldlc.m * 10),
            "simva_po_80mg": (Q(80, "mg"), 119 / self.Mr.ldlc.m * 10),
        }
        tcsims: dict[str, Simulation | Scan] = {}
        for key, (dose, ldlc_init) in tcs_dict.items():
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"{key}_{fh_type_key}")] = self.presim(
                    end=WEEK + (6 * 7 + 1) * DAY,
                    dt=DAY / 25,
                    changes=[self.doses(dose, 6 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of every group (Table 3, weeks 0 and 6).

        The health is not reported (hypertriglyceridemia is no health of the
        vocabulary).
        """
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.NR,
            dosing=Dosing.MULTIPLE,
            health=Health.NR,
            data=PKPDData.PD,
            data_type=DataType.MEAN,
        )
        return {
            f"fm_ldlc_{intervention}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab3_ldl-c_{intervention}"),
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
                metadata=metadata,
            )
            for intervention, task_key, _, _ in self.group_info
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho()}

    def _plot_simulations(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types."""
        for _, task_key, dose, label in self.group_info:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: {label}",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=task_key),
            )

    def _plot_data(self, ax: Axes) -> None:
        """Plot the LDL cholesterol of the groups.

        The number of subjects is the one of the last time point.
        """
        for intervention, _, dose, label in self.group_info:
            dataset = self._datasets[self.to_sid(f"Tab3_ldl-c_{intervention}")]
            count = dataset["count"][dataset["time"].idxmax()]
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
                marker="s",
                linestyle="None",
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        self._plot_simulations(ax)
        self._plot_data(ax)
        ax.set_xlim((-0.5, 6.5))
        ax.set_ylim((0.0, 5))
        ax.legend(ncol=2, loc="lower left", prop={"size": 10})
        ax.tick_params(axis="both", labelsize=18)
        return fig
