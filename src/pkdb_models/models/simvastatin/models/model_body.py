"""Whole-body model of simvastatin and cholesterol.

The PBPK model of simvastatin, simvastatin acid and the simvastatin metabolites
with the oral and intravenous dosing, coupled to the plasma LDL and VLDL
cholesterol. The intestine, the liver and the kidney are submodels.
"""

import logging
import os
from typing import Any, NotRequired, TypedDict

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    PORT_SUFFIX,
    AssignmentRule,
    Compartment,
    ExternalModelDefinition,
    FactoryResult,
    Model,
    ModelUnits,
    Parameter,
    RateRule,
    Reaction,
    ReplacedElement,
    Species,
    Submodel,
    UnitDefinition,
    Units,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.simvastatin.models import annotations
from pkdb_models.models.simvastatin.models.fits import FITS
from pkdb_models.models.simvastatin.models.templates import creators

logger = logging.getLogger(__name__)


class U(Units):
    """UnitsDefinitions."""

    mmole = UnitDefinition("mmole")
    min = UnitDefinition("min")
    kg = UnitDefinition("kg")
    per_kg = UnitDefinition("per_kg", "1/kg")
    m2 = UnitDefinition("m2", "meter^2")
    mM = UnitDefinition("mM", "mmole/liter")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_min_l = UnitDefinition("mmole_per_min_l", "mmole/min/l")
    l_per_min = UnitDefinition("l_per_min", "l/min")
    per_min = UnitDefinition("per_min", "1/min")
    s = UnitDefinition("s", "second")
    mg = UnitDefinition("mg", "mg")
    ml = UnitDefinition("ml", "ml")
    hr = UnitDefinition("hr", "hr")
    per_hr = UnitDefinition("per_hr", "1/hr")
    cm = UnitDefinition("cm", "cm")
    mg_per_l = UnitDefinition("mg_per_l", "mg/l")
    mg_per_g = UnitDefinition("mg_per_g", "mg/g")
    mg_per_hr = UnitDefinition("mg_per_hr", "mg/hr")
    l_per_hr = UnitDefinition("l_per_hr", "l/hr")
    l_per_kg = UnitDefinition("l_per_kg", "l/kg")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")
    l_per_mmole = UnitDefinition("l_per_mmole", "l/mmole")
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    m2_per_kg = UnitDefinition("m2_per_kg", "meter^2/kg")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    mmole_per_hr = UnitDefinition("mmole_per_hr", "mmole/hr")
    mmole_per_l = UnitDefinition("mmole_per_l", "mmole/l")
    mmole_per_min_kg = UnitDefinition("mmole_per_min_kg", "mmole/min/kg")
    mmole_per_hr_ml = UnitDefinition("mmole_per_hr_ml", "mmole/hr/ml")
    ml_per_s = UnitDefinition("ml_per_s", "ml/s")
    ml_per_s_kg = UnitDefinition("ml_per_s_kg", "ml/s/kg")
    ml_per_l = UnitDefinition("ml_per_l", "ml/l")
    mul_per_g = UnitDefinition("mul_per_g", "microliter/g")
    mul_per_min_mg = UnitDefinition("mul_per_min_mg", "microliter/min/mg")
    min_per_day = UnitDefinition("min_per_day", "min/day")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")
    s_per_min = UnitDefinition("s_per_min", "s/min")
    s_per_hr = UnitDefinition("s_per_hr", "s/hr")
    mg_per_day = UnitDefinition("mg_per_day", "mg/day")


# -----------------------------------------------------------------------------
# Whole Body Metabolism
# -----------------------------------------------------------------------------
_m = Model(
    "simvastatin_body",
    name="PK/PD model for whole-body simvastatin and cholesterol metabolism",
    notes="""
    # PK/PD model for whole-body simvastatin and cholesterol metabolism

    ## Changelog
    - replaced inital assignments with rules
    - fixed constant flags on parameters
    """
    + terms_of_use,
    creators=creators,
    units=U,
    model_units=ModelUnits(
        time=U.min,
        extent=U.mmole,
        substance=U.mmole,
        length=U.meter,
        area=U.m2,
        volume=U.liter,
    ),
    annotations=[
        (BQB.IS, "taxonomy/9606"),  # Homo sapiens
    ],
)
_m.deletions = []
_m.replaced_elements = []

# -----------------------------------------------------------------------------
# Submodels
# -----------------------------------------------------------------------------
COMPARTMENTS_BODY = {
    "gu": "gut",
    "ki": "kidney",
    "li": "liver",
    "lu": "lung",
    "re": "rest",
    "ar": "arterial blood",
    "ve": "venous blood",
    "po": "portal vein",
    "hv": "hepatic vein",
}

SUBMODEL_SID_DICT = {  # tissue to submodel mapping
    "ki": "KI",  # kidney
    "li": "LI",  # liver
    "gu": "GU",  # Gut
}

kidney_id = "simvastatin_kidney"
liver_id = "simvastatin_liver"
gut_id = "simvastatin_intestine"

_m.external_model_definitions = [
    ExternalModelDefinition(
        sid="kidney",
        source=f"{kidney_id}.xml",
        modelRef=kidney_id,
        name="kidney model definition",
    ),
    ExternalModelDefinition(
        sid="liver",
        source=f"{liver_id}.xml",
        modelRef=liver_id,
        name="liver model definition",
    ),
    ExternalModelDefinition(
        sid="gut",
        source=f"{gut_id}.xml",
        modelRef=gut_id,
        name="intestine model definition",
    ),
]

_m.submodels = [
    Submodel(sid=SUBMODEL_SID_DICT["ki"], modelRef="kidney", name="kidney submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["li"], modelRef="liver", name="liver submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["gu"], modelRef="gut", name="intestine submodel"),
]

for emd in _m.external_model_definitions:
    logger.info("%s (%s)", emd, os.path.abspath(emd.source))


class SubstanceBody(TypedDict):
    """Definition of a substance transported in the whole-body model."""

    name: str
    unit: UnitDefinition
    cinit: float  # initial concentration [mmole/l]
    Mr: float  # molecular weight [g/mole]
    IVDOSE: NotRequired[float]  # intravenous dose [mg]
    PODOSE: NotRequired[float]  # oral dose [mg]
    # rate of dissolution and stomach passage [1/hr]; None: fitted, see `FITS`
    Ka_dis: NotRequired[float | None]
    fup: float  # fraction unbound in plasma [-]
    # distribution in tissues [litre/min], 0: no distribution; None: fitted
    ftissue: float | None
    # tissue to plasma partition coefficient [-]; None: fitted
    Kp: NotRequired[float | None]
    annotations: list[tuple[BQB, str]]


def value_of(pid: str, value: float | None, unit: UnitDefinition) -> dict[str, Any]:
    """Get the value of a parameter with its unit.

    Args:
        pid: id of the parameter.
        value: value of the parameter, None for a fitted parameter, whose value
            and uncertainty come from the records of the adopted fits (`FITS`).
        unit: unit of the parameter.

    Returns:
        The keyword arguments `value` and `unit` of the parameter, and
        `uncertainties` of a fitted parameter.
    """
    if value is None:
        return FITS.parameter(pid, unit=unit)
    return {"value": value, "unit": unit}


def distributed(sdict: SubstanceBody) -> bool:
    """Check whether a substance distributes into the tissues."""
    return "ftissue" in sdict and (
        sdict["ftissue"] is None or not np.isclose(sdict["ftissue"], 0.0)
    )


# -----------------------------------------------------------------------------
# substances transported via circulation
SUBSTANCES_BODY: dict[str, SubstanceBody] = {
    "simva": {
        "name": "simvastatin",
        "unit": U.mmole,
        # initial concentration
        "cinit": 0.0,  # [mmole/l]
        # Molecular weight
        "Mr": 418.6,  # [g/mole]
        # iv doses [mg]
        "IVDOSE": 0,
        # oral absorption
        "PODOSE": 0,  # dose
        # the dissolution and stomach passage, the distribution in the
        # tissues and the partition coefficient of the tissues are fitted,
        # see `fits.FITS`
        "Ka_dis": None,
        "fup": 0.05,  # fraction unbound in plasma
        "ftissue": None,
        "Kp": None,
        "annotations": annotations.species["simva"],
    },
    "simacid": {
        "name": "simvastatin acid",
        "unit": U.mmole,
        "cinit": 0.0,  # [mmole/l] # initial concentration
        "Mr": 436.6,  # [g/mole] molecular weight
        "fup": 0.05,  # [-] fraction unbound in plasma
        "ftissue": 10.0,  # [litre/min] distribution in tissues (flow limited)
        # [-] partition coefficient of the tissues: the volume of distribution
        # of the acid is small, about 22 l (half-life 1.9 h after an
        # intravenous dose of the acid, Zocor label; the model has 3.3 h)
        "Kp": 0.254,
        "annotations": annotations.species["simacid"],
    },
    "simmets": {
        "name": "simvastatin metabolites",
        "unit": U.mmole,
        "cinit": 0.0,  # [mmole/l] initial concentration
        # [g/mole] molecular weight of simvastatin acid: the metabolites are
        # lumped and measured as simvastatin acid equivalents
        "Mr": 436.6,
        "fup": 0.05,  # [-] fraction unbound in plasma
        # [litre/min] distribution in tissues, the one of simvastatin acid
        # (`ftissue_simmets = ftissue_simacid`)
        "ftissue": 10.0,
        "Kp": 1.0,  # [-] partition coefficient of the tissues
        "annotations": annotations.species["simmets"],
    },
    "ldlc": {
        "name": "ldl-cholesterol",
        "unit": U.mmole,
        # initial concentration (! set identical in liver model !)
        "cinit": 3.0,  # [mmole/l] optimal <3.36 [mM], intermediate 3.36-3.11 [mM]; high > 4.11;
        "Mr": 386.654,  # [g/mole] (molecular weight of cholesterol!)
        "fup": 1.0,  # [-] fraction unbound in plasma
        "ftissue": 0.0,  # [litre/min] distribution in tissues (no distribution)
        "annotations": annotations.species["ldlc"],
    },
    "vldlc": {
        "name": "vldl-cholesterol",
        "unit": U.mmole,
        # initial concentration (! set identical in liver model !)
        "cinit": 1.0,  # FIXME
        "Mr": 386.654,  # [g/mole] (molecular weight of cholesterol!)
        "fup": 1.0,  # [-] fraction unbound in plasma
        "ftissue": 0.0,  # [litre/min] distribution in tissues (no distribution)
        "annotations": annotations.species["vldlc"],
    },
}

# -------------------------------------------------------------------------------------
# Compartments
# -------------------------------------------------------------------------------------
_m.compartments = [
    Compartment(
        "Vre",
        metaId="meta_Vre",
        value=1,
        unit=U.liter,
        constant=False,
        name="rest of body",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["re"],
    ),
    Compartment(
        "Vgu",
        metaId="meta_Vgu",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vki",
        metaId="meta_Vki",
        value=1,
        unit=U.liter,
        constant=False,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vli",
        metaId="meta_Vli",
        value=1,
        unit=U.liter,
        constant=False,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
    ),
    Compartment(
        "Vlu",
        metaId="meta_Vlu",
        value=1,
        unit=U.liter,
        constant=False,
        name="lung",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["lu"],
    ),
    Compartment(
        "Vve",
        metaId="meta_Vve",
        value=1,
        unit=U.liter,
        constant=False,
        name="venous blood",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ve"],
    ),
    Compartment(
        "Var",
        metaId="meta_Var",
        value=1,
        unit=U.liter,
        constant=False,
        name="arterial blood",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ar"],
    ),
    Compartment(
        "Vurine",
        metaId="meta_Vurine",
        value=1,
        unit=U.liter,
        constant=True,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["urine"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["feces"],
    ),
    Compartment(
        "Vstomach",
        metaId="meta_Vstomach",
        value=1,
        unit=U.liter,
        constant=True,
        name="stomach",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["stomach"],
    ),
    Compartment(
        "Vpo",
        metaId="meta_Vpo",
        value=1,
        unit=U.liter,
        constant=False,
        name="portal plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["po"],
    ),
    Compartment(
        "Vhv",
        metaId="meta_Vhv",
        value=1,
        unit=U.liter,
        constant=False,
        name="hepatic venous plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["hv"],
    ),
]

# create plasma and tissue compartments (for correct blood volume)
for cid in COMPARTMENTS_BODY:
    if cid not in ["ar", "ve", "po", "hv"]:
        _m.compartments.extend(
            [
                Compartment(
                    f"V{cid}_tissue",
                    value=1,
                    unit=U.liter,
                    constant=False,
                    name=f"{cid} tissue",
                    metaId=f"meta_V{cid}_tissue",
                    port=True,
                    sboTerm=SBO.PHYSICAL_COMPARTMENT,
                    annotations=annotations.compartments["pa"]
                    + [
                        (BQB.IS_PART_OF, aid[1])
                        for aid in annotations.compartments[cid]
                    ],
                ),
                Compartment(
                    f"V{cid}_plasma",
                    value=1,
                    unit=U.liter,
                    constant=False,
                    name=f"{cid} plasma",
                    metaId=f"meta_V{cid}_plasma",
                    port=True,
                    sboTerm=SBO.PHYSICAL_COMPARTMENT,
                    annotations=annotations.compartments["plasma"]
                    + [
                        (BQB.IS_PART_OF, aid[1])
                        for aid in annotations.compartments[cid]
                    ],
                ),
            ]
        )

# the gut lumen, its volume is `f_lumen * Vgu` (rule below)
_m.compartments.append(
    Compartment(
        "Vgulumen",
        metaId="meta_Vgulumen",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut lumen",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
    )
)

# replace volumes of submodels
_m.replaced_elements.extend(
    [
        # kidney
        ReplacedElement(
            sid="Vki_tissue_RE",
            metaId="Vki_tissue_RE",
            elementRef="Vki_tissue",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vki{PORT_SUFFIX}",
        ),
        # plasma
        ReplacedElement(
            sid="Vki_plasma_RE",
            metaId="Vki_plasma_RE",
            elementRef="Vki_plasma",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        # urine
        ReplacedElement(
            sid="Vurine_RE",
            metaId="Vurine_RE",
            elementRef="Vurine",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vurine{PORT_SUFFIX}",
        ),
        # liver
        ReplacedElement(
            sid="Vli_tissue_RE",
            metaId="Vli_tissue_RE",
            elementRef="Vli_tissue",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vli{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vli_plasma_RE",
            metaId="Vli_plasma_RE",
            elementRef="Vli_plasma",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        # gut lumen
        ReplacedElement(
            sid="Vgulumen_RE1",
            metaId="Vgulumen_RE1",
            elementRef="Vgulumen",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vlumen{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgulumen_RE2",
            metaId="Vgulumen_RE2",
            elementRef="Vgulumen",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vlumen{PORT_SUFFIX}",
        ),
        # gut tissue
        ReplacedElement(
            sid="Vgu_tissue_RE1",
            metaId="Vgu_tissue_RE1",
            elementRef="Vgu_tissue",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vgu{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgu_plasma_RE",
            metaId="Vgu_plasma_RE",
            elementRef="Vgu_plasma",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgu_feces_RE",
            metaId="Vgu_feces_RE",
            elementRef="Vfeces",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vfeces{PORT_SUFFIX}",
        ),
    ]
)

# -------------------------------------------------------------------------------------
# Species
# -------------------------------------------------------------------------------------
_m.species = []
for sid, sdict in SUBSTANCES_BODY.items():
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in ["ve", "ar", "po", "hv"]:
            sid_ex = f"C{cid}_{sid}"
            cid_ex = f"V{cid}"
        else:
            # plasma compartment
            sid_ex = f"C{cid}_plasma_{sid}"
            cid_ex = f"V{cid}_plasma"

        _m.species.append(
            Species(
                sid_ex,
                metaId=f"meta_{sid_ex}",
                initialConcentration=sdict["cinit"],
                compartment=cid_ex,
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} ({cname})",
                hasOnlySubstanceUnits=False,
                port=True,
                annotations=sdict["annotations"],
                sboTerm=SBO.SIMPLE_CHEMICAL,
            )
        )

    # tissue species
    if distributed(sdict):
        for cid, cname in COMPARTMENTS_BODY.items():
            if cid not in ["ve", "ar", "li", "ki", "gu", "po", "hv"]:
                sid_ex = f"C{cid}_{sid}"
                cid_ex = f"V{cid}_tissue"
                _m.species.extend(
                    [
                        Species(
                            sid_ex,
                            metaId=f"meta_{sid_ex}",
                            initialConcentration=sdict["cinit"],
                            compartment=cid_ex,
                            substanceUnit=sdict["unit"],
                            name=f"{sdict['name']} ({cname})",
                            hasOnlySubstanceUnits=False,
                            port=True,
                            annotations=sdict["annotations"],
                            sboTerm=SBO.SIMPLE_CHEMICAL,
                        )
                    ]
                )

    # urine metabolites
    if sid in ["simmets"]:
        _m.species.append(
            Species(
                f"Aurine_{sid}",
                metaId=f"meta_Aurine_{sid}",
                initialConcentration=0,
                compartment="Vurine",
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} (urine)",
                hasOnlySubstanceUnits=True,
                annotations=sdict["annotations"],
                sboTerm=SBO.SIMPLE_CHEMICAL,
            )
        )
    # stomach metabolites
    if sid in ["simva"]:
        _m.species.append(
            Species(
                f"Astomach_{sid}",
                metaId=f"meta_Astomach_{sid}",
                initialConcentration=0.0,
                compartment="Vstomach",
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} (stomach)",
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                boundaryCondition=True,
            )
        )

    # feces simvastatin (unabsorbed) and metabolites
    if sid in ["simva", "simmets"]:
        _m.species.append(
            Species(
                f"Afeces_{sid}",
                metaId=f"meta_Afeces_{sid}",
                initialConcentration=0,
                compartment="Vfeces",
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} (feces)",
                hasOnlySubstanceUnits=True,
                annotations=sdict["annotations"],
                sboTerm=SBO.SIMPLE_CHEMICAL,
            )
        )
    if sid in ["simva", "simmets"]:
        # gut lumen
        _m.species.append(
            Species(
                sid=f"Cgulumen_{sid}",
                initialConcentration=0.0,
                metaId=f"meta_Cgulumen_{sid}",
                name=f"{sdict['name']} (gut lumen)",
                compartment="Vgulumen",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=False,
                port=True,
            )
        )
        _m.replaced_elements.append(
            ReplacedElement(
                sid=f"Cgulumen_{sid}_RE1",
                metaId=f"Cgulumen_{sid}_RE1",
                elementRef=f"Cgulumen_{sid}",
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{sid}_lumen{PORT_SUFFIX}",
            )
        )
        if sid in ["simmets"]:
            _m.replaced_elements.append(
                ReplacedElement(
                    sid=f"Cgulumen_{sid}_RE2",
                    metaId=f"Cgulumen_{sid}_RE2",
                    elementRef=f"Cgulumen_{sid}",
                    submodelRef=SUBMODEL_SID_DICT["li"],
                    portRef=f"{sid}_lumen{PORT_SUFFIX}",
                ),
            )


# replace plasma species between body and tissue models
replaced_species = {
    "li": ["simva", "simacid", "simmets", "vldlc", "ldlc"],
    "ki": ["simmets"],
    "gu": ["simva", "simmets"],
}
for tkey, skey_list in replaced_species.items():
    for skey in skey_list:
        _m.replaced_elements.extend(
            [
                ReplacedElement(
                    sid=f"C{tkey}_plasma_{skey}_RE",
                    metaId=f"C{tkey}_plasma_{skey}_RE",
                    elementRef=f"C{tkey}_plasma_{skey}",
                    submodelRef=SUBMODEL_SID_DICT[tkey],
                    portRef=f"{skey}_ext{PORT_SUFFIX}",
                ),
            ]
        )

# urine species replacements
for skey in ["simmets"]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Aurine_{skey}_RE",
            metaId=f"Aurine_{skey}_RE",
            elementRef=f"Aurine_{skey}",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"{skey}_urine{PORT_SUFFIX}",
        )
    )

# feces species replacements
for skey in ["simva", "simmets"]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Afeces_{skey}_RE",
            metaId=f"Afeces_{skey}_RE",
            elementRef=f"Afeces_{skey}",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"{skey}_feces{PORT_SUFFIX}",
        )
    )

# -------------------------------------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------------------------------------

_m.parameters = [
    # conversion factors
    Parameter(
        "conversion_min_per_day",
        1440,
        U.min_per_day,
        constant=True,
        name="Conversion factor min to hours",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "conversion_ml_per_l",
        1000,
        U.ml_per_l,
        constant=True,
        name="volume conversion factor",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "conversion_l_per_ml",
        0.001,
        U.l_per_ml,
        constant=True,
        name="volume conversion factor",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # whole body data
    Parameter(
        "BW",
        75,
        U.kg,
        constant=True,
        name="body weight [kg]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        annotations=[
            (BQB.IS, "efo/0004338"),
            (BQB.IS, "ncit/C25208"),
            (BQB.IS, "cmo/CMO:0000012"),
        ],
    ),
    Parameter(
        "BW_ref",
        75,
        U.kg,
        constant=True,
        name="reference body weight [kg]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes=(
            "Body weight at which the exchange flows of the tissue "
            "distribution (`ftissue_<sid>`) are given; they scale with the "
            "body weight as the volumes, the blood flows and the renal "
            "clearance do."
        ),
    ),
    Parameter("HEIGHT", 170, U.cm, constant=True, name="height [cm]"),
    Parameter("HR", 70, U.per_min, constant=True, name="heart rate [1/min]"),
    Parameter("HRrest", 70, U.per_min, constant=True, name="heart rate [1/min]"),
    Parameter(
        "BSA",
        0,
        U.m2,
        constant=False,
        name="body surface area [m^2]",
        annotations=[(BQB.IS, "ncit/C25157"), (BQB.IS, "omit/0003188")],
    ),
    Parameter(
        "COBW",
        1.25,
        U.ml_per_s_kg,
        constant=True,
        name="cardiac output per bodyweight [ml/s/kg]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        annotations=[
            (BQB.IS, "ncit/C119246"),
            (BQB.IS, "omit/0003637"),
        ],
        notes="""Simone1997 75 [50-100] ml/min/kg; 1.25 [0.83 - 1.66] ml/s/kg""",
    ),
    Parameter(
        "CO",
        np.nan,
        U.ml_per_s,
        constant=False,
        name="cardiac output [ml/s]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        annotations=[
            (BQB.IS, "ncit/C119246"),
            (BQB.IS, "omit/0003637"),
        ],
        notes="""BW*COBW (100 ml/s)""",
    ),
    Parameter(
        "QC",
        np.nan,
        U.l_per_min,
        constant=False,
        name="cardiac output [L/min]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        annotations=[
            (BQB.IS, "ncit/C119246"),
            (BQB.IS, "omit/0003637"),
        ],
    ),
    Parameter(
        "COHRI",
        150,
        U.ml,
        constant=True,
        name="increase of cardiac output per heartbeat [ml/min*min]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # fractional tissue volumes
    Parameter(
        "Fblood",
        0.02,
        U.dimensionless,
        constant=True,
        name="blood fraction of organ volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "HCT",
        0.51,
        U.dimensionless,
        constant=True,
        metaId="meta_HCT",
        name="hematocrit",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        annotations=[
            (BQB.IS, "ncit/C64796"),
            (BQB.IS, "omit/0007571"),
            (BQB.IS, "efo/0004348"),
        ],
    ),
    # fractional tissue volumes
    Parameter(
        "FVgi",
        0.0297,
        U.l_per_kg,
        constant=True,
        name="fractional tissue volume gastrointestinal tract",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""FVgi = FVgu + FVpa + FVsp = 0.0171 + 0.01 + 0.0026 = 0.0297""",
        annotations=[
            (BQB.IS_VERSION_OF, item[1]) for item in annotations.compartments["gi"]
        ],
    ),
    Parameter(
        "FVki",
        0.0044,
        U.l_per_kg,
        constant=True,
        name="kidney fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FVli",
        0.0210,
        U.l_per_kg,
        constant=True,
        name="liver fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FVlu",
        0.0076,
        U.l_per_kg,
        constant=True,
        name="lung fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FVre",
        0,
        U.l_per_kg,
        constant=False,
        name="rest of body fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # calculated based on other tissues
    Parameter(
        "FVve",
        0.0514,
        U.l_per_kg,
        constant=True,
        name="venous fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FVar",
        0.0257,
        U.l_per_kg,
        constant=True,
        name="arterial fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FVpo",
        0.001,
        U.l_per_kg,
        constant=True,
        name="portal fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FVhv",
        0.001,
        U.l_per_kg,
        constant=True,
        name="hepatic venous fractional tissue volume",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # fractional tissue blood flows
    Parameter(
        "FQgu",
        0.18,
        U.dimensionless,
        constant=True,
        name="gut fractional tissue blood flow",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
    Assumed FQgu is the sum of FQgu + FQsp + FQpa for correct portal blood flow.
    with FQgu=0.146, FQsp=0.017, FQpa=0.017
    """,
    ),
    Parameter(
        "FQki",
        0.190,
        U.dimensionless,
        constant=True,
        name="kidney fractional tissue blood flow",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FQh",
        0.215,
        U.dimensionless,
        constant=True,
        name="hepatic (venous side) fractional tissue blood flow",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FQlu",
        1,
        U.dimensionless,
        constant=True,
        name="lung fractional tissue blood flow",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    Parameter(
        "FQre",
        0,
        U.dimensionless,
        constant=False,
        name="rest of body fractional tissue blood flow",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # ------------------------------
    # gut lumen
    # ------------------------------
    Parameter(
        "f_lumen",
        0.9,
        U.dimensionless,
        constant=True,
        name="fraction lumen of intestine",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # ------------------------------
    # CYP3A4 and CYP3A5 (liver and intestine)
    # ------------------------------
    Parameter(
        "CYP3A4_Km",
        25e-3,
        unit=U.mM,
        constant=True,
        name="Km CYP3A4",
        port=True,
        sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
        notes="""
        assumptions: identical Km for simvastin & simvastatin acid; identical Km in
        liver and intestine
        [Prueksaritanont2003, Prueksaritanont1997] 21-29 [µM]
        """,
    ),
    Parameter(
        "f_cyp3a5",
        0.0,
        U.dimensionless,
        constant=True,
        name="functional CYP3A5",
        port=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        Functional CYP3A5 of the genotype in the liver and the intestine: 0
        for *3/*3 (the reference of the model; *3 is a splicing defect without
        functional protein), 0.5 for *1/*3 and 1 for *1/*1. Set by the
        experiments, not fitted.
        """,
    ),
    Parameter(
        "r_cyp3a5",
        1.0,
        U.dimensionless,
        constant=True,
        name="capacity of CYP3A5 *1/*1 relative to CYP3A4",
        port=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        Capacity of CYP3A5 in *1/*1 carriers for simvastatin and simvastatin
        acid relative to the one of CYP3A4. CYP3A5 is at least half of the
        hepatic CYP3A in *1 carriers (Kuehl2001), its activity per protein
        for simvastatin is assumed equal to the one of CYP3A4. Not fitted;
        the CYP3A5 genotypes of Kim2007 (*1/*1 vs *3/*3: AUC of simvastatin
        0.30-fold) validate it.
        """,
    ),
    # ------------------------------
    Parameter(
        "simmets_inhibitor_activity",
        0.4,
        U.dimensionless,
        constant=True,
        name="HMG-CoA Reductase inhibitor activity of simmets",
        sboTerm=SBO.INHIBITORY_CONSTANT,
        notes="""
        The inhibitor activity of the lumped metabolites relative to
        simvastatin acid, in the active inhibitors of the enzymatic assays and
        in the inhibition of the HMG-CoA reductase. The active inhibitors are
        0.34 - 0.42 of the total inhibitors (AUC, Pentikainen1992,
        Prueksaritanont2001); 0.4 gives 0.4 at 40 mg.
        """,
    ),
]

replaced_parameters = {
    "li": [
        "CYP3A4_Km",
        "f_cyp3a5",
        "r_cyp3a5",
        "simmets_inhibitor_activity",
        "Mr_ldlc",
    ],
    "gu": ["CYP3A4_Km", "f_cyp3a5", "r_cyp3a5"],
    "ki": [],
}
for ckey, pids in replaced_parameters.items():
    for pid in pids:
        _m.replaced_elements.append(
            ReplacedElement(
                sid=f"{pid}_{ckey}_RE",
                metaId=f"{pid}_{ckey}_RE",
                elementRef=f"{pid}",
                submodelRef=SUBMODEL_SID_DICT[ckey],
                portRef=f"{pid}{PORT_SUFFIX}",
            )
        )

_m.rules = []

# species specific parameters
for sid, sdict in SUBSTANCES_BODY.items():
    _m.parameters.extend(
        [
            # molecular weights
            Parameter(
                f"Mr_{sid}",
                sdict["Mr"],
                U.g_per_mole,
                constant=True,
                name=f"Molecular weight {sid} [g/mole]",
                sboTerm=SBO.MOLECULAR_MASS,
            ),
            # fraction unbound (for free concentration)
            Parameter(
                f"fup_{sid}",
                sdict["fup"],
                U.dimensionless,
                constant=True,
                name=f"fraction unbound in plasma {sid}",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ]
    )

    # tissue distribution
    p = Parameter(
        f"ftissue_{sid}",
        **value_of(f"ftissue_{sid}", sdict["ftissue"], U.l_per_min),
        constant=True,
        name=f"tissue distribution {sid}",
        notes="Exchange flow at the reference body weight `BW_ref`.",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    )
    _m.parameters.append(p)
    if "Kp" in sdict:
        _m.parameters.append(
            Parameter(
                f"Kp_{sid}",
                **value_of(f"Kp_{sid}", sdict["Kp"], U.dimensionless),
                constant=True,
                name=f"tissue to plasma partition coefficient {sid}",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes=(
                    "Partition coefficient of the tissue of the rest of the "
                    "body (total concentrations): the tissue concentration in "
                    "equilibrium is `Kp` times the plasma concentration."
                ),
            )
        )
    if sid == "simmets":
        # tissue distribution of metabolites assumed identical to simvastatin acid
        p.constant = False
        _m.rules.append(
            AssignmentRule(f"ftissue_{sid}", "ftissue_simacid", unit=U.l_per_min)
        )

    # dosing
    if "IVDOSE" in sdict:
        _m.parameters.extend(
            [
                Parameter(
                    f"IVDOSE_{sid}",
                    sdict["IVDOSE"],
                    U.mg,
                    constant=False,
                    name=f"IV bolus dose {sid} [mg]",
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    annotations=[(BQB.IS, "ncit/C38274")],
                ),
                # iv kinetics after application
                Parameter(
                    f"ti_{sid}",
                    10,
                    U.s,
                    constant=True,
                    name=f"injection time {sid} [s]",
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    annotations=[(BQB.IS, "ncit/C69282")],
                ),
                Parameter(
                    f"Ki_{sid}",
                    0.02,
                    U.per_min,
                    constant=False,
                    name=f"Ki [1/min] injection {sid}",
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                ),
                # continuous infusion
                Parameter(
                    f"Ri_{sid}",
                    0,
                    U.mg_per_min,
                    constant=True,
                    name=f"Ri [mg/min] rate of infusion {sid}",
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    annotations=[(BQB.IS, "ncit/C94916")],
                ),
                Parameter(
                    f"cum_dose_{sid}",
                    0,
                    U.mg,
                    constant=False,
                    name=f"Cumulative dose due to infusion {sid}",
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    annotations=[
                        (BQB.IS, "ncit/C94394"),
                    ],
                ),
            ]
        )

# the fraction unbound of the metabolites in the renal excretion
_m.replaced_elements.append(
    ReplacedElement(
        sid="fup_simmets_ki_RE",
        metaId="fup_simmets_ki_RE",
        elementRef="fup_simmets",
        submodelRef=SUBMODEL_SID_DICT["ki"],
        portRef=f"fu_simmets{PORT_SUFFIX}",
    )
)


# -------------------------------------------------------------------------------------------------
# AssignmentRules
# -------------------------------------------------------------------------------------------------
_m.rules = [
    *_m.rules,
    # Rest body volume
    AssignmentRule(
        "FVre",
        "1.0 l_per_kg - (FVgi + FVki + FVli + FVlu + FVve + FVar)",
        U.l_per_kg,
    ),
    # Rest body perfusion
    AssignmentRule("FQre", "1.0 dimensionless - (FQki + FQh)", U.dimensionless),
    # Body surface area (Haycock1978)
    AssignmentRule(
        "BSA", "0.024265 m2 * power(BW/1 kg, 0.5378) * power(HEIGHT/1 cm, 0.3964)", U.m2
    ),
    # cardiac output (depending on heart rate and bodyweight)
    AssignmentRule("CO", "BW*COBW + (HR-HRrest) * COHRI / 60 s_per_min", U.ml_per_s),
    # cardiac output (depending on bodyweight)
    AssignmentRule("QC", "CO/1000 ml_per_l * 60 s_per_min", U.l_per_min),
    # volumes
    AssignmentRule("Vgu", "BW*FVgi", U.liter),
    AssignmentRule("Vki", "BW*FVki", U.liter),
    AssignmentRule("Vli", "BW*FVli", U.liter),
    AssignmentRule("Vlu", "BW*FVlu", U.liter),
    AssignmentRule("Vre", "BW*FVre", U.liter),
    AssignmentRule("Vgulumen", "f_lumen * Vgu", U.liter),
    # venous and arterial blood volume (corrected for tissue blood volumes)
    AssignmentRule(
        "Vve",
        "BW*FVve - FVve/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
        U.liter,
    ),
    AssignmentRule(
        "Var",
        "BW*FVar - FVar/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
        U.liter,
    ),
    AssignmentRule(
        "Vpo",
        "(1 dimensionless - HCT) * (BW*FVpo - FVpo/(FVar+FVve+FVpo+FVhv) "
        "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
        U.liter,
    ),
    AssignmentRule(
        "Vhv",
        "(1 dimensionless - HCT) * (BW*FVhv - FVhv/(FVar+FVve+FVpo+FVhv) "
        "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
        U.liter,
    ),
    # blood flows
    AssignmentRule("Qgu", "QC*FQgu", U.l_per_min, name="gut blood flow"),
    AssignmentRule("Qki", "QC*FQki", U.l_per_min, name="kidney blood flow"),
    AssignmentRule(
        "Qh", "QC*FQh", U.l_per_min, name="hepatic (venous side) blood flow"
    ),
    AssignmentRule("Qha", "Qh - Qgu", U.l_per_min, name="hepatic artery blood flow"),
    AssignmentRule("Qlu", "QC*FQlu", U.l_per_min, name="lung blood flow"),
    AssignmentRule("Qre", "QC*FQre", U.l_per_min, name="rest of body blood flow"),
    AssignmentRule("Qpo", "Qgu", U.l_per_min, name="portal blood flow"),
]

# Volumes for explicit tissue models
for cid in COMPARTMENTS_BODY:
    if cid not in ["ve", "ar", "po", "hv"]:
        _m.rules.extend(
            [
                AssignmentRule(
                    f"V{cid}_tissue", f"V{cid}*(1 dimensionless - Fblood)", unit=U.liter
                ),
                AssignmentRule(
                    f"V{cid}_plasma",
                    value=f"V{cid}* Fblood * (1 dimensionless - HCT)",
                    unit=U.liter,
                ),
            ]
        )

for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # injection
    if "IVDOSE" in sdict:
        _m.rules.extend(
            [
                AssignmentRule(
                    f"Ki_{sid}",
                    f"0.693 dimensionless/ti_{sid} * 60 s_per_min",
                    U.per_min,
                    name="injection rate IV",
                    notes="""
                          log(2) ~ 0.693 used for conversion of half-life injection time to
                          injection rate.
                          """,
                ),
            ]
        )

    # ---------------------------------
    # X Amount [mg], C Concentration
    # ---------------------------------
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid not in ["ve", "ar", "po", "hv"]:
            _m.rules.extend(
                [
                    AssignmentRule(
                        f"A{cid}_plasma_{sid}",
                        f"C{cid}_plasma_{sid}*V{cid}_plasma",
                        U.mmole,
                        name=f"{sname} concentration ({cname})",
                    ),
                    AssignmentRule(
                        f"C{cid}_free_{sid}",
                        f"C{cid}_plasma_{sid} * fup_{sid}",
                        U.mM,
                        name=f"{sname} free concentration ({cname})",
                    ),
                    AssignmentRule(
                        f"X{cid}_plasma_{sid}",
                        f"A{cid}_plasma_{sid}*Mr_{sid}",
                        U.mg,
                        name=f"{sname} amount ({cname})",
                    ),
                    AssignmentRule(
                        f"M{cid}_plasma_{sid}",
                        f"A{cid}_plasma_{sid}/V{cid}_plasma*Mr_{sid}",
                        U.mg_per_l,
                        name=f"{sname} amount ({cname})",
                    ),
                ]
            )
        else:
            _m.rules.extend(
                [
                    AssignmentRule(
                        f"A{cid}_{sid}",
                        f"C{cid}_{sid}*V{cid}",
                        U.mmole,
                        name=f"{sname} amount ({cname})",
                    ),
                    AssignmentRule(
                        f"X{cid}_{sid}",
                        f"A{cid}_{sid}*Mr_{sid}",
                        U.mg,
                        name=f"{sname} amount ({cname})",
                    ),
                    AssignmentRule(
                        f"M{cid}_{sid}",
                        f"A{cid}_{sid}/V{cid}*Mr_{sid}",
                        U.mg_per_l,
                        name=f"{sname} concentration ({cname})",
                    ),
                ]
            )

    # urine metabolites
    if sid in ["simmets"]:
        cid, cname = "urine", "urine"
        _m.rules.append(
            AssignmentRule(
                f"X{cid}_{sid}",
                f"A{cid}_{sid}*Mr_{sid}",
                U.mg,
                name=f"{sname} amount ({cname})",
            ),
        )
    if sid in ["simva", "simmets"]:
        cid, cname = "feces", "feces"
        _m.rules.append(
            AssignmentRule(
                f"X{cid}_{sid}",
                f"A{cid}_{sid}*Mr_{sid}",
                U.mg,
                name=f"{sname} amount ({cname})",
            ),
        )


# balance equations to track total and active compounds
_m.rules.extend(
    [
        # sum of simva and simacic via hydrolyzation of lactone
        AssignmentRule(
            "Cve_simva_and_simacid",
            "Cve_simva + Cve_simacid",
            U.mM,
            name="total simvastatin and simvastatin acid in venous blood",
        ),
        # active metabolites
        AssignmentRule(
            "Cve_active_inhibitors",
            "Cve_simacid + simmets_inhibitor_activity * Cve_simmets",
            U.mM,
            name="active HMG-CoA reductase inhibitors in venous blood",
        ),
        # hydrolyzation of lactone & measurement of active
        AssignmentRule(
            "Cve_total_inhibitors",
            "Cve_simva + Cve_simacid + Cve_simmets",
            U.mM,
            name="total HMG-CoA reductase inhibitors in venous blood",
        ),
    ]
)

# -------------------------------------------------------------------------------------
# Reactions
# -------------------------------------------------------------------------------------
_m.reactions = []
# --------------------------------------------
# cholesterol consumption body & LDLC changes
# --------------------------------------------
_m.parameters.extend(
    [
        Parameter(
            "ldlc_init",
            3,
            unit=U.mM,
            name="Initial LDLC -concentration",
            port=True,
            sboTerm=SBO.MOLAL_CONCENTRATION_OF_AN_ENTITY,
        ),
        Parameter(
            "v_cho_ref",
            1000,
            unit=U.mg_per_day,
            name="reference cholesterol turnover [mg/day]",
            port=True,
            sboTerm=SBO.BASAL_RATE_CONSTANT,
        ),
    ]
)

_m.replaced_elements.append(
    ReplacedElement(
        sid="v_cho_ref_li_RE",
        metaId="v_cho_ref_li_RE",
        elementRef="v_cho_ref",
        submodelRef=SUBMODEL_SID_DICT["li"],
        portRef=f"v_cho_ref{PORT_SUFFIX}",
    )
)

# whole-body net change in cholesterol
# FIXME: scale with bodyweight!

_m.parameters.extend(
    [
        # +1.0 [g/day]
        Parameter(
            "ldlc_diet_k",
            1.0,
            unit=U.dimensionless,
            sboTerm=SBO.KINETIC_CONSTANT,
            name="rate of cholesterol uptake from diet",
            notes="""
       +1.0 [g/day] cholesterol uptake diet
       """,
        ),
        # -1.2 [g/day]
        Parameter(
            "ldlc_loss_k",
            1.2,
            unit=U.dimensionless,
            sboTerm=SBO.KINETIC_CONSTANT,
            name="rate of cholesterol loss in feces",
            notes="""
        -1.2 [g/day] loss feces
        """,
        ),
        # -0.8 [g/day]
        Parameter(  # calculated using parameter scan and referencing it on 3mM plasma LDLC in stst
            "ldlc_utilization_Vmax",
            0.6521432619924221,
            unit=U.dimensionless,
        ),
        Parameter(
            "ldlc_consumption_Km",
            60,
            unit=U.mmole_per_l,
        ),
        Parameter(
            "f_ldlc_utilization_Vmax",
            1,
            U.dimensionless,
            constant=True,
            name="scaling factor for utilization",
            sboTerm=SBO.MAXIMAL_VELOCITY,
            notes="""
        FH patients are simulated via a different net consumption (i.e. here utilization)
        """,
        ),
        Parameter(
            "vldlc_conversion_k",
            2,
            U.l_per_mmole,
            constant=True,
            name="conversion rate for plasma vldlc into plasma ldlc",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
        """,
        ),
    ]
)

_m.rules.extend(
    [
        AssignmentRule(
            "ldlc_change",
            "(Cve_ldlc - ldlc_init) / ldlc_init",
            U.dimensionless,
            name="relative LDL-C reduction in plasma in [0,-1]",
        ),
        AssignmentRule(
            "v_cho_reference",
            "v_cho_ref / Mr_ldlc / conversion_min_per_day",
            unit=U.mmole_per_min,
            name="reference cholesterol turnover [mmole/min]",
        ),
        AssignmentRule(
            "ldlc_loss",
            "v_cho_reference * ldlc_loss_k",
            U.mmole_per_min,
            name="total loss of cholesterol",
            notes="""
        Baseline loss plus additional ldlc dependent loss
        """,
        ),
        AssignmentRule(
            "ldlc_diet",
            "v_cho_reference * ldlc_diet_k",
            U.mmole_per_min,
            name="total dietary cholesterol",
        ),
        AssignmentRule(
            "ldlc_utilization",
            "v_cho_reference * ldlc_utilization_Vmax * f_ldlc_utilization_Vmax",
            U.mmole_per_min,
            name="total utilized cholesterol",
        ),
    ]
)

_m.reactions.extend(
    [
        Reaction(
            sid="ldlc_net_consumption",
            name="whole-body net consumption of plasma LDL-C",
            equation="Cve_ldlc -> ",
            formula=(
                "(ldlc_utilization + ldlc_loss) * (1 dimensionless + Cve_ldlc/ldlc_consumption_Km) - ldlc_diet",  # This is default
                U.mmole_per_min,
            ),
            sboTerm=SBO.TRANSLOCATION_REACTION,
        ),
        Reaction(
            sid="vldlc_conversion",
            name="VLDL-C to LDL-C conversion",
            equation="Cve_vldlc -> Cve_ldlc",  # default
            formula=(
                "v_cho_reference * vldlc_conversion_k * Cve_vldlc",
                U.mmole_per_min,
            ),
            sboTerm=SBO.TRANSLOCATION_REACTION,
            notes="""VLDL particles are converted to LDL by loosing triglycerides.
            Assumption is that the cholesterol stays constant in the VLDL to LDL conversion.
            """,
        ),
    ]
)

# Unit conversions
_m.rules.extend(
    [
        AssignmentRule(
            "v_ldlc_net_consumption",
            "ldlc_net_consumption * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol net consumption [mg/day]",
        ),
        AssignmentRule(
            "v_vldlc_conversion",
            "vldlc_conversion * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma vldlc conversion into ldlc [mg/day]",
        ),
        AssignmentRule(
            "v_ldlc_utilization",  # if treshold reached more ldlc should be utilized
            "ldlc_utilization * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol net consumption [mg/day]",
        ),
        # FIXME: dietary uptake of LDL-C takes place in the intestine
        AssignmentRule(
            "v_ldlc_diet",
            "ldlc_diet * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol diet [mg/day]",
        ),
        AssignmentRule(
            "v_ldlc_loss",  # if treshold reached, the loss should be higher
            "ldlc_loss * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol loss [mg/day]",
        ),
    ]
)


# --------------------------------------------
# Transport & administration reactions
# --------------------------------------------
for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # --------------------
    # tissue distribution
    # --------------------
    if distributed(sdict):
        for cid in COMPARTMENTS_BODY:
            if cid not in ["ve", "ar", "li", "gu", "ki", "po", "hv"]:
                _m.reactions.append(
                    Reaction(
                        sid=f"transport_{cid}_{sid}",
                        name=f"transport {sname}",
                        formula=(
                            f"ftissue_{sid} * BW/BW_ref * "
                            f"(C{cid}_plasma_{sid} - C{cid}_{sid} / Kp_{sid})",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} <-> C{cid}_{sid}",
                        compartment=f"V{cid}_tissue",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                )

    if "IVDOSE" in sdict:
        _m.reactions.extend(
            [
                # --------------------
                # iv application
                # --------------------
                Reaction(
                    sid=f"iv_{sid}",
                    name=f"iv {sname}",
                    formula=(f"Ki_{sid}*IVDOSE_{sid}/Mr_{sid}", U.mmole_per_min),
                    equation=f"-> Cve_{sid}",
                    compartment="Vve",
                    sboTerm=SBO.TRANSPORT_REACTION,
                ),
            ]
        )

    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in ["ve", "ar", "po", "hv"]:
            continue
        # --------------------
        # ve -> lung -> ar
        # --------------------
        if cid == "lu":
            rid_in = f"Flow_ve_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"

            rid_out = f"Flow_{cid}_ar_{sid}"
            name_out = f"outflow {cname} {sname}"

            # distribution in plasma volume
            _m.reactions.extend(
                [
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Cve_{sid}", U.mmole_per_min),
                        equation=f"Cve_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Car_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> organ -> ve
        # --------------------
        if cid in ["ki", "re"]:
            rid_in = f"Flow_ar_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"
            rid_out = f"Flow_{cid}_ve_{sid}"
            name_out = f"outflow {cname} {sname}"

            # only distribution in plasma volume
            _m.reactions.extend(
                [
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Cve_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> organ -> po
        # --------------------
        if cid in ["gu", "sp", "pa"]:
            rid_in = f"Flow_ar_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"
            rid_out = f"Flow_{cid}_po_{sid}"
            name_out = f"outflow {cname} {sname}"

            _m.reactions.extend(
                [
                    # only distribution in plasma volume
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Cpo_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> li
        # po -> li
        # li -> hv -> ve
        # --------------------
        if cid == "li":
            # liver

            _m.reactions.extend(
                [
                    Reaction(
                        sid=f"Flow_ar_li_{sid}",
                        name=f"inflow liver {sname}",
                        formula=(f"Qha*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> Cli_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_po_li_{sid}",
                        name=f"outflow po {sname}",
                        formula=(f"Qpo*Cpo_{sid}", U.mmole_per_min),
                        equation=f"Cpo_{sid} -> Cli_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_li_hv_{sid}",
                        name=f"outflow liver {sname}",
                        formula=(f"Qh*Cli_plasma_{sid}", U.mmole_per_min),
                        equation=f"Cli_plasma_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_hv_ve_{sid}",
                        name=f"outflow hepatic vein {sname}",
                        formula=(f"Qh*Chv_{sid}", U.mmole_per_min),
                        equation=f"Chv_{sid} -> Cve_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )

# -------------------------------------------------------------------------------------
# RateRules (Dissolution & Absorption)
# -------------------------------------------------------------------------------------
_m.rate_rules = []

for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]
    if "PODOSE" in sdict:
        # Dissolution and absorption
        _m.parameters.extend(
            [
                Parameter(
                    f"PODOSE_{sid}",
                    sdict["PODOSE"],
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    annotations=[(BQB.IS, "ncit/C38288")],
                ),
                # dissolution
                Parameter(
                    f"Ka_dis_{sid}",
                    **value_of(f"Ka_dis_{sid}", sdict["Ka_dis"], U.per_hr),
                    constant=True,
                    name=f"Ka_dis [1/hr] dissolution {sid}",
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                ),
            ]
        )

        # -------------------------------------
        # Dissolution of tablet/dose in stomach
        # -------------------------------------
        _m.reactions.extend(
            [
                # fraction dose available for absorption from stomach
                Reaction(
                    sid=f"dissolution_{sid}",
                    name=f"dissolution {sname}",
                    formula=(
                        f"Ka_dis_{sid}/60 min_per_hr * PODOSE_{sid}/Mr_{sid}",
                        U.mmole_per_min,
                    ),
                    equation=f"Astomach_{sid} -> Cgulumen_{sid}",
                    compartment="Vgu",
                ),
            ]
        )
        _m.rate_rules.extend(
            [
                # absorption of dose
                # d(PODOSE)/dt = -k_dis
                RateRule(
                    f"PODOSE_{sid}", f"-dissolution_{sid} * Mr_{sid}", U.mg_per_min
                ),
            ]
        )

    if "IVDOSE" in sdict:
        _m.rate_rules.extend(
            [
                # injection of dose
                RateRule(
                    f"IVDOSE_{sid}", f"-iv_{sid}*Mr_{sid} + Ri_{sid}", U.mg_per_min
                ),
                # cumulative infusion dose
                RateRule(f"cum_dose_{sid}", f"Ri_{sid}", U.mg_per_min),
            ]
        )

model_body = _m

if __name__ == "__main__":
    from pkdb_models.models.simvastatin import MODEL_BASE_PATH

    result: FactoryResult = create_model(
        model=model_body,
        filepath=MODEL_BASE_PATH / f"{model_body.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
