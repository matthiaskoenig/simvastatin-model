"""Base of the liver models of simvastatin and cholesterol.

The compartments of the liver and the species shared by the simvastatin and
the cholesterol part of the liver model.
"""

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    Compartment,
    Model,
    Species,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.simvastatin.models import annotations, templates


class U(templates.U):
    """UnitDefinitions."""


_m = Model(
    "simvastatin_liver_base",
    name="Model for base liver elements",
    notes="""
    # Liver base model
    Used in cholesterol and simvastatin model.
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        1,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vbaso",
        1,
        name="basolateral membrane",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        spatialDimensions=2,
        annotations=annotations.compartments["basolateral"],
    ),
    Compartment(
        "Vapical",
        np.nan,
        name="apical membrane",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        spatialDimensions=2,
        annotations=annotations.compartments["apical"],
    ),
    Compartment(
        "Vli",
        1.5,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["li"],
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
]

_m.species = [
    Species(
        sid="simacid",
        initialConcentration=0.0,
        name="simvastatin acid (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simacid"],
    ),
    Species(
        sid="simmets",
        initialConcentration=0.0,
        name="simvastatin metabolites (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["simmets"],
    ),
]

model_liver_base = _m

if __name__ == "__main__":
    from pkdb_models.models.simvastatin import MODEL_BASE_PATH

    result = create_model(
        model=model_liver_base,
        filepath=MODEL_BASE_PATH / f"{model_liver_base.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
