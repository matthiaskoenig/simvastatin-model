"""Pharmacokinetic parameters of simvastatin and simvastatin acid.

The pharmacokinetic parameters are the non-compartmental analysis of
`pkpdutils`, named like the variables of its `NCAResult` (e.g. `auc_last`,
`auc_inf_obs`, `cmax`, `tmax`, `thalf`, `lambda_z`, `cl_f`, `vz_f`), with the
unit of every parameter in `<name>_unit`, for simvastatin, simvastatin acid
and the simvastatin metabolites in venous plasma (`[Cve_<id>]`). The dose is
the oral dose of simvastatin (`PODOSE_simva`), so the clearance and the volume
of simvastatin are the apparent ones (`cl_f`, `vz_f`). Simvastatin acid is
formed from the prodrug simvastatin and the metabolites from both: they have
no dose of their own and only the parameters which need no dose. The
concentrations below `LLOQ_FRACTION` of the maximum are below the limit of
quantification, so that the noise of the integrator is not the terminal phase.

The parameters are calculated for every simulation of a scan or for the
result of a single simulation, with the times in hours and the concentrations
in nmol/l. A scan has at most one dimension besides the draws of the fitted
parameters, which a run over them (`run_simulation
pkdb_models.models.simvastatin --uncertainty`) adds; the rows have the
position of their point along the dimension of the scan (`point`) and of the
draw (`draw`), see `summarize`.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame
from pkpdsim.scan import point_timecourse, scan_dimensions, start_values
from pkpdutils import Dose, Route, Timecourse, Timecourses, nca
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.units import Quantity

if TYPE_CHECKING:
    from pkdb_models.models.simvastatin.experiments.base_experiment import (
        SimvastatinSimulationExperiment,
    )

#: oral dose of simvastatin
DOSE = "PODOSE_simva"
#: the substances by id of the concentration in venous plasma (`[Cve_<id>]`)
SUBSTANCES: dict[str, str] = {
    "simva": "simvastatin",
    "simacid": "simvastatin acid",
    "simmets": "simvastatin metabolites",
}
#: the substance the dose is given of, the others are formed from it
DOSED_SUBSTANCE = "simva"
#: units of the times and the concentrations of the analysis
TIME_UNIT = "hr"
CONCENTRATION_UNIT = "nmol/l"
#: the limit of quantification relative to the maximal concentration
LLOQ_FRACTION = 1e-4


def pk_selections(substances: Iterable[str]) -> list[str]:
    """Get the selections the pharmacokinetic parameters of substances read.

    An experiment with large scans which uses nothing else records only these.

    Args:
        substances: ids of the substances, keys of `SUBSTANCES`.

    Returns:
        The time, the oral dose of simvastatin and the concentrations of the
        substances in venous plasma.
    """
    return ["time", DOSE, *(f"[Cve_{sid}]" for sid in substances)]


def _rows(
    df: pd.DataFrame, xres: ScanResult, across: str | None, **columns: object
) -> pd.DataFrame:
    """Get the rows of the analysis of a result, in the order of the simulations.

    A single simulation has no dimension (`point` 0), a scan at most one
    besides the draws `across`; its position is the column `point`, the
    position of the draw the column `draw`, followed by the `columns` (e.g.
    the substance, a value or a value per row of `df`); the rows are ordered
    by the point and then the draw.

    Raises:
        ValueError: if the scan has more than one dimension besides the draws.
    """
    dims = scan_dimensions(xres, across) if xres.dims else []
    if len(dims) > 1:
        raise ValueError(
            f"A scan of at most one dimension is required, not of {dims} "
            f"(draws: {across})."
        )
    names = {
        **dict.fromkeys(dims, "point"),
        **({across: "draw"} if across is not None else {}),
    }
    df = df.rename(columns=names).assign(**columns)
    if not dims:
        df.insert(0, "point", 0)
    positions = ["point", *(["draw"] if across is not None else [])]
    df = df.sort_values(positions, kind="stable", ignore_index=True)
    leading = [*positions, *columns]
    return df[[*leading, *(c for c in df.columns if c not in leading)]]


def dose_simvastatin(xres: ScanResult, point: dict[str, int] | None = None) -> Quantity:
    """Get the oral dose of simvastatin of a simulation as a mass.

    `PODOSE_simva` is the amount which is not yet absorbed, the dose is its
    value at the start of the simulation.

    Args:
        xres: result of the simulation or of the scan.
        point: position of the simulation along the dimensions of the scan,
            none for a single simulation.
    """
    point = point or {}
    return Q(start_values(xres.isel(**point), DOSE).item(), xres.units[DOSE])


def pk_timecourse(
    xres: ScanResult,
    sid: str,
    mr_simva: Quantity,
    point: dict[str, int] | None = None,
) -> Timecourse:
    """Get the timecourse of a substance in venous plasma for the analysis.

    The timecourse has the state after a change at its time
    (`pkpdsim.scan.point_timecourse`).

    Args:
        xres: result of the simulation or of the scan.
        sid: id of the substance, a key of `SUBSTANCES`.
        mr_simva: molecular weight of simvastatin, for the dose in mmole.
        point: position of the simulation along the dimensions of the scan,
            none for a single simulation.

    Returns:
        The timecourse in `TIME_UNIT` and `CONCENTRATION_UNIT`, with the oral
        dose of simvastatin for simvastatin and without a dose otherwise, and
        the limit of quantification `LLOQ_FRACTION` of the maximum.
    """
    point = point or {}
    units = xres.units

    # the dose in the substance unit of the concentration, which `cl_f` and
    # `vz_f` require
    dose: Dose | None = None
    if sid == DOSED_SUBSTANCE:
        amount = (dose_simvastatin(xres, point) / mr_simva).to("mmole")
        dose = Dose(amount=amount.magnitude, unit="mmol", route=Route.ORAL)

    concentration = f"[Cve_{sid}]"
    times, values = point_timecourse(xres, concentration, **point)
    time = Q(times, units["time"]).to(TIME_UNIT)
    value = np.asarray(Q(values, units[concentration]).to(CONCENTRATION_UNIT).magnitude)
    cmax = float(value.max())
    return Timecourse(
        time=np.asarray(time.magnitude),
        value=value,
        time_unit=TIME_UNIT,
        unit=CONCENTRATION_UNIT,
        lloq=LLOQ_FRACTION * cmax if cmax > 0 else None,
        dose=dose,
        substance=SUBSTANCES[sid],
    )


def pk_parameters(
    xres: ScanResult,
    sid: str,
    mr_simva: Quantity,
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of a substance in every simulation.

    The non-compartmental analysis of all simulations at once, of the
    timecourses of `pk_timecourse` (the times in `TIME_UNIT`, the
    concentrations in `CONCENTRATION_UNIT`, the dose of simvastatin for
    simvastatin and the limit of quantification `LLOQ_FRACTION` of the
    maximum).

    Args:
        xres: result of the simulation or of the scan.
        sid: id of the substance, a key of `SUBSTANCES`.
        mr_simva: molecular weight of simvastatin, for the dose in mmole.
        across: the dimension of the draws of the fitted parameters, `None`
            for a result without draws.

    Returns:
        One row per simulation with its position (`point`, and `draw` with
        draws), the id of the substance (`substance`), the oral dose of
        simvastatin (`dose`) and the parameters with their units
        (`<name>_unit`).
    """
    units = xres.units
    dose_mass = Q(start_values(xres, DOSE).values, units[DOSE])
    concentration = f"[Cve_{sid}]"
    ds = xres.to_timecourses(concentration).ds
    values = ds["value"].values
    time = ds["times"].values if "times" in ds else ds["time"].values
    dims = tuple(xres.dims)
    timecourses = Timecourses.from_arrays(
        Q(time, units["time"]).to(TIME_UNIT).magnitude,
        Q(values, units[concentration]).to(CONCENTRATION_UNIT).magnitude,
        time_unit=TIME_UNIT,
        unit=CONCENTRATION_UNIT,
        dims=dims,
        coords={dim: ds[dim].values for dim in dims} or None,
        # the dose in the substance unit of the concentration, which `cl_f`
        # and `vz_f` require
        dose=(
            {"amount": (dose_mass / mr_simva).to("mmole").magnitude, "unit": "mmol"}
            if sid == DOSED_SUBSTANCE
            else None
        ),
        route=Route.ORAL if sid == DOSED_SUBSTANCE else None,
        substance=SUBSTANCES[sid],
    )
    value = timecourses.ds["value"]
    cmax = value.max(dim=[d for d in value.dims if d not in dims])
    lloq = (LLOQ_FRACTION * cmax).where(cmax > 0)
    result = nca(Timecourses(timecourses.ds.assign(lloq=lloq)))

    df = nca_frame(result).drop(columns="nca_flags")
    position = tuple(df[dim].to_numpy() for dim in dims)
    dose = dose_mass.to("mg")
    return _rows(
        df,
        xres,
        across,
        substance=sid,
        dose=np.reshape(np.asarray(dose.magnitude)[position], -1),
        dose_unit=str(dose.units),
    )


def calculate_simvastatin_pk(
    experiment: SimvastatinSimulationExperiment,
    xres: ScanResult,
    substances: tuple[str, ...] = ("simva", "simacid"),
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a result.

    Args:
        experiment: experiment of the simulations, for the molecular weight.
        xres: result of a scan with at most one dimension besides the draws or
            of a single simulation.
        substances: ids of the substances, keys of `SUBSTANCES`.
        across: the dimension of the draws of the fitted parameters, `None`
            for a result without draws.

    Returns:
        One row per substance and simulation, with its position (`point`, and
        `draw` with draws), the simulations of a substance in the order of the
        scan.
    """
    return pd.concat(
        [pk_parameters(xres, sid, experiment.Mr.simva, across) for sid in substances],
        ignore_index=True,
    )


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters of one substance with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
