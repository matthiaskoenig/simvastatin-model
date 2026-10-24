"""Simulation experiment of the study Sivkov2021."""

from typing import ClassVar, NamedTuple, override

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Genotype,
    Health,
    PKPDData,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.simulation import Change, Scan, Simulation

from pkdb_models.models.simvastatin.experiments.base_experiment import (
    DAY,
    WEEK,
    FontKwargs,
    SimvastatinSimulationExperiment,
)


class Group(NamedTuple):
    """A simvastatin group of Sivkov2021."""

    #: name of the group in the keys of the datasets, simulations and mappings
    name: str
    #: table of the data
    fig_id: str
    #: SLCO1B1 c.521T>C genotype which the simulation sets, None: reference
    slco1b1: str | None
    genotype: Genotype
    #: baseline LDL cholesterol [mM] (Table 3 or 4)
    ldlc_init: float
    label: str
    marker: str


class Sivkov2021(SimvastatinSimulationExperiment):
    """Simulation experiment of Sivkov2021.

    180 Russian patients with hyperlipidemia (type IIa 60 %, IIb 40 %), group A
    genotyped for SLCO1B1 c.521T>C, group B for ABCB1 (MDR1) C3435T, each split
    into a rosuvastatin, an atorvastatin and a simvastatin subgroup of 30.
    Simvastatin 10 mg once daily for 4 months (subgroups A III and B III); Tables
    3 and 4 give the total and LDL cholesterol at baseline and after 4 months
    (simulated as 17 weeks, as the data). The errors of the tables are standard
    errors ("M +- m", an SD of 0.16 - 0.23 mM of the LDL cholesterol in
    hyperlipidemic patients is not possible), the data copies hold them as
    `se` and the SD as `se * sqrt(n)`.

    The SLCO1B1 genotypes set the activity of OATP1B1 (`slco1b1_changes`): a
    lower hepatic uptake of simvastatin acid lowers the inhibition of the
    HMG-CoA reductase in the liver. ABCB1 is not part of the model, its
    genotypes differ only by their baseline. The groups of 30 are simulated
    with the reference activities (genotype not reported, as the other
    studies).
    """

    #: the FH type of the fit mappings, the reduced LDL clearance of a non
    #: familial hypercholesterolemia (see `Tuomilehto1995.fit_fh_type`)
    fit_fh_type: ClassVar[str] = "FH_type4"

    #: the weeks of the doses (4 months)
    weeks_dosing: ClassVar[int] = 17

    groups: ClassVar[list[Group]] = [
        Group("521", "Tab3", None, Genotype.NR, 5.12, "SLCO1B1 c.521 all", "s"),
        Group("521TT", "Tab3", "TT", Genotype.SLCO1B1_521TT, 5.14, "c.521TT", "o"),
        Group("521TC", "Tab3", "TC", Genotype.SLCO1B1_521TC, 5.09, "c.521TC", "^"),
        Group("521CC", "Tab3", "CC", Genotype.SLCO1B1_521CC, 5.13, "c.521CC", "v"),
        Group("3435", "Tab4", None, Genotype.NR, 5.11, "ABCB1 C3435 all", "s"),
        Group("3435CC", "Tab4", None, Genotype.ABCB1_3435CC, 5.14, "C3435CC", "o"),
        Group("3435TC", "Tab4", None, Genotype.ABCB1_3435CT, 5.13, "C3435TC", "^"),
        Group("3435TT", "Tab4", None, Genotype.ABCB1_3435TT, 5.07, "C3435TT", "v"),
    ]

    #: line styles of the simulations of the genotypes of SLCO1B1
    linestyles: ClassVar[dict[str | None, str]] = {
        None: "solid",
        "TT": "dashed",
        "TC": "dashdot",
        "CC": "dotted",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Tab3", "Tab4"]:
            dframes = self.load_dataframes_by_substance(fig_id)
            for substance, df in dframes.items():
                for measurement_type, suffix in [
                    ("concentration", ""),
                    ("concentration change", "_relative_change"),
                ]:
                    dset_mtype = self.measurement_dataset(df, measurement_type)
                    for group in self.groups:
                        if group.fig_id != fig_id:
                            continue
                        dsets[
                            self.to_sid(f"{fig_id}_{substance}_{group.name}{suffix}")
                        ] = dset_mtype[dset_mtype.group == f"subgroup_sim_{group.name}"]
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation | Scan]:
        """The doses of the groups.

        The activity of OATP1B1 of a SLCO1B1 genotype is set at the end of the
        presimulation, a week before the first dose: it changes only the
        transport of simvastatin acid, the presimulation of the cholesterol
        without simvastatin does not depend on it.
        """
        tcsims: dict[str, Simulation | Scan] = {}
        number = self.weeks_dosing * 7 + 1
        for group in self.groups:
            changes = [self.doses(Q(10, "mg"), number)]
            if group.slco1b1 is not None:
                changes.append(Change([0], self.slco1b1_changes(group.slco1b1)))
            for fh_type_key in self.fh_types:
                tcsims[self.to_sid(f"simva_po_10mg_{group.name}_{fh_type_key}")] = (
                    self.presim(
                        end=WEEK + number * DAY,
                        dt=DAY / 25,
                        changes=changes,
                        ldlc=group.ldlc_init,
                        FH_type=fh_type_key,
                        time_shift=-WEEK,
                    )
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        """The LDL cholesterol of the groups (weeks 0 and 17)."""
        mappings = {}
        for group in self.groups:
            mappings[f"fm_ldlc_{group.name}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"{group.fig_id}_ldl-c_{group.name}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(
                        f"task_simva_po_10mg_{group.name}_{self.fit_fh_type}"
                    ),
                    xid="time",
                    yid="[Cve_ldlc]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.MULTIPLE,
                    health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
                    genotype=group.genotype,
                    data=PKPDData.PD,
                    data_type=DataType.MEAN,
                ),
            )
        return mappings

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        figures = {}
        for gene in ["521", "3435"]:
            figures[f"fig_cho_{gene}"] = self._figure_cho(gene)
            if self.show_all_cho_data:
                figures[f"fig_all_{gene}"] = self._figure_all(gene)
        return figures

    def _groups(self, gene: str) -> list[Group]:
        """The groups of a gene, `521` (SLCO1B1) or `3435` (ABCB1)."""
        return [group for group in self.groups if group.name.startswith(gene)]

    def _plot_simulations(self, ax: Axes, gene: str) -> None:
        """Plot the LDL cholesterol of the simulations, the range of the FH types.

        The genotypes of ABCB1 are not part of the model, only the group of 30
        is plotted.
        """
        for group in self._groups(gene):
            if gene == "3435" and group.name != gene:
                continue
            self.plot_FH_results(
                ax=ax,
                label=f"sim: SV 10mg {group.label}",
                color=10,
                linestyle=self.linestyles[group.slco1b1],
                df=self.create_FH_results(task_key=f"10mg_{group.name}"),
            )

    def _plot_data(self, ax: Axes, substance: str, gene: str) -> None:
        """Plot the data of a substance of the groups of a gene.

        The groups are shifted by a few days to show the error bars.
        """
        for k, group in enumerate(self._groups(gene)):
            dataset = self._datasets[
                self.to_sid(f"{group.fig_id}_{substance}_{group.name}")
            ]
            count = int(dataset["count"].iloc[0])
            color = self.colormap_SV_dose(10)
            ax.errorbar(
                dataset["time"] + 0.25 * (k - 1.5),
                dataset["mean"],
                dataset["mean_sd"],
                color=color,
                label=f"{self.sid}: {group.label} (n={count})",
                markerfacecolor=color,
                markeredgecolor="black",
                markersize=8,
                marker=group.marker,
                linestyle="None",
            )

    def _figure_cho(self, gene: str) -> FigureMPL:
        """LDL cholesterol of the simulations and the data of a gene."""
        fig, ax = self.create_cholesterol_plot()
        self._plot_simulations(ax, gene)
        self._plot_data(ax, "ldl-c", gene)
        ax.set_xlim((-1, 19))
        ax.set_ylim((0.0, 7))
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), prop={"size": 10})
        ax.tick_params(axis="both", labelsize=18)
        return fig

    def _figure_all(self, gene: str) -> FigureMPL:
        """The total and LDL cholesterol of the data and the simulations."""
        kwargs: FontKwargs = {"weight": "bold", "size": 16}
        fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1, sharex="col", figsize=(15, 8))
        fig.subplots_adjust(bottom=0.12, top=0.925, left=0.07, right=0.95, hspace=0.05)
        ax2.set_xlabel("Time [weeks]", **kwargs)
        ax1.set_ylabel("LDL-C [mM]", **kwargs)
        ax2.set_ylabel("Total Cholesterol [mM]", **kwargs)

        self._plot_simulations(ax1, gene)
        self._plot_data(ax1, "ldl-c", gene)
        self._plot_data(ax2, "cholesterol", gene)

        for ax in [ax1, ax2]:
            ax.legend(ncol=1, loc="best", prop={"size": 12})
            ax.tick_params(axis="both", labelsize=18)
        ax1.set_ylim((0.0, 7))
        ax2.set_ylim((0.0, 9))
        return fig
