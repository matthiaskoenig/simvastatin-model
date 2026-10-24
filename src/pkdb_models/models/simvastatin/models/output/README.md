[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5554092.svg)](https://doi.org/10.5281/zenodo.5554092)
[![GitHub Action](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/python.yml/badge.svg)](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/python.yml)
[![GitHub Action](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/docker.yml/badge.svg)](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/docker.yml)

# simvastatin model
This repository provides the simvastatin physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model: the oral absorption of simvastatin, its first pass metabolism by CYP3A4 in the intestine and the liver, its hydrolysis to the active simvastatin acid, the hepatic uptake of the acid by OATP1B1, the enterohepatic circulation and excretion of the metabolites and the inhibition of the HMG-CoA reductase with the lowering of the LDL cholesterol in the familial hypercholesterolemia (FH) types.

The model is distributed as [SBML](http://sbml.org) format available from [`simvastatin_body_flat.xml`](./models/simvastatin_body_flat.xml) with
corresponding [SBML4humans model report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fsimvastatin-model%2Fmain%2Fmodels%2Fsimvastatin_body_flat.xml) and [model equations](./models/simvastatin_body_flat.md).

The COMBINE archive is available from [`simvastatin_model.omex`](./simvastatin_model.omex).

### Comp submodels
* **liver** submodel [`simvastatin_liver.xml`](./models/simvastatin_liver.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fsimvastatin-model%2Fmain%2Fmodels%2Fsimvastatin_liver.xml) and [equations](./models/simvastatin_liver.md), composed of the metabolism of simvastatin [`simvastatin_liver_simvastatin.xml`](./models/simvastatin_liver_simvastatin.xml) ([equations](./models/simvastatin_liver_simvastatin.md)) and the cholesterol metabolism [`simvastatin_liver_cholesterol.xml`](./models/simvastatin_liver_cholesterol.xml) ([equations](./models/simvastatin_liver_cholesterol.md)) on the common base [`simvastatin_liver_base.xml`](./models/simvastatin_liver_base.xml) ([equations](./models/simvastatin_liver_base.md)).
* **kidney** submodel [`simvastatin_kidney.xml`](./models/simvastatin_kidney.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fsimvastatin-model%2Fmain%2Fmodels%2Fsimvastatin_kidney.xml) and [equations](./models/simvastatin_kidney.md).
* **intestine** submodel [`simvastatin_intestine.xml`](./models/simvastatin_intestine.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fsimvastatin-model%2Fmain%2Fmodels%2Fsimvastatin_intestine.xml) and [equations](./models/simvastatin_intestine.md).
* **whole-body** submodel [`simvastatin_body.xml`](./models/simvastatin_body.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fsimvastatin-model%2Fmain%2Fmodels%2Fsimvastatin_body.xml) and [equations](./models/simvastatin_body.md).

The severities of the FH types which give the baseline LDL cholesterol of a study are the calibration [`calibration_results.csv`](./calibration_results.csv).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5554092.svg)](https://doi.org/10.5281/zenodo.5554092)

> Bartsch, F. & König, M. (2026).
> *Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of simvastatin.*
> Zenodo. [https://doi.org/10.5281/zenodo.5554092](https://doi.org/10.5281/zenodo.5554092)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.


## Run simulations
### python
Clone the repository
```bash
git clone https://github.com/matthiaskoenig/simvastatin-model.git
cd simvastatin-model
```

#### uv
Run the complete analysis with uv (https://docs.astral.sh/uv/getting-started/installation/):
```bash
uv run run_simulation pkdb_models.models.simvastatin -a all -r results
```

#### pip
If you use pip install the package via
```bash
pip install -e .
```
Run the complete analysis in the environment via:
```bash
run_simulation pkdb_models.models.simvastatin -a all -r results
```

### docker
Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/simvastatin:latest /bin/bash
```

Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.simvastatin -a all -r /results
```
The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:
```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```

## Funding
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2020-2026 Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)
