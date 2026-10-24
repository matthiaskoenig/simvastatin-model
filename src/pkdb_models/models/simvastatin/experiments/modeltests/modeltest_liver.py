"""Test of the cholesterol metabolism in the liver model."""

from copy import deepcopy
from pathlib import Path
from typing import ClassVar, override

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.scan import state_after_changes
from sbmlsim import Q
from sbmlsim.data import Data
from sbmlsim.model import AbstractModel
from sbmlsim.simulation import Change, Scan, Simulation
from sbmlsim.task import Task
from sbmlsim.units import Quantity

from pkdb_models.models.simvastatin import MODEL, MODEL_BASE_PATH
from pkdb_models.models.simvastatin.experiments.base_experiment import (
    FontKwargs,
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.experiments.FH_experiments.readout_dict_FH_scans import (
    Readout,
    axes_liver,
    readout_dict,
)


def _liver_readouts() -> dict[str, Readout]:
    """Get the quantities of the figures with the ids of the liver model.

    The liver model has the ids of the liver of the body model without the
    prefix `LI__`; the plasma LDL-C is the external LDL-C of the liver.
    """
    readouts = deepcopy(readout_dict)
    for readout in readouts.values():
        readout["sid"] = readout["sid"].replace("LI__", "")
    readouts["plasma ldlc"]["sid"] = "[ldlc_ext]"
    return readouts


class CholesterolLiverTestExperiment(PKPDSimulationExperiment):
    """Test the liver in isolation.

    Simulate:
    - healthy subject, normal cholesterol values 3 [mM] plasma LDL-C
    - no statins (no simvastatin)
    - good energy state (sufficient precursors synthesis, i.e. acetyl-CoA)
    - expectation: all concentrations are close to reference values (hmgcoa,
      cholesterol)

    The FH types with and without simvastatin acid, and the turnover of the
    LDLR pool for the calibration of the model.
    """

    pkpd_model = MODEL

    readout_dict: ClassVar[dict[str, Readout]] = _liver_readouts()
    axes_liver: ClassVar[dict[str, int]] = deepcopy(axes_liver)

    @override
    def models(self) -> dict[str, AbstractModel | Path]:
        return {
            "model": MODEL_BASE_PATH / "simvastatin_liver.xml",
        }

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        tcsims: dict[str, Simulation | Scan] = {}
        # the default changes of the liver of the body model
        default_changes = {
            k.replace("LI__", ""): v
            for k, v in SimvastatinSimulationExperiment._default_changes().items()
            if k.startswith("LI__")
        }

        fh_changes: dict[str, dict[str, Quantity]] = {
            "control": {
                "SYNTHESIS_LDLR_Vmax_f": Q(1, "dimensionless"),
            },
            "FH_type1": {
                "SYNTHESIS_LDLR_Vmax_f": Q(0.1, "dimensionless"),
            },
            "FH_type2_6": {"LDLRMEMBRANE_Kcat_f": Q(0.1, "dimensionless")},
            "FH_type3": {
                "LDLRLDLCIMP_Km_f": Q(10, "dimensionless"),
            },
            "FH_type4": {
                "LDLRLDLCIMP_Kcat_f": Q(0.1, "dimensionless"),
            },
            "FH_type5": {
                "LDLRRECYCLING_Kcat_f": Q(0.1, "dimensionless"),
            },
            "PCSK9": {
                "DEGRADATION_LDLR_Vmax_f": Q(10, "dimensionless"),
            },
        }
        for fh_key in fh_changes:
            for simva_key in ["placebo", "simva"]:
                # longterm simvastatin therapy
                simva_dose = Q(2.0, "nM") if simva_key == "simva" else Q(0.0, "nM")

                # 2 weeks each: control, simvastatin acid, washout
                tcsims[f"sim_{fh_key}_{simva_key}"] = Simulation(
                    start=0,
                    end=3 * 14 * 24 * 60,
                    preinit_changes={
                        **default_changes,
                        "[ldlc_ext]": Q(3, "mM"),
                        **fh_changes[fh_key],
                    },
                    changes=[
                        Change(14 * 24 * 60, {"[simacid]": simva_dose / 10}),
                        Change(2 * 14 * 24 * 60, {"[simacid]": Q(0.0, "nM")}),
                    ],
                )

        tcsims["sim_ldlr_pool"] = Simulation(
            start=0,
            end=5 * 60,
            preinit_changes={
                **default_changes,
                # look at pool turnover
                "ldlr": Q(1.0, "dimensionless"),
                "ldlr_membrane": Q(0.0, "dimensionless"),
                "ldlr_ldlc": Q(0.0, "dimensionless"),
                # no synthesis and degradation
                "SYNTHESIS_LDLR_Vmax_f": Q(0, "dimensionless"),
                "DEGRADATION_LDLR_Vmax_f": Q(0, "dimensionless"),
            },
        )

        # Simulation to set the half-life of LDLR (which is ~ 20 hr)
        # set synthesis and membrane transport to 0 -> no translocation; no recycling
        # only degradation of LDLR!
        tcsims["sim_ldlr_halflife"] = Simulation(
            start=0,
            end=50 * 60,
            preinit_changes={
                **default_changes,
                # look at pool turnover
                "ldlr": Q(1.0, "dimensionless"),
                "ldlr_membrane": Q(0.0, "dimensionless"),
                "ldlr_ldlc": Q(0.0, "dimensionless"),
                # no synthesis/membrane transport/recycling
                "SYNTHESIS_LDLR_Vmax_f": Q(0, "dimensionless"),
                "LDLRMEMBRANE_Kcat": Q(0, "mmole/min/l"),
                "LDLRRECYCLING_Kcat": Q(0, "mmole/min/l"),
            },
        )
        # Simulation of LDR turnover at constant cholesterol
        tcsims["sim_ldlr_turnover_constant"] = Simulation(
            start=0,
            end=5 * 60,
            preinit_changes={
                **default_changes,
                # look at pool turnover
                "ldlr": Q(1.0, "dimensionless"),
                "ldlr_membrane": Q(0.0, "dimensionless"),
                "ldlr_ldlc": Q(0.0, "dimensionless"),
            },
        )
        tcsims["sim_ldlr_turnover"] = Simulation(
            start=0,
            end=5 * 60,
            preinit_changes={
                **default_changes,
                # look at pool turnover
                "ldlr": Q(1.0, "dimensionless"),
                "ldlr_membrane": Q(0.0, "dimensionless"),
                "ldlr_ldlc": Q(0.0, "dimensionless"),
            },
        )

        tcsims["sim_default"] = Simulation(
            start=0,
            end=5 * 60,
            preinit_changes={
                **default_changes,
                "VLDLCEXP_Vmax": Q(0.05 * 50, "dimensionless"),
            },
        )

        return tcsims

    @override
    def tasks(self) -> dict[str, Task]:
        return {
            f"task_{key}": Task(model="model", simulation=key)
            for key in self.simulations()
        }

    @override
    def data(self) -> dict[str, Data]:
        self.add_selections_data(
            selections=[
                "time",
                "[ldlc_ext]",
                "[cho]",
                "[acoa]",
                "[hmgcoa]",
                "[hmgcoareductase]",
                "[hmgcoasynthase]",
                "ldlr_total",
                "ldlr",
                "ldlr_membrane",
                "ldlr_ldlc",
                "ldlr_degraded",
                "ldlr_fraction",
                "ldlr_ldlc_fraction",
                "ldlr_membrane_fraction",
                "v_uptake",
                "v_export",
                "v_synthesis",
                "v_reference",
                "v_net_export",
                "v_net_export_rate",
                "SYNTHESIS_LDLR",
                "DEGRADATION_LDLR",
                "TURNOVER_LDLR",
                "VLDLCEXP",
                "LDLRLDLCIMP",
                "LDLR_TO_MEMBRANE",
                "LDLRRECYCLING",
                "[vldlc_ext]",
                "[simacid]",
                "[simmets]",
                "active_inhibitors",
            ]
        )
        return {}

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {**self.figure_mpl1()}

    def figure_mpl1(self) -> dict[str, FigureMPL]:
        """The FH types with and without simvastatin and the test simulations."""
        # the weight normal: DejaVu Sans has no medium weight, matplotlib warns
        kwargs: FontKwargs = {"weight": "normal", "size": 17}
        title_kwargs: FontKwargs = {"weight": "bold", "size": 19}

        figures: dict[str, FigureMPL] = {}
        fig, axs_fig3 = plt.subplots(
            nrows=7, ncols=7, figsize=(38, 27), sharex="col", sharey="row"
        )
        fig.subplots_adjust(
            hspace=0.05, wspace=0.05, bottom=0.07, top=0.95, left=0.05, right=0.85
        )
        fig.suptitle("Liver Test Experiment", **title_kwargs)

        for k in range(7):
            axs_fig3[6, k].set_xlabel("time [weeks]", **kwargs)
        axs_fig3[0, 0].set_ylabel("Plasma cholesterol[mM]", **kwargs)
        axs_fig3[1, 0].set_ylabel("Hepatic cholesterol[mM]", **kwargs)
        axs_fig3[2, 0].set_ylabel("LDLR pool [1/litre]", **kwargs)
        axs_fig3[3, 0].set_ylabel("Fraction of total LDLR [-]", **kwargs)
        axs_fig3[4, 0].set_ylabel("LDLR rates [mmol/min]", **kwargs)
        axs_fig3[5, 0].set_ylabel("LDLC rates [mg/day]", **kwargs)
        axs_fig3[6, 0].set_ylabel("LDLC rates [mmol/min]", **kwargs)

        for k, task in enumerate(
            [
                "control",
                "FH_type1",
                "FH_type2_6",
                "FH_type3",
                "FH_type4",
                "FH_type5",
                "PCSK9",
            ]
        ):
            axs_fig3[0, k].set_title(task, **title_kwargs)
            for simva_key in ["placebo", "simva"]:
                task_id = f"task_sim_{task}_{simva_key}"
                xres = state_after_changes(self.results[task_id])
                for var_key, ax in self.axes_liver.items():
                    # get the time and convert it to weeks
                    x = Q(xres["time"].values, "min").to("weeks")

                    # get the sid to readout and get the array
                    sid = self.readout_dict[var_key]["sid"]
                    y = xres[sid].values

                    # plot adjustments
                    color = self.readout_dict[var_key]["color"]
                    linestyle = "solid" if simva_key == "simva" else "dotted"
                    label = (
                        self.readout_dict[var_key]["label"]
                        if simva_key != "placebo"
                        else None
                    )

                    # plot the data and the legend
                    axs_fig3[ax, k].plot(
                        x.magnitude,
                        y,
                        label=label,
                        linestyle=linestyle,
                        color=color,
                    )
        # the legend of every row, right of its last column
        for ax in self.axes_liver.values():
            axs_fig3[ax, 6].legend(
                loc="center left",
                bbox_to_anchor=(1.05, 0.5),
            )
        handles = []
        for simva_key in ["placebo", "simva"]:
            label = "Placebo" if simva_key == "placebo" else "2.0 nM SV"
            linestyle = "solid" if simva_key == "simva" else "dotted"

            handles.append(
                Line2D([], [], label=label, color="black", linestyle=linestyle)
            )
        axs_fig3[6, 3].legend(
            handles=handles,
            ncol=len(handles),
            loc="upper center",
            bbox_to_anchor=(0.5, -0.2),
        )
        figures["modeltest_liver_FH"] = fig

        # -------------------
        # figure for test conditions to calibrate the model
        for task, unit_time in {
            "sim_ldlr_turnover": "hr",
            "sim_ldlr_turnover_constant": "hr",
            "sim_ldlr_halflife": "hr",
            "sim_ldlr_pool": "min",
            "sim_default": "min",
        }.items():
            task_id = f"task_{task}"
            xres = state_after_changes(self.results[task_id])
            fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8), (ax9, _ax10)) = (
                plt.subplots(nrows=5, ncols=2, figsize=(25, 25), sharex="col")
            )
            # the panel, selection and label of the quantities
            readouts: list[tuple[Axes, str, str]] = [
                (
                    ax2,
                    "active_inhibitors",
                    "hepatic \nactive HMG-CoA\nreductase inhibitors",
                ),
                (ax3, "[ldlc_ext]", "plasma\nldl-c"),
                (ax3, "[vldlc_ext]", "plasma\nvldl-c"),
                (ax4, "[cho]", "hepatic cholesterol"),
                (ax5, "v_uptake", "cholesterol import"),
                (ax5, "v_reference", "reference (1 [g/day])"),
                (ax5, "v_synthesis", "cholesterol synthesis"),
                (ax5, "v_export", "cholesterol export"),
                (ax5, "v_net_export", "cholesterol net export"),
                (ax6, "[acoa]", "Acetyl-CoA"),
                (ax6, "[hmgcoa]", "HMG-CoA"),
                (ax7, "ldlr_ldlc", "LDLR_LDLC complex"),
                (ax7, "ldlr_membrane", "membrane bound LDLR"),
                (ax7, "ldlr", "free LDLR"),
                (ax7, "ldlr_degraded", "degraded LDLR"),
                (ax7, "ldlr_total", "total LDLR"),
                (ax8, "SYNTHESIS_LDLR", "protein synthesis"),
                (ax8, "DEGRADATION_LDLR", "protein degradation"),
                (ax9, "LDLR_TO_MEMBRANE", "LDLR membrane transport"),
                (ax9, "LDLRLDLCIMP", "LDLR internalization"),
                (ax9, "LDLRRECYCLING", "LDLR recycling"),
            ]
            fig.subplots_adjust(
                hspace=0.05, wspace=0.15, bottom=0.07, top=0.95, left=0.1, right=0.85
            )
            fig.suptitle(f"Liver Test Experiment {task_id}", **title_kwargs)

            ax1.set_ylabel("concentration [nM]")
            ax2.set_ylabel("concentration [nM]")
            ax3.set_ylabel("concentration [mM]")
            ax4.set_ylabel("concentration [mM]")
            ax5.set_ylabel("rates [g/day]")
            ax6.set_ylabel("concentration [mM]")
            ax7.set_ylabel("LDLR pool concentration [1/litre]")
            ax8.set_ylabel("LDLR turnover rates [µmole/min]")
            ax9.set_ylabel("LDLR pool turnover rates [µmole/min]")

            ax9.set_xlabel(f"time [{unit_time}]")
            ax8.set_xlabel(f"time [{unit_time}]")

            x = Q(xres["time"].values, "min").to(unit_time)

            for ax, sid, label in readouts:
                ax.plot(x.magnitude, xres[sid].values, label=label)
                ax.legend(loc="best")

            # hepatic simvastatin acid and metabolites
            sim_info = {
                "[simacid]": {"color": "blue", "label": "hepatic SVA"},
                "[simmets]": {"color": "red", "label": "hepatic SVM"},
            }
            for sid, info in sim_info.items():
                ax1.plot(
                    x.magnitude,
                    xres[sid].values,
                    label=info["label"],
                    color=info["color"],
                )
            ax1.legend(loc="best")

            figures[f"modeltest_liver_{task_id}"] = fig
        return figures
