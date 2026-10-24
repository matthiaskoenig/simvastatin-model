# Release notes

## Release notes for simvastatin-model 0.10.0

Made from pkdb_models 3a0b49144b with pkpdsim 0.11.0.

The changes since 0.9.1.

### Core libraries

The versions of the core libraries cannot be compared, there is no lock file in the previous release. The release uses:

- pkpdsim 0.11.0
- sbmlsim 0.13.0
- sbmlutils 0.17.0

### Libraries

The versions cannot be compared, there is no lock file in the previous release.

### Data

- Added: `cholesterol/Crouse1999`, `cholesterol/Davidson1997`, `cholesterol/Geiss2002`, `cholesterol/Isaacsohn2003`, `cholesterol/Jones1998a`, `cholesterol/Keech1994`, `cholesterol/Kosoglou2002`, `cholesterol/Li2003`, `cholesterol/Loria1993`, `cholesterol/Moelgaard1988`, `cholesterol/Mol1986`, `cholesterol/Mol1988`, `cholesterol/Ntanios1999`, `cholesterol/Owens1991`, `cholesterol/Pietro1989`, `cholesterol/Recto2000`, `cholesterol/Saito1991`, `cholesterol/Sivkov2021`, `cholesterol/Stern2000`, `cholesterol/Tuomilehto1995`, `cholesterol/Walker1990`, `simvastatin/Backman2000`, `simvastatin/Bergman2004`, `simvastatin/Cheng1992`, `simvastatin/Cheng1994`, `simvastatin/Chung2006`, `simvastatin/Gehin2015`, `simvastatin/Harvey2018`, `simvastatin/Hsyu2001`, `simvastatin/Jacobson2004`, `simvastatin/Jiang2017`, `simvastatin/Kantola1998`, `simvastatin/Keskitalo2008`, `simvastatin/Keskitalo2009`, `simvastatin/Kim2007`, `simvastatin/Kim2019`, `simvastatin/Kyrklund2000`, `simvastatin/Lilja1998`, `simvastatin/Lilja2000`, `simvastatin/Lilja2004`, `simvastatin/Lohitnavy2004`, `simvastatin/Marino2000`, `simvastatin/Mousa2000`, `simvastatin/Najib2003`, `simvastatin/Neuvonen1998`, `simvastatin/Nishio2005`, `simvastatin/OBrien2003`, `simvastatin/Pasanen2006`, `simvastatin/Pentikainen1992`, `simvastatin/Prueksaritanont2001`, `simvastatin/Simard2001`, `simvastatin/Sugimoto2001`, `simvastatin/TubicGrozdanis2008`, `simvastatin/Ucar2004`, `simvastatin/Watanabe2004`, `simvastatin/Zhi2003`, `simvastatin/Zhou2013`, `simvastatin/Ziviani2001`

### Analysis

#### Models

- `simvastatin_body.xml`: added 1 species, 8 parameters; removed 8 parameters; changed values `Ka_dis_simva` 0.358189 → 0.603596, `ftissue_simacid` 38.5622 → 10, `ftissue_simva` 0.150167 → 1.37428, `ldlc_utilization_Vmax` 0.95 → 0.652143, `simmets_inhibitor_activity` 0.5 → 0.4
- `simvastatin_body_flat.xml`: added 1 species, 4 reactions, 29 parameters; removed 1 reaction, 20 parameters; changed values `GU__F_abs_simmets` 0.269059 → 0.536, `GU__F_abs_simva` 1 → 0.85, `GU__SIMMETSABS_k` 0.022453 → 0.226, `GU__SIMVAABS_k` 1.5088 → 1.29, `Ka_dis_simva` 0.358189 → 0.603596, `LI__EHC_simmets_k` 3.11377 → 3.02803, `LI__HMGCOAREDUCTASE_Ki_simacid` 1.5e-06 → 9.16748e-07, `ftissue_simacid` 38.5622 → 10, `ftissue_simva` 0.150167 → 1.37428, `ldlc_utilization_Vmax` 0.95 → 0.652143, `simmets_inhibitor_activity` 0.5 → 0.4
- `simvastatin_intestine.xml`: added 1 species, 1 reaction, 6 parameters; removed 6 parameters; changed values `F_abs_simmets` 0.269059 → 0.536, `F_abs_simva` 1 → 0.85, `SIMMETSABS_k` 0.022453 → 0.226, `SIMVAABS_k` 1.5088 → 1.29
- `simvastatin_kidney.xml`: added 1 reaction, 5 parameters; removed 1 reaction, 1 parameter
- `simvastatin_liver.xml`: added 2 reactions, 15 parameters; removed 7 parameters; changed values `EHC_simmets_k` 3.11377 → 3.02803, `HMGCOAREDUCTASE_Ki_simacid` 1.5e-06 → 9.16748e-07, `simmets_inhibitor_activity` 0.5 → 0.4
- `simvastatin_liver_base.xml`: changed, with the same species, reactions and parameter values
- `simvastatin_liver_cholesterol.xml`: added 1 parameter; changed values `HMGCOAREDUCTASE_Ki_simacid` 1.5e-06 → 9.16748e-07, `simmets_inhibitor_activity` 0.5 → 0.4
- `simvastatin_liver_simvastatin.xml`: added 2 reactions, 14 parameters; removed 7 parameters; changed values `EHC_simmets_k` 3.11377 → 3.02803

#### Experiments

- Added: `Backman2000`, `Bergman2004`, `CholesterolBodyTestExperiment`, `CholesterolLiverTestExperiment`, `Chung2006`, `Crouse1999`, `Davidson1997`, `FHCalibration`, `FH_scan_simulation`, `FH_scans`, `FH_scans_3D`, `FH_testexperiments`, `FH_timecourses`, `Gehin2015`, `Geiss2002`, `Harvey2018`, `Hsyu2001`, `Isaacsohn2003`, `Jacobson2004`, `Jiang2017`, `Jones1998a`, `Kantola1998`, `Keech1994`, `Keskitalo2008`, `Keskitalo2009`, `Kim2007`, `Kim2019`, `Kosoglou2002`, `Kyrklund2000`, `LDLCUtilizationCalibration`, `Li2003`, `Lilja1998`, `Lilja2000`, `Lilja2000_2004`, `Lilja2004`, `Lohitnavy2004`, `Loria1993`, `Marino2000`, `Moelgaard1988`, `Mol1986`, `Mol1988`, `Mousa2000`, `Najib2003`, `Neuvonen1998`, `Nishio2005`, `Ntanios1999`, `OBrien2003`, `Owens1991`, `PKParameter`, `PKScanExperiment`, `Pasanen2006`, `Pentikainen1992`, `Pietro1989`, `Prueksaritanont2001`, `Recto2000`, `Saito1991`, `Simard2001`, `Sivkov2021`, `Sugimoto2001`, `TubicGrozdanis2008`, `Tuomilehto1995`, `Ucar2004`, `Walker1990`, `Zhi2003`, `Zhou2013`, `Ziviani2001`, `modeltest`

#### Fits

- `PD`: `PD_20261020_133635__e8729`, no fit record in the previous release
- `PK`: `PK_20261020_132206__ce0a9`, no fit record in the previous release

## Release notes for simvastatin-model 0.9.1

We are pleased to release a new version of the simvastatin-model including the 
following changes:

### Features
- renaming transporters for clarification
- updated parameter values

Your simvastatin-model team

## Release notes for simvastatin-model 0.9.0

We are pleased to release a new version of the simvastatin-model including the 
following changes:

### Features
- refitted parameters
- updated whole-body

Your simvastatin-model team

## Release notes for simvastatin-model 0.7.0

We are pleased to release a new version of the simvastatin-model including the 
following changes:

### Features
- sbml4humans report
- model annotations
- zenodo integration

Your simvastatin-model team

