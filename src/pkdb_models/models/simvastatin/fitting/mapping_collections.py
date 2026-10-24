"""Parameter fit problems for simvastatin.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the training data a fit is evaluated on but
not fitted to. The metadata of a mapping describes its curve, what a fit does
with the curve is decided here.

The training data are the studies without a coadministered drug in healthy
subjects (single doses and the exactly encoded repeated doses of Simard2001
and Ziviani2001) for the pharmacokinetics, and the LDL cholesterol of
hypercholesterolemic patients under daily doses for the pharmacodynamics. The
validation data has four parts, each a different question: the interactions
(`INTERACTION_VALIDATION`, the arms with a coadministered drug, simulated with
activity factors of CYP3A4, OATP1B1 and the glucuronidation which are not
fitted, and the arms of drugs without an interaction, the same subjects as the
control arms), the doses (`DOSE_VALIDATION`, the steady states of 80 mg and of
other regimens, which the training predicts), the populations
(`POPULATION_VALIDATION`, the genotypes, patients and ethnicities whose
difference the model describes with factors which are not fitted, or does not
describe) and the limitations (`LIMITATION_VALIDATION`, data of a formulation,
an assay or a process the model does not describe). The summaries of data
which is fitted one by one are excluded (`AGGREGATE_MAPPINGS`).
"""

from enum import StrEnum

from pkpdsim.fit import mapping_metadata, observable_filter, observable_id
from pkpdsim.metadata import Coadministration
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.simvastatin import DATA_PATHS, SIMVASTATIN_PATH
from pkdb_models.models.simvastatin.experiments.cholesterol import (
    Crouse1999,
    Davidson1997,
    Geiss2002,
    Isaacsohn2003,
    Jones1998a,
    Keech1994,
    Kosoglou2002,
    Li2003,
    Loria1993,
    Moelgaard1988,
    Mol1986,
    Mol1988,
    Ntanios1999,
    Owens1991,
    Pietro1989,
    Recto2000,
    Saito1991,
    Sivkov2021,
    Tuomilehto1995,
    Walker1990,
)
from pkdb_models.models.simvastatin.experiments.simvastatin import (
    Backman2000,
    Bergman2004,
    Chung2006,
    Gehin2015,
    Harvey2018,
    Hsyu2001,
    Jacobson2004,
    Jiang2017,
    Kantola1998,
    Keskitalo2008,
    Keskitalo2009,
    Kim2007,
    Kim2019,
    Kyrklund2000,
    Lilja1998,
    Lilja2000,
    Lilja2004,
    Lohitnavy2004,
    Marino2000,
    Mousa2000,
    Najib2003,
    Neuvonen1998,
    Nishio2005,
    OBrien2003,
    Pasanen2006,
    Pentikainen1992,
    Prueksaritanont2001,
    Simard2001,
    Sugimoto2001,
    TubicGrozdanis2008,
    Ucar2004,
    Zhi2003,
    Zhou2013,
    Ziviani2001,
)

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share, so a named mapping is named with
#: its study
type NamedMappings = dict[str, set[str]]

#: the experiments with fit mappings: the pharmacokinetic studies and the
#: studies of the LDL cholesterol. Lilja2000_2004 is a figure of the data of
#: Lilja2000 and Lilja2004 and has no mappings
EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
    # pharmacokinetics
    Backman2000,
    Bergman2004,
    Chung2006,
    Gehin2015,
    Harvey2018,
    Hsyu2001,
    Jacobson2004,
    Jiang2017,
    Kantola1998,
    Keskitalo2008,
    Keskitalo2009,
    Kim2007,
    Kim2019,
    Kyrklund2000,
    Lilja1998,
    Lilja2000,
    Lilja2004,
    Lohitnavy2004,
    Marino2000,
    Mousa2000,
    Najib2003,
    Neuvonen1998,
    Nishio2005,
    OBrien2003,
    Pasanen2006,
    Pentikainen1992,
    Prueksaritanont2001,
    Simard2001,
    Sugimoto2001,
    TubicGrozdanis2008,
    Ucar2004,
    Zhi2003,
    Zhou2013,
    Ziviani2001,
    # the LDL cholesterol
    Crouse1999,
    Davidson1997,
    Geiss2002,
    Isaacsohn2003,
    Jones1998a,
    Keech1994,
    Kosoglou2002,
    Li2003,
    Loria1993,
    Moelgaard1988,
    Mol1986,
    Mol1988,
    Ntanios1999,
    Owens1991,
    Pietro1989,
    Recto2000,
    Saito1991,
    Sivkov2021,
    Tuomilehto1995,
    Walker1990,
]


class Interaction(StrEnum):
    """Interaction of the coadministered substance with simvastatin."""

    NONE = "none"  # no coadministration
    INHIBITOR = "CYP3A4 inhibitor"
    # inhibits CYP3A4 in the intestine only
    INTESTINAL_INHIBITOR = "intestinal CYP3A4 inhibitor"
    INDUCER = "CYP3A4 inducer"
    # changes the pharmacokinetics, but not via CYP3A4
    NOT_CYP3A4 = "not CYP3A4 related"
    NO_INTERACTION = "no interaction"


#: the interaction of every coadministered substance with simvastatin, as the
#: studies simulate it (the factors and the observed ratios are in the
#: experiments)
INTERACTIONS: dict[Coadministration, Interaction] = {
    Coadministration.NONE: Interaction.NONE,
    Coadministration.AMLODIPINE: Interaction.INHIBITOR,
    Coadministration.CARBAMAZEPINE: Interaction.INDUCER,
    Coadministration.CILOSTAZOL: Interaction.INHIBITOR,
    # gastrointestinal motility, no CYP3A4 inhibition (Simard2001)
    Coadministration.CISAPRIDE: Interaction.NOT_CYP3A4,
    Coadministration.CLARITHROMYCIN: Interaction.INHIBITOR,
    Coadministration.DILTIAZEM: Interaction.INHIBITOR,
    Coadministration.ERYTHROMYCIN: Interaction.INHIBITOR,
    Coadministration.FENOFIBRATE: Interaction.NO_INTERACTION,
    # OATP1B1 and the glucuronidation of the acid (Backman2000)
    Coadministration.GEMFIBROZIL: Interaction.NOT_CYP3A4,
    Coadministration.GRAPEFRUIT_JUICE: Interaction.INTESTINAL_INHIBITOR,
    Coadministration.IMATINIB: Interaction.INHIBITOR,
    Coadministration.IRBESARTAN: Interaction.NO_INTERACTION,
    Coadministration.ITRACONAZOLE: Interaction.INHIBITOR,
    Coadministration.KETOCONAZOLE: Interaction.INHIBITOR,
    # the simulation inhibits the intestinal CYP3A4 only (Ziviani2001)
    Coadministration.LACIDIPINE: Interaction.INTESTINAL_INHIBITOR,
    Coadministration.NELFINAVIR: Interaction.INHIBITOR,
    Coadministration.ORLISTAT: Interaction.NO_INTERACTION,
    Coadministration.OSIMERTINIB: Interaction.NO_INTERACTION,
    Coadministration.PIOGLITAZONE: Interaction.NO_INTERACTION,
    Coadministration.RIFAMPICIN: Interaction.INDUCER,
    Coadministration.SETIPIPRANT: Interaction.NO_INTERACTION,
    Coadministration.ST_JOHNS_WORT: Interaction.INDUCER,
    Coadministration.TROGLITAZONE: Interaction.INDUCER,
    Coadministration.VERAPAMIL: Interaction.INHIBITOR,
}


def interaction_filter(*interactions: Interaction) -> MappingFilter:
    """Select the mappings whose coadministered substance has one of the interactions."""

    def select(_key: str, fit_mapping: FitMapping) -> bool:
        return (
            INTERACTIONS[mapping_metadata(fit_mapping).coadministration] in interactions
        )

    return select


#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {
    # the data are 55 - 70 % below the simulations and 2.3-fold below
    # Pasanen2006 at the same dose and formulation (Zocor 40 mg, fasted),
    # neither the assay nor the population explains it
    "Najib2003": {
        "fm_simva_zocor",
        "fm_simacid_zocor",
        "fm_simva_simvast",
        "fm_simacid_simvast",
    },
    # the acid is 7 - 10 times the one of every other study of 40 mg with a
    # normal lactone (hydrolysis of the lactone ex vivo or the assay)
    "Lohitnavy2004": {"fm_simacid_ref", "fm_simacid_test"},
}

#: the validation of the interactions: the arms with a coadministered drug,
#: simulated with activity factors which are not fitted, and the arms of drugs
#: without an interaction, which are the subjects of the control arms again.
#: `filter_coadministration` lets the validation data through for this reason,
#: every other coadministration stays out of the selection altogether
INTERACTION_VALIDATION: NamedMappings = {
    # gemfibrozil, OATP1B1 and the glucuronidation of the acid
    "Backman2000": {"fm_simva_gem", "fm_simacid_gem"},
    # fenofibrate, no interaction
    "Bergman2004": {
        "fm_simva_no_interaction",
        "fm_simacid_no_interaction",
        "fm_active_inhibitors_no_interaction",
        "fm_total_inhibitors_no_interaction",
    },
    # ketoconazole (strong inhibitor) and rifampicin (inducer)
    "Chung2006": {"fm_simva_inhi", "fm_simva_indu"},
    # setipiprant, no interaction
    "Gehin2015": {"fm_simva_no_interaction", "fm_simacid_no_interaction"},
    # osimertinib, no interaction
    "Harvey2018": {"fm_simva_no_interaction", "fm_simacid_no_interaction"},
    # nelfinavir, strong inhibitor
    "Hsyu2001": {"fm_active_inhibitors_inhi"},
    # verapamil (moderate) and clarithromycin (strong inhibitor)
    "Jacobson2004": {
        "fm_simva_single_inhi",
        "fm_simacid_single_inhi",
        "fm_simva_multi_inhibitor",
    },
    # amlodipine, weak inhibitor
    "Jiang2017": {"fm_simva_inhi", "fm_simacid_inhi"},
    # erythromycin and verapamil, moderate inhibitors
    "Kantola1998": {
        "fm_simva_inhi_ERY",
        "fm_simacid_inhi_ERY",
        "fm_simva_inhi_VER",
        "fm_simacid_inhi_VER",
    },
    # cilostazol, weak inhibitor
    "Kim2019": {"fm_simva_inhi", "fm_simacid_inhi"},
    # rifampicin, inducer
    "Kyrklund2000": {"fm_simva_indu", "fm_simacid_indu"},
    # grapefruit juice of double strength
    "Lilja1998": {
        "fm_simva_inhi",
        "fm_simacid_inhi",
        "fm_active_inhibitors_inhi",
        "fm_total_inhibitors_inhi",
    },
    # grapefruit juice of double strength, and the duration of its effect
    "Lilja2000": {
        "fm_simva_inhi",
        "fm_simacid_inhi",
        "fm_simva_gfj1d",
        "fm_simacid_gfj1d",
        "fm_simva_gfj3d",
        "fm_simacid_gfj3d",
        "fm_simva_gfj7d",
        "fm_simacid_gfj7d",
    },
    # grapefruit juice of normal strength, intestinal CYP3A4 only
    "Lilja2004": {"fm_simva_inhi", "fm_simacid_inhi"},
    # irbesartan, no interaction
    "Marino2000": {"fm_simva_and_simacid_irb"},
    # diltiazem, moderate inhibitor
    "Mousa2000": {"fm_simva_inhi"},
    # itraconazole, strong inhibitor
    "Neuvonen1998": {
        "fm_simva_inhi",
        "fm_simva_and_simacid_inhi",
        "fm_total_inhibitors_inhi",
    },
    # amlodipine at a steady state of 5 mg simvastatin
    "Nishio2005": {"fm_active_inhibitors_amlodipine"},
    # imatinib, moderate inhibitor
    "OBrien2003": {"fm_simva_inhi", "fm_simacid_inhi"},
    # troglitazone (inducer) and pioglitazone (no interaction)
    "Prueksaritanont2001": {
        "fm_activeInhibitors1_indu",
        "fm_totalInhibitors1_indu",
        "fm_activeInhibitors2_no_interaction",
        "fm_totalInhibitors2_no_interaction",
    },
    # St John's wort, inducer
    "Sugimoto2001": {"fm_simva_stjohnswort", "fm_simacid_stjohnswort"},
    # carbamazepine, inducer
    "Ucar2004": {"fm_simva_carbamazepine", "fm_simacid_carbamazepine"},
    # orlistat, no interaction
    "Zhi2003": {"fm_simva_orlistat", "fm_simacid_orlistat"},
    # lacidipine, intestinal CYP3A4
    "Ziviani2001": {"fm_simva_and_simacid_lacidipine"},
}

#: the validation of the doses: the steady states of 80 mg and of other
#: regimens, which the training predicts
DOSE_VALIDATION: NamedMappings = {
    # 80 mg daily, steady state
    "Bergman2004": {
        "fm_simva",
        "fm_simacid",
        "fm_active_inhibitors",
        "fm_total_inhibitors",
    },
    # 20 mg daily, steady state
    "Hsyu2001": {"fm_active_inhibitors"},
    # 40 mg daily, steady state
    "Jacobson2004": {"fm_simva_multi"},
    # 40 and 80 mg daily for 10 days
    "Prueksaritanont2001": {
        "fm_activeInhibitors1",
        "fm_totalInhibitors1",
        "fm_activeInhibitors2",
        "fm_totalInhibitors2",
    },
    # LDL cholesterol: medians of 40, 80 and 160 mg (160 mg above the
    # licensed range)
    "Davidson1997": {"fm_ldlc_SIM40", "fm_ldlc_SIM80", "fm_ldlc_SIM160"},
    # LDL cholesterol after 2 weeks, Chinese patients with comedication
    "Li2003": {"fm_ldlc_SIM20", "fm_ldlc_SIM40"},
    # the stable baseline of the placebo
    "Mol1986": {"fm_ldlc_placebo"},
    # switches of the regimen over 24 weeks, the patients of Mol1986 later
    "Mol1988": {"fm_ldlc_all", "fm_ldlc_group1", "fm_ldlc_group2", "fm_ldlc_group3"},
    # 40 and 80 mg pooled, plateau at 6 weeks
    "Ntanios1999": {"fm_ldlc_all"},
    # titration groups selected by the response, no error bars
    "Owens1991": {"fm_ldlc_placebo", "fm_ldlc_SIM20", "fm_ldlc_SIM40"},
    # 6 weeks of 20 and 40 mg, crossover
    "Recto2000": {"fm_ldlc_SIM20", "fm_ldlc_SIM40"},
    # the offset 4 weeks after the last dose
    "Saito1991": {
        "fm_ldlc_2_5mg_evening_withdrawal",
        "fm_ldlc_5mg_evening_withdrawal",
    },
}

#: the validation of the populations: genotypes, patients and ethnicities
#: which the model describes with factors which are not fitted (SLCO1B1,
#: CYP3A5), or does not describe (ABCG2, the Japanese acid of Sugimoto2001)
POPULATION_VALIDATION: NamedMappings = {
    # patients with non-small cell lung cancer, 33 % Asian, geometric means
    "Harvey2018": {"fm_simva", "fm_simacid"},
    # CYP3A5 *1/*3 and *1/*1 (f_cyp3a5)
    "Kim2007": {"fm_simva_CYP3A5_1_3", "fm_simva_CYP3A5_1_1"},
    # ABCG2 c.421C>A, not in the model
    "Keskitalo2009": {
        "fm_simva_c421C_A",
        "fm_simacid_c421C_A",
        "fm_simva_c421A_A",
        "fm_simacid_c421A_A",
    },
    # SLCO1B1 c.521T>C (f_oatp1b1)
    "Pasanen2006": {
        "fm_simva_c521TC",
        "fm_simacid_c521TC",
        "fm_simva_c521CC",
        "fm_simacid_c521CC",
    },
    # elderly Japanese hypercholesterolemic patients, 5 mg daily
    "Nishio2005": {"fm_active_inhibitors_control"},
    # Japanese: the acid per dose is 3 times the one of the other studies
    "Sugimoto2001": {"fm_simacid"},
    # LDL cholesterol of heterozygous familial hypercholesterolemia and type 2
    # diabetes, mean doses
    "Geiss2002": {"fm_ldlc_SIM_FH", "fm_ldlc_SIM_diabetics"},
    # hypertriglyceridemia, a low baseline and a flatter dose response
    "Isaacsohn2003": {"fm_ldlc_SIM20", "fm_ldlc_SIM40", "fm_ldlc_SIM80"},
    # Russian type IIa/IIb hyperlipidemia, 10 mg for 4 months
    "Sivkov2021": {"fm_ldlc_521", "fm_ldlc_3435"},
}

#: the validation of the limitations of the model: valid data of a
#: formulation, an assay or a process the model does not describe, which would
#: distort the fitted parameters of the processes it does describe
LIMITATION_VALIDATION: NamedMappings = {
    # patients with chronic myeloid leukemia, fed: the acid peaks at 1 h and is
    # about equal to the lactone
    "OBrien2003": {"fm_simva", "fm_simacid"},
    # cisapride changes the gastrointestinal motility, not CYP3A4
    "Simard2001": {"fm_simva_cisapride", "fm_simacid_cisapride"},
    # a solubilizing capsule (presystemic hydrolysis) and a delayed release
    # tablet (regional absorption)
    "TubicGrozdanis2008": {
        "fm_simva_immediate",
        "fm_simacid_immediate",
        "fm_simva_delayed",
        "fm_simacid_delayed",
    },
    # LDL cholesterol after 3 years: intention to treat with non-compliance
    # and step down; the drift of the placebo is not modelled
    "Keech1994": {
        "fm_ldlc_SIM20_late",
        "fm_ldlc_SIM40_late",
        "fm_ldlc_placebo_early",
        "fm_ldlc_placebo_late",
    },
    # the drift of the placebo and the regression to the mean
    "Kosoglou2002": {"fm_ldlc_placebo"},
    "Isaacsohn2003": {"fm_ldlc_placebo"},
    "Tuomilehto1995": {"fm_ldlc_SIM0"},
    "Walker1990": {"fm_ldlc_SIM0"},
    # the placebo, and the morning doses which lowered the LDL cholesterol
    # 7 - 9 % less than the evening doses: the model has no time of the day
    "Saito1991": {
        "fm_ldlc_placebo",
        "fm_ldlc_2_5mg_morning_treatment",
        "fm_ldlc_2_5mg_morning_withdrawal",
        "fm_ldlc_5mg_morning_treatment",
        "fm_ldlc_5mg_morning_withdrawal",
    },
    # the acute fall under biliary diversion after cholecystectomy
    "Loria1993": {"fm_ldlc_SIM80"},
    # the genotype groups: the SLCO1B1 effect on the LDL cholesterol is not
    # reproduced, ABCB1 is not in the model
    "Sivkov2021": {
        "fm_ldlc_521TT",
        "fm_ldlc_521TC",
        "fm_ldlc_521CC",
        "fm_ldlc_3435CC",
        "fm_ldlc_3435TC",
        "fm_ldlc_3435TT",
    },
}

#: the summaries of data which the fits use one by one, excluded from every
#: fit: a mean of subjects would count the subjects twice
AGGREGATE_MAPPINGS: NamedMappings = {
    # the subjects of the reference formulation, bioequivalent test tablet
    "Lohitnavy2004": {"fm_simva_test"},
    # the week 4 point of the subjects of Fig. 1
    "Mol1986": {"fm_ldlc_SIM10_once", "fm_ldlc_SIM40_once"},
}

#: the validation data by question
VALIDATION_QUESTIONS: dict[str, NamedMappings] = {
    "interactions": INTERACTION_VALIDATION,
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}

#: the validation data
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(mappings.get(study, set()) for mappings in VALIDATION_QUESTIONS.values())
    )
    for questions in VALIDATION_QUESTIONS.values()
    for study in questions
}


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_coadministration(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No coadministered drug, besides the validation data."""
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping):
        return True
    return mapping_metadata(fit_mapping).coadministration == Coadministration.NONE


#: the observables of the pharmacodynamics, the plasma LDL cholesterol
PD_OBSERVABLES: set[str] = {"Cve_ldlc", "ldlc_change"}


def filter_pk(_key: str, fit_mapping: FitMapping) -> bool:
    """Only the pharmacokinetic data (not the LDL cholesterol)."""
    return observable_id(fit_mapping) not in PD_OBSERVABLES


#: Only the pharmacodynamic data, the LDL cholesterol.
filter_pd = observable_filter(PD_OBSERVABLES)


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`) and the arms with a coadministered drug
    (`filter_coadministration`). The outliers are `OUTLIER_MAPPINGS`, the
    validation data is `VALIDATION_MAPPINGS`. Neither kind enters the cost;
    both are simulated and evaluated with the training data, so a report says
    how the fitted parameters describe data they were not fitted on.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=EXPERIMENT_CLASSES,
        base_path=SIMVASTATIN_PATH,
        data_path=DATA_PATHS,
    )
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation]:
        check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
            filter_coadministration,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in VALIDATION_QUESTIONS.items()
        )
    )
    return selection.collections


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """The pharmacokinetic data."""
    return mapping_collections([filter_pk])


def f_collections_pd() -> dict[str, list[FitMappingCollection]]:
    """The pharmacodynamic data, the LDL cholesterol."""
    return mapping_collections([filter_pd])


if __name__ == "__main__":
    for f in [f_collections_pk, f_collections_pd]:
        console.rule(title=f.__name__, align="left", style="white")
        f()
