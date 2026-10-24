"""Simvastatin therapy of the FH types, the LDL-C over 50 weeks of daily doses."""

from copy import deepcopy
from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.scan import state_after_changes
from sbmlsim import Q
from sbmlsim.data import Data
from sbmlsim.simulation import Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.experiments.FH_experiments.readout_dict_FH_scans import (
    DoseProtocol,
    simvastatin_protocol,
)


class FH_scan_simulation(SimvastatinSimulationExperiment):
    """Simulate timecourse of simvastatin therapy for different FH types.

    Every dose of the simvastatin protocol for every FH type, with the
    baseline LDL-C 5.9 mM: the plasma LDL-C, its absolute and its relative
    change, per FH type and the mean and range over the FH types. The results are the input of the comparison with the data
    (`Data_comparison.DataComparison`).
    """

    simvastatin_protocol: ClassVar[dict[str, DoseProtocol]] = deepcopy(
        simvastatin_protocol
    )

    @override
    def data(self) -> dict[str, Data]:
        # the plasma LDL-C, which the figure and the comparison with the data
        # read (the latter from the saved results)
        self.add_selections_data(selections=["time", "[Cve_ldlc]"])
        return {}

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            **self.simulation_cho(),
        }

    def simulation_cho(self) -> dict[str, Simulation]:
        """Daily doses of simvastatin for 50 weeks for every dose and FH type."""
        tcsims: dict[str, Simulation] = {}
        # vary the simvastatin dose
        for simva_key, simva_info in self.simvastatin_protocol.items():
            if simva_key == "control":
                continue
            # vary the fh_type
            for fh_type_key in self.fh_types:
                # non-weighted ldlc of all simulation experiments -> 5.9, 50 weeks
                number = 50 * 7
                tcsims[f"{simva_info['key']}_{fh_type_key}"] = self.presim(
                    end=WEEK + number * DAY,
                    dt=DAY / 10,
                    changes=[self.doses(Q(simva_info["dose"], "mg"), number)],
                    ldlc=5.9,
                    FH_type=fh_type_key,
                    time_shift=-(7 * 24 * 60),
                    # one simulation in a run over the draws of the fitted
                    # parameters: the draws would multiply the simulations of
                    # two years of every dose and FH type
                    preinit_changes=self.fitted_changes(),
                )

        return tcsims

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {**self.figure_mpl1()}

    #: the titles of the columns of the figure, the FH types
    fh_titles: ClassVar[dict[str, str]] = {
        "FH_type1": "FH class 1\nLDLR synthesis",
        "FH_type2_6": "FH class 2 & 6\nLDLR membrane transport",
        "FH_type3": "FH class 3\nLDLR-LDL binding",
        "FH_type4": "FH class 4\nLDLR-LDL internalization",
        "FH_type5": "FH class 5\nLDLR recycling",
        "PCSK9": "PCSK9 mutation\nLDLR degradation",
    }

    def figure_mpl1(self) -> dict[str, FigureMPL]:
        """Plasma LDL-C and its absolute and relative change per FH type and dose.

        A column per FH type and a last column with the mean over the FH types
        and their range (the band).
        """
        kwargs = {"weight": "bold", "size": 14}
        fh_types = list(self.fh_titles)
        fig, axs_fig = plt.subplots(
            nrows=3,
            ncols=len(fh_types) + 1,
            figsize=(5 * (len(fh_types) + 1), 12),
            sharex=True,
            sharey="row",
            layout="constrained",
        )
        rows = [
            ("LDL-C", "mM"),
            ("absolute change LDL-C", "mM"),
            ("relative change LDL-C", "%"),
        ]
        for simva_key, simva_info in self.simvastatin_protocol.items():
            if simva_key == "control":
                continue
            changes: list[list[np.ndarray]] = [[], [], []]
            time = np.empty(0)
            for n, fh_type in enumerate(fh_types):
                task_id = f"task_{simva_info['key']}_{fh_type}"
                xres = state_after_changes(self.results[task_id])
                time = Q(xres["time"].values, xres.units["time"]).to("week").magnitude
                conc = (
                    Q(xres["[Cve_ldlc]"].values.flatten(), xres.units["[Cve_ldlc]"])
                    .to("mM")
                    .magnitude
                )
                baseline = float(np.interp(0.0, time, conc))
                values = [
                    conc,
                    conc - baseline,
                    (conc - baseline) / baseline * 100,
                ]
                for row, y in enumerate(values):
                    changes[row].append(y)
                    axs_fig[row, n].plot(
                        time, y, color=simva_info["color"], linewidth=2
                    )
            # the mean over the FH types and their range
            for row in range(3):
                stacked = np.vstack(changes[row])
                ax = axs_fig[row, len(fh_types)]
                ax.fill_between(
                    time,
                    stacked.min(axis=0),
                    stacked.max(axis=0),
                    color=simva_info["color"],
                    alpha=0.2,
                    linewidth=0,
                )
                ax.plot(
                    time,
                    stacked.mean(axis=0),
                    color=simva_info["color"],
                    linewidth=2,
                    label=f"SV {simva_key}",
                )

        titles = [*self.fh_titles.values(), "mean of the FH types\n(range)"]
        for col, title in enumerate(titles):
            axs_fig[0, col].set_title(title, **kwargs)
            axs_fig[2, col].set_xlabel("time [weeks]", **kwargs)
        for row, (label, unit) in enumerate(rows):
            axs_fig[row, 0].set_ylabel(f"{label} [{unit}]", **kwargs)
        axs_fig[0, 0].set_ylim([0, 6.5])
        axs_fig[1, 0].set_ylim([-6, 0.2])
        axs_fig[2, 0].set_ylim([-90, 2])
        axs_fig[0, len(fh_types)].legend(loc="upper right")
        return {"fig": fig}
