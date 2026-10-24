"""Sensitivity analysis of the simvastatin model.

The outputs are the pharmacokinetic parameters of simvastatin and simvastatin
acid in venous plasma after a single oral dose of simvastatin (the
non-compartmental analysis of `pkpdutils`) and the inhibition of the hepatic
HMG-CoA reductase, the effect of the drug on the cholesterol synthesis: its
maximum and its mean over the first day after the dose. The parameters are the
parameters of the model with bounds of +-15 % around their value. The analyses
are run as a script, the local analysis by default:

    python -m pkdb_models.models.simvastatin.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.simvastatin.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the SLCO1B1
genotypes, leaves out `LI__f_oatp1b1`. The environment variable
`PKPDSIM_SENSITIVITY_N` replaces the numbers of samples of the global analyses
for a quick run, see `pkpdsim.sensitivity.sample_size`.

The pharmacokinetics of simvastatin do not depend on the cholesterol, so the
simulation of a group starts with the dose (the cholesterol part of the model
starts close to, not at, its steady state, which the outputs do not read). The
dose is followed for `END_HR` hours, long enough for the terminal phases of
simvastatin and simvastatin acid (half-lives of 4 - 7 hr). The inhibition of
the HMG-CoA reductase is the fraction by which the inhibitors in the liver
(simvastatin acid and its active metabolites, `LI__active_inhibitors`) lower
the rate of the enzyme at the concentration of HMG-CoA: the competitive
inhibition of the rate law of `LI__HMGCOAREDUCTASE`.
"""

from collections.abc import Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Custom, Formula, Simulation

from pkdb_models.models.simvastatin import MODEL, MODEL_PATH
from pkdb_models.models.simvastatin.experiments.base_experiment import (
    SimvastatinSimulationExperiment,
)
from pkdb_models.models.simvastatin.fitting.parameters import (
    parameters_pd,
    parameters_pk,
)

#: oral dose of simvastatin of the analysis [mg]
DOSE_SIMVA = 40
#: the hours after the dose
END_HR = 72
#: the hours of the mean inhibition of the HMG-CoA reductase after the dose
INHIBITION_HR = 24
#: the limit of quantification of the non-compartmental analysis [mM], about
#: 1e-4 of the maximal concentration of simvastatin acid after 40 mg (4e-6 mM)
#: and 3e-5 of the one of simvastatin, so that the noise of the integrator is
#: not the terminal phase
LLOQ = 4e-10
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of simvastatin -> unit of the output
PK_OUTPUTS_SIMVA: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
}
#: outputs of the non-compartmental analysis of simvastatin acid, which is
#: formed from the dose of simvastatin: no clearance or volume -> unit
PK_OUTPUTS_SIMACID: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
}
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_simva` in mg), so they are divided by the molecular weight (its
#: value at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})

#: the symbols of the inhibition of the HMG-CoA reductase: the inhibitors and
#: HMG-CoA in the liver, the constants of the rate law
INHIBITION_SYMBOLS: list[str] = [
    "LI__active_inhibitors",
    "[LI__hmgcoa]",
    "LI__HMGCOAREDUCTASE_Km",
    "LI__HMGCOAREDUCTASE_Ki_simacid",
]


def hmgcr_inhibition(values: dict[str, np.ndarray]) -> np.ndarray:
    """Get the inhibition of the HMG-CoA reductase over time.

    The competitive inhibition of the rate law: the rate at the inhibitors
    relative to the rate without them, `(Km + S) / (Km (1 + I/Ki) + S)`, at the
    same HMG-CoA `S`; the inhibition is one minus it.
    """
    inhibitors = np.asarray(values["LI__active_inhibitors"])
    hmgcoa = np.asarray(values["[LI__hmgcoa]"])
    km = np.asarray(values["LI__HMGCOAREDUCTASE_Km"])
    ki = np.asarray(values["LI__HMGCOAREDUCTASE_Ki_simacid"])
    return 1.0 - (km + hmgcoa) / (km * (1.0 + inhibitors / ki) + hmgcoa)


def max_hmgcr_inhibition(time: np.ndarray, values: dict[str, np.ndarray]) -> float:
    """Get the maximal inhibition of the HMG-CoA reductase after the dose."""
    return float(np.max(hmgcr_inhibition(values)[time >= 0]))


def mean_hmgcr_inhibition(time: np.ndarray, values: dict[str, np.ndarray]) -> float:
    """Get the mean inhibition of the HMG-CoA reductase in the first day [min]."""
    shown = (time >= 0) & (time <= INHIBITION_HR * 60)
    inhibition = hmgcr_inhibition(values)[shown]
    t = time[shown]
    return float(np.trapezoid(inhibition, t) / (t[-1] - t[0]))


#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("simva_auc_inf_obs", "simvastatin AUC∞"),
    SensitivityOutput("simva_cmax", "simvastatin Cmax"),
    SensitivityOutput("simva_tmax", "simvastatin tmax"),
    SensitivityOutput("simva_thalf", "simvastatin Half-life"),
    SensitivityOutput("simva_vz_f", "simvastatin Vz/F"),
    SensitivityOutput("simva_cl_f", "simvastatin CL/F"),
    SensitivityOutput("simacid_auc_inf_obs", "simvastatin acid AUC∞"),
    SensitivityOutput("simacid_cmax", "simvastatin acid Cmax"),
    SensitivityOutput("simacid_tmax", "simvastatin acid tmax"),
    SensitivityOutput("simacid_thalf", "simvastatin acid Half-life"),
    SensitivityOutput("max_hmgcr_inhibition", "max HMG-CoA reductase inhibition"),
    SensitivityOutput("mean_hmgcr_inhibition", "mean HMG-CoA reductase inhibition"),
]


def _pk_observables(sid: str, outputs: Mapping[str, str]) -> list:
    """Get the non-compartmental analysis of a substance and its outputs."""
    pk_id = f"pk_{sid}"
    return [
        PK(
            pk_id,
            f"[Cve_{sid}]",
            dose="PODOSE_simva",
            route="oral",
            options=NCAOptions(lloq=LLOQ),
            parameters=list(outputs),
        ),
        *(
            Formula(
                f"{sid}_{key}",
                f"{pk_id}.{key} / at(Mr_simva, 0)"
                if key in PK_PER_DOSE_MASS
                else f"{pk_id}.{key}",
                unit=unit,
            )
            for key, unit in outputs.items()
        ),
    ]


#: the observables of a simulation, the outputs with their units; the ids of
#: the analyses (`pk_simva`, `pk_simacid`) are no species of the model
OBSERVABLES = [
    *_pk_observables("simva", PK_OUTPUTS_SIMVA),
    *_pk_observables("simacid", PK_OUTPUTS_SIMACID),
    Custom(
        "max_hmgcr_inhibition",
        max_hmgcr_inhibition,
        "dimensionless",
        symbols=INHIBITION_SYMBOLS,
    ),
    Custom(
        "mean_hmgcr_inhibition",
        mean_hmgcr_inhibition,
        "dimensionless",
        symbols=INHIBITION_SYMBOLS,
    ),
]

#: the output times [hr]: every 0.02 hr in the first day after the dose
#: (absorption and maximum), every 0.25 hr after it
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 24, 1201),
                np.linspace(24, END_HR, 4 * (END_HR - 24) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of simvastatin at time 0."""
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes, "PODOSE_simva": Q(DOSE_SIMVA, "mg")},
    )


#: the colors of the SLCO1B1 c.521T>C genotypes
SLCO1B1_COLORS: dict[str, str] = {"TC": "tab:orange", "CC": "tab:red"}

#: the groups the analyses are run for: the reference (SLCO1B1 c.521TT) and the
#: SLCO1B1 c.521T>C genotypes with a lower activity of OATP1B1, the largest
#: genetic effect on simvastatin acid (Pasanen2006)
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    *(
        SensitivityGroup(
            f"slco1b1_{genotype}",
            f"SLCO1B1 c.521{genotype}",
            sensitivity_simulation(
                {
                    "LI__f_oatp1b1": SimvastatinSimulationExperiment.slco1b1_activity[
                        genotype
                    ]
                }
            ),
            color,
        )
        for genotype, color in SLCO1B1_COLORS.items()
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # conversion factors
            "conversion_min_per_day",
            "conversion_ml_per_l",
            "conversion_l_per_ml",
            "LI__conversion_min_per_day",
            "LI__cf_units_per_mmole",
            # molecular weights
            "Mr_simva",
            "Mr_simacid",
            "Mr_simmets",
            "Mr_ldlc",
            "Mr_vldlc",
            # reference values
            "BW_ref",
            "ldlc_init",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            # dosing parameters
            "PODOSE_simva",
            "IVDOSE_simva",
            "ti_simva",
            "Ri_simva",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [
            (fp.pid, np.nan, np.nan, ParameterType.FIT)
            for fp in [*parameters_pk, *parameters_pd]
        ],
    )
    # the scaling factors of the organ functions and the activities of the
    # enzymes and transporters
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in [
                "KI__f_renal_function",
                "LI__f_cyp3a4",
                "GU__f_cyp3a4",
                "LI__f_oatp1b1",
                "LI__f_ugt",
            ]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
