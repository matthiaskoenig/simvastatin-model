"""Parameters to optimize in the simvastatin fits.

The start values were tuned by hand to the pharmacokinetics of the
literature (40 mg simvastatin: Cmax about 8 ng/ml, AUC about 28 ng*h/ml and
half-life about 4.5 h of simvastatin; Cmax about 2.4 ng/ml, tmax about 4 h and
AUC about 20 ng*h/ml of simvastatin acid; the ratios of the interactions); the
model takes the fitted values from the adopted fit (`models/fits.py`). Not
fitted, with the reason:

- the intestinal availability (`GU__SIMVA_CYP3A4_Vmax`, `GU__SIMVAEXP_Vmax`):
  about 0.28 from regular grapefruit juice, an inhibitor of the intestinal
  CYP3A4 only (simvastatin AUC 3.6-fold, Lilja2004); the control data do not
  separate the intestinal from the hepatic first pass;
- the fraction absorbed `GU__F_abs_simva` (85 %, Zocor label) and the
  absorption rate `GU__SIMVAABS_k` (collinear with `Ka_dis_simva`);
- the excretion of the metabolites (`GU__F_abs_simmets`, `GU__SIMMETSABS_k`,
  `KI__SIMMETSEX_f`): 13 % of a dose in the urine, the rest in the feces
  (Zocor label), no study has urine or feces data;
- the exchange of the metabolites between the liver and the plasma
  (`LI__SIMMETSEXP_Vmax`): the profile likelihood of the first fit
  (PK_20261020_130012__c4676) is flat above 0.3 mmole/min/l, where the
  exchange is fast and not limiting; the value of the model (0.744) lies there;
- the hepatic uptake of simvastatin (`LI__SIMVAIMP_Vmax`, passive and fast),
  the efflux and the metabolism of the acid besides CYP3A4
  (`LI__SIMACIDEXP_k`, `LI__SIMACIDMET_k`) and the CYP3A4 of the acid
  (`LI__SIMACID_CYP3A4_Vmax`): set with the half-life of 1.9 h of an
  intravenous dose of the acid (Zocor label) and the similar ratios of
  simvastatin and its acid with the inhibitors of CYP3A4, which the control
  data do not identify;
- the tissue distribution of the acid (`ftissue_simacid` flow limited,
  `Kp_simacid` from the volume of the acid);
- the activity factors (`f_cyp3a4`, `f_cyp3a5`, `f_oatp1b1`, `f_ugt`,
  `f_renal_function`), which the experiments set.
"""

from sbmlsim.fit import FitParameter

#: the absorption: the dissolution and gastric passage of simvastatin
parameters_pk_absorption: list[FitParameter] = [
    FitParameter(
        pid="Ka_dis_simva",
        start_value=1.22,
        lower_bound=0.1,
        upper_bound=10,
        unit="1/hr",
    ),
]

#: the hepatic metabolism of simvastatin (CYP3A4 and the hydrolysis to the
#: acid) and the hepatic uptake of simvastatin acid by OATP1B1, which sets the
#: clearance of the acid in the plasma
parameters_pk_liver: list[FitParameter] = [
    FitParameter(
        pid="LI__SIMVA_CYP3A4_Vmax",
        start_value=7.6e-2,
        lower_bound=1e-3,
        upper_bound=1,
        unit="mmole/min/l",
    ),
    FitParameter(
        pid="LI__ESTERASE_Vmax",
        start_value=5.3e-4,
        lower_bound=1e-5,
        upper_bound=1e-2,
        unit="mmole/min/l",
    ),
    FitParameter(
        pid="LI__SIMACIDIMP_Vmax",
        start_value=2.0e-4,
        lower_bound=1e-5,
        upper_bound=1e-2,
        unit="mmole/min/l",
    ),
]

#: the tissue distribution of simvastatin, which makes the terminal phase
parameters_pk_distribution: list[FitParameter] = [
    FitParameter(
        pid="ftissue_simva",
        start_value=1.12,
        lower_bound=0.05,
        upper_bound=20,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_simva",
        start_value=2.9,
        lower_bound=0.5,
        upper_bound=20,
        unit="dimensionless",
    ),
]

#: the metabolites: their biliary excretion, which sets the active and total
#: inhibitors
parameters_pk_metabolites: list[FitParameter] = [
    FitParameter(
        pid="LI__EHC_simmets_k",
        start_value=4.0,
        lower_bound=0.1,
        upper_bound=100,
        unit="1/min",
    ),
]

#: the parameters of the pharmacokinetics
parameters_pk: list[FitParameter] = [
    *parameters_pk_absorption,
    *parameters_pk_liver,
    *parameters_pk_distribution,
    *parameters_pk_metabolites,
]

#: the inhibition of the HMG-CoA reductase (0.1 - 2.3 nM, Istvan2001; 0.12 nM,
#: Corsini1995), fitted on the adopted pharmacokinetics. The inhibitor activity
#: of the metabolites (`simmets_inhibitor_activity`, 0.4) is not fitted: the
#: inhibition in the liver is the one of the metabolites (simvastatin acid is
#: metabolized in the liver, its concentration there is 100-fold lower), so the
#: activity and `Ki` are collinear
parameters_pd: list[FitParameter] = [
    FitParameter(
        pid="LI__HMGCOAREDUCTASE_Ki_simacid",
        start_value=1.2e-6,
        lower_bound=1e-7,
        upper_bound=1e-5,
        unit="mmole/l",
    ),
]
