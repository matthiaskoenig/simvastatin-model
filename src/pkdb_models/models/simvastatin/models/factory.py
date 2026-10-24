"""Simvastatin model factory."""

from pathlib import Path
from typing import Any

from pkpdsim.licenses import License, write_license
from pymetadata.omex import EntryFormat, ManifestEntry, Omex
from sbmlode import OdeSystem
from sbmlutils.comp import flatten_sbml
from sbmlutils.factory import create_model

from pkdb_models.models.simvastatin import MODEL_BASE_PATH
from pkdb_models.models.simvastatin.models.model_body import model_body
from pkdb_models.models.simvastatin.models.model_intestine import model_intestine
from pkdb_models.models.simvastatin.models.model_kidney import model_kidney
from pkdb_models.models.simvastatin.models.model_liver import model_liver
from pkdb_models.models.simvastatin.models.model_liver_base import model_liver_base
from pkdb_models.models.simvastatin.models.model_liver_cholesterol import (
    model_liver_cholesterol,
)
from pkdb_models.models.simvastatin.models.model_liver_simvastatin import (
    model_liver_simvastatin,
)


def create_simvastatin_models(model_output_dir: Path) -> dict[str, dict[str, Any]]:
    """Create the tissue models and the whole-body model of simvastatin.

    Args:
        model_output_dir: directory of the models, the COMBINE archive and the
            license texts are written into its parent.

    Returns:
        The files of the model with their entries in the COMBINE archive.
    """
    model_output_dir.mkdir(parents=True, exist_ok=True)
    output_dir = model_output_dir
    results: dict[str, dict[str, Any]] = {
        "README": {
            "path": MODEL_BASE_PATH.parent / "README.md",
            "entry": ManifestEntry(
                location="./README.md",
                format=EntryFormat.MARKDOWN,
                master=False,
            ),
        },
        "cc-by": {
            "path": write_license(model_output_dir.parent, License.CC_BY_SA_4_0),
            "entry": ManifestEntry(
                location="./cc-by-sa-4.0.txt",
                format=EntryFormat.TXT,
                master=False,
            ),
        },
        "mit": {
            "path": write_license(
                model_output_dir.parent,
                License.MIT,
                copyright="2020-2026 Matthias König",
            ),
            "entry": ManifestEntry(
                location="./mit.txt",
                format=EntryFormat.TXT,
                master=False,
            ),
        },
    }

    # create tissue and body models
    for models in [
        (model_intestine,),
        (model_kidney,),
        (model_liver_base,),
        (
            model_liver_base,
            model_liver_simvastatin,
            model_liver_cholesterol,
            model_liver,
        ),
        # isolated models
        (
            model_liver_base,
            model_liver_simvastatin,
        ),
        (
            model_liver_base,
            model_liver_cholesterol,
        ),
        (model_body,),
    ]:
        # the models are merged into the last one
        model_sid = models[-1].sid
        factory_results = create_model(
            filepath=output_dir / f"{model_sid}.xml",
            model=models,
            sbml_level=3,
            sbml_version=2,
        )
        sbml_path = factory_results.sbml_path
        results[model_sid] = {
            "path": sbml_path,
            "entry": ManifestEntry(
                location=f"./models/{sbml_path.name}",
                format=EntryFormat.SBML_L3V2,
                master=False,
            ),
        }

        # create differential equations
        md_path = output_dir / f"{model_sid}.md"
        ode_system = OdeSystem.from_sbml(sbml_path)
        ode_system.write(md_path)
        results[f"{model_sid}_md"] = {
            "path": md_path,
            "entry": ManifestEntry(
                location=f"./models/{md_path.name}",
                format=EntryFormat.MARKDOWN,
                master=False,
            ),
        }

    # create whole-body model
    sbml_path = results["simvastatin_body"]["path"]
    sbml_path_flat = output_dir / f"{sbml_path.stem}_flat.xml"
    flatten_sbml(sbml_path, sbml_flat_path=sbml_path_flat)

    results["simvastatin_body_flat"] = {
        "path": sbml_path_flat,
        "entry": ManifestEntry(
            location=f"./models/{sbml_path_flat.name}",
            format=EntryFormat.SBML_L3V2,
            master=True,
        ),
    }

    # create differential equations
    md_path = output_dir / f"{model_body.sid}_flat.md"
    ode_system = OdeSystem.from_sbml(sbml_path_flat)
    ode_system.write(md_path)
    results[f"{model_body.sid}_flat_md"] = {
        "path": md_path,
        "entry": ManifestEntry(
            location=f"./models/{md_path.name}",
            format=EntryFormat.MARKDOWN,
            master=False,
        ),
    }

    # create omex
    omex = Omex()
    for info in results.values():
        omex.add_entry(entry_path=info["path"], entry=info["entry"])
    omex.to_omex(omex_path=model_output_dir.parent / "simvastatin_model.omex")

    return results


if __name__ == "__main__":
    # create the models
    # The FH calibration (`calibration_results.csv` in the results of the
    # models, the disease severity for given LDL-C plasma concentrations) is
    # not created by the factory; after a change of the model it is updated by
    # `experiments/model_calibration/fh_calibration.py`.
    create_simvastatin_models(MODEL_BASE_PATH)
