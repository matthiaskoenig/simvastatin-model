"""Dose-dependency of the pharmacokinetic parameters of simvastatin."""

from typing import ClassVar, override

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.scan import point_band, point_timecourse
from sbmlsim import Q
from sbmlsim.data import Data
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.simvastatin_pk import (
    SUBSTANCES,
    calculate_simvastatin_pk,
    pk_selections,
    summarize,
)


class PKScanExperiment(SimvastatinSimulationExperiment):
    """Scan of the oral dose of simvastatin.

    The pharmacokinetic parameters of simvastatin and simvastatin acid in
    venous plasma are calculated for every dose of the scan, see
    `simvastatin_pk`. Simvastatin acid is formed from simvastatin and has no
    dose of its own, so it has no apparent clearance and volume. The
    simulations end 48 hr after the dose, in the terminal phase of both. The
    scan records only what the pharmacokinetic parameters read.
    """

    #: the substances of the figures, keys of `simvastatin_pk.SUBSTANCES`
    substances: ClassVar[list[str]] = ["simva", "simacid"]
    #: the pharmacokinetic parameters of the figures -> their label and unit
    pk_parameters: ClassVar[dict[str, tuple[str, str]]] = {
        "auc_last": ("AUC(0-tlast)", "nmol/l*hr"),
        "auc_inf_obs": ("AUC(0-inf)", "nmol/l*hr"),
        "cmax": ("Cmax", "nmol/l"),
        "tmax": ("tmax", "hr"),
        "lambda_z": ("lambda_z", "1/hr"),
        "thalf": ("Half-life", "hr"),
        "vz_f": ("Vz/F", "l"),
        "cl_f": ("CL/F", "l/hr"),
    }

    @override
    def data(self) -> dict[str, Data]:
        # the concentrations of the figures are those of the parameters
        self.add_selections_data(selections=pk_selections(self.substances))
        return {}

    @override
    def simulations(self) -> dict[str, Scan]:
        """Scan of the oral dose of simvastatin, 48 hr after the dose."""
        return {
            "simva_po_scan": Scan(
                simulation=Simulation(
                    time_unit="min",
                    end=48 * 60,
                    preinit_changes={**self.default_changes()},
                ),
                dimensions=[
                    Dimension(
                        "dim_dose",
                        values={"PODOSE_simva": Q(np.logspace(-1, 2, num=15), "mg")},
                    )
                ],
            )
        }

    def _across(self) -> str | None:
        """Get the dimension of the draws of the fitted parameters, if any."""
        return None if self.uncertainty is None else self.uncertainty.id

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        """Timecourses of the scan and the pharmacokinetic parameters versus dose.

        In a run over the draws of the fitted parameters (`uncertainty`) the
        curves are the medians of the draws with a band of their quantiles.
        """
        xres = self.results["task_simva_po_scan"]
        df = calculate_simvastatin_pk(
            self, xres, substances=tuple(self.substances), across=self._across()
        )
        return {
            **self.fig_timecourse(df),
            **self.fig_pk_versus_dose(df),
        }

    def fig_timecourse(self, df: pd.DataFrame) -> dict[str, FigureMPL]:
        """Plasma concentrations of simvastatin and simvastatin acid of the scan.

        A curve per dose, colored by the dose, on a linear (top) and a
        logarithmic (bottom) scale, with the band of the draws.
        """
        unit_time = "hr"
        unit_conc = "nmol/l"
        band_alpha = 0.25

        xres = self.results["task_simva_po_scan"]
        units = xres.units
        run = self.uncertainty
        doses = (
            df[df.substance == self.substances[0]]
            .groupby("point")["dose"]
            .first()
            .to_numpy()
        )
        norm = LogNorm(vmin=doses.min(), vmax=doses.max())
        cmap = plt.get_cmap("viridis")

        fig, axes = plt.subplots(
            nrows=2, ncols=2, figsize=(11, 9), layout="constrained"
        )
        fig.suptitle("Simvastatin dose scan (oral)", fontsize=14, fontweight="bold")
        for col, sid in enumerate(self.substances):
            selection = f"[Cve_{sid}]"

            def convert(values: np.ndarray, selection: str = selection) -> np.ndarray:
                """Get concentrations in the unit of the figure."""
                return Q(values, units[selection]).to(unit_conc).magnitude

            bottom = np.inf
            for k, dose in enumerate(doses):
                if run is None:
                    times, values = point_timecourse(xres, selection, dim_dose=k)
                    lower = upper = values
                else:
                    times, lower, values, upper = point_band(
                        xres,
                        selection,
                        across=run.id,
                        quantiles=run.quantiles,
                        dim_dose=k,
                    )
                t = Q(times, units["time"]).to(unit_time).magnitude
                c, c_lower, c_upper = convert(values), convert(lower), convert(upper)
                bottom = min(bottom, float(c_lower[-1]))
                color = cmap(norm(dose))
                for ax in axes[:, col]:
                    if run is not None:
                        ax.fill_between(
                            t, c_lower, c_upper, color=color, alpha=band_alpha, lw=0
                        )
                    ax.plot(t, c, color=color, linewidth=1.2)
                    ax.set_xlim(0, t[-1])
            for row, ax in enumerate(axes[:, col]):
                ax.set_title(f"{SUBSTANCES[sid]} (venous plasma)")
                ax.set_xlabel(f"time [{unit_time}]")
                ax.set_ylabel(f"concentration [{unit_conc}]")
                if row == 1:
                    ax.set_yscale("log")
                    # down to the last concentration of the smallest dose, the
                    # rise within the first minutes starts far below it
                    ax.set_ylim(bottom=0.5 * bottom)
                else:
                    ax.set_ylim(bottom=0)
        cbar = fig.colorbar(
            ScalarMappable(norm=norm, cmap=cmap),
            ax=axes,
            label="oral dose simvastatin [mg]",
            shrink=0.6,
        )
        # the gradient as vector cells: matplotlib rasterizes it into an
        # embedded image, which some SVG viewers do not show; the edges of
        # the cells in their color close the seams between them
        if cbar.solids is not None:
            cbar.solids.set_rasterized(False)
            cbar.solids.set_edgecolor("face")
        return {"fig_timecourse": fig}

    def fig_pk_versus_dose(self, df: pd.DataFrame) -> dict[str, FigureMPL]:
        """Pharmacokinetic parameters of simvastatin and simvastatin acid versus dose.

        A figure per parameter with a panel per substance which has the
        parameter: the apparent clearance and volume only exist for
        simvastatin, which has the dose. In a run over the draws the median of
        the draws with the band of their quantiles.
        """
        unit_dose = "mg"
        run = self.uncertainty
        figures: dict[str, FigureMPL] = {}
        for pkkey, (label, unit) in self.pk_parameters.items():
            substances = [
                sid
                for sid in self.substances
                if df[df.substance == sid][pkkey].notna().any()
            ]
            fig, axes = plt.subplots(
                nrows=1,
                ncols=len(substances),
                figsize=(5.5 * len(substances), 4.5),
                layout="constrained",
                squeeze=False,
            )
            fig.suptitle(f"{label} versus dose", fontsize=14, fontweight="bold")
            for ax, sid in zip(axes[0], substances, strict=True):
                df_sid = df[df.substance == sid]
                pk_unit = df_sid[f"{pkkey}_unit"].iloc[0]
                doses = df_sid.groupby("point")["dose"].first().sort_index()
                x = Q(doses.to_numpy(), df_sid["dose_unit"].iloc[0]).to(unit_dose)
                if run is None:
                    y = df_sid.set_index("point")[pkkey].sort_index().to_numpy()
                    lower = upper = y
                else:
                    summary = summarize(df_sid, pkkey, run.quantiles).sort_index()
                    y, lower, upper = (
                        summary[column].to_numpy()
                        for column in ["median", "lower", "upper"]
                    )
                y_q, lower_q, upper_q = (
                    Q(np.asarray(v, dtype=float), pk_unit).to(unit)
                    for v in (y, lower, upper)
                )
                color = self.colors_simva[sid]
                if run is not None:
                    ax.fill_between(
                        x.magnitude,
                        lower_q.magnitude,
                        upper_q.magnitude,
                        color=color,
                        alpha=0.25,
                        linewidth=0,
                    )
                ax.plot(
                    x.magnitude,
                    y_q.magnitude,
                    marker="o",
                    linestyle="-",
                    color=color,
                )
                ax.set_title(SUBSTANCES[sid])
                ax.set_xscale("log")
                ax.set_xlabel(f"oral dose simvastatin [{unit_dose}]")
                ax.set_ylabel(f"{label} [{y_q.units:~P}]")
                if pkkey in {"auc_last", "auc_inf_obs", "cmax"}:
                    # exposure is proportional to the dose
                    ax.set_yscale("log")
                else:
                    ax.set_ylim(bottom=0, top=1.2 * np.nanmax(upper_q.magnitude))
            figures[f"fig_{pkkey}"] = fig

        return figures
