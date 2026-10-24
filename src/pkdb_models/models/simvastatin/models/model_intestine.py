"""Intestine model of simvastatin.

The absorption of simvastatin and of the metabolites (enterohepatic
circulation), the first pass metabolism of simvastatin by CYP3A4 in the
enterocytes and the fecal excretion of the unabsorbed simvastatin and
metabolites.
"""

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.simvastatin.models import annotations, templates


class U(templates.U):
    """UnitDefinitions."""


_m = Model(
    "simvastatin_intestine",
    name="Model for intestinal/gut simvastatin metabolism",
    notes="""
    # Model for intestinal/gut simvastatin metabolism

    - Simvastatin (lactone) is absorbed from the intestinal lumen into the
      enterocytes, the fraction `F_abs_simva` of it; the rest is excreted in
      the feces.
    - Simvastatin is metabolized by CYP3A4 (and CYP3A5) in the enterocytes
      (first pass metabolism) or exported into the gut plasma (portal vein).
      The intestinal availability is about 0.25 - 0.3: regular grapefruit
      juice, an inhibitor of the intestinal CYP3A4 only, increases the AUC of
      simvastatin 3.6-fold (Lilja2004).
    - The simvastatin metabolites from the bile (enterohepatic circulation)
      are absorbed with the fraction `F_abs_simmets`, the rest is excreted in
      the feces (only metabolites and unabsorbed simvastatin are in the feces).
    - The hydrolysis of simvastatin to simvastatin acid (esterases) and the
      metabolism of simvastatin acid take place in the liver, not in the
      intestine.
    - Food does not change the bioavailability of simvastatin (Zocor label),
      the model has no food effect.
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
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vlumen",
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9,
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
    ),
    Compartment(
        "Vfeces",
        1.0,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
    Compartment(
        "Ventero",
        np.nan,
        name="intestinal lining (enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=True,
    ),
    Compartment(
        "Vapical",
        np.nan,
        name="apical membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        spatialDimensions=2,
        annotations=annotations.compartments["apical"],
    ),
    Compartment(
        "Vbaso",
        np.nan,
        name="basolateral membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        spatialDimensions=2,
        annotations=annotations.compartments["basolateral"],
    ),
]

_m.species = [
    Species(
        sid="simva_lumen",
        initialConcentration=0.0,
        name="simvastatin (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simva"],
        port=True,
    ),
    Species(
        sid="simva",
        initialConcentration=0.0,
        name="simvastatin (enterocytes)",
        compartment="Vgu",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simva"],
    ),
    Species(
        sid="simva_ext",
        initialConcentration=0.0,
        name="simvastatin (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        port=True,
        annotations=annotations.species["simva"],
    ),
    Species(
        sid="simva_feces",
        initialConcentration=0.0,
        name="simvastatin (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simva"],
    ),
    Species(
        sid="simmets_lumen",
        initialConcentration=0.0,
        name="simvastatin metabolites (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
        port=True,
    ),
    Species(
        sid="simmets",
        initialConcentration=0.0,
        name="simvastatin metabolites (intestine)",
        compartment="Vgu",
        substanceUnit=U.mmole,
        port=True,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
    ),
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
    Species(
        sid="simmets_feces",
        initialConcentration=0.0,
        name="simvastatin metabolites (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
    ),
]

# ---------------------------------------------------------------------------
# absorption and fecal excretion
# ---------------------------------------------------------------------------
_m.parameters = [
    Parameter(
        "F_abs_simva",
        0.85,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="fraction absorbed simvastatin",
        notes="""
        Fraction of simvastatin in the intestinal lumen which is absorbed into
        the enterocytes, the rest is excreted in the feces. The absorption of
        simvastatin relative to an intravenous dose is about 85 % in two animal
        species (Zocor label; 60 - 85 % Cheng1993, Vickers1990a).
        """,
    ),
    Parameter(
        "SIMVAABS_k",
        1.29,
        U.per_hr,
        constant=True,
        name="rate of absorption simvastatin",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        First order rate of the transit of simvastatin from the intestinal
        lumen (amount based), split into the absorption (`F_abs_simva`) and
        the fecal excretion of the unabsorbed fraction.
        """,
    ),
    Parameter(
        "F_abs_simmets",
        0.536,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="fraction absorbed simvastatin metabolites",
        notes="""
        Fraction of the simvastatin metabolites in the intestinal lumen (from
        the bile) which is reabsorbed in every round of the enterohepatic
        circulation; `1 - F_abs_simmets` is excreted in the feces. Set with
        the renal excretion so that about 13 % of a dose is excreted in the
        urine and the rest in the feces (14C simvastatin: 13 % urine, 60 %
        feces, Zocor label).
        """,
    ),
    Parameter(
        "SIMMETSABS_k",
        0.226,
        U.per_hr,
        constant=True,
        name="rate of absorption simvastatin metabolites",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        First order rate of the transit of the simvastatin metabolites from
        the intestinal lumen (amount based), split into the absorption
        (`F_abs_simmets`) and the fecal excretion.
        """,
    ),
]

_m.reactions.extend(
    [
        Reaction(
            sid="SIMVAABS",
            name="absorption simvastatin",
            equation="simva_lumen -> simva",
            formula=(
                "F_abs_simva * SIMVAABS_k/60 min_per_hr * Vlumen * simva_lumen",
                U.mmole_per_min,
            ),
            compartment="Vapical",
            sboTerm=SBO.TRANSPORT_REACTION,
        ),
        Reaction(
            sid="SIMVAEXC",
            name="excretion simvastatin (feces)",
            equation="simva_lumen -> simva_feces",
            formula=(
                "(1 dimensionless - F_abs_simva) * SIMVAABS_k/60 min_per_hr * "
                "Vlumen * simva_lumen",
                U.mmole_per_min,
            ),
            compartment="Vlumen",
            sboTerm=SBO.TRANSPORT_REACTION,
        ),
        Reaction(
            sid="SIMMETSABS",
            name="absorption simvastatin metabolites",
            equation="simmets_lumen -> simmets",
            formula=(
                "F_abs_simmets * SIMMETSABS_k/60 min_per_hr * Vlumen * simmets_lumen",
                U.mmole_per_min,
            ),
            compartment="Vapical",
            sboTerm=SBO.TRANSPORT_REACTION,
        ),
        Reaction(
            sid="SIMMETSEXC",
            name="excretion simvastatin metabolites (feces)",
            equation="simmets_lumen -> simmets_feces",
            formula=(
                "(1 dimensionless - F_abs_simmets) * SIMMETSABS_k/60 min_per_hr * "
                "Vlumen * simmets_lumen",
                U.mmole_per_min,
            ),
            compartment="Vlumen",
            sboTerm=SBO.TRANSPORT_REACTION,
        ),
    ]
)

# ---------------------------------------------------------------------------
# first pass metabolism and export
# ---------------------------------------------------------------------------
_m.parameters.extend(
    [
        Parameter(
            "CYP3A4_Km",
            25e-3,
            unit=U.mM,
            sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
            name="Km CYP3A4",
            port=True,
        ),
        Parameter(
            "f_cyp3a4",
            1.0,
            unit=U.dimensionless,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="activity of CYP3A4 (intestine)",
            notes="""
            Activity of the intestinal CYP3A4 relative to the reference.
            f_cyp3a4 = 1: normal activity;
            f_cyp3a4 < 1: reduced activity, inhibition of CYP3A4 (e.g.
            grapefruit juice, which inhibits the intestinal CYP3A4 only);
            f_cyp3a4 > 1: increased activity, induction of CYP3A4.
            Set by the experiments, not fitted.
            """,
        ),
        Parameter(
            "f_cyp3a5",
            0.0,
            unit=U.dimensionless,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="functional CYP3A5",
            port=True,
        ),
        Parameter(
            "r_cyp3a5",
            1.0,
            unit=U.dimensionless,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="capacity of CYP3A5 *1/*1 relative to CYP3A4",
            port=True,
        ),
        Parameter(
            "SIMVA_CYP3A4_Vmax",
            6.3e-3,
            unit=U.mmole_per_min_l,
            sboTerm=SBO.MAXIMAL_VELOCITY,
            name="Vmax CYP3A4 simvastatin (intestine)",
            notes="""
            Capacity of the intestinal CYP3A4 for simvastatin, independent of
            the liver. Together with `SIMVAEXP_Vmax` it sets the intestinal
            availability (about 0.25 - 0.3, Lilja2004); not identified by the
            data of the control arms, not fitted.
            """,
        ),
        Parameter(
            "SIMVAEXP_Km",
            9.7e-3,
            unit=U.mM,
            sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
            name="Km simvastatin export",
            notes="""
            Assuming the Km of OATP1B1 in the liver for simvastatin lactone
            9.7 µM (Chen et al., 2005).
            """,
        ),
        Parameter(
            "SIMVAEXP_Vmax",
            1e-3,
            unit=U.mmole_per_min_l,
            sboTerm=SBO.MAXIMAL_VELOCITY,
            name="Vmax simvastatin export (intestine)",
        ),
        Parameter(
            "SIMMETSEXP_Km",
            6.7e-3,
            unit=U.mM,
            sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
            name="Km simvastatin metabolite export",
        ),
        Parameter(
            "SIMMETSEXP_Vmax",
            1e-2,
            unit=U.mmole_per_min_l,
            sboTerm=SBO.MAXIMAL_VELOCITY,
            name="Vmax simvastatin metabolite export (intestine)",
            notes="""
            Export of the reabsorbed metabolites into the gut plasma, fast
            compared to their transit (not rate limiting).
            """,
        ),
    ]
)

_m.reactions.extend(
    [
        Reaction(
            sid="SIMVAEXP",
            name="SV export",
            compartment="Vbaso",
            equation="simva -> simva_ext",
            sboTerm=SBO.TRANSPORT_REACTION,
            formula=(
                "Vgu * SIMVAEXP_Vmax * simva / (SIMVAEXP_Km + simva)",
                U.mmole_per_min,
            ),
        ),
        Reaction(
            sid="SIMMETSEXP",
            name="SVM export",
            compartment="Vbaso",
            equation="simmets -> simmets_ext",
            sboTerm=SBO.TRANSPORT_REACTION,
            formula=(
                "Vgu * SIMMETSEXP_Vmax * simmets / (simmets + SIMMETSEXP_Km)",
                U.mmole_per_min,
            ),
        ),
        Reaction(
            sid="SIMVA_CYP3A4",
            name="CYP3A4: SV to SVM",
            compartment="Ventero",
            equation="simva -> simmets",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            formula=(
                "(f_cyp3a4 + r_cyp3a5 * f_cyp3a5) * Vgu * SIMVA_CYP3A4_Vmax * "
                "simva / (simva + CYP3A4_Km)",
                U.mmole_per_min,
            ),
            notes="""
            CYP3A4 and CYP3A5 with the Km of CYP3A4 for simvastatin; the
            capacity of CYP3A5 (*1/*1) is `r_cyp3a5` times the one of CYP3A4.
            """,
        ),
    ]
)

model_intestine = _m

if __name__ == "__main__":
    from pkdb_models.models.simvastatin import MODEL_BASE_PATH

    factory_result: FactoryResult = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine,
        sbml_level=3,
        sbml_version=2,
    )
