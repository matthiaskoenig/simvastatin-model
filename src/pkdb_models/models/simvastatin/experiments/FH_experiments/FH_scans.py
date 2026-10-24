"""Scans of the severity of the FH types with simvastatin therapy."""

from copy import deepcopy
from typing import ClassVar, TypedDict, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from pkpdsim.scan import single_dimension, state_after_changes
from sbmlsim import Q
from sbmlsim.data import Data
from sbmlsim.simulation import Dimension, Scan

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.experiments.FH_experiments.readout_dict_FH_scans import (
    DoseProtocol,
    Readout,
    axes,
    readout_dict,
    simvastatin_protocol,
    time_FH_steadystate,
    time_SV_treatment,
)


class FHTypeInfo(TypedDict):
    """A FH type: the parameter it changes and its column of the figures."""

    fh_parameter: str
    title: str
    x_label: str
    label: str
    n_column: int


class FH_scans(SimvastatinSimulationExperiment):
    """Simulate timecourse of simvastatin therapy under varying FH strength.

    The factor of the parameter of every FH type is scanned (0.01 - 100) for
    every dose of the simvastatin protocol: the steady state of the FH type,
    then daily doses of simvastatin. The figures show the plasma LDL-C, its
    reduction by simvastatin and the LDLR pathway on the last day.
    """

    #: the time to the steady state of the FH type and of the treatment [weeks]
    time_FH_steadystate: ClassVar[int] = time_FH_steadystate
    time_SV_treatment: ClassVar[int] = time_SV_treatment

    simvastatin_protocol: ClassVar[dict[str, DoseProtocol]] = deepcopy(
        simvastatin_protocol
    )
    readout_dict: ClassVar[dict[str, Readout]] = deepcopy(readout_dict)
    axes: ClassVar[dict[str, int]] = deepcopy(axes)

    #: the factors of the scan, log10 from `scanspace_start` to `scanspace_stop`
    scanspace_start: ClassVar[int] = -2
    scanspace_stop: ClassVar[int] = 2
    scanspace_num: ClassVar[int] = 21

    #: the output steps of the last day
    steps_last_day: ClassVar[int] = 100

    #: the parameter of the liver which a FH type changes
    fh_scans: ClassVar[dict[str, dict[str, str]]] = {
        "control": {
            "parameter": "LI__SYNTHESIS_LDLR_Vmax_f",
        },
        "FH_type1": {
            "parameter": "LI__SYNTHESIS_LDLR_Vmax_f",
        },
        "FH_type2_6": {
            "parameter": "LI__LDLRMEMBRANE_Kcat_f",
        },
        "FH_type3": {
            "parameter": "LI__LDLRLDLCIMP_Km_f",
        },
        "FH_type4": {
            "parameter": "LI__LDLRLDLCIMP_Kcat_f",
        },
        "FH_type5": {
            "parameter": "LI__LDLRRECYCLING_Kcat_f",
        },
        "PCSK9": {
            "parameter": "LI__DEGRADATION_LDLR_Vmax_f",
        },
    }

    FH_type_dict: ClassVar[dict[str, FHTypeInfo]] = {
        "FH_type1": {
            "fh_parameter": "LI__SYNTHESIS_LDLR_Vmax_f",
            "title": "FH class 1\nLDLR synthesis",
            "x_label": "Class 1",
            "label": "LDLR synthesis",
            "n_column": 0,
        },
        "FH_type2_6": {
            "fh_parameter": "LI__LDLRMEMBRANE_Kcat_f",
            "title": "FH class 2 & 6\nLDLR membrane transport",
            "label": "LDLR membrane transport",
            "x_label": "Class 2 & 6",
            "n_column": 1,
        },
        "FH_type3": {
            "fh_parameter": "LI__LDLRLDLCIMP_Km_f",
            "title": "FH class 3\nLDLR-LDL binding",
            "label": "LDLR-LDL binding",
            "x_label": "Class 3",
            "n_column": 2,
        },
        "FH_type4": {
            "fh_parameter": "LI__LDLRLDLCIMP_Kcat_f",
            "title": "FH class 4\nLDLR-LDL internalization",
            "label": "LDLR-LDL internalization",
            "x_label": "Class 4",
            "n_column": 3,
        },
        "FH_type5": {
            "fh_parameter": "LI__LDLRRECYCLING_Kcat_f",
            "title": "FH class 5\nLDLR recycling",
            "label": "LDLR recycling",
            "x_label": "Class 5",
            "n_column": 4,
        },
        "PCSK9": {
            "fh_parameter": "LI__DEGRADATION_LDLR_Vmax_f",
            "title": "PCSK9 mutation\nLDLR degradation",
            "label": "LDLR degradation",
            "x_label": "PCSK9",
            "n_column": 5,
        },
    }

    @override
    def data(self) -> dict[str, Data]:
        # the 56 scans of 21 simulations of 7441 steps record only what the
        # figures read, every selection of the base experiment takes 3.9 GB
        self.add_selections_data(
            selections=[
                "time",
                self.readout_dict["plasma ldlc"]["sid"],
                *(self.readout_dict[key]["sid"] for key in self.rows_ldlr()),
            ]
        )
        return {}

    @override
    def simulations(self) -> dict[str, Scan]:
        return {
            **self.simulation_cho(),
        }

    def simulation_cho(self) -> dict[str, Scan]:
        """Scan of every FH type for every dose of simvastatin."""
        tcscans = {}

        # vary the FH type
        for fh_key in self.fh_scans:
            # vary the simvastatin dose
            for simva_key in self.simvastatin_protocol:
                simva_info = self.simvastatin_protocol[simva_key]
                # steady state for the parameter change (FH type) from 0, then the
                # daily doses of simvastatin
                start = WEEK + self.time_FH_steadystate * WEEK
                number = 7 * self.time_SV_treatment
                scan_info = self.fh_scans[fh_key]
                tcscans[self.to_sid(f"{fh_key}_{simva_key}")] = Scan(
                    simulation=self.presim(
                        end=start + number * DAY,
                        dt=DAY / 10,
                        changes=[
                            self.doses(Q(simva_info["dose"], "mg"), number, start=start)
                        ],
                        ldlc=3,
                        last_day_steps=self.steps_last_day,
                        # one scan in a run over the draws of the fitted
                        # parameters: the draws would multiply the 56 scans
                        preinit_changes=self.fitted_changes(),
                    ),
                    dimensions=[
                        Dimension(
                            "dim_fh",
                            values={
                                scan_info["parameter"]: Q(
                                    np.logspace(
                                        self.scanspace_start,
                                        self.scanspace_stop,
                                        num=self.scanspace_num,
                                    ),
                                    "dimensionless",
                                )
                            },
                            at=0,
                        )
                    ],
                )
        return tcscans

    def rows_ldlr(self) -> dict[str, int]:
        """Get the quantities of the figure of the LDLR pathway and their rows.

        The quantities and rows of `axes` without its first row, the plasma
        concentrations of simvastatin and simvastatin acid.
        """
        return {
            key: row - 1
            for key, row in self.axes.items()
            if key not in ["plasma simva", "plasma simacid"]
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {**self.figure_mpl1()}

    def figure_mpl1(self) -> dict[str, FigureMPL]:
        """Reduction of the plasma LDL-C and the LDLR pathway on the last day."""
        kwargs: FontKwargs = {"weight": "bold", "size": 20}
        title_kwargs: FontKwargs = {"weight": "bold", "size": 24}

        shaded_area_color = "grey"
        shaded_area_alpha = 0.2
        figures: dict[str, FigureMPL] = {}

        # -----------------------
        # relative reduction plot
        # -----------------------
        fig4, axs_fig4 = plt.subplots(
            nrows=3, ncols=6, figsize=(40, 17), sharey="row", sharex="col"
        )
        fig4.subplots_adjust(
            bottom=0.05, top=0.95, left=0.035, right=0.92, wspace=0.035, hspace=0.035
        )
        # going over FH types
        for key, value in self.FH_type_dict.items():
            ax_column = value["n_column"]
            axs_fig4[0, ax_column].set_title(value["title"], **title_kwargs)

            # FIXME: read from results
            x = np.logspace(start=-2, stop=2, num=21)
            for ax_row, reduction_type in enumerate(
                ["Plasma", "Absolute reduction", "Relative reduction"]
            ):
                y_placebo_data: list[float] = []
                # dependency on simvastatin dose
                for (
                    simvastatin_dict_key,
                    simvastatin_dict_value,
                ) in self.simvastatin_protocol.items():
                    # get results, a row per simulation of the scan
                    task_id = f"task_{key}_{simvastatin_dict_key}"
                    xres = state_after_changes(self.results[self.to_sid(task_id)])
                    data = (
                        xres[self.readout_dict["plasma ldlc"]["sid"]]
                        .transpose(single_dimension(xres), "time")
                        .values
                    )
                    mean_list: list[float] = []

                    for single_dim_data in data:
                        # mean of the last day
                        last_day = single_dim_data[-self.steps_last_day :]
                        mean = sum(last_day) / len(last_day)
                        mean_list.append(mean)
                        if simvastatin_dict_key == "control":
                            y_placebo_data = mean_list
                    if reduction_type == "Relative reduction":
                        # (placebo - dose) / placebo in
                        y = np.multiply(
                            100,
                            np.divide(
                                np.subtract(mean_list, y_placebo_data), y_placebo_data
                            ),
                        )
                        unit = "[%]"
                    elif reduction_type == "Absolute reduction":
                        # placebo - dose
                        y = np.subtract(mean_list, y_placebo_data)
                        unit = "[mM]"
                    else:
                        # plasma
                        y = mean_list
                        unit = "[mM]"

                    label = (
                        "No therapy"
                        if simvastatin_dict_key == "control"
                        else f"{simvastatin_dict_key} SV"
                    )
                    # plot results
                    axs_fig4[ax_row, ax_column].plot(
                        x,
                        y,
                        label=label,
                        linestyle="solid",
                        color="black",
                        markerfacecolor=self.colormap_SV_dose(
                            simvastatin_dict_value["dose"]
                        ),
                        marker="o",
                        markersize=10,
                        markeredgecolor="black",
                    )

                    axs_fig4[ax_row, 0].set_ylabel(
                        f"{reduction_type} LDL-C {unit}", **kwargs
                    )

                # make plot adjustments
                axs_fig4[2, ax_column].set_xlabel(
                    f"Change {value['label']} [-]", **kwargs
                )
                axs_fig4[ax_row, ax_column].set_xscale("log")

        axs_fig4[0, 5].legend(
            loc="center left", bbox_to_anchor=(1.05, 0.0), prop={"size": 22}
        )

        # add shaded areas
        for ax_row in [0, 1, 2]:
            for ax_column in [2, 5]:
                grey_lim_lower = -200 if ax_row == 2 else -20
                axs_fig4[ax_row, ax_column].fill(
                    [1, 10e3, 10e3, 1],
                    [grey_lim_lower, grey_lim_lower, 35, 35],
                    shaded_area_color,
                    alpha=shaded_area_alpha,
                    edgecolor="None",
                )
                axs_fig4[ax_row, ax_column].set_xlim(0.005, 200)
            for ax_column in [0, 1, 3, 4]:
                axs_fig4[ax_row, ax_column].fill(
                    [10**-3, 1, 1, 10**-3],
                    [-150, -150, 35, 35],
                    shaded_area_color,
                    alpha=shaded_area_alpha,
                    edgecolor="None",
                )
                axs_fig4[ax_row, ax_column].set_xlim(0.005, 200)

        for column in range(6):
            axs_fig4[0, column].set_ylim(0, 35)
            axs_fig4[1, column].set_ylim(-20.1, 0.1)
            axs_fig4[2, column].set_ylim(-101, 1)

            axs_fig4[0, column].vlines(
                x=1, ymin=0, ymax=35, linestyle="-", color="gray"
            )
            axs_fig4[1, column].vlines(
                x=1, ymin=-35, ymax=0.2, linestyle="-", color="gray"
            )
            axs_fig4[2, column].vlines(
                x=1, ymin=-250, ymax=0.2, linestyle="-", color="gray"
            )
            axs_fig4[0, column].get_xaxis().set_ticks([])
            axs_fig4[1, column].get_xaxis().set_ticks([])
            axs_fig4[2, column].get_xaxis().set_ticks([0.01, 0.1, 1, 10, 100])

        figures["ldlc_relative_reduction"] = fig4

        # ------------------------------------------------
        # create plots for LDLR readouts species and rates
        # ------------------------------------------------
        fig3, axs_fig3 = plt.subplots(
            nrows=7, ncols=6, figsize=(35, 28), sharex="col", sharey="row"
        )
        fig3.subplots_adjust(
            hspace=0.05, wspace=0.05, bottom=0.05, top=0.925, left=0.05, right=0.85
        )

        for key, value in self.FH_type_dict.items():
            n_column = value["n_column"]

            # dependency on simvastatin dose
            for k_simvastatin, simvastatin_dict_key in enumerate(
                self.simvastatin_protocol
            ):
                if simvastatin_dict_key not in ["control", "20 mg"]:
                    continue
                simvastatin_dict_value = self.simvastatin_protocol[simvastatin_dict_key]
                task_id = f"task_{key}_{simvastatin_dict_key}"
                xres = state_after_changes(self.results[self.to_sid(task_id)])
                x = Q(
                    np.logspace(
                        start=self.scanspace_start,
                        stop=self.scanspace_stop,
                        num=self.scanspace_num,
                    ),
                    "dimensionless",
                )

                for var_key, ax in self.rows_ldlr().items():
                    var_info = self.readout_dict[var_key]
                    axs_fig3[ax, 0].set_ylabel(
                        f"{var_info['y_label']}\n[{var_info['unit']}]", **kwargs
                    )

                    label = None if k_simvastatin == 0 else var_info["label"]

                    # a row per simulation of the scan, in the unit of the figure
                    data = (
                        Q(
                            xres[var_info["sid"]]
                            .transpose(single_dimension(xres), "time")
                            .values,
                            var_info["model_unit"],
                        )
                        .to(var_info["unit"])
                        .magnitude
                    )

                    # mean and standard deviation of the last day
                    mean_list = []
                    sd_list = []
                    for single_dim_data in data:
                        last_day = single_dim_data[-self.steps_last_day :]
                        mean = sum(last_day) / len(last_day)
                        mean_list.append(mean)

                        sd = np.std(last_day)
                        sd_list.append(sd)

                    axs_fig3[ax, n_column].errorbar(
                        x.magnitude,
                        mean_list,
                        yerr=sd_list,
                        marker=simvastatin_dict_value["marker"],
                        label=label,
                        linestyle=simvastatin_dict_value["linestyle"],
                        color=var_info["color"],
                        alpha=1,
                        markerfacecolor=var_info["color"],
                        markeredgecolor="black",
                        markersize=8,
                    )

                    axs_fig3[ax, n_column].axvline(x=1, linestyle="--", color="gray")
                    axs_fig3[ax, n_column].set_xscale("log")
                    if ax == 2:
                        axs_fig3[ax, n_column].set_yscale("log")

            # set title and some xaxis adjustments
            axs_fig3[0, n_column].set_title(value["title"], **title_kwargs)
            axs_fig3[6, n_column].get_xaxis().set_ticks([0.01, 0.1, 1, 10, 100])
            axs_fig3[6, n_column].set_xlabel(f"Change\n{value['label']} [-]", **kwargs)

        axs_fig3[0, 0].set_ylim(0, 35)

        for ax_row in range(7):
            axs_fig3[ax_row, 5].legend(
                loc="center left", bbox_to_anchor=(1.03, 0.5), prop={"size": 20}
            )

        # add shaded areas
        for ax_row in range(7):
            ylim = axs_fig3[ax_row, 0].get_ylim()
            ylim_lower = ylim[0]
            ylim_upper = ylim[1]
            for ax_column in range(6):
                ylim = axs_fig3[ax_row, ax_column].get_ylim()
                ylim_lower = min(ylim_lower, ylim[0])
                ylim_upper = max(ylim_upper, ylim[1])

            for ax_column in [2, 5]:
                axs_fig3[ax_row, ax_column].fill(
                    [1, 10e3, 10e3, 1],
                    [
                        ylim_lower * 0.5,
                        ylim_lower * 0.5,
                        ylim_upper * 2,
                        ylim_upper * 2,
                    ],
                    shaded_area_color,
                    alpha=shaded_area_alpha,
                    edgecolor="None",
                )
                axs_fig3[ax_row, ax_column].set_xlim(0.005, 150)
                axs_fig3[ax_row, ax_column].set_ylim(ylim_lower * 0.9, ylim_upper * 1.1)
            for ax_column in [0, 1, 3, 4]:
                axs_fig3[ax_row, ax_column].fill(
                    [10**-3, 1, 1, 10**-3],
                    [
                        ylim_lower * 0.5,
                        ylim_lower * 0.5,
                        ylim_upper * 1.5,
                        ylim_upper * 1.5,
                    ],
                    shaded_area_color,
                    alpha=shaded_area_alpha,
                    edgecolor="None",
                )
                axs_fig3[ax_row, ax_column].set_ylim(ylim_lower * 0.9, ylim_upper * 1.1)
                axs_fig3[ax_row, ax_column].set_xlim(0.005, 150)

        # custom legend for simvastatin dosing scheme
        handles = []
        for (
            simvastatin_dict_key,
            simvastatin_dict_value,
        ) in self.simvastatin_protocol.items():
            if simvastatin_dict_key not in ["control", "20 mg"]:
                continue
            label = (
                "No therapy"
                if simvastatin_dict_key == "control"
                else f"{simvastatin_dict_key} SV"
            )
            linestyle = "dotted" if simvastatin_dict_key == "control" else "solid"
            handles.append(
                Line2D(
                    [],
                    [],
                    alpha=1,
                    color="black",
                    label=label,
                    linestyle=linestyle,
                    marker=simvastatin_dict_value["marker"],
                    markersize=15,
                )
            )
        axs_fig3[0, 3].legend(
            handles=handles,
            ncol=len(handles),
            loc="upper center",
            bbox_to_anchor=(0.5, 1.5),
            prop={
                "size": 24,
            },
        )
        figures["ldlr_readouts_species"] = fig3

        return figures
