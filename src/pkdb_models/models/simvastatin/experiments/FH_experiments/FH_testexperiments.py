"""Test of the familial hypercholesterolemia (FH) types in the whole-body model."""

from typing import ClassVar, override

from pkpdsim.initial_values import init_concentrations_changes
from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)


class FH_testexperiments(SimvastatinSimulationExperiment):
    """Test of the FH types: the LDL-C and the LDLR pathway over 24 weeks.

    The plasma LDL-C of every tissue starts at 4 mM, a presimulation of 35 days
    precedes the 24 weeks. Only the control is simulated; the FH types are
    - type 1: LDLR not synthesized at all
    - type 2: LDLR is not properly transported from the endoplasmic reticulum
      to the Golgi apparatus for expression on the cell surface; the parameter
      scales the kcat of the transport LDLR -> LDLR_membrane
    - type 3: LDLR does not properly bind LDL on the cell surface because of a
      defect in either apolipoprotein B100 (R3500Q) or in LDL-R; the parameter
      scales the km of LDLC_plasma -> cho_liver
    - type 4: LDLR bound to LDL does not properly cluster in clathrin-coated
      pits for receptor-mediated endocytosis
    - type 5: LDLR is not recycled back to the cell surface; the parameter
      scales the kcat of the recycling LDLR_inactive -> LDLR
    """

    #: the simulations and their colors
    tcs_dict: ClassVar[dict[str, dict[str, str]]] = {
        "control": {"color": "black"},
    }

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        simva_po = Q(0, "mg")
        presim_time = 24 * 60 * 35
        # initial plasma LDL-C of all tissues [mM], the units of the model
        initial_concentration = 4
        weeks = 24
        days = 7 * weeks

        # changes to set all cholesterol plasma concentrations prior to the
        # actual dosing scheme
        r = self._models["model"].r
        if r is None:
            raise ValueError(f"The model of '{self.sid}' is not loaded.")
        for key in self.tcs_dict:
            # presimulation of 35 days, then daily doses
            end = presim_time + days * 24 * 60
            tcsims[key] = Simulation(
                start=0,
                end=end,
                # one simulation in a run over the draws of the fitted
                # parameters, which have no effect without simvastatin
                preinit_changes={
                    **self.default_changes(),
                    **self.fitted_changes(),
                    **init_concentrations_changes(r, "ldlc", initial_concentration),
                },
                changes=[self.doses(simva_po, days, start=presim_time)],
                time_shift=-(presim_time),
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.fig_simulation()}

    def fig_simulation(self) -> dict[str, Figure]:
        """LDL-C, liver cholesterol and the LDLR pathway."""
        fig_fh = Figure(
            experiment=self,
            sid="Figure_fh",
            num_rows=4,
            num_cols=2,
            height=20,
            width=25,
        )

        plots = fig_fh.create_plots(xaxis=Axis("time", unit="weeks"), legend=True)
        fig_fh.set_title(self.sid)

        plots[0].set_yaxis("plasma LDL-C", self.info.ldlc.unit)
        plots[1].set_yaxis("liver cholesterol", self.info.cho.unit)

        plots[2].set_yaxis("LDL-R synthesis rate", unit="mmole/min")
        plots[3].set_yaxis("LDL-C import rate", unit="mg/day")
        plots[4].set_yaxis("LDL-R", unit="dimensionless")
        plots[5].set_yaxis("LDL-R rates", unit="mmole/min")
        plots[6].set_yaxis("LDL-R-LDL-C complex", unit="dimensionless")
        plots[7].set_yaxis("LDL-R membrane bound", unit="dimensionless")

        for k in range(4):
            xaxis = plots[k].xaxis
            if xaxis is not None:  # set by `create_plots`
                xaxis.label_visible = False

        for key, value in self.tcs_dict.items():
            plots[0].add_data(
                task=f"task_{key}",
                xid="time",
                yid="[Cve_ldlc]",
                label=key,
                color=value["color"],
            )
            plots[1].add_data(
                task=f"task_{key}",
                xid="time",
                yid="[LI__cho]",
                label=key,
                color=value["color"],
            )
            plots[2].add_data(
                task=f"task_{key}",
                xid="time",
                yid="LI__SYNTHESIS_LDLR",
                label=key,
                color=value["color"],
            )
            plots[3].add_data(
                task=f"task_{key}",
                xid="time",
                yid="LI__v_uptake",
                label=key,
                color=value["color"],
            )
            plots[4].add_data(
                task=f"task_{key}",
                xid="time",
                yid="LI__ldlr",
                label=key,
                color=value["color"],
            )
            plots[5].add_data(
                task=f"task_{key}",
                xid="time",
                yid="LI__LDLRRECYCLING",
                label=f"{key} LDLR recycling",
                color=value["color"],
            )

            plots[6].add_data(
                task=f"task_{key}",
                xid="time",
                yid="LI__ldlr_ldlc",
                label=f"{key} LDLR-LDLC complex",
                color=value["color"],
            )
            plots[7].add_data(
                task=f"task_{key}",
                xid="time",
                yid="LI__ldlr_membrane",
                label=f"{key} LDLR membrane bound",
                color=value["color"],
            )

        return {"fig_fh_experiments": fig_fh}
