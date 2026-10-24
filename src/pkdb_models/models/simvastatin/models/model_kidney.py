"""Kidney model of simvastatin: the urinary excretion of the metabolites."""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.simvastatin.models import annotations, templates


class U(templates.U):
    """UnitDefinitions."""

    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")


_m = Model(
    "simvastatin_kidney",
    name="Model for simvastatin excretion via the kidney",
    notes="""
    # Model for simvastatin excretion via the kidney

    - Only simvastatin metabolites are excreted in the urine.
    - No unchanged simvastatin and simvastatin acid are excreted in the urine.
    - The renal clearance of the metabolites is relative to the glomerular
      filtration rate of their unbound fraction, `GFR * fu_simmets *
      SIMMETSEX_f`, with the renal function `f_renal_function`.
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vki",
        0.3,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]
_m.species = [
    # plasma
    Species(
        sid="simmets_ext",
        initialConcentration=0.0,
        name="simvastatin metabolites (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
    ),
    # urine (volume)
    Species(
        sid="simmets_urine",
        initialConcentration=0.0,
        name="simvastatin metabolites (urine)",
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
    ),
]

_m.parameters = [
    Parameter(
        "f_renal_function",
        1.0,
        U.dimensionless,
        name="parameter for renal function",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
        notes="""
        scaling factor for renal function
        1.0: normal renal function
        <1.0: decreased kidney function

        Renal function relative to the healthy glomerular filtration rate
        GFR_base, which is 101 ml/min at 75 kg; a measured creatinine
        clearance of X ml/min is the renal function X/101.
        """,
    ),
    Parameter(
        "GFR_base",
        101,
        U.ml_per_min,
        name="glomerular filtration rate (healthy)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
    Parameter(
        "fu_simmets",
        0.05,
        U.dimensionless,
        constant=True,
        name="fraction unbound in plasma simvastatin metabolites",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
    Parameter(
        "SIMMETSEX_f",
        910,
        U.dimensionless,
        name="renal clearance of unbound metabolites relative to the GFR",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        The renal clearance of the simvastatin metabolites is SIMMETSEX_f
        times the filtration of their unbound fraction, fu_simmets * GFR.
        The lumped metabolites include polar (inactive) metabolites with a
        renal clearance far above the filtration of a 95 % bound substance;
        the value is set so that about 13 % of a dose is excreted in the urine
        (14C simvastatin, Zocor label), there are no urine data in the studies.
        """,
    ),
]

_m.rules = [
    AssignmentRule(
        "GFR",
        "f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
]

_m.reactions = [
    Reaction(
        sid="SIMMETSEX",
        name="renal excretion simvastatin metabolites",
        compartment="Vki",
        equation="simmets_ext -> simmets_urine",
        sboTerm=SBO.TRANSPORT_REACTION,
        # [ml/min] * [l/ml] * [-] * [-] * [mmole/l]
        formula=(
            "GFR * 0.001 l_per_ml * fu_simmets * SIMMETSEX_f * simmets_ext",
            U.mmole_per_min,
        ),
    )
]

model_kidney = _m

if __name__ == "__main__":
    from pkdb_models.models.simvastatin import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        model=model_kidney,
        sbml_level=3,
        sbml_version=2,
    )
