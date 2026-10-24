"""Collect the data of the simvastatin and cholesterol studies from the PK-DB study folders.

The studies are copied from a `pkdb_data` checkout (`PKDB_DATA`, else
`../pkdb_data`, see `pkpdsim.data.studies_dir`) into the data folder of the
model, see `pkpdsim.data.collect_tsv_files`.
Besides the simvastatin studies, the cholesterol studies are collected, the
studies of the lipid lowering effect of statins on the LDL cholesterol.
"""

from pathlib import Path

from pkpdsim.data import collect_tsv_files
from pkpdsim.data import studies_dir as pkdb_studies_dir

from pkdb_models.models.simvastatin import (
    DATA_PATH_CHOLESTEROL,
    DATA_PATH_SIMVASTATIN,
)


def is_study(study_name: str) -> bool:
    """Exclude the template of the curation, which is no study."""
    return study_name != "template"


def collect_data(studies_dir: Path | None = None) -> None:
    """Copy the data of the simvastatin and cholesterol studies into the data folder.

    Args:
        studies_dir: the `studies` folder of pkdb_data, by default the one of
            the checkout `pkpdsim.data.studies_dir` finds.
    """
    if studies_dir is None:
        studies_dir = pkdb_studies_dir()
    DATA_PATH_SIMVASTATIN.parent.mkdir(exist_ok=True)
    collect_tsv_files(
        source_dir=studies_dir / "simvastatin",
        target_dir=DATA_PATH_SIMVASTATIN,
        filter_study=is_study,
    )
    collect_tsv_files(
        source_dir=studies_dir / "cholesterol",
        target_dir=DATA_PATH_CHOLESTEROL,
        filter_study=is_study,
    )


if __name__ == "__main__":
    collect_data()
