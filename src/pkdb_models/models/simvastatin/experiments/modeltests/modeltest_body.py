"""Test of the cholesterol metabolism in the whole-body model."""

from typing import override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)


class CholesterolBodyTestExperiment(SimvastatinSimulationExperiment):
    """Test effect of simvastatin repeated dosing on cholesterol metabolism.

    Simulation of whole-body model performance.
    """

    @override
    def simulations(self) -> dict[str, Simulation]:
        # FIXME: check default changes/presim
        simva_po_dict = {
            "simva_po_placebo": {"dose": Q(0, "mg")},
            "simva_po_40mg": {"dose": Q(40, "mg")},
        }

        tcsims = {}
        for key, value in simva_po_dict.items():
            # 30 weeks of daily doses, then 20 weeks without
            number = 30 * 7
            end = number * 24 * 60 + 20 * 7 * 60 * 24
            tcsims[key] = Simulation(
                start=0,
                end=end,
                # one simulation in a run over the draws of the fitted
                # parameters, a test of the whole-body model over 50 weeks
                preinit_changes={
                    **self.default_changes(),
                    **self.fitted_changes(),
                    "PODOSE_simva": value["dose"],
                },
                changes=[self.doses(value["dose"], number - 1, start=24 * 60)],
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_cho()}

    def figure_cho(self) -> dict[str, Figure]:
        """Simvastatin, cholesterol, the rates of cholesterol and the LDLR pathway."""
        fig1 = Figure(
            experiment=self,
            sid="fig1",
            name=self.sid,
            num_rows=5,
            num_cols=2,
            height=25,
            width=25,
        )
        plots = fig1.create_plots(xaxis=Axis("time", unit="weeks"), legend=True)

        plots[0].set_yaxis("concentration\n", unit="nM")
        plots[1].set_yaxis("concentration\n", unit="nM")
        plots[2].set_yaxis("concentration\n", unit="mM")
        plots[3].set_yaxis("concentration\n", unit="mM")
        plots[4].set_yaxis("rates\n", unit="mg/day")
        plots[5].set_yaxis("rates\n", unit="mg/day")
        plots[6].set_yaxis("concentration\n", unit="mM")
        plots[7].set_yaxis("protein concentration\n", unit="dimensionless")
        plots[8].set_yaxis("protein rates\n", unit="mmole/min")
        plots[9].set_yaxis("protein rates\n", unit="mmole/min")
        sim_info = {
            "Cve_simva": {"color": "darkgrey", "label": "plasma SV"},
            "LI__simva": {"color": "black", "label": "hepatic SV"},
            "LI__simacid": {"color": "blue", "label": "hepatic SVA"},
            "LI__simmets": {"color": "red", "label": "hepatic SVM"},
        }
        # plot simulation
        tcs_dict = {
            "40mg": {"color": "red", "dose": "simva_po_40mg"},
        }
        for dose_key, tcs_info in tcs_dict.items():
            linestyle = "solid" if dose_key == "no_dose" else "dashed"
            for key, value in sim_info.items():
                plots[0].add_data(
                    task=f"task_{tcs_info['dose']}",
                    xid="time",
                    yid=f"[{key}]",
                    linestyle=linestyle,
                    label=value["label"],
                    color=value["color"],
                )
            plots[1].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="Cve_active_inhibitors",
                color="black",
                linestyle=linestyle,
                label="plasma \nactive HMG-CoA\nreductase inhibitors",
            )
            plots[2].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="[Cve_ldlc]",
                color="black",
                linestyle=linestyle,
                label="plasma LDL-C",
            )
            plots[2].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="[Cve_vldlc]",
                color="tab:blue",
                linestyle=linestyle,
                label="plasma VLDL-C",
            )
            plots[3].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="[LI__cho]",
                color="black",
                linestyle=linestyle,
                label="hepatic cholesterol",
            )

            plots[4].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__v_synthesis",
                linestyle=linestyle,
                label="cholesterol synthesis",
            )

            # cholesterol plasma rates
            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="v_ldlc_net_consumption",
                label="ldlc net consumption (loss+utilization-diet)",
            )
            #  Cve_ldlc -> {}
            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="v_ldlc_utilization",
                label="ldlc utilization",
                linestyle=linestyle,
            )
            # diet: {} -> Cve_ldlc
            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="v_ldlc_diet",
                label="ldlc diet",
                linestyle=linestyle,
            )
            # loss: Cve_ldlc -> {}
            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="v_ldlc_loss",
                label="ldlc loss",
                linestyle=linestyle,
            )
            # conversion: Cve_vldlc -> Cve_ldlc
            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="v_vldlc_conversion",
                label="vldlc to ldlc conversion",
                linestyle=linestyle,
            )

            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__v_recycling",
                label="LDLR liver recycling\n& cho release",
                linestyle=linestyle,
            )

            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__v_export",
                label="ldlc liver export into vldlc",
                linestyle=linestyle,
            )
            plots[5].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__v_uptake",
                label="ldlc liver uptake",
                linestyle=linestyle,
            )

            # cholesterol precursors
            plots[6].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="[LI__acoa]",
                label="Acetyl-CoA",
                linestyle=linestyle,
            )
            plots[6].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="[LI__hmgcoa]",
                label="HMG-CoA",
                linestyle=linestyle,
            )

            plots[7].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__ldlr_ldlc",
                label="LDLR-LDLC complex",
                linestyle=linestyle,
            )
            plots[7].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__ldlr_membrane",
                label="membrane bound LDLR",
                linestyle=linestyle,
            )

            plots[7].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__ldlr",
                label="free LDLR",
                color="black",
                linestyle=linestyle,
            )

            # LDLR pathway rates
            plots[8].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__SYNTHESIS_LDLR",
                label="protein synthesis",
                color="blue",
                linestyle=linestyle,
            )
            plots[8].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__DEGRADATION_LDLR",
                label="protein degradation",
                color="red",
                linestyle=linestyle,
            )
            plots[8].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__TURNOVER_LDLR",
                label="LDLR turnover (SYNTHESIS - DEGRADATION)",
                color="green",
                linestyle=linestyle,
            )
            plots[9].add_data(
                task=f"task_{tcs_info['dose']}",
                xid="time",
                yid="LI__LDLRLDLCIMP",
                label="LDLR internalization",
                linestyle=linestyle,
            )

        # the axes are set by `create_plots` and `set_yaxis`
        for k in range(8):
            xaxis = plots[k].xaxis
            if xaxis is not None:
                xaxis.label_visible = False
        for k in [0, 1, 2, 3, 5, 6]:
            yaxis = plots[k].yaxis
            if yaxis is not None:
                yaxis.min = 0

        xaxis, yaxis = plots[2].xaxis, plots[2].yaxis
        if xaxis is not None and yaxis is not None:
            xaxis.grid = True
            yaxis.grid = True

        return self.figures_by_sid(fig1)
