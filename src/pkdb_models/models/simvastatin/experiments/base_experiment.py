"""Base class of the simvastatin simulation experiments."""

import math
from collections.abc import Sequence
from typing import ClassVar, NamedTuple, TypedDict, override

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS, RENAL_FUNCTION_GFR
from pkpdsim.scan import state_after_changes
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.simulation import Change, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.simvastatin import FH_CALIBRATION_PATH, MODEL
from pkdb_models.models.simvastatin.experiments.simva_helpers import colormap_SV_dose
from pkdb_models.models.simvastatin.models.fits import FITS

#: one day and one week [min]
DAY = 24 * 60
WEEK = 7 * DAY
#: presimulation of the cholesterol into its steady state [min]
PRESIM_TIME = 52 * WEEK

#: the parameter of the liver which a familial hypercholesterolemia (FH) type changes
FH_PARAMETERS: dict[str, str] = {
    "FH_type1": "LI__SYNTHESIS_LDLR_Vmax_f",
    "FH_type2_6": "LI__LDLRMEMBRANE_Kcat_f",
    "FH_type3": "LI__LDLRLDLCIMP_Km_f",
    "FH_type4": "LI__LDLRLDLCIMP_Kcat_f",
    "FH_type5": "LI__LDLRRECYCLING_Kcat_f",
    "PCSK9": "LI__DEGRADATION_LDLR_Vmax_f",
}


class FontKwargs(TypedDict):
    """Font of the labels of the matplotlib figures."""

    weight: str
    size: int


class FigureSize(TypedDict):
    """Size of a figure of sbmlsim, spread into `Figure(...)`."""

    width: float
    height: float


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data."""

    simva: Quantity
    simacid: Quantity
    ActiveInh: Quantity
    TotalInh: Quantity
    hmgcoa: Quantity
    cho: Quantity
    acoa: Quantity
    vldlc: Quantity
    hdlc: Quantity
    ldlc: Quantity
    choprecursors: Quantity


class SidData(NamedTuple):
    """Name, unit and axis label of a quantity of the figures."""

    name: str
    unit: str
    axis: str


class SidInfo(NamedTuple):
    """The quantities of the figures."""

    time: SidData
    time_days: SidData
    time_weeks: SidData
    simva: SidData
    simacid: SidData
    simva_and_simacid: SidData
    totalsimvainhibitors: SidData
    activesimvainhibitors: SidData
    totalsimva: SidData
    simmets_urine: SidData
    simva_feces: SidData
    simmets_feces: SidData
    cho: SidData
    hdlc: SidData
    ldlc: SidData
    vldlc: SidData
    triglycerides: SidData
    bloodlipids: SidData
    choprecursors: SidData
    ldlcreceptor: SidData
    hmgcoareductase: SidData
    hmgcoasynthase: SidData
    ldlc_change: SidData


class SimvastatinSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the simvastatin simulation experiments."""

    pkpd_model = MODEL
    selections = (
        "time",
        # simvastatin
        "PODOSE_simva",
        "[Cve_simva]",
        "[Cve_simacid]",
        "[Cve_simmets]",
        "[Cgu_plasma_simva]",
        "[Cgu_plasma_simacid]",
        "[Cli_plasma_simva]",
        "[Cli_plasma_simacid]",
        "Cve_simva_and_simacid",
        "Cve_active_inhibitors",
        "Cve_total_inhibitors",
        # urine and feces
        "Aurine_simmets",
        "Afeces_simva",
        "Afeces_simmets",
        # activities of the cases (interactions, genotypes, renal function)
        "BW",
        "KI__f_renal_function",
        "GU__f_cyp3a4",
        "LI__f_cyp3a4",
        "f_cyp3a5",
        "LI__f_oatp1b1",
        # cholesterol
        "[Cve_ldlc]",
        "[Cve_vldlc]",
        "[LI__cho]",
        "[LI__hmgcoa]",
        "[LI__acoa]",
        "[LI__simva]",
        "[LI__simacid]",
        "[LI__simmets]",
        "ldlc_change",
        "ldlc_init",
        # cholesterol protein expression
        "LI__ldlr",
        "LI__ldlr_membrane",
        "LI__ldlr_ldlc",
        "LI__ldlr_total",
        "LI__ldlr_fraction",
        "LI__ldlr_membrane_fraction",
        "LI__ldlr_ldlc_fraction",
        "[LI__hmgcoareductase]",
        "[LI__hmgcoasynthase]",
        "LI__SYNTHESIS_LDLR",
        "LI__DEGRADATION_LDLR",
        # cholesterol rates
        "LI__TURNOVER_LDLR",
        "LI__LDLR_TO_MEMBRANE",
        "LI__LDLRRECYCLING",
        "LI__LDLRLDLCIMP",
        "LI__VLDLCEXP",
        "LI__HMGCOAREDUCTASE",
        "LI__v_synthesis",
        "LI__v_recycling",
        "LI__v_export",
        "LI__v_uptake",
        "LI__v_liver_balance",
        "LI__v_reference",
        "ldlc_utilization",
        "ldlc_loss",
        "ldlc_diet",
        "ldlc_net_consumption",
        "vldlc_conversion",
        "LI__v_net_export",  # [mg/day]
        "v_ldlc_net_consumption",  # [mg/day]
        "v_ldlc_utilization",  # [mg/day]
        "v_ldlc_loss",  # [mg/day]
        "v_ldlc_diet",  # [mg/day]
        "v_vldlc_conversion",  # [mg/day]
    )

    info: ClassVar[SidInfo] = SidInfo(
        time=SidData(name="time", unit="hr", axis="time"),
        time_days=SidData(name="time", unit="days", axis="time"),
        time_weeks=SidData(name="time", unit="weeks", axis="time"),
        simva=SidData(name="simvastatin", unit="nM", axis="Simvastatin"),
        simacid=SidData(name="simvastatin acid", unit="nM", axis="Simvastatin acid"),
        simva_and_simacid=SidData(
            name="simva + simacid",
            unit="nM",
            axis="Simvastatin+\nSimvastatin acid",
        ),
        # the enzymatic assays measure the inhibition of the HMG-CoA reductase:
        # the active inhibitors are simvastatin acid and its active metabolites,
        # the total inhibitors in addition the lactones after their hydrolysis
        totalsimvainhibitors=SidData(
            name="total simva inhibitors",
            unit="nM",
            axis="Total simvastatin\ninhibitors",
        ),
        activesimvainhibitors=SidData(
            name="active simva inhibitors",
            unit="nM",
            axis="Active simvastatin\ninhibitors",
        ),
        totalsimva=SidData(name="total simva", unit="nM", axis="Total simvastatin"),
        simmets_urine=SidData(
            name="simva metabolites urine",
            unit="µmole",
            axis="Simvastatin metabolites\n(urine)",
        ),
        simva_feces=SidData(
            name="simva feces", unit="µmole", axis="Simvastatin\n(feces)"
        ),
        simmets_feces=SidData(
            name="simva metabolites feces",
            unit="µmole",
            axis="Simvastatin metabolites\n(feces)",
        ),
        cho=SidData(name="cholesterol", unit="mM", axis="Cholesterol"),
        choprecursors=SidData(
            name="cholesterol precursors", unit="mM", axis="Cholesterol precursors"
        ),
        ldlc=SidData(name="ldl-c", unit="mM", axis="Plasma LDL-C"),
        vldlc=SidData(name="vldl-c", unit="mM", axis="Plasma VLDL-C"),
        hdlc=SidData(name="hdl-c", unit="mM", axis="Plasma HDL-C"),
        triglycerides=SidData(name="triglyceride", unit="mM", axis="Trigylcerides"),
        bloodlipids=SidData(name="blood lipids", unit="mM", axis="Blood lipids"),
        ldlcreceptor=SidData(name="ldlc receptor", unit="mM", axis="LDL-C receptor"),
        hmgcoareductase=SidData(
            name="hmgcoa reductase", unit="mM", axis="HMGCOA reductase"
        ),
        hmgcoasynthase=SidData(
            name="hmgcoa synthase", unit="mM", axis="HMGCOA synthase"
        ),
        ldlc_change=SidData(name="ldl-c change", unit="percent", axis="LDL-C change"),
    )

    # molecular weights for the conversion of the data
    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        cho=Q(386.7, "g/mole"),
        choprecursors=Q(386, "g/mole"),  # FIXME ???
        hmgcoa=Q(911, "g/mole"),
        simva=Q(418.6, "g/mole"),
        simacid=Q(436.6, "g/mole"),
        ActiveInh=Q(436.6, "g/mole"),  # enzymatic assay: simacid Mr used
        TotalInh=Q(436.6, "g/mole"),  # enzymatic assay: simacid Mr used
        acoa=Q(809.57, "g/mole"),
        ldlc=Q(386.7, "g/mole"),  # lipid conversion factor
        hdlc=Q(386.7, "g/mole"),  # lipid conversion factor
        vldlc=Q(386.7, "g/mole"),  # lipid conversion factor
    )

    simtype_linestyle: ClassVar[dict[str, str]] = {
        "control": "solid",
        "inducer": "dotted",
        "inhibitor": "dashed",
        "no_interaction": "dashdotdotted",
        "intestinal_inhibitor": "dashdot",
        "non_CYP3A4_related_inducers": "solid",
    }

    colors_simva: ClassVar[dict[str, str]] = {
        "simva": "#070D0D",  # almost black
        "simacid": "tab:blue",
        "totalsimvainhibitors": "tab:orange",
        "activesimvainhibitors": "tab:red",
        "simva_and_simacid": "tab:green",
        "totalsimva": "purple",
        "ldlc": "black",
    }

    # the sizes of figures with rows x columns panels
    figuresize_kwargs_one_panel: ClassVar[FigureSize] = {
        # 1 x 1
        "width": 9,
        "height": 4.5,
    }
    figuresize_kwargs_two_panel: ClassVar[FigureSize] = {
        # 2 x 1
        "width": 9,
        "height": 9,
    }
    figuresize_kwargs_three_panel: ClassVar[FigureSize] = {
        # 3 x 1
        "width": 9,
        "height": 13.5,
    }
    figuresize_kwargs_four_panel: ClassVar[FigureSize] = {
        # 2 x 2
        "width": 18,
        "height": 9,
    }

    # the familial hypercholesterolemia (FH) types and their line styles
    fh_types: ClassVar[dict[str, str]] = {
        "FH_type1": "solid",
        "FH_type2_6": "dotted",
        "FH_type3": "dashed",
        "FH_type4": "dashdot",
        "FH_type5": "dashed",  # FIXME no duplicates in linestyles
        "PCSK9": "dashdotdotted",
    }

    # flag to get combined cholesterol figures with all data
    show_all_cho_data: ClassVar[bool] = False

    def measurement_dataset(self, df: pd.DataFrame, measurement_type: str) -> DataSet:
        """Get the data set of the rows of a table of one measurement type.

        The table of a substance can have the rows of several measurement types,
        e.g. the concentration in mg/dl and its change in percent; a data set
        holds the rows of one, whose units are of one kind (sbmlsim reads a
        column in one unit). Without a row of the measurement type the data set
        is the empty selection of the data set of the table.

        Args:
            df: the table of a substance, with the column `measurement_type`.
            measurement_type: the measurement type of the rows.

        Returns:
            The data set of the rows.
        """
        rows = df[df["measurement_type"] == measurement_type]
        if rows.empty:
            dset = DataSet.from_df(df, self.ureg)
            return dset[dset["measurement_type"] == measurement_type]
        return DataSet.from_df(rows, self.ureg)

    def colormap_SV_dose(self, dose: float) -> str | tuple[float, float, float, float]:
        """Color of a simvastatin dose [mg], see `simva_helpers.colormap_SV_dose`."""
        return colormap_SV_dose(dose)

    # ----------- Renal function --------------
    #: the renal function (`KI__f_renal_function`) of the classes of the
    #: renal impairment, relative to the healthy GFR of 101 ml/min: a
    #: measured creatinine clearance of X ml/min is X/101
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS

    # ----------- Genotypes --------------
    #: the activity of OATP1B1 per SLCO1B1 c.521T>C allele (`LI__f_oatp1b1`,
    #: c.521TT = 1): the C allele (*5, *15) reduces the hepatic uptake
    #: transport of OATP1B1 to about a third (Kameyama2005: transport of the
    #: *5 and *15 variants 30 - 40 % of *1a in vitro); not fitted, Pasanen2006
    #: (acid AUC c.521TC 1.2-fold, CC 3.2-fold of TT) validates it
    slco1b1_allele_activity: ClassVar[dict[str, float]] = {
        "T": 1.0,
        "C": 0.35,
    }
    slco1b1_activity: ClassVar[dict[str, float]] = {
        "TT": (slco1b1_allele_activity["T"] + slco1b1_allele_activity["T"]) / 2,
        "TC": (slco1b1_allele_activity["T"] + slco1b1_allele_activity["C"]) / 2,
        "CC": slco1b1_allele_activity["C"],
    }
    #: the functional CYP3A5 per allele (`f_cyp3a5`): *3 is a null allele (a
    #: splicing defect, no functional protein), *3/*3 is the reference of the
    #: model (0); the capacity of CYP3A5 *1/*1 relative to CYP3A4 is the model
    #: parameter `r_cyp3a5`
    cyp3a5_allele_activity: ClassVar[dict[str, float]] = {
        "*1": 1.0,
        "*3": 0.0,
    }
    cyp3a5_activity: ClassVar[dict[str, float]] = {
        "*1/*1": (cyp3a5_allele_activity["*1"] + cyp3a5_allele_activity["*1"]) / 2,
        "*1/*3": (cyp3a5_allele_activity["*1"] + cyp3a5_allele_activity["*3"]) / 2,
        "*3/*3": (cyp3a5_allele_activity["*3"] + cyp3a5_allele_activity["*3"]) / 2,
    }

    # ----------- Draws of the fitted parameters --------------
    def across(self) -> str | None:
        """Get the dimension of the draws of the fitted parameters.

        `None` without a run over the draws (`uncertainty`).
        """
        return None if self.uncertainty is None else self.uncertainty.id

    def over_draws(
        self, values: xr.DataArray
    ) -> tuple[xr.DataArray, xr.DataArray, xr.DataArray]:
        """Get the median and the band of the draws of a variable of a result.

        Args:
            values: the variable of a result, e.g. `xres["[Cve_ldlc]"]`.

        Returns:
            The median, the lower and the upper quantile over the draws of the
            fitted parameters (`uncertainty`), without their dimension; the
            values three times without draws.
        """
        run = self.uncertainty
        if run is None or run.id not in values.dims:
            return values, values, values
        q_low, q_high = run.quantiles
        return (
            values.median(dim=run.id),
            values.quantile(q_low, dim=run.id).drop_vars("quantile"),
            values.quantile(q_high, dim=run.id).drop_vars("quantile"),
        )

    @staticmethod
    def fitted_changes() -> dict[str, Quantity]:
        """Changes of the fitted parameters to their fitted values.

        The values of the model, so the changes change nothing; a simulation
        which sets the fitted parameters runs once in a run over their draws
        (`run_simulation --uncertainty`, `pkpdsim.uncertainty`). For the scans
        of the FH types and the experiments of the cholesterol model without
        simvastatin, where the draws would multiply the simulations of weeks
        by the number of draws for no band (without simvastatin the fitted
        parameters have no effect).
        """
        return {p.pid: Q(p.value, p.unit) for p in FITS.parameters.values()}

    @override
    def default_changes(self) -> dict[str, Quantity]:
        """Changes of every simulation of the experiments, none at the moment.

        The parameters are part of the model and are not changed in the
        simulations: a parameter which is fitted must not be set by a simulation,
        it would override the value of the fit. The default changes of the
        experiments, the initial LDL cholesterol for the change of the LDL
        cholesterol (`ldlc_init`, 3 mM) and the factors of the familial
        hypercholesterolemia types (1), were the values of the model. The
        changes are `_default_changes`, a dictionary of quantities, which the
        changes of the interactions, the genotypes and of the FH types extend.
        """
        return SimvastatinSimulationExperiment._default_changes()

    @staticmethod
    def _default_changes() -> dict[str, Quantity]:
        """Changes of every simulation of the experiments, see `default_changes`."""
        return {}

    # ----------- Interactions --------------
    @staticmethod
    def cyp3a4_changes(
        f_cyp3a4: float, f_cyp3a4_gu: float | None = None
    ) -> dict[str, Quantity]:
        """Changes of the activity of CYP3A4 by an inhibitor or an inducer.

        The factors are documented in the experiment with the mechanism of the
        interaction and the observed ratio of the study, they are never
        fitted (the arms of the interactions are validation data).

        Args:
            f_cyp3a4: activity of the hepatic CYP3A4 relative to the
                reference (`LI__f_cyp3a4`), < 1 inhibition, > 1 induction.
            f_cyp3a4_gu: activity of the intestinal CYP3A4 (`GU__f_cyp3a4`),
                the hepatic one by default; an inhibitor of the intestinal
                CYP3A4 only (grapefruit juice) has `f_cyp3a4=1`.

        Returns:
            The changes of the activities.
        """
        if f_cyp3a4_gu is None:
            f_cyp3a4_gu = f_cyp3a4
        return {
            "LI__f_cyp3a4": Q(f_cyp3a4, "dimensionless"),
            "GU__f_cyp3a4": Q(f_cyp3a4_gu, "dimensionless"),
        }

    @staticmethod
    def oatp1b1_changes(f_oatp1b1: float) -> dict[str, Quantity]:
        """Changes of the activity of OATP1B1 (`LI__f_oatp1b1`).

        An inhibitor of OATP1B1 or a variant of SLCO1B1 (`slco1b1_activity`).
        """
        return {"LI__f_oatp1b1": Q(f_oatp1b1, "dimensionless")}

    def cyp3a5_changes(self, genotype: str) -> dict[str, Quantity]:
        """Changes of the CYP3A5 genotype (`f_cyp3a5`), a key of `cyp3a5_activity`."""
        return {"f_cyp3a5": Q(self.cyp3a5_activity[genotype], "dimensionless")}

    def slco1b1_changes(self, genotype: str) -> dict[str, Quantity]:
        """Changes of the SLCO1B1 c.521T>C genotype, a key of `slco1b1_activity`."""
        return self.oatp1b1_changes(self.slco1b1_activity[genotype])

    @staticmethod
    def bodyweight_changes(bodyweight: float) -> dict[str, Quantity]:
        """Changes of the body weight [kg] of the subjects (`BW`)."""
        return {"BW": Q(bodyweight, "kg")}

    # -----------------
    # Pre-simulation
    # -----------------
    def fh_changes(
        self,
        ldlc: float = 3.0,  # [mM]
        FH_type: str | None = None,
    ) -> dict[str, Quantity]:
        """Changes of the familial hypercholesterolemia (FH) type.

        The severity of the FH type is the one which gives the LDL cholesterol
        `ldlc` in steady state, interpolated from the tracked calibration of the
        model (`FH_CALIBRATION_PATH`, which `update_fh_calibration` of
        `model_calibration/fh_calibration.py` updates; a run does not change
        it). Without a FH type there are no changes.
        """
        return SimvastatinSimulationExperiment._fh_changes(ldlc=ldlc, FH_type=FH_type)

    @staticmethod
    def _fh_changes(
        ldlc: float = 3.0,  # [mM]
        FH_type: str | None = None,
    ) -> dict[str, Quantity]:
        """Changes of the FH type, see `fh_changes`."""
        changes = SimvastatinSimulationExperiment._default_changes()
        if FH_type is None:
            return changes

        results_csv = pd.read_csv(FH_CALIBRATION_PATH)
        fh_parameter = FH_PARAMETERS[FH_type]

        # FIXME: update
        ldlc_rounded = np.round(ldlc, 1)
        difference = ldlc - ldlc_rounded
        if difference == 0:
            # the severity of the calibrated LDL cholesterol
            index = results_csv.loc[results_csv["concentration"] == ldlc]
            severity = index[FH_type].values
        else:
            # interpolation between the two calibrated LDL cholesterol values
            index_ceil = results_csv.loc[
                results_csv["concentration"] == (math.ceil(ldlc * 10) / 10)
            ]
            value_ceil = index_ceil[FH_type].values
            index_floor = results_csv.loc[
                results_csv["concentration"] == (math.floor(ldlc * 10) / 10)
            ]
            value_floor = index_floor[FH_type].values
            difference = difference * 10
            if difference > 0:
                severity = value_floor * (1 - difference) + value_ceil * difference
            else:
                severity = value_ceil * (1 + difference) + value_floor * (-difference)

        return {
            **changes,
            fh_parameter: Q(severity.item(), "dimensionless"),
        }

    def presim(
        self,
        end: float,
        dt: float,
        changes: Sequence[Change] = (),
        ldlc: float = 3.0,  # [mM]
        FH_type: str | None = None,
        time_shift: float = 0.0,
        presim_time: float = PRESIM_TIME,
        last_day_steps: int | None = None,
        preinit_changes: dict[str, Quantity] | None = None,
    ) -> Simulation:
        """Simulation after the presimulation of the cholesterol experiments.

        The presimulation, from `-presim_time` (52 weeks) to 0, brings the
        cholesterol into the steady state of the FH type and is not part of the
        output. The FH type has the severity which gives the baseline LDL
        cholesterol `ldlc` of the study, see `fh_changes`. The output are the
        times from 0 to `end` [min] every `dt` [min] and `end`, shifted by
        `time_shift`; the last day has `last_day_steps` equidistant steps if
        given. The `preinit_changes` are applied before the initialization,
        after the changes of the FH type.
        """
        n = int(np.floor(end / dt + 1e-9))
        times = dt * np.arange(n + 1)
        if times[-1] < end - 1e-9:
            times = np.append(times, end)
        if last_day_steps is not None:
            times = np.concatenate(
                [
                    times[times < end - DAY - 1e-9],
                    np.linspace(end - DAY, end, last_day_steps + 1),
                ]
            )
        return Simulation(
            start=-presim_time,
            end=end,
            times=times.tolist(),
            preinit_changes={
                **self.fh_changes(ldlc=ldlc, FH_type=FH_type),
                **(preinit_changes or {}),
            },
            changes=list(changes),
            time_shift=time_shift,
        )

    def multiple_doses(
        self,
        dose: Quantity,
        number: int,
        interval: float,
        time_shift: float,
        dt: float = 1.0,
        changes: dict[str, Quantity] | None = None,
        end: float | None = None,
    ) -> Simulation:
        """Simulation of `number` oral doses of simvastatin, one every `interval` [min].

        The simulation ends 1 min after the dosing interval of the last dose,
        unless `end` is given, and has an output every `dt` [min]. The `changes`
        are applied before the initialization. The first dose is a change
        before the initialization, the later doses add to the undissolved rest
        of the earlier ones (`doses`).
        """
        if end is None:
            end = number * interval + 1
        return Simulation(
            start=0,
            end=end,
            preinit_changes={**(changes or {}), "PODOSE_simva": dose},
            changes=[self.doses(dose, number - 1, start=interval, interval=interval)],
            time_shift=time_shift,
        )

    @staticmethod
    def doses(
        dose: Quantity,
        number: int,
        start: float = WEEK,
        interval: float = DAY,
    ) -> Change:
        """Oral doses of simvastatin [min], one every `interval` from `start`.

        A dose adds to the undissolved rest of the earlier doses
        (`PODOSE_simva + <dose>` in mg, the unit of the model), which a dose
        given as the value of `PODOSE_simva` would overwrite.
        """
        mg = dose.to("mg").magnitude
        return Change(
            [start + k * interval for k in range(number)],
            {"PODOSE_simva": f"PODOSE_simva + {mg}"},
        )

    def create_cholesterol_plot(self) -> tuple[FigureMPL, Axes]:
        """Create the matplotlib figure of the LDL cholesterol over time."""
        kwargs: FontKwargs = {"weight": "bold", "size": 20}

        fig_cho, axs_cho = plt.subplots(
            nrows=1,
            ncols=1,
            figsize=(
                SimvastatinSimulationExperiment.figuresize_kwargs_one_panel["width"],
                SimvastatinSimulationExperiment.figuresize_kwargs_one_panel["height"],
            ),
        )
        axs_cho.set_xlabel("Time [weeks]", **kwargs)
        axs_cho.set_ylabel("LDL-C [mM]", **kwargs)

        return fig_cho, axs_cho

    def create_FH_results(
        self, task_key: str, substance: str | None = None
    ) -> pd.DataFrame:
        """Get a quantity of the simulations of the FH types of a dose.

        In a run over the draws of the fitted parameters (`uncertainty`) the
        value of a FH type is the median of its draws, and the range includes
        the quantiles of the draws of every FH type.

        Args:
            task_key: the dose part of the task ids `task_simva_po_<task_key>_<FH type>`.
            substance: the selection, by default the plasma LDL cholesterol.

        Returns:
            The quantity per FH type [mM], the time [weeks] and the mean,
            minimum and maximum over all FH types.
        """
        substance_key = "[Cve_ldlc]" if substance is None else substance
        columns: dict[str, np.ndarray] = {}
        lower: list[np.ndarray] = []
        upper: list[np.ndarray] = []
        for fh_type_key in self.fh_types:
            task = f"task_simva_po_{task_key}_{fh_type_key}"
            xres = state_after_changes(self.results[self.to_sid(task)])
            if "time" not in columns:
                columns["time"] = (
                    Q(xres["time"].values, xres.units["time"]).to("weeks").magnitude
                )
            unit = xres.units[substance_key]
            y, low, high = (
                Q(np.asarray(da.values).flatten(), unit).to("mM").magnitude
                for da in self.over_draws(xres[substance_key])
            )
            columns[fh_type_key] = y
            lower.append(low)
            upper.append(high)

        df = pd.DataFrame(columns)
        fh_columns = list(self.fh_types)
        df["mean"] = df[fh_columns].mean(axis=1)
        df["min"] = np.min(lower, axis=0)
        df["max"] = np.max(upper, axis=0)
        return df

    def plot_FH_results(
        self, ax: Axes, label: str, color: float, df: pd.DataFrame, linestyle: str
    ) -> Axes:
        """Plot the mean and the range of the FH types of `create_FH_results`.

        Args:
            ax: the axes to plot into.
            label: label of the mean.
            color: dose of simvastatin [mg], which gives the color.
            df: the results of `create_FH_results`.
            linestyle: line style of the mean.

        Returns:
            The axes.
        """
        face_color = colormap_SV_dose(color)

        ax.fill_between(
            df["time"], df["min"], df["max"], facecolor=face_color, alpha=0.3
        )
        ax.plot(
            df["time"], df["mean"], label=label, color=face_color, linestyle=linestyle
        )
        return ax
