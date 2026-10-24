"""Simvastatin part of the liver model.

The hepatic uptake of simvastatin, its activation to simvastatin acid, the
metabolism of both by CYP3A4, the uptake of simvastatin acid (OATP1B1) and its
efflux, the exchange of the metabolites with the plasma and the biliary
excretion of the metabolites (enterohepatic circulation).

Every process has a capacity of its own; the activity factors of CYP3A4
(`f_cyp3a4`), CYP3A5 (`f_cyp3a5`), the glucuronidation and CYP2C8 of the
acid (`f_ugt`) and OATP1B1 (`f_oatp1b1`) are set by the experiments of the
interactions and genotypes.
"""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.simvastatin.models import annotations, templates
from pkdb_models.models.simvastatin.models.fits import FITS


class U(templates.U):
    """UnitDefinitions."""


_m = Model(
    "simvastatin_liver_simvastatin",
    name="Model for simvastatin metabolism in the liver",
    notes="""
    # Model for simvastatin metabolism in the liver

    - Simvastatin (lactone) is taken up passively (reversible) into the
      hepatocytes, hydrolyzed to simvastatin acid (esterases, paraoxonases)
      and metabolized by CYP3A4/CYP3A5.
    - Simvastatin acid is taken up from the plasma by OATP1B1 (SLCO1B1) and
      leaves the hepatocytes by efflux; in the liver it is metabolized by
      CYP3A4/CYP3A5 and by glucuronidation and CYP2C8. The acid formed in the liver reaches the plasma by the
      efflux only, so the activity of OATP1B1 sets the clearance of the plasma
      acid (SLCO1B1 c.521CC: AUC of the acid 3.2-fold, Pasanen2006).
    - The metabolites (lumped, active and inactive) are exchanged with the
      plasma and excreted into the bile (enterohepatic circulation).
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)
_m.species = [
    # plasma
    Species(
        sid="simva_ext",
        initialConcentration=0.0,
        name="simvastatin (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simva"],
    ),
    Species(
        sid="simacid_ext",
        initialConcentration=0.0,
        name="simvastatin acid (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simacid"],
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
    # liver
    Species(
        sid="simva",
        initialConcentration=0.0,
        name="simvastatin (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simva"],
    ),
    # intestinal lumen
    Species(
        sid="simmets_lumen",
        initialConcentration=0.0,
        name="simvastatin metabolites (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
    ),
]

_m.parameters = [
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
        name="activity of CYP3A4 (liver)",
        notes="""
        Activity of the hepatic CYP3A4 relative to the reference.
        f_cyp3a4 = 1: normal activity;
        f_cyp3a4 < 1: reduced activity, inhibition of CYP3A4;
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
        "f_ugt",
        1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="activity of the glucuronidation and CYP2C8 of simvastatin acid",
        notes="""
        Activity of the metabolism of simvastatin acid besides CYP3A4
        (UGT1A1/1A3 glucuronidation, CYP2C8) relative to the reference.
        f_ugt < 1: inhibition (e.g. gemfibrozil). Set by the experiments, not
        fitted.
        """,
    ),
    Parameter(
        "f_oatp1b1",
        1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="activity of OATP1B1",
        notes="""
        Activity of OATP1B1 (SLCO1B1) relative to the reference (c.521TT).
        f_oatp1b1 < 1: reduced activity, the SLCO1B1 c.521T>C variant or an
        inhibitor of OATP1B1 (e.g. gemfibrozil). Set by the experiments, not
        fitted.
        """,
    ),
]

_m.reactions = [
    Reaction(
        "SIMVAIMP",
        name="SV import",
        compartment="Vbaso",
        equation="simva_ext <-> simva",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "SIMVAIMP_Km",
                9.7e-3,
                unit=U.mM,
                sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                name="Km for simvastatin import",
                notes="""
                Simvastatin lactone 9.7 µM (Chen et al., 2005).
                """,
            ),
            Parameter(
                "SIMVAIMP_Vmax",
                1.0,
                unit=U.mmole_per_min_l,
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax for simvastatin import",
                notes="""
                The lipophilic lactone enters the hepatocytes mainly by
                passive diffusion (reversible), fast compared to its
                metabolism; not identified by the data, not fitted.
                """,
            ),
        ],
        formula=(
            "Vli * SIMVAIMP_Vmax / SIMVAIMP_Km * "
            "(simva_ext - simva) / "
            "(1 dimensionless + simva_ext / SIMVAIMP_Km + simva / SIMVAIMP_Km)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "SIMACIDIMP",
        name="SVA import (OATP1B1)",
        compartment="Vbaso",
        equation="simacid_ext -> simacid",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "SIMACIDIMP_Km",
                3.6e-3,
                unit=U.mM,
                sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                name="Km for simvastatin acid import",
                notes="""
                Km of OATP1B1 for simvastatin acid 3.6 µM (Chen et al., 2005).
                """,
            ),
            Parameter(
                "SIMACIDIMP_Vmax",
                **FITS.parameter("LI__SIMACIDIMP_Vmax", unit=U.mmole_per_min_l),
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax for simvastatin acid import",
            ),
        ],
        formula=(
            "f_oatp1b1 * Vli * SIMACIDIMP_Vmax * simacid_ext / "
            "(simacid_ext + SIMACIDIMP_Km)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "SIMACIDEXP",
        name="SVA efflux",
        compartment="Vbaso",
        equation="simacid -> simacid_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "SIMACIDEXP_k",
                0.925,
                unit=U.per_min,
                sboTerm=SBO.KINETIC_CONSTANT,
                name="rate of simvastatin acid efflux",
                notes="""
                Efflux of simvastatin acid from the hepatocytes into the
                plasma (passive and basolateral efflux transporters).
                """,
            ),
        ],
        formula=("SIMACIDEXP_k * Vli * simacid", U.mmole_per_min),
    ),
    Reaction(
        "SIMMETSEXP",
        name="SVM exchange",
        compartment="Vbaso",
        equation="simmets <-> simmets_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "SIMMETSEXP_Km",
                6.7e-3,
                unit=U.mM,
                sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                name="Km for simvastatin metabolites exchange",
                notes="""
                Assuming a Km similar to the ones of simvastatin and
                simvastatin acid for OATP1B1: simvastatin acid 3.6 µM (Nakai
                et al., 2001; Chen et al., 2005), simvastatin lactone 9.7 µM
                (Chen et al., 2005).
                """,
            ),
            Parameter(
                "SIMMETSEXP_Vmax",
                0.744,
                unit=U.mmole_per_min_l,
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax for simvastatin metabolites exchange",
            ),
        ],
        formula=(
            "Vli * SIMMETSEXP_Vmax / SIMMETSEXP_Km * "
            "(simmets - simmets_ext) / "
            "(1 dimensionless + simmets_ext / SIMMETSEXP_Km + simmets / SIMMETSEXP_Km)",
            U.mmole_per_min,
        ),
    ),
    # esterases activation pathway
    Reaction(
        "ESTERASE",
        name="Esterase: SV to SVA",
        compartment="Vli",
        equation="simva -> simacid",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "ESTERASE_Km",
                0.8e-3,
                unit=U.mM,
                sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                name="Km esterase",
                notes="""
                [Fukami2010] Ki, 0.8 +- 0.1 (human liver microsomes)
                """,
            ),
            Parameter(
                "ESTERASE_Vmax",
                **FITS.parameter("LI__ESTERASE_Vmax", unit=U.mmole_per_min_l),
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax esterase",
            ),
        ],
        formula=(
            "Vli * ESTERASE_Vmax * simva / (simva + ESTERASE_Km)",
            U.mmole_per_min,
        ),
    ),
    # CYP3A4 pathway
    Reaction(
        "SIMVA_CYP3A4",
        name="CYP3A4: SV to SVM",
        compartment="Vli",
        equation="simva -> simmets",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "SIMVA_CYP3A4_Vmax",
                **FITS.parameter("LI__SIMVA_CYP3A4_Vmax", unit=U.mmole_per_min_l),
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax CYP3A4 simvastatin (liver)",
            ),
        ],
        formula=(
            "(f_cyp3a4 + r_cyp3a5 * f_cyp3a5) * Vli * SIMVA_CYP3A4_Vmax * "
            "simva / (simva + CYP3A4_Km)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "SIMACID_CYP3A4",
        name="CYP3A4: SVA to SVM",
        compartment="Vli",
        equation="simacid -> simmets",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "SIMACID_CYP3A4_Vmax",
                1.5e-3,
                unit=U.mmole_per_min_l,
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax CYP3A4 simvastatin acid (liver)",
            )
        ],
        formula=(
            "(f_cyp3a4 + r_cyp3a5 * f_cyp3a5) * Vli * SIMACID_CYP3A4_Vmax * "
            "simacid / (simacid + CYP3A4_Km)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "SIMACIDMET",
        name="SVA to SVM (glucuronidation, CYP2C8)",
        compartment="Vli",
        equation="simacid -> simmets",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "SIMACIDMET_k",
                16.0,
                unit=U.per_min,
                sboTerm=SBO.KINETIC_CONSTANT,
                name="rate of the metabolism of simvastatin acid not by CYP3A4",
                notes="""
                The metabolism of simvastatin acid besides CYP3A4: the
                glucuronidation (UGT1A1, UGT1A3; followed by the lactonization
                of the acyl glucuronide) and CYP2C8 (Prueksaritanont2002). The
                inhibition of these pathways and of OATP1B1 by gemfibrozil
                increases the AUC of simvastatin acid 2.9-fold (Backman2000)
                without a change of simvastatin. Without this pathway the acid
                would rise far more than simvastatin with an inhibitor of
                CYP3A4, the data show similar ratios (clarithromycin:
                simvastatin 10-fold, acid 12-fold, Jacobson2004; erythromycin
                6.2- and 3.9-fold, Kantola1998).
                """,
            ),
        ],
        formula=("f_ugt * SIMACIDMET_k * Vli * simacid", U.mmole_per_min),
    ),
    # li -> gu (enterohepatic circulation)
    Reaction(
        sid="EHC_simmets",
        name="EHC SVM",
        compartment="Vapical",
        equation="simmets -> simmets_lumen",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "EHC_simmets_k",
                **FITS.parameter("LI__EHC_simmets_k", unit=U.per_min),
                sboTerm=SBO.KINETIC_CONSTANT,
                name="rate of biliary excretion of the simvastatin metabolites",
            ),
        ],
        formula=("EHC_simmets_k * Vli * simmets", U.mmole_per_min),
    ),
]

model_liver_simvastatin = _m


if __name__ == "__main__":
    from pkdb_models.models.simvastatin import MODEL_BASE_PATH
    from pkdb_models.models.simvastatin.models.model_liver_base import model_liver_base

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_liver_simvastatin.sid}.xml",
        model=[
            model_liver_base,
            model_liver_simvastatin,
        ],
        sbml_level=3,
        sbml_version=2,
    )
