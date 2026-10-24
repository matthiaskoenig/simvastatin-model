"""Simulation experiment of the study Lilja2000_2004."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.experiments.simvastatin.Lilja2000 import (
    Lilja2000,
)
from pkdb_models.models.simvastatin.experiments.simvastatin.Lilja2004 import (
    Lilja2004,
)


class Lilja2000_2004(SimvastatinSimulationExperiment):
    """The grapefruit juice studies Lilja2000 and Lilja2004 together.

    Single oral dose of 40 mg simvastatin with water (control) or with
    grapefruit juice, an inhibitor of the intestinal CYP3A4: double strength
    three times daily (Lilja2000) or one glass of normal strength daily
    (Lilja2004), each with the factors of its study. A figure of the two
    regimens of the same dose, without fit mappings: the studies are fitted by
    their own experiments.
    """

    #: the studies: the simulation of their grapefruit juice and the marker
    studies: ClassVar[dict[str, tuple[str, str]]] = {
        "Lilja2000": ("gfj_double", "s"),
        "Lilja2004": ("gfj_regular", "o"),
    }

    #: the interventions of the data of both studies
    interventions: ClassVar[dict[str, str]] = {
        "control": "SIM",
        "intestinal_inhibitor": "SIM,GRA",
    }

    #: the simulations: the label and the line style
    arms: ClassVar[dict[str, tuple[str, str]]] = {
        "control": ("control", "solid"),
        "gfj_double": ("grapefruit juice, double strength", "dashdot"),
        "gfj_regular": ("grapefruit juice, normal strength", "dashed"),
    }

    #: the analytes: the substance and its selection
    analytes: ClassVar[list[tuple[str, str]]] = [
        ("simva", "[Cve_simva]"),
        ("simacid", "[Cve_simacid]"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        mr = {"simvastatin": self.Mr.simva, "simvastatin acid": self.Mr.simacid}
        dsets = {}
        for study in self.studies:
            dframes = self.load_dataframes_by_substance("Fig1", study=study)
            for substance, df in dframes.items():
                dset = DataSet.from_df(df, ureg=self.ureg)
                dset.unit_conversion("mean", 1 / mr[substance])
                for key, intervention in self.interventions.items():
                    dsets[self.to_sid(f"{study}_Fig1_{substance}_{key}")] = dset[
                        dset.intervention == intervention
                    ]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """Single oral dose of 40 mg simvastatin, control and grapefruit juice."""
        simva_po = Q(40, "mg")
        changes = {
            "control": self.default_changes(),
            "gfj_double": self.cyp3a4_changes(
                Lilja2000.f_cyp3a4_li_grapefruit,
                f_cyp3a4_gu=Lilja2000.f_cyp3a4_gu_grapefruit,
            ),
            "gfj_regular": self.cyp3a4_changes(
                1.0, f_cyp3a4_gu=Lilja2004.f_cyp3a4_gu_grapefruit
            ),
        }
        return {
            f"simva_po_{arm}": Simulation(
                start=0,
                end=24 * 60,
                preinit_changes={**changes[arm], "PODOSE_simva": simva_po},
            )
            for arm in self.arms
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {}

    @override
    def figures(self) -> dict[str, Figure]:
        """Simvastatin and its acid, control and the two grapefruit juice regimens."""
        figures = {}
        for key, arms in [
            ("control", ["control"]),
            ("intestinal_inhibitor", ["control", "gfj_double", "gfj_regular"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}",
                num_rows=2,
                num_cols=1,
                **SimvastatinSimulationExperiment.figuresize_kwargs_two_panel,
                settings={"legend_scope": "row"},
            )
            plots = fig.create_plots(
                xaxis=Axis("Time", unit=self.info.time.unit), legend=True
            )
            plots[0].set_yaxis(self.info.simva.axis, self.info.simva.unit)
            plots[1].set_yaxis(self.info.simacid.axis, self.info.simacid.unit)

            for arm in arms:
                label, linestyle = self.arms[arm]
                for k, (sid, yid) in enumerate(self.analytes):
                    plots[k].add_data(
                        task=f"task_simva_po_{arm}",
                        xid="time",
                        yid=yid,
                        label=f"sim: {label}",
                        color=self.colors_simva[sid],
                        linestyle=linestyle,
                    )

            for study, (gfj_arm, marker) in self.studies.items():
                data_arms = {"control": "control"}
                if key != "control":
                    data_arms["intestinal_inhibitor"] = gfj_arm
                for data_key, arm in data_arms.items():
                    label, linestyle = self.arms[arm]
                    for k, (sid, _) in enumerate(self.analytes):
                        substance = getattr(self.info, sid).name
                        plots[k].add_data(
                            dataset=self.to_sid(f"{study}_Fig1_{substance}_{data_key}"),
                            xid="time",
                            yid="mean",
                            # Lilja2000 has no error bars
                            yid_sd="mean_sd" if study == "Lilja2004" else None,
                            count="count",
                            color=self.colors_simva[sid],
                            linestyle=linestyle,
                            marker=marker,
                            label=f"{study}: {label}",
                        )
            figures[f"fig_{key}"] = fig

        return figures
