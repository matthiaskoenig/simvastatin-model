"""The tolerances of the integrator for the simvastatin model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(value: float, species: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the simvastatin model.

    Simvastatin is dosed in mg, about 0.1 mmole: the plasma concentrations of
    simvastatin and simvastatin acid are 1e-5 mM and below, the concentrations
    of the cholesterol part 1e-3 - 10 mM. The species get an absolute
    tolerance of the scale of the pharmacokinetics, the other states (the
    oral and intravenous dose and the cumulative dose, which are rate rules in
    mg) `value`. With the tolerance of the fits for all states (1e-6) the
    plasma concentrations of simvastatin differed by 1e-3 from the tight
    integration, with 1e-10 for the species by 2e-5.

    Args:
        value: tolerance of every other state.
        species: tolerance of the amounts and concentrations of the species.

    Returns:
        The absolute tolerance per kind of state.
    """
    return AbsoluteTolerance(amount=species, concentration=species, other=value)


#: the absolute tolerance of the simulation experiments
ABSOLUTE_TOLERANCE = absolute_tolerance(1e-10, species=1e-10)
