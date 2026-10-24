"""Templates of the simvastatin models: units, model units and creators."""

from pkpdsim.templates import creators as creators_generic
from sbmlutils.factory import Creator, ModelUnits, UnitDefinition, Units


class U(Units):
    """UnitDefinitions."""

    mmole = UnitDefinition("mmole")
    min = UnitDefinition("min")
    mg = UnitDefinition("mg")
    kg = UnitDefinition("kg", "kilogram")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")
    per_min = UnitDefinition("per_min", "1/min")
    per_hr = UnitDefinition("per_hr", "1/hr")
    per_min_l = UnitDefinition("per_min_l", "1/min/liter")
    m2 = UnitDefinition("m2", "meter^2")
    mM = UnitDefinition("mM", "mmole/liter")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_min_l = UnitDefinition("mmole_per_min_l", "mmole/min/liter")
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    l_per_min = UnitDefinition("l_per_min", "l/min")
    l_per_min_mmole = UnitDefinition("l_per_min_mmole", "l/min/mmole")
    l_per_min_kg = UnitDefinition("l_per_min_kg", "l/min/kg")


model_units = ModelUnits(
    time=U.min,
    extent=U.mmole,
    substance=U.mmole,
    length=U.meter,
    area=U.m2,
    volume=U.liter,
)


creators = [
    Creator(
        familyName="Bartsch",
        givenName="Florian",
        email="florian@mathiasbartsch.de",
        organization="Humboldt-University Berlin, Institute for Theoretical Biology",
    ),
    *creators_generic,
]
