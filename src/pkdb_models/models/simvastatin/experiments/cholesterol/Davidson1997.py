"""Simulation experiment of the study Davidson1997."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
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
from pkpdsim.scan import state_after_changes
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.simulation import Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)

#: the day of the pharmacokinetics, the mid-point of a period of 6 weeks: the
#: dose of this day and the 24 h after it [days after the first dose]
PK_DAY = 21


class Davidson1997(SimvastatinSimulationExperiment):
    """Simulation experiment of Davidson1997.

    Double-blind crossover of 3 periods of 6 weeks with a placebo washout of 2
    weeks between them: 156 patients with primary hypercholesterolemia (LDL-C
    160 - 250 mg/dl, TG <= 350 mg/dl) on the NCEP step 1 diet after a placebo
    run-in of 4 weeks, simvastatin 40, 80 and 160 mg (tablets of 20 and 40 mg)
    every evening. Fasting lipids at weeks 0, 6, 14 and 22. Table 1 has the
    baseline (mean, n=147) and the median change after 6 weeks of every dose
    (n 141, 144, 140); the concentrations at 6 weeks are derived from the mean
    baseline and the median change. Every period is simulated from the
    untreated baseline (the 2 weeks of washout), and the medians are compared
    with the simulation of the mean subject. The model has no time of the day,
    the evening doses are doses every 24 h.

    Fig 2 has the pharmacokinetic substudy (n=18): the HMG-CoA reductase
    inhibitory activity in plasma (simvastatin acid equivalents, the active
    inhibitors) over 24 h at the mid-point of every period (steady state, 4 h
    fasting before the dose), its AUC(0-24 h) and Cmax (mean and SD).
    """

    #: the FH type of the fit mappings (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the doses [mg] and the number of subjects at 6 weeks
    dose_count: ClassVar[dict[int, int]] = {40: 141, 80: 144, 160: 140}

    #: the pharmacokinetic parameters of Fig 2 and their labels
    pk_parameters: ClassVar[dict[str, str]] = {
        "auc24": "AUC(0-24 h) [ng eq h/ml]",
        "cmax": "Cmax [ng eq/ml]",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        mr = {
            "hdl-c": self.Mr.hdlc,
            "ldl-c": self.Mr.ldlc,
            "vldl-c": self.Mr.vldlc,
            "cholesterol": self.Mr.cho,
        }
        dsets = {}
        for fig_id in ["Tab1"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    if measurement_type == "concentration" and substance in mr:
                        dset_mtype.unit_conversion("mean", 1 / mr[substance])
                        dset_mtype.unit_conversion("median", 1 / mr[substance])
                    for dose in self.dose_count:
                        intervention = f"SIM{dose}"
                        key = f"{fig_id}_{substance}_{intervention}{suffix}"
                        dsets[self.to_sid(key)] = dset_mtype[
                            dset_mtype.intervention == intervention
                        ]
                        if substance == "ldl-c" and not suffix:
                            # the median at 6 weeks of the fit mappings
                            dsets[self.to_sid(f"{key}_week6")] = dset_mtype[
                                (dset_mtype.intervention == intervention)
                                & (dset_mtype.time == 6)
                            ]
        for fig_id in ["Fig2"]:
            for _, df in self.load_dataframes_by_substance(fig_id).items():
                for parameter in self.pk_parameters:
                    dsets[self.to_sid(f"{fig_id}_{parameter}")] = (
                        self.measurement_dataset(df, parameter)
                    )
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        ldlc_init = 199 / self.Mr.ldlc.m * 10  # [mM]
        tcsims: dict[str, Simulation | Scan] = {}
        for dose in self.dose_count:
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_{dose}mg_{fh_type_key}")] = self.presim(
                    end=WEEK + (6 * 7 + 1) * DAY,
                    dt=DAY / 100,
                    changes=[self.doses(Q(dose, "mg"), 6 * 7 + 1)],
                    ldlc=ldlc_init,
                    FH_type=fh_type_key,
                    time_shift=-WEEK,
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The median LDL cholesterol after 6 weeks of every dose (Table 1)."""
        metadata = PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.MULTIPLE,
            health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
            data=PKPDData.PD,
            data_type=DataType.MEDIAN,
        )
        return {
            f"fm_ldlc_SIM{dose}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Tab1_ldl-c_SIM{dose}_week6"),
                    xid="time",
                    yid="median",
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
            for dose in self.dose_count
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cho": self._figure_cho(), "fig_pk": self._figure_pk()}

    def _plot_data(self, ax: Axes, dose: int) -> None:
        """Plot the LDL cholesterol of a dose, one point per time.

        The baseline is the mean with its standard deviation, the value after 6
        weeks the median (derived from the median change).
        """
        dataset = self._datasets[self.to_sid(f"Tab1_ldl-c_SIM{dose}")]
        color = self.colormap_SV_dose(dose)
        for _, row in dataset.iterrows():
            if row["time"] == 0:
                y, y_err, point_label = row["mean"], row["mean_sd"], None
            else:
                y, y_err = row["median"], None
                point_label = (
                    f"{self.sid}: SV {dose}mg (median, n={self.dose_count[dose]})"
                )
            ax.errorbar(
                row["time"],
                y,
                y_err,
                color=color,
                label=point_label,
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker="s",
                linestyle="None",
            )

    def _figure_cho(self) -> FigureMPL:
        """LDL cholesterol of the simulations and the data."""
        fig, ax = self.create_cholesterol_plot()
        for dose in self.dose_count:
            self.plot_FH_results(
                ax=ax,
                label=f"sim: SV {dose}mg",
                color=dose,
                linestyle="solid",
                df=self.create_FH_results(task_key=f"{dose}mg"),
            )
        for dose in self.dose_count:
            self._plot_data(ax, dose)
        ax.set_xlim((-0.5, 6.5))
        ax.set_ylim((0.0, 7))
        ax.legend(ncol=2, loc="lower left", prop={"size": 10})
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _simulated_pk(self, dose: int) -> dict[str, tuple[float, float, float]]:
        """AUC(0-24 h) [ng eq h/ml] and Cmax [ng eq/ml] of the active inhibitors.

        The 24 h after the dose of day `PK_DAY` (steady state); the active
        inhibitors are converted with the molecular weight of simvastatin acid
        (hydroxyacid equivalents).

        Returns:
            The value, its lower and its upper quantile over the draws of the
            fitted parameters in a run over them (`uncertainty`, the median of
            the draws), the value three times without draws.
        """
        task = self.to_sid(f"task_simva_po_{dose}mg_{self.fit_fh_type}")
        xres = state_after_changes(self.results[task])
        time = Q(xres["time"].values, xres.units["time"]).to("hr").magnitude
        across = self.across()
        values = xres["Cve_active_inhibitors"]
        if across is not None and across in values.dims:
            values = values.transpose(across, "time")
        else:
            values = values.expand_dims("draw").transpose("draw", "time")
        conc = (
            (Q(values.values, xres.units["Cve_active_inhibitors"]) * self.Mr.ActiveInh)
            .to("ng/ml")
            .magnitude
        )
        t0 = Q(PK_DAY * DAY, "min").to("hr").magnitude
        window = (time >= t0 - 1e-6) & (time <= t0 + 24 + 1e-6)
        draws = {
            "auc24": np.trapezoid(conc[:, window], time[window], axis=1),
            "cmax": conc[:, window].max(axis=1),
        }
        run = self.uncertainty
        quantiles = (0.5, 0.5) if run is None else run.quantiles
        return {
            key: (
                float(np.median(v)),
                float(np.quantile(v, quantiles[0])),
                float(np.quantile(v, quantiles[1])),
            )
            for key, v in draws.items()
        }

    def _figure_pk(self) -> FigureMPL:
        """AUC(0-24 h) and Cmax of the active inhibitors at steady state (Fig 2)."""
        kwargs: FontKwargs = {"weight": "bold", "size": 14}
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
        doses = list(self.dose_count)
        x = np.arange(len(doses))
        simulated = {dose: self._simulated_pk(dose) for dose in doses}
        for ax, (parameter, label) in zip(
            axes, self.pk_parameters.items(), strict=True
        ):
            dataset = self._datasets[self.to_sid(f"Fig2_{parameter}")]
            means, sds = [], []
            for dose in doses:
                row = dataset[dataset.intervention == f"SIM{dose}"]
                means.append(float(row["mean"].iloc[0]))
                sds.append(float(row["mean_sd"].iloc[0]))
            ax.bar(
                x,
                means,
                yerr=sds,
                width=0.5,
                color=[self.colormap_SV_dose(dose) for dose in doses],
                edgecolor="black",
                capsize=6,
                label=f"{self.sid} (n=18)",
            )
            value, lower, upper = (
                np.array([simulated[dose][parameter][k] for dose in doses])
                for k in range(3)
            )
            ax.errorbar(
                x,
                value,
                yerr=[value - lower, upper - value],
                marker="o",
                markersize=10,
                color="black",
                linestyle="None",
                capsize=6,
                label="sim: active inhibitors",
            )
            ax.set_xticks(x, [f"{dose} mg" for dose in doses])
            ax.set_xlabel("Daily dose", **kwargs)
            ax.set_ylabel(label, **kwargs)
            ax.set_ylim(bottom=0)
            ax.legend(loc="upper left", prop={"size": 11})
        fig.tight_layout()
        return fig
