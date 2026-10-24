[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5554092.svg)](https://doi.org/10.5281/zenodo.5554092)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/simvastatin-model)](https://github.com/matthiaskoenig/simvastatin-model/releases)
[![Documentation](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/simvastatin-model/)
[![CI](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/simvastatin-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/simvastatin?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/simvastatin)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of simvastatin

This repository provides the simvastatin physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model: the oral absorption of simvastatin, its first pass metabolism by CYP3A4 in the intestine and the liver, its hydrolysis to the active simvastatin acid, the hepatic uptake of the acid by OATP1B1, the enterohepatic circulation and excretion of the metabolites and the inhibition of the HMG-CoA reductase with the lowering of the LDL cholesterol.

Documentation: <https://matthiaskoenig.github.io/simvastatin-model/>

## Quick start

```bash
git clone https://github.com/matthiaskoenig/simvastatin-model.git && cd simvastatin-model
uv sync
uv run run_simulation pkdb_models.models.simvastatin --action all -r results
```

## How to cite

> Bartsch, F. & König, M. (2026). *Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of simvastatin*. Zenodo. https://doi.org/10.5281/zenodo.5554092

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2020-2026 Florian Bartsch and Matthias König
