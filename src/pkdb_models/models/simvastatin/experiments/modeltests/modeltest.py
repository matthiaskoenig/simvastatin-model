"""Test of the pharmacokinetics of simvastatin in the whole-body model."""

from typing import override

from sbmlsim import Q
from sbmlsim.data import Data
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)


class modeltest(SimvastatinSimulationExperiment):
    """Test simulations.

    Checking basic model performance: a single oral dose of 20 mg simvastatin
    and the concentrations of simvastatin and simvastatin acid in the tissues
    and the amounts of the metabolites in urine and feces.
    """

    @override
    def data(self) -> dict[str, Data]:
        super().data()
        self.add_selections_data(
            selections=[
                "[Cki_plasma_simva]",
                "[Cki_plasma_simacid]",
                "Aurine_simmets",
                "Afeces_simmets",
            ]
        )
        return {}

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {**self.simulation_simva()}

    def simulation_simva(self) -> dict[str, Simulation]:
        """Single oral dose of 20 mg simvastatin, 15 hr."""
        simva_po = Q(20, "mg")

        tcsims = {}
        tcsims["simva_po"] = Simulation(
            start=0,
            end=15 * 60,
            preinit_changes={**self.default_changes(), "PODOSE_simva": simva_po},
        )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_all()}

    def figure_all(self) -> dict[str, Figure]:
        """Concentrations in the tissues and amounts in urine and feces."""
        unit_time = "hr"
        unit_concentration = "nM"
        unit_amount = "nmole"

        fig = Figure(
            experiment=self, sid="fig1", num_rows=3, num_cols=2, name="modeltest"
        )
        plots = fig.create_plots(xaxis=Axis("time", unit=unit_time), legend=True)
        # the left column linear, the right column logarithmic
        for k, scale in [(0, "linear"), (1, "log")]:
            plots[k].set_yaxis("simvastatin", unit_concentration, scale=scale)
        for k, scale in [(2, "linear"), (3, "log")]:
            plots[k].set_yaxis("simvastatin acid", unit_concentration, scale=scale)
        for k, scale in [(4, "linear"), (5, "log")]:
            plots[k].set_yaxis("amount", unit_amount, scale=scale)

        colors = {
            "ve": "black",
            "ki": "blue",
            "gu": "red",
            "li": "green",
            "urine": "darkorange",
            "feces": "brown",
        }

        tissues1 = {
            "ve": "venous blood",
            "ki": "kidney",
            "gu": "intestine",
            "li": "liver",
        }
        for tkey, tname in tissues1.items():
            yid_prefix = f"C{tkey}" if tkey == "ve" else f"C{tkey}_plasma"
            for k in [0, 1]:
                # concentrations
                plots[k].add_data(
                    task="task_simva_po",
                    xid="time",
                    yid=f"[{yid_prefix}_simva]",
                    label=tname,
                    color=colors[tkey],
                )
            for k in [2, 3]:
                # concentrations
                plots[k].add_data(
                    task="task_simva_po",
                    xid="time",
                    yid=f"[{yid_prefix}_simacid]",
                    label=tname,
                    color=colors[tkey],
                )

        # simvastatin and simvastatin acid are not excreted in the model, the
        # metabolites in urine and feces
        for tkey in ["urine", "feces"]:
            for k in [4, 5]:
                plots[k].add_data(
                    task="task_simva_po",
                    xid="time",
                    yid=f"A{tkey}_simmets",
                    label=f"metabolites ({tkey})",
                    color=colors[tkey],
                )
        return {"fig_all": fig}
