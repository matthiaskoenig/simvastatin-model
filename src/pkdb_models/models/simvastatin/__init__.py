"""Simvastatin: PBPK/PD model of simvastatin and the LDL cholesterol.

The paths of the model and its model object `MODEL`, which the commands
`run_simulation`, `run_fit`, `run_report` and `run_identifiability` of pkpdsim
run by its package `pkdb_models.models.simvastatin`.
"""

from pathlib import Path

from pkpdsim.model import FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

from pkdb_models.models.simvastatin.tolerances import ABSOLUTE_TOLERANCE

SIMVASTATIN_PATH = Path(__file__).parent

MODEL_BASE_PATH = SIMVASTATIN_PATH / "models" / "output" / "models"
MODEL_PATH = MODEL_BASE_PATH / "simvastatin_body_flat.xml"
#: the calibration of the severities of the familial hypercholesterolemia (FH)
#: types, read by the presimulations of the cholesterol experiments and updated
#: with `update_fh_calibration` (`experiments/model_calibration/fh_calibration.py`)
FH_CALIBRATION_PATH = MODEL_BASE_PATH.parent / "calibration_results.csv"

DATA_PATH_BASE = SIMVASTATIN_PATH / "data"
DATA_PATH_SIMVASTATIN = DATA_PATH_BASE / "simvastatin"
DATA_PATH_CHOLESTEROL = DATA_PATH_BASE / "cholesterol"
DATA_PATHS = [
    DATA_PATH_SIMVASTATIN,
    DATA_PATH_CHOLESTEROL,
]

MODEL = PKPDModel(
    name="simvastatin",
    package=__name__,
    title="Simvastatin PBPK/PD model",
    path=SIMVASTATIN_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH.parent / "simvastatin_model.omex",
    factory=".models.factory:create_simvastatin_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    # the adopted fits, whose values the factory takes (`models/fits.py`)
    fits=("PK_20261020_132206__ce0a9", "PD_20261020_133635__e8729"),
    simulator=SimulatorSettings(
        absolute_tolerance=ABSOLUTE_TOLERANCE, relative_tolerance=1e-10
    ),
    figures=FigureSettings(
        formats=("svg",), panel_width=8.5, panel_height=5, fig_titlesize=15
    ),
    # the release of the model repository
    release=ReleaseSettings(
        title=(
            "Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) "
            "model of simvastatin"
        ),
        repository="matthiaskoenig/simvastatin-model",
        doi="10.5281/zenodo.5554092",
        authors=(
            Author(
                "Bartsch, Florian",
                "0000-0002-8285-9964",
                "Humboldt-University Berlin, Institute for Theoretical Biology",
            ),
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
        ),
        keywords=(
            "model",
            "simvastatin",
            "simvastatin acid",
            "statin",
            "HMG-CoA reductase inhibitor",
            "cholesterol",
            "LDL cholesterol",
            "pharmacokinetics",
            "pharmacodynamics",
            "PBPK",
            "physiologically based pharmacokinetic model",
            "SBML",
        ),
        docker_image="matthiaskoenig/simvastatin",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the simvastatin physiologically based"
            " pharmacokinetic/pharmacodynamic (PBPK/PD) model: the oral"
            " absorption of simvastatin, its first pass metabolism by CYP3A4"
            " in the intestine and the liver, its hydrolysis to the active"
            " simvastatin acid, the hepatic uptake of the acid by OATP1B1, the"
            " enterohepatic circulation and excretion of the metabolites and"
            " the inhibition of the HMG-CoA reductase with the lowering of the"
            " LDL cholesterol."
        ),
        first_year=2020,
    ),
)
"""The simvastatin model: its commands, see `pkpdsim.model`."""
