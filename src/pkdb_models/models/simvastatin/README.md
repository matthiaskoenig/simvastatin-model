# Simvastatin

Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of the HMG-CoA reductase inhibitor simvastatin and the LDL cholesterol. The pharmacokinetics: the dissolution and absorption of the prodrug simvastatin (a lactone, 85 % absorbed), its first pass metabolism by CYP3A4 in the intestine and the liver, its hydrolysis by the hepatic esterases to the active simvastatin acid, the hepatic uptake of the acid by OATP1B1 and its metabolism by CYP3A4 and the glucuronidation, and the enterohepatic circulation and the biliary and renal excretion of the lumped metabolites. The model describes the interactions with inhibitors and inducers of CYP3A4 (in the gut and the liver separately, e.g. grapefruit juice in the gut only), of OATP1B1 and of the glucuronidation (gemfibrozil), the SLCO1B1 c.521T>C and CYP3A5 genotypes and the renal function. The pharmacodynamics: the active inhibitors in the liver (the acid and its active metabolites) inhibit the HMG-CoA reductase of the hepatic cholesterol synthesis, which raises the LDL receptor and lowers the plasma LDL cholesterol over weeks. The baseline LDL cholesterol of a study is the steady state of one of the familial hypercholesterolemia (FH) types, the defects of the LDL receptor pathway, with the calibrated severity of the type.

The published version of the model is [simvastatin-model](https://github.com/matthiaskoenig/simvastatin-model) ([doi:10.5281/zenodo.5554092](https://doi.org/10.5281/zenodo.5554092)).

## Structure

- `__init__.py`: the paths of the model and its model object `MODEL` with its release metadata and its adopted fits, which the commands below run (pkpdsim).
- `models/`: the tissue models (`model_intestine.py`, `model_kidney.py`, the liver `model_liver.py` composed of `model_liver_simvastatin.py` and `model_liver_cholesterol.py` on `model_liver_base.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated, the ODEs and the COMBINE archive in `models/output/`; the fitted values come from the adopted fits (`models/fits.py`, `models/output/fits/`). `models/output/calibration_results.csv` is the calibration of the severities of the FH types.
- `experiments/`: the simulation experiments of the clinical studies, the pharmacokinetics (`simvastatin/`) and the LDL cholesterol (`cholesterol/`), the scans of the FH types (`FH_experiments/`), the calibration of the FH types (`model_calibration/`), the tests of the cholesterol model (`modeltests/`) and the dose scan and the pharmacokinetic parameters (`pk/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`.
- `fitting/`: the fit problems of the pharmacokinetics (`PK`) and of the LDL cholesterol on the adopted pharmacokinetics (`PD`), their parameters and the selection of the training, validation and outlier data.
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics and of the inhibition of the HMG-CoA reductase.
- `simvastatin_pk.py`: the pharmacokinetic parameters of the scans, the non-compartmental analysis of `pkpdutils`.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`).
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.simvastatin --action factory
run_simulation pkdb_models.models.simvastatin --action list_experiments
run_simulation pkdb_models.models.simvastatin --action simulate --experiments all
run_simulation pkdb_models.models.simvastatin --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.simvastatin --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.simvastatin --subset=PD --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.simvastatin --adopt PK_<fit id>
run_report pkdb_models.models.simvastatin --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.simvastatin --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.simvastatin.sensitivity.sensitivity_analysis

# calibration of the FH types (replaces models/output/calibration_results.csv)
python pkdb_models/models/simvastatin/experiments/model_calibration/fh_calibration.py
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fits of the model,
not from numbers in the code. `run_fit pkdb_models.models.simvastatin --adopt <fit id>`
copies the record of a finished fit (its parameters, problem, profile
likelihood and Fisher information) into `models/output/fits/<fit id>/`, which is
tracked; the ids of the adopted fits are listed in `fits` of the model object
(`__init__.py`). The factory takes the fitted values and their uncertainty from
the records (`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`. The
scans of the FH types, the calibration and the tests of the cholesterol model
run once with the fitted values (`fitted_changes` of the base experiment): the
draws would multiply simulations of years for no band. The PD fit runs on the
adopted PK fit: a refit of the pharmacokinetics is followed by a refit of the
LDL cholesterol. A refit is: fit, adopt, replace the id in `fits`, rebuild the
model. See the documentation of the repository on fitting (`docs/fitting.md`).
