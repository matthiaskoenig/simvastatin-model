# PK/PD model for whole-body simvastatin and cholesterol metabolism

Model `simvastatin_body`, SBML Level 3 Version 2, read from simvastatin\_body\_flat.xml, written by sbmlode 0.3.0.

PK/PD model for whole-body simvastatin and cholesterol metabolism

Changelog

replaced inital assignments with rules

fixed constant flags on parameters

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{Vgulumen}$ | `Vgulumen` | gut lumen |  | l |  |
| $\mathrm{LI}_{\mathrm{\_Vbaso}}$ | `LI__Vbaso` | basolateral membrane | $1$ | m<sup>2</sup> | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vapical}}$ | `LI__Vapical` | apical membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ventero}}$ | `GU__Ventero` | intestinal lining (enterocytes) | $\mathrm{NaN}$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vapical}}$ | `GU__Vapical` | apical membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vbaso}}$ | `GU__Vbaso` | basolateral membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cgu}_{\mathrm{plasma\_simva}}$ | `Cgu_plasma_simva` | simvastatin (gut) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_simva}}$ | `Cki_plasma_simva` | simvastatin (kidney) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_simva}}$ | `Cli_plasma_simva` | simvastatin (liver) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_simva}}$ | `Clu_plasma_simva` | simvastatin (lung) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_simva}}$ | `Cre_plasma_simva` | simvastatin (rest) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{simva}}$ | `Car_simva` | simvastatin (arterial blood) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{simva}}$ | `Cve_simva` | simvastatin (venous blood) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{simva}}$ | `Cpo_simva` | simvastatin (portal vein) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{simva}}$ | `Chv_simva` | simvastatin (hepatic vein) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{simva}}$ | `Clu_simva` | simvastatin (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{simva}}$ | `Cre_simva` | simvastatin (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Astomach}_{\mathrm{simva}}$ | `Astomach_simva` | simvastatin (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |
| $\mathrm{Afeces}_{\mathrm{simva}}$ | `Afeces_simva` | simvastatin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cgulumen}_{\mathrm{simva}}$ | `Cgulumen_simva` | simvastatin (gut lumen) | $\mathrm{Vgulumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_simacid}}$ | `Cgu_plasma_simacid` | simvastatin acid (gut) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_simacid}}$ | `Cki_plasma_simacid` | simvastatin acid (kidney) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_simacid}}$ | `Cli_plasma_simacid` | simvastatin acid (liver) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_simacid}}$ | `Clu_plasma_simacid` | simvastatin acid (lung) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_simacid}}$ | `Cre_plasma_simacid` | simvastatin acid (rest) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{simacid}}$ | `Car_simacid` | simvastatin acid (arterial blood) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{simacid}}$ | `Cve_simacid` | simvastatin acid (venous blood) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{simacid}}$ | `Cpo_simacid` | simvastatin acid (portal vein) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{simacid}}$ | `Chv_simacid` | simvastatin acid (hepatic vein) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{simacid}}$ | `Clu_simacid` | simvastatin acid (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{simacid}}$ | `Cre_simacid` | simvastatin acid (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_simmets}}$ | `Cgu_plasma_simmets` | simvastatin metabolites (gut) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_simmets}}$ | `Cki_plasma_simmets` | simvastatin metabolites (kidney) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_simmets}}$ | `Cli_plasma_simmets` | simvastatin metabolites (liver) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_simmets}}$ | `Clu_plasma_simmets` | simvastatin metabolites (lung) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_simmets}}$ | `Cre_plasma_simmets` | simvastatin metabolites (rest) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{simmets}}$ | `Car_simmets` | simvastatin metabolites (arterial blood) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{simmets}}$ | `Cve_simmets` | simvastatin metabolites (venous blood) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{simmets}}$ | `Cpo_simmets` | simvastatin metabolites (portal vein) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{simmets}}$ | `Chv_simmets` | simvastatin metabolites (hepatic vein) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{simmets}}$ | `Clu_simmets` | simvastatin metabolites (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{simmets}}$ | `Cre_simmets` | simvastatin metabolites (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{simmets}}$ | `Aurine_simmets` | simvastatin metabolites (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{simmets}}$ | `Afeces_simmets` | simvastatin metabolites (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cgulumen}_{\mathrm{simmets}}$ | `Cgulumen_simmets` | simvastatin metabolites (gut lumen) | $\mathrm{Vgulumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_ldlc}}$ | `Cgu_plasma_ldlc` | ldl-cholesterol (gut) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_ldlc}}$ | `Cki_plasma_ldlc` | ldl-cholesterol (kidney) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_ldlc}}$ | `Cli_plasma_ldlc` | ldl-cholesterol (liver) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_ldlc}}$ | `Clu_plasma_ldlc` | ldl-cholesterol (lung) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_ldlc}}$ | `Cre_plasma_ldlc` | ldl-cholesterol (rest) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{ldlc}}$ | `Car_ldlc` | ldl-cholesterol (arterial blood) | $\mathrm{Var}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{ldlc}}$ | `Cve_ldlc` | ldl-cholesterol (venous blood) | $\mathrm{Vve}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{ldlc}}$ | `Cpo_ldlc` | ldl-cholesterol (portal vein) | $\mathrm{Vpo}$ | $3$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{ldlc}}$ | `Chv_ldlc` | ldl-cholesterol (hepatic vein) | $\mathrm{Vhv}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_vldlc}}$ | `Cgu_plasma_vldlc` | vldl-cholesterol (gut) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_vldlc}}$ | `Cki_plasma_vldlc` | vldl-cholesterol (kidney) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ | `Cli_plasma_vldlc` | vldl-cholesterol (liver) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_vldlc}}$ | `Clu_plasma_vldlc` | vldl-cholesterol (lung) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_vldlc}}$ | `Cre_plasma_vldlc` | vldl-cholesterol (rest) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{vldlc}}$ | `Car_vldlc` | vldl-cholesterol (arterial blood) | $\mathrm{Var}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{vldlc}}$ | `Cve_vldlc` | vldl-cholesterol (venous blood) | $\mathrm{Vve}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{vldlc}}$ | `Cpo_vldlc` | vldl-cholesterol (portal vein) | $\mathrm{Vpo}$ | $1$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{vldlc}}$ | `Chv_vldlc` | vldl-cholesterol (hepatic vein) | $\mathrm{Vhv}$ | $1$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_simacid}}$ | `LI__simacid` | simvastatin acid (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_simmets}}$ | `LI__simmets` | simvastatin metabolites (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_simva}}$ | `LI__simva` | simvastatin (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_acoa}}$ | `LI__acoa` | acetyl-CoA (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0.043$ | mmol/l | concentration, boundary |
| $\mathrm{LI}_{\mathrm{\_hmgcoa}}$ | `LI__hmgcoa` | HMG-CoA (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0.022$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_cho}}$ | `LI__cho` | cholesterol (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0.02$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_hmgcoareductase}}$ | `LI__hmgcoareductase` | HMG-CoA reductase (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_hmgcoasynthase}}$ | `LI__hmgcoasynthase` | HMG-CoA synthase (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr}}$ | `LI__ldlr` | LDLR | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}$ | `LI__ldlr_membrane` | LDLR membrane | $\mathrm{LI}_{\mathrm{\_Vbaso}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}$ | `LI__ldlr_ldlc` | LDLR-LDLC complex | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr\_degraded}}$ | `LI__ldlr_degraded` | LDLR degraded | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{GU}_{\mathrm{\_simva}}$ | `GU__simva` | simvastatin (enterocytes) | $\mathrm{Vgu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_simmets}}$ | `GU__simmets` | simvastatin metabolites (intestine) | $\mathrm{Vgu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{conversion}_{\mathrm{min\_per\_day}}$ | `conversion_min_per_day` | Conversion factor min to hours | $1440$ | min/day | ✓ |
| $\mathrm{conversion}_{\mathrm{ml\_per\_l}}$ | `conversion_ml_per_l` | volume conversion factor | $1000$ | ml/l | ✓ |
| $\mathrm{conversion}_{\mathrm{l\_per\_ml}}$ | `conversion_l_per_ml` | volume conversion factor | $0.001$ | l/ml | ✓ |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{HEIGHT}$ | `HEIGHT` | height \[cm\] | $170$ | cm | ✓ |
| $\mathrm{HR}$ | `HR` | heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{HRrest}$ | `HRrest` | heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{BSA}$ | `BSA` | body surface area \[m^2\] |  | m<sup>2</sup> |  |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.25$ | ml/s/kg | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[L/min\] |  | l/min |  |
| $\mathrm{COHRI}$ | `COHRI` | increase of cardiac output per heartbeat \[ml/min\*min\] | $150$ | ml | ✓ |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- | ✓ |
| $\mathrm{HCT}$ | `HCT` | hematocrit | $0.51$ | \- | ✓ |
| $\mathrm{FVgi}$ | `FVgi` | fractional tissue volume gastrointestinal tract | $0.0297$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $f_{\mathrm{lumen}}$ | `f_lumen` | fraction lumen of intestine | $0.9$ | \- | ✓ |
| $\mathrm{CYP3A4}_{\mathrm{Km}}$ | `CYP3A4_Km` | Km CYP3A4 | $0.025$ | mmol/l | ✓ |
| $f_{\mathrm{cyp3a5}}$ | `f_cyp3a5` | functional CYP3A5 | $0$ | \- | ✓ |
| $r_{\mathrm{cyp3a5}}$ | `r_cyp3a5` | capacity of CYP3A5 \*1/\*1 relative to CYP3A4 | $1$ | \- | ✓ |
| $\mathrm{simmets}_{\mathrm{inhibitor\_activity}}$ | `simmets_inhibitor_activity` | HMG-CoA Reductase inhibitor activity of simmets | $0.4$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{simva}}$ | `Mr_simva` | Molecular weight simva \[g/mole\] | $418.6$ | g/mol | ✓ |
| $\mathrm{fup}_{\mathrm{simva}}$ | `fup_simva` | fraction unbound in plasma simva | $0.05$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{simva}}$ | `ftissue_simva` | tissue distribution simva | $1.37427767139463$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{simva}}$ | `Kp_simva` | tissue to plasma partition coefficient simva | $5.87362036474485$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{simva}}$ | `IVDOSE_simva` | IV bolus dose simva \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{simva}}$ | `ti_simva` | injection time simva \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{simva}}$ | `Ki_simva` | Ki \[1/min\] injection simva |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{simva}}$ | `Ri_simva` | Ri \[mg/min\] rate of infusion simva | $0$ | mg/min | ✓ |
| $\mathrm{cum}_{\mathrm{dose\_simva}}$ | `cum_dose_simva` | Cumulative dose due to infusion simva | $0$ | mg |  |
| $\mathrm{Mr}_{\mathrm{simacid}}$ | `Mr_simacid` | Molecular weight simacid \[g/mole\] | $436.6$ | g/mol | ✓ |
| $\mathrm{fup}_{\mathrm{simacid}}$ | `fup_simacid` | fraction unbound in plasma simacid | $0.05$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{simacid}}$ | `ftissue_simacid` | tissue distribution simacid | $10$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{simacid}}$ | `Kp_simacid` | tissue to plasma partition coefficient simacid | $0.254$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{simmets}}$ | `Mr_simmets` | Molecular weight simmets \[g/mole\] | $436.6$ | g/mol | ✓ |
| $\mathrm{fup}_{\mathrm{simmets}}$ | `fup_simmets` | fraction unbound in plasma simmets | $0.05$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{simmets}}$ | `ftissue_simmets` | tissue distribution simmets |  | l/min |  |
| $\mathrm{Kp}_{\mathrm{simmets}}$ | `Kp_simmets` | tissue to plasma partition coefficient simmets | $1$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{ldlc}}$ | `Mr_ldlc` | Molecular weight ldlc \[g/mole\] | $386.654$ | g/mol | ✓ |
| $\mathrm{fup}_{\mathrm{ldlc}}$ | `fup_ldlc` | fraction unbound in plasma ldlc | $1$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{ldlc}}$ | `ftissue_ldlc` | tissue distribution ldlc | $0$ | l/min | ✓ |
| $\mathrm{Mr}_{\mathrm{vldlc}}$ | `Mr_vldlc` | Molecular weight vldlc \[g/mole\] | $386.654$ | g/mol | ✓ |
| $\mathrm{fup}_{\mathrm{vldlc}}$ | `fup_vldlc` | fraction unbound in plasma vldlc | $1$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{vldlc}}$ | `ftissue_vldlc` | tissue distribution vldlc | $0$ | l/min | ✓ |
| $\mathrm{ldlc}_{\mathrm{init}}$ | `ldlc_init` | Initial LDLC -concentration | $3$ | mmol/l | ✓ |
| $v_{\mathrm{cho\_ref}}$ | `v_cho_ref` | reference cholesterol turnover \[mg/day\] | $1000$ | mg/day | ✓ |
| $\mathrm{ldlc}_{\mathrm{diet\_k}}$ | `ldlc_diet_k` | rate of cholesterol uptake from diet | $1$ | \- | ✓ |
| $\mathrm{ldlc}_{\mathrm{loss\_k}}$ | `ldlc_loss_k` | rate of cholesterol loss in feces | $1.2$ | \- | ✓ |
| $\mathrm{ldlc}_{\mathrm{utilization\_Vmax}}$ | `ldlc_utilization_Vmax` |  | $0.652143261992422$ | \- | ✓ |
| $\mathrm{ldlc}_{\mathrm{consumption\_Km}}$ | `ldlc_consumption_Km` |  | $60$ | mmol/l | ✓ |
| $f_{\mathrm{ldlc\_utilization\_Vmax}}$ | `f_ldlc_utilization_Vmax` | scaling factor for utilization | $1$ | \- | ✓ |
| $\mathrm{vldlc}_{\mathrm{conversion\_k}}$ | `vldlc_conversion_k` | conversion rate for plasma vldlc into plasma ldlc | $2$ | l/mmol | ✓ |
| $\mathrm{PODOSE}_{\mathrm{simva}}$ | `PODOSE_simva` |  | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_simva}}$ | `Ka_dis_simva` | Ka\_dis \[1/hr\] dissolution simva | $0.603595698194537$ | 1/hr | ✓ |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{Agu}_{\mathrm{plasma\_simva}}$ | `Agu_plasma_simva` | simvastatin concentration (gut) |  | mmol |  |
| $\mathrm{Cgu}_{\mathrm{free\_simva}}$ | `Cgu_free_simva` | simvastatin free concentration (gut) |  | mmol/l |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_simva}}$ | `Xgu_plasma_simva` | simvastatin amount (gut) |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_simva}}$ | `Mgu_plasma_simva` | simvastatin amount (gut) |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_simva}}$ | `Aki_plasma_simva` | simvastatin concentration (kidney) |  | mmol |  |
| $\mathrm{Cki}_{\mathrm{free\_simva}}$ | `Cki_free_simva` | simvastatin free concentration (kidney) |  | mmol/l |  |
| $\mathrm{Xki}_{\mathrm{plasma\_simva}}$ | `Xki_plasma_simva` | simvastatin amount (kidney) |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_simva}}$ | `Mki_plasma_simva` | simvastatin amount (kidney) |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_simva}}$ | `Ali_plasma_simva` | simvastatin concentration (liver) |  | mmol |  |
| $\mathrm{Cli}_{\mathrm{free\_simva}}$ | `Cli_free_simva` | simvastatin free concentration (liver) |  | mmol/l |  |
| $\mathrm{Xli}_{\mathrm{plasma\_simva}}$ | `Xli_plasma_simva` | simvastatin amount (liver) |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_simva}}$ | `Mli_plasma_simva` | simvastatin amount (liver) |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_simva}}$ | `Alu_plasma_simva` | simvastatin concentration (lung) |  | mmol |  |
| $\mathrm{Clu}_{\mathrm{free\_simva}}$ | `Clu_free_simva` | simvastatin free concentration (lung) |  | mmol/l |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_simva}}$ | `Xlu_plasma_simva` | simvastatin amount (lung) |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_simva}}$ | `Mlu_plasma_simva` | simvastatin amount (lung) |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_simva}}$ | `Are_plasma_simva` | simvastatin concentration (rest) |  | mmol |  |
| $\mathrm{Cre}_{\mathrm{free\_simva}}$ | `Cre_free_simva` | simvastatin free concentration (rest) |  | mmol/l |  |
| $\mathrm{Xre}_{\mathrm{plasma\_simva}}$ | `Xre_plasma_simva` | simvastatin amount (rest) |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_simva}}$ | `Mre_plasma_simva` | simvastatin amount (rest) |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{simva}}$ | `Aar_simva` | simvastatin amount (arterial blood) |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{simva}}$ | `Xar_simva` | simvastatin amount (arterial blood) |  | mg |  |
| $\mathrm{Mar}_{\mathrm{simva}}$ | `Mar_simva` | simvastatin concentration (arterial blood) |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{simva}}$ | `Ave_simva` | simvastatin amount (venous blood) |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{simva}}$ | `Xve_simva` | simvastatin amount (venous blood) |  | mg |  |
| $\mathrm{Mve}_{\mathrm{simva}}$ | `Mve_simva` | simvastatin concentration (venous blood) |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{simva}}$ | `Apo_simva` | simvastatin amount (portal vein) |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{simva}}$ | `Xpo_simva` | simvastatin amount (portal vein) |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{simva}}$ | `Mpo_simva` | simvastatin concentration (portal vein) |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{simva}}$ | `Ahv_simva` | simvastatin amount (hepatic vein) |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{simva}}$ | `Xhv_simva` | simvastatin amount (hepatic vein) |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{simva}}$ | `Mhv_simva` | simvastatin concentration (hepatic vein) |  | mg/l |  |
| $\mathrm{Xfeces}_{\mathrm{simva}}$ | `Xfeces_simva` | simvastatin amount (feces) |  | mg |  |
| $\mathrm{Agu}_{\mathrm{plasma\_simacid}}$ | `Agu_plasma_simacid` | simvastatin acid concentration (gut) |  | mmol |  |
| $\mathrm{Cgu}_{\mathrm{free\_simacid}}$ | `Cgu_free_simacid` | simvastatin acid free concentration (gut) |  | mmol/l |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_simacid}}$ | `Xgu_plasma_simacid` | simvastatin acid amount (gut) |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_simacid}}$ | `Mgu_plasma_simacid` | simvastatin acid amount (gut) |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_simacid}}$ | `Aki_plasma_simacid` | simvastatin acid concentration (kidney) |  | mmol |  |
| $\mathrm{Cki}_{\mathrm{free\_simacid}}$ | `Cki_free_simacid` | simvastatin acid free concentration (kidney) |  | mmol/l |  |
| $\mathrm{Xki}_{\mathrm{plasma\_simacid}}$ | `Xki_plasma_simacid` | simvastatin acid amount (kidney) |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_simacid}}$ | `Mki_plasma_simacid` | simvastatin acid amount (kidney) |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_simacid}}$ | `Ali_plasma_simacid` | simvastatin acid concentration (liver) |  | mmol |  |
| $\mathrm{Cli}_{\mathrm{free\_simacid}}$ | `Cli_free_simacid` | simvastatin acid free concentration (liver) |  | mmol/l |  |
| $\mathrm{Xli}_{\mathrm{plasma\_simacid}}$ | `Xli_plasma_simacid` | simvastatin acid amount (liver) |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_simacid}}$ | `Mli_plasma_simacid` | simvastatin acid amount (liver) |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_simacid}}$ | `Alu_plasma_simacid` | simvastatin acid concentration (lung) |  | mmol |  |
| $\mathrm{Clu}_{\mathrm{free\_simacid}}$ | `Clu_free_simacid` | simvastatin acid free concentration (lung) |  | mmol/l |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_simacid}}$ | `Xlu_plasma_simacid` | simvastatin acid amount (lung) |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_simacid}}$ | `Mlu_plasma_simacid` | simvastatin acid amount (lung) |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_simacid}}$ | `Are_plasma_simacid` | simvastatin acid concentration (rest) |  | mmol |  |
| $\mathrm{Cre}_{\mathrm{free\_simacid}}$ | `Cre_free_simacid` | simvastatin acid free concentration (rest) |  | mmol/l |  |
| $\mathrm{Xre}_{\mathrm{plasma\_simacid}}$ | `Xre_plasma_simacid` | simvastatin acid amount (rest) |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_simacid}}$ | `Mre_plasma_simacid` | simvastatin acid amount (rest) |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{simacid}}$ | `Aar_simacid` | simvastatin acid amount (arterial blood) |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{simacid}}$ | `Xar_simacid` | simvastatin acid amount (arterial blood) |  | mg |  |
| $\mathrm{Mar}_{\mathrm{simacid}}$ | `Mar_simacid` | simvastatin acid concentration (arterial blood) |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{simacid}}$ | `Ave_simacid` | simvastatin acid amount (venous blood) |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{simacid}}$ | `Xve_simacid` | simvastatin acid amount (venous blood) |  | mg |  |
| $\mathrm{Mve}_{\mathrm{simacid}}$ | `Mve_simacid` | simvastatin acid concentration (venous blood) |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{simacid}}$ | `Apo_simacid` | simvastatin acid amount (portal vein) |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{simacid}}$ | `Xpo_simacid` | simvastatin acid amount (portal vein) |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{simacid}}$ | `Mpo_simacid` | simvastatin acid concentration (portal vein) |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{simacid}}$ | `Ahv_simacid` | simvastatin acid amount (hepatic vein) |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{simacid}}$ | `Xhv_simacid` | simvastatin acid amount (hepatic vein) |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{simacid}}$ | `Mhv_simacid` | simvastatin acid concentration (hepatic vein) |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_simmets}}$ | `Agu_plasma_simmets` | simvastatin metabolites concentration (gut) |  | mmol |  |
| $\mathrm{Cgu}_{\mathrm{free\_simmets}}$ | `Cgu_free_simmets` | simvastatin metabolites free concentration (gut) |  | mmol/l |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_simmets}}$ | `Xgu_plasma_simmets` | simvastatin metabolites amount (gut) |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_simmets}}$ | `Mgu_plasma_simmets` | simvastatin metabolites amount (gut) |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_simmets}}$ | `Aki_plasma_simmets` | simvastatin metabolites concentration (kidney) |  | mmol |  |
| $\mathrm{Cki}_{\mathrm{free\_simmets}}$ | `Cki_free_simmets` | simvastatin metabolites free concentration (kidney) |  | mmol/l |  |
| $\mathrm{Xki}_{\mathrm{plasma\_simmets}}$ | `Xki_plasma_simmets` | simvastatin metabolites amount (kidney) |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_simmets}}$ | `Mki_plasma_simmets` | simvastatin metabolites amount (kidney) |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_simmets}}$ | `Ali_plasma_simmets` | simvastatin metabolites concentration (liver) |  | mmol |  |
| $\mathrm{Cli}_{\mathrm{free\_simmets}}$ | `Cli_free_simmets` | simvastatin metabolites free concentration (liver) |  | mmol/l |  |
| $\mathrm{Xli}_{\mathrm{plasma\_simmets}}$ | `Xli_plasma_simmets` | simvastatin metabolites amount (liver) |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_simmets}}$ | `Mli_plasma_simmets` | simvastatin metabolites amount (liver) |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_simmets}}$ | `Alu_plasma_simmets` | simvastatin metabolites concentration (lung) |  | mmol |  |
| $\mathrm{Clu}_{\mathrm{free\_simmets}}$ | `Clu_free_simmets` | simvastatin metabolites free concentration (lung) |  | mmol/l |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_simmets}}$ | `Xlu_plasma_simmets` | simvastatin metabolites amount (lung) |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_simmets}}$ | `Mlu_plasma_simmets` | simvastatin metabolites amount (lung) |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_simmets}}$ | `Are_plasma_simmets` | simvastatin metabolites concentration (rest) |  | mmol |  |
| $\mathrm{Cre}_{\mathrm{free\_simmets}}$ | `Cre_free_simmets` | simvastatin metabolites free concentration (rest) |  | mmol/l |  |
| $\mathrm{Xre}_{\mathrm{plasma\_simmets}}$ | `Xre_plasma_simmets` | simvastatin metabolites amount (rest) |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_simmets}}$ | `Mre_plasma_simmets` | simvastatin metabolites amount (rest) |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{simmets}}$ | `Aar_simmets` | simvastatin metabolites amount (arterial blood) |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{simmets}}$ | `Xar_simmets` | simvastatin metabolites amount (arterial blood) |  | mg |  |
| $\mathrm{Mar}_{\mathrm{simmets}}$ | `Mar_simmets` | simvastatin metabolites concentration (arterial blood) |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{simmets}}$ | `Ave_simmets` | simvastatin metabolites amount (venous blood) |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{simmets}}$ | `Xve_simmets` | simvastatin metabolites amount (venous blood) |  | mg |  |
| $\mathrm{Mve}_{\mathrm{simmets}}$ | `Mve_simmets` | simvastatin metabolites concentration (venous blood) |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{simmets}}$ | `Apo_simmets` | simvastatin metabolites amount (portal vein) |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{simmets}}$ | `Xpo_simmets` | simvastatin metabolites amount (portal vein) |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{simmets}}$ | `Mpo_simmets` | simvastatin metabolites concentration (portal vein) |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{simmets}}$ | `Ahv_simmets` | simvastatin metabolites amount (hepatic vein) |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{simmets}}$ | `Xhv_simmets` | simvastatin metabolites amount (hepatic vein) |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{simmets}}$ | `Mhv_simmets` | simvastatin metabolites concentration (hepatic vein) |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{simmets}}$ | `Xurine_simmets` | simvastatin metabolites amount (urine) |  | mg |  |
| $\mathrm{Xfeces}_{\mathrm{simmets}}$ | `Xfeces_simmets` | simvastatin metabolites amount (feces) |  | mg |  |
| $\mathrm{Agu}_{\mathrm{plasma\_ldlc}}$ | `Agu_plasma_ldlc` | ldl-cholesterol concentration (gut) |  | mmol |  |
| $\mathrm{Cgu}_{\mathrm{free\_ldlc}}$ | `Cgu_free_ldlc` | ldl-cholesterol free concentration (gut) |  | mmol/l |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_ldlc}}$ | `Xgu_plasma_ldlc` | ldl-cholesterol amount (gut) |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_ldlc}}$ | `Mgu_plasma_ldlc` | ldl-cholesterol amount (gut) |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_ldlc}}$ | `Aki_plasma_ldlc` | ldl-cholesterol concentration (kidney) |  | mmol |  |
| $\mathrm{Cki}_{\mathrm{free\_ldlc}}$ | `Cki_free_ldlc` | ldl-cholesterol free concentration (kidney) |  | mmol/l |  |
| $\mathrm{Xki}_{\mathrm{plasma\_ldlc}}$ | `Xki_plasma_ldlc` | ldl-cholesterol amount (kidney) |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_ldlc}}$ | `Mki_plasma_ldlc` | ldl-cholesterol amount (kidney) |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_ldlc}}$ | `Ali_plasma_ldlc` | ldl-cholesterol concentration (liver) |  | mmol |  |
| $\mathrm{Cli}_{\mathrm{free\_ldlc}}$ | `Cli_free_ldlc` | ldl-cholesterol free concentration (liver) |  | mmol/l |  |
| $\mathrm{Xli}_{\mathrm{plasma\_ldlc}}$ | `Xli_plasma_ldlc` | ldl-cholesterol amount (liver) |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_ldlc}}$ | `Mli_plasma_ldlc` | ldl-cholesterol amount (liver) |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_ldlc}}$ | `Alu_plasma_ldlc` | ldl-cholesterol concentration (lung) |  | mmol |  |
| $\mathrm{Clu}_{\mathrm{free\_ldlc}}$ | `Clu_free_ldlc` | ldl-cholesterol free concentration (lung) |  | mmol/l |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_ldlc}}$ | `Xlu_plasma_ldlc` | ldl-cholesterol amount (lung) |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_ldlc}}$ | `Mlu_plasma_ldlc` | ldl-cholesterol amount (lung) |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_ldlc}}$ | `Are_plasma_ldlc` | ldl-cholesterol concentration (rest) |  | mmol |  |
| $\mathrm{Cre}_{\mathrm{free\_ldlc}}$ | `Cre_free_ldlc` | ldl-cholesterol free concentration (rest) |  | mmol/l |  |
| $\mathrm{Xre}_{\mathrm{plasma\_ldlc}}$ | `Xre_plasma_ldlc` | ldl-cholesterol amount (rest) |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_ldlc}}$ | `Mre_plasma_ldlc` | ldl-cholesterol amount (rest) |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{ldlc}}$ | `Aar_ldlc` | ldl-cholesterol amount (arterial blood) |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{ldlc}}$ | `Xar_ldlc` | ldl-cholesterol amount (arterial blood) |  | mg |  |
| $\mathrm{Mar}_{\mathrm{ldlc}}$ | `Mar_ldlc` | ldl-cholesterol concentration (arterial blood) |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{ldlc}}$ | `Ave_ldlc` | ldl-cholesterol amount (venous blood) |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{ldlc}}$ | `Xve_ldlc` | ldl-cholesterol amount (venous blood) |  | mg |  |
| $\mathrm{Mve}_{\mathrm{ldlc}}$ | `Mve_ldlc` | ldl-cholesterol concentration (venous blood) |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{ldlc}}$ | `Apo_ldlc` | ldl-cholesterol amount (portal vein) |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{ldlc}}$ | `Xpo_ldlc` | ldl-cholesterol amount (portal vein) |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{ldlc}}$ | `Mpo_ldlc` | ldl-cholesterol concentration (portal vein) |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{ldlc}}$ | `Ahv_ldlc` | ldl-cholesterol amount (hepatic vein) |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{ldlc}}$ | `Xhv_ldlc` | ldl-cholesterol amount (hepatic vein) |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{ldlc}}$ | `Mhv_ldlc` | ldl-cholesterol concentration (hepatic vein) |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_vldlc}}$ | `Agu_plasma_vldlc` | vldl-cholesterol concentration (gut) |  | mmol |  |
| $\mathrm{Cgu}_{\mathrm{free\_vldlc}}$ | `Cgu_free_vldlc` | vldl-cholesterol free concentration (gut) |  | mmol/l |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_vldlc}}$ | `Xgu_plasma_vldlc` | vldl-cholesterol amount (gut) |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_vldlc}}$ | `Mgu_plasma_vldlc` | vldl-cholesterol amount (gut) |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_vldlc}}$ | `Aki_plasma_vldlc` | vldl-cholesterol concentration (kidney) |  | mmol |  |
| $\mathrm{Cki}_{\mathrm{free\_vldlc}}$ | `Cki_free_vldlc` | vldl-cholesterol free concentration (kidney) |  | mmol/l |  |
| $\mathrm{Xki}_{\mathrm{plasma\_vldlc}}$ | `Xki_plasma_vldlc` | vldl-cholesterol amount (kidney) |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_vldlc}}$ | `Mki_plasma_vldlc` | vldl-cholesterol amount (kidney) |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_vldlc}}$ | `Ali_plasma_vldlc` | vldl-cholesterol concentration (liver) |  | mmol |  |
| $\mathrm{Cli}_{\mathrm{free\_vldlc}}$ | `Cli_free_vldlc` | vldl-cholesterol free concentration (liver) |  | mmol/l |  |
| $\mathrm{Xli}_{\mathrm{plasma\_vldlc}}$ | `Xli_plasma_vldlc` | vldl-cholesterol amount (liver) |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_vldlc}}$ | `Mli_plasma_vldlc` | vldl-cholesterol amount (liver) |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_vldlc}}$ | `Alu_plasma_vldlc` | vldl-cholesterol concentration (lung) |  | mmol |  |
| $\mathrm{Clu}_{\mathrm{free\_vldlc}}$ | `Clu_free_vldlc` | vldl-cholesterol free concentration (lung) |  | mmol/l |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_vldlc}}$ | `Xlu_plasma_vldlc` | vldl-cholesterol amount (lung) |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_vldlc}}$ | `Mlu_plasma_vldlc` | vldl-cholesterol amount (lung) |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_vldlc}}$ | `Are_plasma_vldlc` | vldl-cholesterol concentration (rest) |  | mmol |  |
| $\mathrm{Cre}_{\mathrm{free\_vldlc}}$ | `Cre_free_vldlc` | vldl-cholesterol free concentration (rest) |  | mmol/l |  |
| $\mathrm{Xre}_{\mathrm{plasma\_vldlc}}$ | `Xre_plasma_vldlc` | vldl-cholesterol amount (rest) |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_vldlc}}$ | `Mre_plasma_vldlc` | vldl-cholesterol amount (rest) |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{vldlc}}$ | `Aar_vldlc` | vldl-cholesterol amount (arterial blood) |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{vldlc}}$ | `Xar_vldlc` | vldl-cholesterol amount (arterial blood) |  | mg |  |
| $\mathrm{Mar}_{\mathrm{vldlc}}$ | `Mar_vldlc` | vldl-cholesterol concentration (arterial blood) |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{vldlc}}$ | `Ave_vldlc` | vldl-cholesterol amount (venous blood) |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{vldlc}}$ | `Xve_vldlc` | vldl-cholesterol amount (venous blood) |  | mg |  |
| $\mathrm{Mve}_{\mathrm{vldlc}}$ | `Mve_vldlc` | vldl-cholesterol concentration (venous blood) |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{vldlc}}$ | `Apo_vldlc` | vldl-cholesterol amount (portal vein) |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{vldlc}}$ | `Xpo_vldlc` | vldl-cholesterol amount (portal vein) |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{vldlc}}$ | `Mpo_vldlc` | vldl-cholesterol concentration (portal vein) |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{vldlc}}$ | `Ahv_vldlc` | vldl-cholesterol amount (hepatic vein) |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{vldlc}}$ | `Xhv_vldlc` | vldl-cholesterol amount (hepatic vein) |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{vldlc}}$ | `Mhv_vldlc` | vldl-cholesterol concentration (hepatic vein) |  | mg/l |  |
| $\mathrm{Cve}_{\mathrm{simva\_and\_simacid}}$ | `Cve_simva_and_simacid` | total simvastatin and simvastatin acid in venous blood |  | mmol/l |  |
| $\mathrm{Cve}_{\mathrm{active\_inhibitors}}$ | `Cve_active_inhibitors` | active HMG-CoA reductase inhibitors in venous blood |  | mmol/l |  |
| $\mathrm{Cve}_{\mathrm{total\_inhibitors}}$ | `Cve_total_inhibitors` | total HMG-CoA reductase inhibitors in venous blood |  | mmol/l |  |
| $\mathrm{ldlc}_{\mathrm{change}}$ | `ldlc_change` | relative LDL-C reduction in plasma in \[0,-1\] |  | \- |  |
| $v_{\mathrm{cho\_reference}}$ | `v_cho_reference` | reference cholesterol turnover \[mmole/min\] |  | mmol/min |  |
| $\mathrm{ldlc}_{\mathrm{loss}}$ | `ldlc_loss` | total loss of cholesterol |  | mmol/min |  |
| $\mathrm{ldlc}_{\mathrm{diet}}$ | `ldlc_diet` | total dietary cholesterol |  | mmol/min |  |
| $\mathrm{ldlc}_{\mathrm{utilization}}$ | `ldlc_utilization` | total utilized cholesterol |  | mmol/min |  |
| $v_{\mathrm{ldlc\_net\_consumption}}$ | `v_ldlc_net_consumption` | plasma cholesterol net consumption \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{vldlc\_conversion}}$ | `v_vldlc_conversion` | plasma vldlc conversion into ldlc \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{ldlc\_utilization}}$ | `v_ldlc_utilization` | plasma cholesterol net consumption \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{ldlc\_diet}}$ | `v_ldlc_diet` | plasma cholesterol diet \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{ldlc\_loss}}$ | `v_ldlc_loss` | plasma cholesterol loss \[mg/day\] |  | mg/day |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | parameter for renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR\_base}}$ | `KI__GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_SIMMETSEX\_f}}$ | `KI__SIMMETSEX_f` | renal clearance of unbound metabolites relative to the GFR | $910$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{LI}_{\mathrm{\_f\_cyp3a4}}$ | `LI__f_cyp3a4` | activity of CYP3A4 (liver) | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_ugt}}$ | `LI__f_ugt` | activity of the glucuronidation and CYP2C8 of simvastatin acid | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_oatp1b1}}$ | `LI__f_oatp1b1` | activity of OATP1B1 | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}}$ | `LI__cf_units_per_mmole` | conversion factor for dimensionless species | $1$ | 1/mmol | ✓ |
| $\mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}}$ | `LI__conversion_min_per_day` | conversion factor min to hours | $1440$ | min/day | ✓ |
| $\mathrm{LI}_{\mathrm{\_SYNTHESIS\_HMG\_Vmax}}$ | `LI__SYNTHESIS_HMG_Vmax` | Protein synthesis Vmax for HMGR and HMGS | $0.001$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DEGRADATION\_HMG\_Vmax}}$ | `LI__DEGRADATION_HMG_Vmax` | Protein degradation Vmax for HMGR and HMGS | $0.0003$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}$ | `LI__HMG_kr_cho` | Protein regulation kr for HMGR and HMGS | $0.02$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax}}$ | `LI__DEGRADATION_LDLR_Vmax` | Protein degradation Vmax for LDLR | $0.0006$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax}}$ | `LI__SYNTHESIS_LDLR_Vmax` | Protein synthesis Vmax for LDLR |  | mmol/min/l |  |
| $\mathrm{LI}_{\mathrm{\_LDLR\_kr\_cho}}$ | `LI__LDLR_kr_cho` | Protein regulation kr for LDLR | $0.02$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax\_f}}$ | `LI__SYNTHESIS_LDLR_Vmax_f` | scaling factor for synthesis Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax\_f}}$ | `LI__DEGRADATION_LDLR_Vmax_f` | scaling factor for degradation Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMVAIMP\_Km}}$ | `LI__SIMVAIMP_Km` | Km for simvastatin import | $0.0097$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMVAIMP\_Vmax}}$ | `LI__SIMVAIMP_Vmax` | Vmax for simvastatin import | $1$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMACIDIMP\_Km}}$ | `LI__SIMACIDIMP_Km` | Km for simvastatin acid import | $0.0036$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMACIDIMP\_Vmax}}$ | `LI__SIMACIDIMP_Vmax` | Vmax for simvastatin acid import | $0.000155861593241634$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMACIDEXP\_k}}$ | `LI__SIMACIDEXP_k` | rate of simvastatin acid efflux | $0.925$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMMETSEXP\_Km}}$ | `LI__SIMMETSEXP_Km` | Km for simvastatin metabolites exchange | $0.0067$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMMETSEXP\_Vmax}}$ | `LI__SIMMETSEXP_Vmax` | Vmax for simvastatin metabolites exchange | $0.744$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_ESTERASE\_Km}}$ | `LI__ESTERASE_Km` | Km esterase | $0.0008$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_ESTERASE\_Vmax}}$ | `LI__ESTERASE_Vmax` | Vmax esterase | $0.000355497735581453$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMVA\_CYP3A4\_Vmax}}$ | `LI__SIMVA_CYP3A4_Vmax` | Vmax CYP3A4 simvastatin (liver) | $0.071371880652173$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMACID\_CYP3A4\_Vmax}}$ | `LI__SIMACID_CYP3A4_Vmax` | Vmax CYP3A4 simvastatin acid (liver) | $0.0015$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SIMACIDMET\_k}}$ | `LI__SIMACIDMET_k` | rate of the metabolism of simvastatin acid not by CYP3A4 | $16$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_EHC\_simmets\_k}}$ | `LI__EHC_simmets_k` | rate of biliary excretion of the simvastatin metabolites | $3.02803101810212$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_VLDLCEXP\_Vmax}}$ | `LI__VLDLCEXP_Vmax` | Vmax VLDL-cholesterol export | $2.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_VLDLCEXP\_Km\_cho}}$ | `LI__VLDLCEXP_Km_cho` | Km VLDL-cholesterol export | $0.0005$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat}}$ | `LI__LDLRLDLCIMP_Kcat` |  | $6$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km}}$ | `LI__LDLRLDLCIMP_Km` | Km LDLR-LDLC binding | $3$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Ki\_ldlr\_ldlc}}$ | `LI__LDLRLDLCIMP_Ki_ldlr_ldlc` | Ki LDLR-LDLC complex on uptake | $0.1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km\_f}}$ | `LI__LDLRLDLCIMP_Km_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat\_f}}$ | `LI__LDLRLDLCIMP_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat}}$ | `LI__LDLRMEMBRANE_Kcat` |  | $0.025$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat\_f}}$ | `LI__LDLRMEMBRANE_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Keq}}$ | `LI__LDLRMEMBRANE_Keq` |  | $10$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat}}$ | `LI__LDLRRECYCLING_Kcat` |  | $0.0125$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat\_f}}$ | `LI__LDLRRECYCLING_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Kcat}}$ | `LI__HMGCOASYNTHASE_Kcat` | kcat HMG-CoA synthase | $245$ | l/mmol | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Ki\_hmgcoa}}$ | `LI__HMGCOASYNTHASE_Ki_hmgcoa` | Ki HMG-CoA synthase (product inhibition by HMG-CoA) | $0.022$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Kcat}}$ | `LI__HMGCOAREDUCTASE_Kcat` | kcat HMG-CoA reductase | $0.7$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Km}}$ | `LI__HMGCOAREDUCTASE_Km` | Km HMG-CoA | $0.004$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Ki\_simacid}}$ | `LI__HMGCOAREDUCTASE_Ki_simacid` | Ki HMG-CoA reductase for simvastatin acid and the active metabolites | $9.16748418506532 \times 10^{-7}$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_ldlr\_total}}$ | `LI__ldlr_total` | Total LDLR |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_ldlr\_fraction}}$ | `LI__ldlr_fraction` | LDLR fraction |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_ldlr\_membrane\_fraction}}$ | `LI__ldlr_membrane_fraction` | LDLR membrane fraction |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc\_fraction}}$ | `LI__ldlr_ldlc_fraction` | LDLR-LDLC fraction |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_v\_cho\_reference}}$ | `LI__v_cho_reference` | reference cholesterol turnover \[mmole/min\] |  | mmol/min |  |
| $\mathrm{LI}_{\mathrm{\_v\_synthesis}}$ | `LI__v_synthesis` | total synthesized cholesterol |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_recycling}}$ | `LI__v_recycling` | LDLR recycling and cholesterol release into free cholesterol |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_uptake}}$ | `LI__v_uptake` | cholesterol uptake (LDL receptor) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_export}}$ | `LI__v_export` | cholesterol export (VLDL) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_reference}}$ | `LI__v_reference` | cholesterol reference flux |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_net\_export\_rate}}$ | `LI__v_net_export_rate` | cholesterol net export rate (VLDL) |  | mmol/min |  |
| $\mathrm{LI}_{\mathrm{\_v\_net\_export}}$ | `LI__v_net_export` | cholesterol net export (VLDL) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_liver\_balance}}$ | `LI__v_liver_balance` | cholesterol liver balance |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_TURNOVER\_LDLR}}$ | `LI__TURNOVER_LDLR` | total turnover of LDL-R expression |  | mmol/min |  |
| $\mathrm{LI}_{\mathrm{\_active\_inhibitors}}$ | `LI__active_inhibitors` | active HMG-CoA reductase inhibitors in liver |  | mmol/l |  |
| $\mathrm{GU}_{\mathrm{\_F\_abs\_simva}}$ | `GU__F_abs_simva` | fraction absorbed simvastatin | $0.85$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMVAABS\_k}}$ | `GU__SIMVAABS_k` | rate of absorption simvastatin | $1.29$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_F\_abs\_simmets}}$ | `GU__F_abs_simmets` | fraction absorbed simvastatin metabolites | $0.536$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMMETSABS\_k}}$ | `GU__SIMMETSABS_k` | rate of absorption simvastatin metabolites | $0.226$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_cyp3a4}}$ | `GU__f_cyp3a4` | activity of CYP3A4 (intestine) | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMVA\_CYP3A4\_Vmax}}$ | `GU__SIMVA_CYP3A4_Vmax` | Vmax CYP3A4 simvastatin (intestine) | $0.0063$ | mmol/min/l | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMVAEXP\_Km}}$ | `GU__SIMVAEXP_Km` | Km simvastatin export | $0.0097$ | mmol/l | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMVAEXP\_Vmax}}$ | `GU__SIMVAEXP_Vmax` | Vmax simvastatin export (intestine) | $0.001$ | mmol/min/l | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMMETSEXP\_Km}}$ | `GU__SIMMETSEXP_Km` | Km simvastatin metabolite export | $0.0067$ | mmol/l | ✓ |
| $\mathrm{GU}_{\mathrm{\_SIMMETSEXP\_Vmax}}$ | `GU__SIMMETSEXP_Vmax` | Vmax simvastatin metabolite export (intestine) | $0.01$ | mmol/min/l | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Astomach}_{\mathrm{simva}} &= 0 \cdot \mathrm{Vstomach} \\[1ex]
\mathrm{Afeces}_{\mathrm{simva}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{Aurine}_{\mathrm{simmets}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{simmets}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{LI}_{\mathrm{\_hmgcoareductase}} &= 1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_hmgcoasynthase}} &= 1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr}} &= 0.1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_membrane}} &= 0.8 \cdot \mathrm{LI}_{\mathrm{\_Vbaso}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} &= 0.1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_degraded}} &= 0 \cdot \mathrm{Vli}_{\mathrm{tissue}}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{ftissue}_{\mathrm{simmets}} &= \mathrm{ftissue}_{\mathrm{simacid}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgi} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{BSA} &= 0.024265 \cdot \mathopen{}\left(\frac{\mathrm{BW}}{1}\right)^{0.5378} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}}{1}\right)^{0.3964} \\[1ex]
\mathrm{CO} &= \mathrm{BW} \cdot \mathrm{COBW} + \frac{\mathopen{}\left(\mathrm{HR} - \mathrm{HRrest}\right) \cdot \mathrm{COHRI}}{60} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgi} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vgulumen} &= f_{\mathrm{lumen}} \cdot \mathrm{Vgu} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Vhv} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{simva}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{simva}}} \cdot 60 \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_simva}} &= \mathrm{Cgu}_{\mathrm{plasma\_simva}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cgu}_{\mathrm{free\_simva}} &= \mathrm{Cgu}_{\mathrm{plasma\_simva}} \cdot \mathrm{fup}_{\mathrm{simva}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_simva}} &= \mathrm{Agu}_{\mathrm{plasma\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_simva}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_simva}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_simva}} &= \mathrm{Cki}_{\mathrm{plasma\_simva}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cki}_{\mathrm{free\_simva}} &= \mathrm{Cki}_{\mathrm{plasma\_simva}} \cdot \mathrm{fup}_{\mathrm{simva}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_simva}} &= \mathrm{Aki}_{\mathrm{plasma\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_simva}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_simva}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_simva}} &= \mathrm{Cli}_{\mathrm{plasma\_simva}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cli}_{\mathrm{free\_simva}} &= \mathrm{Cli}_{\mathrm{plasma\_simva}} \cdot \mathrm{fup}_{\mathrm{simva}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_simva}} &= \mathrm{Ali}_{\mathrm{plasma\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_simva}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_simva}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_simva}} &= \mathrm{Clu}_{\mathrm{plasma\_simva}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Clu}_{\mathrm{free\_simva}} &= \mathrm{Clu}_{\mathrm{plasma\_simva}} \cdot \mathrm{fup}_{\mathrm{simva}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_simva}} &= \mathrm{Alu}_{\mathrm{plasma\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_simva}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_simva}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_simva}} &= \mathrm{Cre}_{\mathrm{plasma\_simva}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cre}_{\mathrm{free\_simva}} &= \mathrm{Cre}_{\mathrm{plasma\_simva}} \cdot \mathrm{fup}_{\mathrm{simva}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_simva}} &= \mathrm{Are}_{\mathrm{plasma\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_simva}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_simva}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Aar}_{\mathrm{simva}} &= \mathrm{Car}_{\mathrm{simva}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{simva}} &= \mathrm{Aar}_{\mathrm{simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mar}_{\mathrm{simva}} &= \frac{\mathrm{Aar}_{\mathrm{simva}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Ave}_{\mathrm{simva}} &= \mathrm{Cve}_{\mathrm{simva}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{simva}} &= \mathrm{Ave}_{\mathrm{simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mve}_{\mathrm{simva}} &= \frac{\mathrm{Ave}_{\mathrm{simva}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Apo}_{\mathrm{simva}} &= \mathrm{Cpo}_{\mathrm{simva}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{simva}} &= \mathrm{Apo}_{\mathrm{simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mpo}_{\mathrm{simva}} &= \frac{\mathrm{Apo}_{\mathrm{simva}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Ahv}_{\mathrm{simva}} &= \mathrm{Chv}_{\mathrm{simva}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{simva}} &= \mathrm{Ahv}_{\mathrm{simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Mhv}_{\mathrm{simva}} &= \frac{\mathrm{Ahv}_{\mathrm{simva}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Xfeces}_{\mathrm{simva}} &= \mathrm{Afeces}_{\mathrm{simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_simacid}} &= \mathrm{Cgu}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cgu}_{\mathrm{free\_simacid}} &= \mathrm{Cgu}_{\mathrm{plasma\_simacid}} \cdot \mathrm{fup}_{\mathrm{simacid}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_simacid}} &= \mathrm{Agu}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_simacid}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_simacid}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_simacid}} &= \mathrm{Cki}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cki}_{\mathrm{free\_simacid}} &= \mathrm{Cki}_{\mathrm{plasma\_simacid}} \cdot \mathrm{fup}_{\mathrm{simacid}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_simacid}} &= \mathrm{Aki}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_simacid}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_simacid}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_simacid}} &= \mathrm{Cli}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cli}_{\mathrm{free\_simacid}} &= \mathrm{Cli}_{\mathrm{plasma\_simacid}} \cdot \mathrm{fup}_{\mathrm{simacid}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_simacid}} &= \mathrm{Ali}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_simacid}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_simacid}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_simacid}} &= \mathrm{Clu}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Clu}_{\mathrm{free\_simacid}} &= \mathrm{Clu}_{\mathrm{plasma\_simacid}} \cdot \mathrm{fup}_{\mathrm{simacid}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_simacid}} &= \mathrm{Alu}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_simacid}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_simacid}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_simacid}} &= \mathrm{Cre}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cre}_{\mathrm{free\_simacid}} &= \mathrm{Cre}_{\mathrm{plasma\_simacid}} \cdot \mathrm{fup}_{\mathrm{simacid}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_simacid}} &= \mathrm{Are}_{\mathrm{plasma\_simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_simacid}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_simacid}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Aar}_{\mathrm{simacid}} &= \mathrm{Car}_{\mathrm{simacid}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{simacid}} &= \mathrm{Aar}_{\mathrm{simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mar}_{\mathrm{simacid}} &= \frac{\mathrm{Aar}_{\mathrm{simacid}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Ave}_{\mathrm{simacid}} &= \mathrm{Cve}_{\mathrm{simacid}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{simacid}} &= \mathrm{Ave}_{\mathrm{simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mve}_{\mathrm{simacid}} &= \frac{\mathrm{Ave}_{\mathrm{simacid}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Apo}_{\mathrm{simacid}} &= \mathrm{Cpo}_{\mathrm{simacid}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{simacid}} &= \mathrm{Apo}_{\mathrm{simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mpo}_{\mathrm{simacid}} &= \frac{\mathrm{Apo}_{\mathrm{simacid}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Ahv}_{\mathrm{simacid}} &= \mathrm{Chv}_{\mathrm{simacid}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{simacid}} &= \mathrm{Ahv}_{\mathrm{simacid}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Mhv}_{\mathrm{simacid}} &= \frac{\mathrm{Ahv}_{\mathrm{simacid}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{simacid}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_simmets}} &= \mathrm{Cgu}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cgu}_{\mathrm{free\_simmets}} &= \mathrm{Cgu}_{\mathrm{plasma\_simmets}} \cdot \mathrm{fup}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_simmets}} &= \mathrm{Agu}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_simmets}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_simmets}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_simmets}} &= \mathrm{Cki}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cki}_{\mathrm{free\_simmets}} &= \mathrm{Cki}_{\mathrm{plasma\_simmets}} \cdot \mathrm{fup}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_simmets}} &= \mathrm{Aki}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_simmets}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_simmets}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_simmets}} &= \mathrm{Cli}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cli}_{\mathrm{free\_simmets}} &= \mathrm{Cli}_{\mathrm{plasma\_simmets}} \cdot \mathrm{fup}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_simmets}} &= \mathrm{Ali}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_simmets}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_simmets}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_simmets}} &= \mathrm{Clu}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Clu}_{\mathrm{free\_simmets}} &= \mathrm{Clu}_{\mathrm{plasma\_simmets}} \cdot \mathrm{fup}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_simmets}} &= \mathrm{Alu}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_simmets}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_simmets}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_simmets}} &= \mathrm{Cre}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cre}_{\mathrm{free\_simmets}} &= \mathrm{Cre}_{\mathrm{plasma\_simmets}} \cdot \mathrm{fup}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_simmets}} &= \mathrm{Are}_{\mathrm{plasma\_simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_simmets}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_simmets}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Aar}_{\mathrm{simmets}} &= \mathrm{Car}_{\mathrm{simmets}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{simmets}} &= \mathrm{Aar}_{\mathrm{simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mar}_{\mathrm{simmets}} &= \frac{\mathrm{Aar}_{\mathrm{simmets}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Ave}_{\mathrm{simmets}} &= \mathrm{Cve}_{\mathrm{simmets}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{simmets}} &= \mathrm{Ave}_{\mathrm{simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mve}_{\mathrm{simmets}} &= \frac{\mathrm{Ave}_{\mathrm{simmets}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Apo}_{\mathrm{simmets}} &= \mathrm{Cpo}_{\mathrm{simmets}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{simmets}} &= \mathrm{Apo}_{\mathrm{simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mpo}_{\mathrm{simmets}} &= \frac{\mathrm{Apo}_{\mathrm{simmets}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Ahv}_{\mathrm{simmets}} &= \mathrm{Chv}_{\mathrm{simmets}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{simmets}} &= \mathrm{Ahv}_{\mathrm{simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Mhv}_{\mathrm{simmets}} &= \frac{\mathrm{Ahv}_{\mathrm{simmets}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xurine}_{\mathrm{simmets}} &= \mathrm{Aurine}_{\mathrm{simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Xfeces}_{\mathrm{simmets}} &= \mathrm{Afeces}_{\mathrm{simmets}} \cdot \mathrm{Mr}_{\mathrm{simmets}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_ldlc}} &= \mathrm{Cgu}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cgu}_{\mathrm{free\_ldlc}} &= \mathrm{Cgu}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{fup}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_ldlc}} &= \mathrm{Agu}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_ldlc}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_ldlc}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_ldlc}} &= \mathrm{Cki}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cki}_{\mathrm{free\_ldlc}} &= \mathrm{Cki}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{fup}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_ldlc}} &= \mathrm{Aki}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_ldlc}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_ldlc}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_ldlc}} &= \mathrm{Cli}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cli}_{\mathrm{free\_ldlc}} &= \mathrm{Cli}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{fup}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_ldlc}} &= \mathrm{Ali}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_ldlc}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_ldlc}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_ldlc}} &= \mathrm{Clu}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Clu}_{\mathrm{free\_ldlc}} &= \mathrm{Clu}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{fup}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_ldlc}} &= \mathrm{Alu}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_ldlc}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_ldlc}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_ldlc}} &= \mathrm{Cre}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cre}_{\mathrm{free\_ldlc}} &= \mathrm{Cre}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{fup}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_ldlc}} &= \mathrm{Are}_{\mathrm{plasma\_ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_ldlc}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_ldlc}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Aar}_{\mathrm{ldlc}} &= \mathrm{Car}_{\mathrm{ldlc}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{ldlc}} &= \mathrm{Aar}_{\mathrm{ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mar}_{\mathrm{ldlc}} &= \frac{\mathrm{Aar}_{\mathrm{ldlc}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Ave}_{\mathrm{ldlc}} &= \mathrm{Cve}_{\mathrm{ldlc}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{ldlc}} &= \mathrm{Ave}_{\mathrm{ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mve}_{\mathrm{ldlc}} &= \frac{\mathrm{Ave}_{\mathrm{ldlc}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Apo}_{\mathrm{ldlc}} &= \mathrm{Cpo}_{\mathrm{ldlc}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{ldlc}} &= \mathrm{Apo}_{\mathrm{ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mpo}_{\mathrm{ldlc}} &= \frac{\mathrm{Apo}_{\mathrm{ldlc}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Ahv}_{\mathrm{ldlc}} &= \mathrm{Chv}_{\mathrm{ldlc}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{ldlc}} &= \mathrm{Ahv}_{\mathrm{ldlc}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Mhv}_{\mathrm{ldlc}} &= \frac{\mathrm{Ahv}_{\mathrm{ldlc}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_vldlc}} &= \mathrm{Cgu}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cgu}_{\mathrm{free\_vldlc}} &= \mathrm{Cgu}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{fup}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_vldlc}} &= \mathrm{Agu}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_vldlc}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_vldlc}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_vldlc}} &= \mathrm{Cki}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cki}_{\mathrm{free\_vldlc}} &= \mathrm{Cki}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{fup}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_vldlc}} &= \mathrm{Aki}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_vldlc}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_vldlc}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_vldlc}} &= \mathrm{Cli}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cli}_{\mathrm{free\_vldlc}} &= \mathrm{Cli}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{fup}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_vldlc}} &= \mathrm{Ali}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_vldlc}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_vldlc}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_vldlc}} &= \mathrm{Clu}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Clu}_{\mathrm{free\_vldlc}} &= \mathrm{Clu}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{fup}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_vldlc}} &= \mathrm{Alu}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_vldlc}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_vldlc}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_vldlc}} &= \mathrm{Cre}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Cre}_{\mathrm{free\_vldlc}} &= \mathrm{Cre}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{fup}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_vldlc}} &= \mathrm{Are}_{\mathrm{plasma\_vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_vldlc}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_vldlc}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Aar}_{\mathrm{vldlc}} &= \mathrm{Car}_{\mathrm{vldlc}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{vldlc}} &= \mathrm{Aar}_{\mathrm{vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mar}_{\mathrm{vldlc}} &= \frac{\mathrm{Aar}_{\mathrm{vldlc}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Ave}_{\mathrm{vldlc}} &= \mathrm{Cve}_{\mathrm{vldlc}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{vldlc}} &= \mathrm{Ave}_{\mathrm{vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mve}_{\mathrm{vldlc}} &= \frac{\mathrm{Ave}_{\mathrm{vldlc}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Apo}_{\mathrm{vldlc}} &= \mathrm{Cpo}_{\mathrm{vldlc}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{vldlc}} &= \mathrm{Apo}_{\mathrm{vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mpo}_{\mathrm{vldlc}} &= \frac{\mathrm{Apo}_{\mathrm{vldlc}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Ahv}_{\mathrm{vldlc}} &= \mathrm{Chv}_{\mathrm{vldlc}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{vldlc}} &= \mathrm{Ahv}_{\mathrm{vldlc}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Mhv}_{\mathrm{vldlc}} &= \frac{\mathrm{Ahv}_{\mathrm{vldlc}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{vldlc}} \\[1ex]
\mathrm{Cve}_{\mathrm{simva\_and\_simacid}} &= \mathrm{Cve}_{\mathrm{simva}} + \mathrm{Cve}_{\mathrm{simacid}} \\[1ex]
\mathrm{Cve}_{\mathrm{active\_inhibitors}} &= \mathrm{Cve}_{\mathrm{simacid}} + \mathrm{simmets}_{\mathrm{inhibitor\_activity}} \cdot \mathrm{Cve}_{\mathrm{simmets}} \\[1ex]
\mathrm{Cve}_{\mathrm{total\_inhibitors}} &= \mathrm{Cve}_{\mathrm{simva}} + \mathrm{Cve}_{\mathrm{simacid}} + \mathrm{Cve}_{\mathrm{simmets}} \\[1ex]
\mathrm{ldlc}_{\mathrm{change}} &= \frac{\mathrm{Cve}_{\mathrm{ldlc}} - \mathrm{ldlc}_{\mathrm{init}}}{\mathrm{ldlc}_{\mathrm{init}}} \\[1ex]
v_{\mathrm{cho\_reference}} &= \frac{\frac{v_{\mathrm{cho\_ref}}}{\mathrm{Mr}_{\mathrm{ldlc}}}}{\mathrm{conversion}_{\mathrm{min\_per\_day}}} \\[1ex]
\mathrm{ldlc}_{\mathrm{loss}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{ldlc}_{\mathrm{loss\_k}} \\[1ex]
\mathrm{ldlc}_{\mathrm{diet}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{ldlc}_{\mathrm{diet\_k}} \\[1ex]
\mathrm{ldlc}_{\mathrm{utilization}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{ldlc}_{\mathrm{utilization\_Vmax}} \cdot f_{\mathrm{ldlc\_utilization\_Vmax}} \\[1ex]
v_{\mathrm{ldlc\_utilization}} &= \mathrm{ldlc}_{\mathrm{utilization}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{ldlc\_diet}} &= \mathrm{ldlc}_{\mathrm{diet}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{ldlc\_loss}} &= \mathrm{ldlc}_{\mathrm{loss}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{KI}_{\mathrm{\_GFR\_base}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_total}} &= \mathrm{LI}_{\mathrm{\_ldlr}} + \mathrm{LI}_{\mathrm{\_ldlr\_membrane}} + \mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_fraction}} &= \frac{\mathrm{LI}_{\mathrm{\_ldlr}}}{\mathrm{LI}_{\mathrm{\_ldlr\_total}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_membrane\_fraction}} &= \frac{\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}}{\mathrm{LI}_{\mathrm{\_ldlr\_total}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_ldlc\_fraction}} &= \frac{\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}}{\mathrm{LI}_{\mathrm{\_ldlr\_total}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_cho\_reference}} &= \frac{\frac{v_{\mathrm{cho\_ref}}}{\mathrm{Mr}_{\mathrm{ldlc}}}}{\mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax}} &= 0.4 \cdot \mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_reference}} &= \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_active\_inhibitors}} &= \mathrm{LI}_{\mathrm{\_simacid}} + \mathrm{simmets}_{\mathrm{inhibitor\_activity}} \cdot \mathrm{LI}_{\mathrm{\_simmets}} \\[1ex]
v_{\mathrm{ldlc\_net\_consumption}} &= \mathrm{ldlc}_{\mathrm{net\_consumption}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{vldlc\_conversion}} &= \mathrm{vldlc}_{\mathrm{conversion}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_export}} &= v_{\mathrm{LI\_\_VLDLCEXP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_uptake}} &= v_{\mathrm{LI\_\_LDLRLDLCIMP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_net\_export\_rate}} &= v_{\mathrm{LI\_\_VLDLCEXP}} - v_{\mathrm{LI\_\_LDLRLDLCIMP}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_net\_export}} &= \mathrm{LI}_{\mathrm{\_v\_net\_export\_rate}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_recycling}} &= v_{\mathrm{LI\_\_LDLRRECYCLING}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_synthesis}} &= v_{\mathrm{LI\_\_HMGCOAREDUCTASE}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_liver\_balance}} &= \mathrm{LI}_{\mathrm{\_v\_synthesis}} + \mathrm{LI}_{\mathrm{\_v\_uptake}} - \mathrm{LI}_{\mathrm{\_v\_export}} \\[1ex]
\mathrm{LI}_{\mathrm{\_TURNOVER\_LDLR}} &= v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}} - v_{\mathrm{LI\_\_DEGRADATION\_LDLR}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $\mathrm{ldlc}_{\mathrm{net\_consumption}}$ | `ldlc_net_consumption` | whole-body net consumption of plasma LDL-C | $\mathrm{Cve}_{\mathrm{ldlc}} \longrightarrow \varnothing$ |  |
| $\mathrm{vldlc}_{\mathrm{conversion}}$ | `vldlc_conversion` | VLDL-C to LDL-C conversion | $\mathrm{Cve}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{transport\_lu\_simva}}$ | `transport_lu_simva` | transport simvastatin | $\mathrm{Clu}_{\mathrm{plasma\_simva}} \rightleftharpoons \mathrm{Clu}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{transport\_re\_simva}}$ | `transport_re_simva` | transport simvastatin | $\mathrm{Cre}_{\mathrm{plasma\_simva}} \rightleftharpoons \mathrm{Cre}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{iv\_simva}}$ | `iv_simva` | iv simvastatin | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_simva}}$ | `Flow_ar_gu_simva` | inflow gut simvastatin | $\mathrm{Car}_{\mathrm{simva}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_simva}}$ | `Flow_gu_po_simva` | outflow gut simvastatin | $\mathrm{Cgu}_{\mathrm{plasma\_simva}} \longrightarrow \mathrm{Cpo}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_simva}}$ | `Flow_ar_ki_simva` | inflow kidney simvastatin | $\mathrm{Car}_{\mathrm{simva}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_simva}}$ | `Flow_ki_ve_simva` | outflow kidney simvastatin | $\mathrm{Cki}_{\mathrm{plasma\_simva}} \longrightarrow \mathrm{Cve}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{Flow\_ar\_li\_simva}}$ | `Flow_ar_li_simva` | inflow liver simvastatin | $\mathrm{Car}_{\mathrm{simva}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_simva}}$ | `Flow_po_li_simva` | outflow po simvastatin | $\mathrm{Cpo}_{\mathrm{simva}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_simva}}$ | `Flow_li_hv_simva` | outflow liver simvastatin | $\mathrm{Cli}_{\mathrm{plasma\_simva}} \longrightarrow \mathrm{Chv}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_simva}}$ | `Flow_hv_ve_simva` | outflow hepatic vein simvastatin | $\mathrm{Chv}_{\mathrm{simva}} \longrightarrow \mathrm{Cve}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_simva}}$ | `Flow_ve_lu_simva` | inflow lung simvastatin | $\mathrm{Cve}_{\mathrm{simva}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_simva}}$ | `Flow_lu_ar_simva` | outflow lung simvastatin | $\mathrm{Clu}_{\mathrm{plasma\_simva}} \longrightarrow \mathrm{Car}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_simva}}$ | `Flow_ar_re_simva` | inflow rest simvastatin | $\mathrm{Car}_{\mathrm{simva}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_simva}}$ | `Flow_re_ve_simva` | outflow rest simvastatin | $\mathrm{Cre}_{\mathrm{plasma\_simva}} \longrightarrow \mathrm{Cve}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{transport\_lu\_simacid}}$ | `transport_lu_simacid` | transport simvastatin acid | $\mathrm{Clu}_{\mathrm{plasma\_simacid}} \rightleftharpoons \mathrm{Clu}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{transport\_re\_simacid}}$ | `transport_re_simacid` | transport simvastatin acid | $\mathrm{Cre}_{\mathrm{plasma\_simacid}} \rightleftharpoons \mathrm{Cre}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_simacid}}$ | `Flow_ar_gu_simacid` | inflow gut simvastatin acid | $\mathrm{Car}_{\mathrm{simacid}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_simacid}}$ | `Flow_gu_po_simacid` | outflow gut simvastatin acid | $\mathrm{Cgu}_{\mathrm{plasma\_simacid}} \longrightarrow \mathrm{Cpo}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_simacid}}$ | `Flow_ar_ki_simacid` | inflow kidney simvastatin acid | $\mathrm{Car}_{\mathrm{simacid}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_simacid}}$ | `Flow_ki_ve_simacid` | outflow kidney simvastatin acid | $\mathrm{Cki}_{\mathrm{plasma\_simacid}} \longrightarrow \mathrm{Cve}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{Flow\_ar\_li\_simacid}}$ | `Flow_ar_li_simacid` | inflow liver simvastatin acid | $\mathrm{Car}_{\mathrm{simacid}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_simacid}}$ | `Flow_po_li_simacid` | outflow po simvastatin acid | $\mathrm{Cpo}_{\mathrm{simacid}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_simacid}}$ | `Flow_li_hv_simacid` | outflow liver simvastatin acid | $\mathrm{Cli}_{\mathrm{plasma\_simacid}} \longrightarrow \mathrm{Chv}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_simacid}}$ | `Flow_hv_ve_simacid` | outflow hepatic vein simvastatin acid | $\mathrm{Chv}_{\mathrm{simacid}} \longrightarrow \mathrm{Cve}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_simacid}}$ | `Flow_ve_lu_simacid` | inflow lung simvastatin acid | $\mathrm{Cve}_{\mathrm{simacid}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_simacid}}$ | `Flow_lu_ar_simacid` | outflow lung simvastatin acid | $\mathrm{Clu}_{\mathrm{plasma\_simacid}} \longrightarrow \mathrm{Car}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_simacid}}$ | `Flow_ar_re_simacid` | inflow rest simvastatin acid | $\mathrm{Car}_{\mathrm{simacid}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_simacid}}$ | `Flow_re_ve_simacid` | outflow rest simvastatin acid | $\mathrm{Cre}_{\mathrm{plasma\_simacid}} \longrightarrow \mathrm{Cve}_{\mathrm{simacid}}$ |  |
| $v_{\mathrm{transport\_lu\_simmets}}$ | `transport_lu_simmets` | transport simvastatin metabolites | $\mathrm{Clu}_{\mathrm{plasma\_simmets}} \rightleftharpoons \mathrm{Clu}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{transport\_re\_simmets}}$ | `transport_re_simmets` | transport simvastatin metabolites | $\mathrm{Cre}_{\mathrm{plasma\_simmets}} \rightleftharpoons \mathrm{Cre}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_simmets}}$ | `Flow_ar_gu_simmets` | inflow gut simvastatin metabolites | $\mathrm{Car}_{\mathrm{simmets}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_simmets}}$ | `Flow_gu_po_simmets` | outflow gut simvastatin metabolites | $\mathrm{Cgu}_{\mathrm{plasma\_simmets}} \longrightarrow \mathrm{Cpo}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_simmets}}$ | `Flow_ar_ki_simmets` | inflow kidney simvastatin metabolites | $\mathrm{Car}_{\mathrm{simmets}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_simmets}}$ | `Flow_ki_ve_simmets` | outflow kidney simvastatin metabolites | $\mathrm{Cki}_{\mathrm{plasma\_simmets}} \longrightarrow \mathrm{Cve}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_ar\_li\_simmets}}$ | `Flow_ar_li_simmets` | inflow liver simvastatin metabolites | $\mathrm{Car}_{\mathrm{simmets}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_simmets}}$ | `Flow_po_li_simmets` | outflow po simvastatin metabolites | $\mathrm{Cpo}_{\mathrm{simmets}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_simmets}}$ | `Flow_li_hv_simmets` | outflow liver simvastatin metabolites | $\mathrm{Cli}_{\mathrm{plasma\_simmets}} \longrightarrow \mathrm{Chv}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_simmets}}$ | `Flow_hv_ve_simmets` | outflow hepatic vein simvastatin metabolites | $\mathrm{Chv}_{\mathrm{simmets}} \longrightarrow \mathrm{Cve}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_simmets}}$ | `Flow_ve_lu_simmets` | inflow lung simvastatin metabolites | $\mathrm{Cve}_{\mathrm{simmets}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_simmets}}$ | `Flow_lu_ar_simmets` | outflow lung simvastatin metabolites | $\mathrm{Clu}_{\mathrm{plasma\_simmets}} \longrightarrow \mathrm{Car}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_simmets}}$ | `Flow_ar_re_simmets` | inflow rest simvastatin metabolites | $\mathrm{Car}_{\mathrm{simmets}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_simmets}}$ | `Flow_re_ve_simmets` | outflow rest simvastatin metabolites | $\mathrm{Cre}_{\mathrm{plasma\_simmets}} \longrightarrow \mathrm{Cve}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_ldlc}}$ | `Flow_ar_gu_ldlc` | inflow gut ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_ldlc}}$ | `Flow_gu_po_ldlc` | outflow gut ldl-cholesterol | $\mathrm{Cgu}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Cpo}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_ldlc}}$ | `Flow_ar_ki_ldlc` | inflow kidney ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_ldlc}}$ | `Flow_ki_ve_ldlc` | outflow kidney ldl-cholesterol | $\mathrm{Cki}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_li\_ldlc}}$ | `Flow_ar_li_ldlc` | inflow liver ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_ldlc}}$ | `Flow_po_li_ldlc` | outflow po ldl-cholesterol | $\mathrm{Cpo}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_ldlc}}$ | `Flow_li_hv_ldlc` | outflow liver ldl-cholesterol | $\mathrm{Cli}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_ldlc}}$ | `Flow_hv_ve_ldlc` | outflow hepatic vein ldl-cholesterol | $\mathrm{Chv}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_ldlc}}$ | `Flow_ve_lu_ldlc` | inflow lung ldl-cholesterol | $\mathrm{Cve}_{\mathrm{ldlc}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_ldlc}}$ | `Flow_lu_ar_ldlc` | outflow lung ldl-cholesterol | $\mathrm{Clu}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Car}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_ldlc}}$ | `Flow_ar_re_ldlc` | inflow rest ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_ldlc}}$ | `Flow_re_ve_ldlc` | outflow rest ldl-cholesterol | $\mathrm{Cre}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_vldlc}}$ | `Flow_ar_gu_vldlc` | inflow gut vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_vldlc}}$ | `Flow_gu_po_vldlc` | outflow gut vldl-cholesterol | $\mathrm{Cgu}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Cpo}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_vldlc}}$ | `Flow_ar_ki_vldlc` | inflow kidney vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_vldlc}}$ | `Flow_ki_ve_vldlc` | outflow kidney vldl-cholesterol | $\mathrm{Cki}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_li\_vldlc}}$ | `Flow_ar_li_vldlc` | inflow liver vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_vldlc}}$ | `Flow_po_li_vldlc` | outflow po vldl-cholesterol | $\mathrm{Cpo}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_vldlc}}$ | `Flow_li_hv_vldlc` | outflow liver vldl-cholesterol | $\mathrm{Cli}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_vldlc}}$ | `Flow_hv_ve_vldlc` | outflow hepatic vein vldl-cholesterol | $\mathrm{Chv}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_vldlc}}$ | `Flow_ve_lu_vldlc` | inflow lung vldl-cholesterol | $\mathrm{Cve}_{\mathrm{vldlc}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_vldlc}}$ | `Flow_lu_ar_vldlc` | outflow lung vldl-cholesterol | $\mathrm{Clu}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Car}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_vldlc}}$ | `Flow_ar_re_vldlc` | inflow rest vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_vldlc}}$ | `Flow_re_ve_vldlc` | outflow rest vldl-cholesterol | $\mathrm{Cre}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{dissolution\_simva}}$ | `dissolution_simva` | dissolution simvastatin | $\mathrm{Astomach}_{\mathrm{simva}} \longrightarrow \mathrm{Cgulumen}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{KI\_\_SIMMETSEX}}$ | `KI__SIMMETSEX` | renal excretion simvastatin metabolites | $\mathrm{Cki}_{\mathrm{plasma\_simmets}} \longrightarrow \mathrm{Aurine}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{LI\_\_SIMVAIMP}}$ | `LI__SIMVAIMP` | SV import | $\mathrm{Cli}_{\mathrm{plasma\_simva}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_simva}}$ |  |
| $v_{\mathrm{LI\_\_SIMACIDIMP}}$ | `LI__SIMACIDIMP` | SVA import (OATP1B1) | $\mathrm{Cli}_{\mathrm{plasma\_simacid}} \longrightarrow \mathrm{LI}_{\mathrm{\_simacid}}$ |  |
| $v_{\mathrm{LI\_\_SIMACIDEXP}}$ | `LI__SIMACIDEXP` | SVA efflux | $\mathrm{LI}_{\mathrm{\_simacid}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_simacid}}$ |  |
| $v_{\mathrm{LI\_\_SIMMETSEXP}}$ | `LI__SIMMETSEXP` | SVM exchange | $\mathrm{LI}_{\mathrm{\_simmets}} \rightleftharpoons \mathrm{Cli}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{LI\_\_ESTERASE}}$ | `LI__ESTERASE` | Esterase: SV to SVA | $\mathrm{LI}_{\mathrm{\_simva}} \longrightarrow \mathrm{LI}_{\mathrm{\_simacid}}$ |  |
| $v_{\mathrm{LI\_\_SIMVA\_CYP3A4}}$ | `LI__SIMVA_CYP3A4` | CYP3A4: SV to SVM | $\mathrm{LI}_{\mathrm{\_simva}} \longrightarrow \mathrm{LI}_{\mathrm{\_simmets}}$ |  |
| $v_{\mathrm{LI\_\_SIMACID\_CYP3A4}}$ | `LI__SIMACID_CYP3A4` | CYP3A4: SVA to SVM | $\mathrm{LI}_{\mathrm{\_simacid}} \longrightarrow \mathrm{LI}_{\mathrm{\_simmets}}$ |  |
| $v_{\mathrm{LI\_\_SIMACIDMET}}$ | `LI__SIMACIDMET` | SVA to SVM (glucuronidation, CYP2C8) | $\mathrm{LI}_{\mathrm{\_simacid}} \longrightarrow \mathrm{LI}_{\mathrm{\_simmets}}$ |  |
| $v_{\mathrm{LI\_\_EHC\_simmets}}$ | `LI__EHC_simmets` | EHC SVM | $\mathrm{LI}_{\mathrm{\_simmets}} \longrightarrow \mathrm{Cgulumen}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{LI\_\_VLDLCEXP}}$ | `LI__VLDLCEXP` | VLDL-cholesterol export | $\mathrm{LI}_{\mathrm{\_cho}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{LI\_\_LDLRLDLCIMP}}$ | `LI__LDLRLDLCIMP` | LDLR-LDLC binding &amp; internalization | $\mathrm{Cli}_{\mathrm{plasma\_ldlc}} + \mathrm{LI}_{\mathrm{\_ldlr\_membrane}} \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}$ | $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}$ |
| $v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}}$ | `LI__LDLR_TO_MEMBRANE` | LDLR membrane transport | $\mathrm{LI}_{\mathrm{\_ldlr}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_ldlr\_membrane}}$ |  |
| $v_{\mathrm{LI\_\_LDLRRECYCLING}}$ | `LI__LDLRRECYCLING` | LDLR recycling | $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr}} + \mathrm{LI}_{\mathrm{\_cho}}$ |  |
| $v_{\mathrm{LI\_\_HMGCOASYNTHASE}}$ | `LI__HMGCOASYNTHASE` | HMG-CoA synthase | $3 \, \mathrm{LI}_{\mathrm{\_acoa}} \longrightarrow \mathrm{LI}_{\mathrm{\_hmgcoa}}$ | $\mathrm{LI}_{\mathrm{\_hmgcoasynthase}}, \mathrm{LI}_{\mathrm{\_hmgcoa}}$ |
| $v_{\mathrm{LI\_\_HMGCOAREDUCTASE}}$ | `LI__HMGCOAREDUCTASE` | HMG-CoA reductase | $6 \, \mathrm{LI}_{\mathrm{\_hmgcoa}} \longrightarrow \mathrm{LI}_{\mathrm{\_cho}}$ | $\mathrm{LI}_{\mathrm{\_simacid}}, \mathrm{LI}_{\mathrm{\_simmets}}, \mathrm{LI}_{\mathrm{\_hmgcoareductase}}$ |
| $v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOAREDUCTASE}}$ | `LI__SYNTHESIS_HMGCOAREDUCTASE` | HMGCOAREDUCTASE synthesis | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_hmgcoareductase}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_DEGRADATION\_HMGCOAREDUCTASE}}$ | `LI__DEGRADATION_HMGCOAREDUCTASE` | HMGCOAREDUCTASE degradation | $\mathrm{LI}_{\mathrm{\_hmgcoareductase}} \longrightarrow \varnothing$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOASYNTHASE}}$ | `LI__SYNTHESIS_HMGCOASYNTHASE` | HMGCOASYNTHASE synthesis | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_hmgcoasynthase}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_DEGRADATION\_HMGCOASYNTHASE}}$ | `LI__DEGRADATION_HMGCOASYNTHASE` | HMGCOASYNTHASE degradation | $\mathrm{LI}_{\mathrm{\_hmgcoasynthase}} \longrightarrow \varnothing$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}}$ | `LI__SYNTHESIS_LDLR` | LDLR synthesis | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_DEGRADATION\_LDLR}}$ | `LI__DEGRADATION_LDLR` | LDLR degradation | $\mathrm{LI}_{\mathrm{\_ldlr}} \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr\_degraded}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{GU\_\_SIMVAABS}}$ | `GU__SIMVAABS` | absorption simvastatin | $\mathrm{Cgulumen}_{\mathrm{simva}} \longrightarrow \mathrm{GU}_{\mathrm{\_simva}}$ |  |
| $v_{\mathrm{GU\_\_SIMVAEXC}}$ | `GU__SIMVAEXC` | excretion simvastatin (feces) | $\mathrm{Cgulumen}_{\mathrm{simva}} \longrightarrow \mathrm{Afeces}_{\mathrm{simva}}$ |  |
| $v_{\mathrm{GU\_\_SIMMETSABS}}$ | `GU__SIMMETSABS` | absorption simvastatin metabolites | $\mathrm{Cgulumen}_{\mathrm{simmets}} \longrightarrow \mathrm{GU}_{\mathrm{\_simmets}}$ |  |
| $v_{\mathrm{GU\_\_SIMMETSEXC}}$ | `GU__SIMMETSEXC` | excretion simvastatin metabolites (feces) | $\mathrm{Cgulumen}_{\mathrm{simmets}} \longrightarrow \mathrm{Afeces}_{\mathrm{simmets}}$ |  |
| $v_{\mathrm{GU\_\_SIMVAEXP}}$ | `GU__SIMVAEXP` | SV export | $\mathrm{GU}_{\mathrm{\_simva}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_simva}}$ |  |
| $v_{\mathrm{GU\_\_SIMMETSEXP}}$ | `GU__SIMMETSEXP` | SVM export | $\mathrm{GU}_{\mathrm{\_simmets}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_simmets}}$ |  |
| $v_{\mathrm{GU\_\_SIMVA\_CYP3A4}}$ | `GU__SIMVA_CYP3A4` | CYP3A4: SV to SVM | $\mathrm{GU}_{\mathrm{\_simva}} \longrightarrow \mathrm{GU}_{\mathrm{\_simmets}}$ |  |

The rates of the reactions are:

$$
\begin{aligned}
\mathrm{ldlc}_{\mathrm{net\_consumption}} &= \mathopen{}\left(\mathrm{ldlc}_{\mathrm{utilization}} + \mathrm{ldlc}_{\mathrm{loss}}\right) \cdot \mathopen{}\left(1 + \frac{\mathrm{Cve}_{\mathrm{ldlc}}}{\mathrm{ldlc}_{\mathrm{consumption\_Km}}}\right) - \mathrm{ldlc}_{\mathrm{diet}} \\[1ex]
\mathrm{vldlc}_{\mathrm{conversion}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{vldlc}_{\mathrm{conversion\_k}} \cdot \mathrm{Cve}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{transport\_lu\_simva}} &= \frac{\mathrm{ftissue}_{\mathrm{simva}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_simva}} - \frac{\mathrm{Clu}_{\mathrm{simva}}}{\mathrm{Kp}_{\mathrm{simva}}}\right) \\[1ex]
v_{\mathrm{transport\_re\_simva}} &= \frac{\mathrm{ftissue}_{\mathrm{simva}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_simva}} - \frac{\mathrm{Cre}_{\mathrm{simva}}}{\mathrm{Kp}_{\mathrm{simva}}}\right) \\[1ex]
v_{\mathrm{iv\_simva}} &= \frac{\mathrm{Ki}_{\mathrm{simva}} \cdot \mathrm{IVDOSE}_{\mathrm{simva}}}{\mathrm{Mr}_{\mathrm{simva}}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_simva}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_simva}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_simva}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_simva}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_simva}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_simva}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_simva}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_simva}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_simva}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_simva}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_simva}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_simva}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_simva}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_simva}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_simva}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_simva}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_simva}} \\[1ex]
v_{\mathrm{transport\_lu\_simacid}} &= \frac{\mathrm{ftissue}_{\mathrm{simacid}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_simacid}} - \frac{\mathrm{Clu}_{\mathrm{simacid}}}{\mathrm{Kp}_{\mathrm{simacid}}}\right) \\[1ex]
v_{\mathrm{transport\_re\_simacid}} &= \frac{\mathrm{ftissue}_{\mathrm{simacid}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_simacid}} - \frac{\mathrm{Cre}_{\mathrm{simacid}}}{\mathrm{Kp}_{\mathrm{simacid}}}\right) \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_simacid}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_simacid}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_simacid}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_simacid}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_simacid}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_simacid}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_simacid}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_simacid}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_simacid}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_simacid}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_simacid}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_simacid}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_simacid}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_simacid}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_simacid}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{simacid}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_simacid}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_simacid}} \\[1ex]
v_{\mathrm{transport\_lu\_simmets}} &= \frac{\mathrm{ftissue}_{\mathrm{simmets}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_simmets}} - \frac{\mathrm{Clu}_{\mathrm{simmets}}}{\mathrm{Kp}_{\mathrm{simmets}}}\right) \\[1ex]
v_{\mathrm{transport\_re\_simmets}} &= \frac{\mathrm{ftissue}_{\mathrm{simmets}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_simmets}} - \frac{\mathrm{Cre}_{\mathrm{simmets}}}{\mathrm{Kp}_{\mathrm{simmets}}}\right) \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_simmets}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_simmets}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_simmets}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_simmets}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_simmets}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_simmets}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_simmets}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_simmets}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_simmets}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_simmets}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_simmets}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_simmets}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_simmets}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_simmets}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_simmets}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_simmets}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_simmets}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_ldlc}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_ldlc}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_ldlc}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_ldlc}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_ldlc}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_ldlc}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_ldlc}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_ldlc}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_ldlc}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_ldlc}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_ldlc}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_ldlc}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_vldlc}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_vldlc}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_vldlc}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_vldlc}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_li\_vldlc}} &= \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_vldlc}} &= \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_vldlc}} &= \mathrm{Qh} \cdot \mathrm{Cli}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_vldlc}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_vldlc}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_vldlc}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_vldlc}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_vldlc}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{dissolution\_simva}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_simva}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{simva}}}{\mathrm{Mr}_{\mathrm{simva}}} \\[1ex]
v_{\mathrm{KI\_\_SIMMETSEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fup}_{\mathrm{simmets}} \cdot \mathrm{KI}_{\mathrm{\_SIMMETSEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_simmets}} \\[1ex]
v_{\mathrm{LI\_\_SIMVAIMP}} &= \frac{\frac{\mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SIMVAIMP\_Vmax}}}{\mathrm{LI}_{\mathrm{\_SIMVAIMP\_Km}}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_simva}} - \mathrm{LI}_{\mathrm{\_simva}}\right)}{1 + \frac{\mathrm{Cli}_{\mathrm{plasma\_simva}}}{\mathrm{LI}_{\mathrm{\_SIMVAIMP\_Km}}} + \frac{\mathrm{LI}_{\mathrm{\_simva}}}{\mathrm{LI}_{\mathrm{\_SIMVAIMP\_Km}}}} \\[1ex]
v_{\mathrm{LI\_\_SIMACIDIMP}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_oatp1b1}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SIMACIDIMP\_Vmax}} \cdot \mathrm{Cli}_{\mathrm{plasma\_simacid}}}{\mathrm{Cli}_{\mathrm{plasma\_simacid}} + \mathrm{LI}_{\mathrm{\_SIMACIDIMP\_Km}}} \\[1ex]
v_{\mathrm{LI\_\_SIMACIDEXP}} &= \mathrm{LI}_{\mathrm{\_SIMACIDEXP\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_simacid}} \\[1ex]
v_{\mathrm{LI\_\_SIMMETSEXP}} &= \frac{\frac{\mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SIMMETSEXP\_Vmax}}}{\mathrm{LI}_{\mathrm{\_SIMMETSEXP\_Km}}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_simmets}} - \mathrm{Cli}_{\mathrm{plasma\_simmets}}\right)}{1 + \frac{\mathrm{Cli}_{\mathrm{plasma\_simmets}}}{\mathrm{LI}_{\mathrm{\_SIMMETSEXP\_Km}}} + \frac{\mathrm{LI}_{\mathrm{\_simmets}}}{\mathrm{LI}_{\mathrm{\_SIMMETSEXP\_Km}}}} \\[1ex]
v_{\mathrm{LI\_\_ESTERASE}} &= \frac{\mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_ESTERASE\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_simva}}}{\mathrm{LI}_{\mathrm{\_simva}} + \mathrm{LI}_{\mathrm{\_ESTERASE\_Km}}} \\[1ex]
v_{\mathrm{LI\_\_SIMVA\_CYP3A4}} &= \frac{\mathopen{}\left(\mathrm{LI}_{\mathrm{\_f\_cyp3a4}} + r_{\mathrm{cyp3a5}} \cdot f_{\mathrm{cyp3a5}}\right) \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SIMVA\_CYP3A4\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_simva}}}{\mathrm{LI}_{\mathrm{\_simva}} + \mathrm{CYP3A4}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{LI\_\_SIMACID\_CYP3A4}} &= \frac{\mathopen{}\left(\mathrm{LI}_{\mathrm{\_f\_cyp3a4}} + r_{\mathrm{cyp3a5}} \cdot f_{\mathrm{cyp3a5}}\right) \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SIMACID\_CYP3A4\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_simacid}}}{\mathrm{LI}_{\mathrm{\_simacid}} + \mathrm{CYP3A4}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{LI\_\_SIMACIDMET}} &= \mathrm{LI}_{\mathrm{\_f\_ugt}} \cdot \mathrm{LI}_{\mathrm{\_SIMACIDMET\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_simacid}} \\[1ex]
v_{\mathrm{LI\_\_EHC\_simmets}} &= \mathrm{LI}_{\mathrm{\_EHC\_simmets\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_simmets}} \\[1ex]
v_{\mathrm{LI\_\_VLDLCEXP}} &= \frac{\mathrm{LI}_{\mathrm{\_VLDLCEXP\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_cho}} + \mathrm{LI}_{\mathrm{\_VLDLCEXP\_Km\_cho}}} \\[1ex]
v_{\mathrm{LI\_\_LDLRLDLCIMP}} &= \frac{\frac{\mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat\_f}} \cdot \mathrm{LI}_{\mathrm{\_ldlr\_membrane}} \cdot \mathrm{Cli}_{\mathrm{plasma\_ldlc}}}{\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km}} \cdot \mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km\_f}} + \mathrm{Cli}_{\mathrm{plasma\_ldlc}}} \cdot 1}{1 + \frac{\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}}{\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Ki\_ldlr\_ldlc}}}} \\[1ex]
v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat\_f}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_ldlr}} - \frac{\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}}{\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Keq}}}\right) \\[1ex]
v_{\mathrm{LI\_\_LDLRRECYCLING}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat\_f}} \cdot \mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} \\[1ex]
v_{\mathrm{LI\_\_HMGCOASYNTHASE}} &= \frac{\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoasynthase}} \cdot \mathrm{LI}_{\mathrm{\_acoa}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_hmgcoa}}}{\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Ki\_hmgcoa}}}} \\[1ex]
v_{\mathrm{LI\_\_HMGCOAREDUCTASE}} &= \frac{\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoareductase}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoa}}}{\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Km}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_simacid}} + \mathrm{simmets}_{\mathrm{inhibitor\_activity}} \cdot \mathrm{LI}_{\mathrm{\_simmets}}}{\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Ki\_simacid}}}\right) + \mathrm{LI}_{\mathrm{\_hmgcoa}}} \\[1ex]
v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOAREDUCTASE}} &= \frac{\mathrm{LI}_{\mathrm{\_SYNTHESIS\_HMG\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}} \\[1ex]
v_{\mathrm{LI\_\_DEGRADATION\_HMGCOAREDUCTASE}} &= \mathrm{LI}_{\mathrm{\_DEGRADATION\_HMG\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoareductase}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}\right) \\[1ex]
v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOASYNTHASE}} &= \frac{\mathrm{LI}_{\mathrm{\_SYNTHESIS\_HMG\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}} \\[1ex]
v_{\mathrm{LI\_\_DEGRADATION\_HMGCOASYNTHASE}} &= \mathrm{LI}_{\mathrm{\_DEGRADATION\_HMG\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoasynthase}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}\right) \\[1ex]
v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}} &= \frac{\mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax\_f}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_LDLR\_kr\_cho}}}} \\[1ex]
v_{\mathrm{LI\_\_DEGRADATION\_LDLR}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax\_f}} \cdot \mathrm{LI}_{\mathrm{\_ldlr}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_LDLR\_kr\_cho}}}\right) \\[1ex]
v_{\mathrm{GU\_\_SIMVAABS}} &= \frac{\mathrm{GU}_{\mathrm{\_F\_abs\_simva}} \cdot \mathrm{GU}_{\mathrm{\_SIMVAABS\_k}}}{60} \cdot \mathrm{Vgulumen} \cdot \mathrm{Cgulumen}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{GU\_\_SIMVAEXC}} &= \frac{\mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_abs\_simva}}\right) \cdot \mathrm{GU}_{\mathrm{\_SIMVAABS\_k}}}{60} \cdot \mathrm{Vgulumen} \cdot \mathrm{Cgulumen}_{\mathrm{simva}} \\[1ex]
v_{\mathrm{GU\_\_SIMMETSABS}} &= \frac{\mathrm{GU}_{\mathrm{\_F\_abs\_simmets}} \cdot \mathrm{GU}_{\mathrm{\_SIMMETSABS\_k}}}{60} \cdot \mathrm{Vgulumen} \cdot \mathrm{Cgulumen}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{GU\_\_SIMMETSEXC}} &= \frac{\mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_abs\_simmets}}\right) \cdot \mathrm{GU}_{\mathrm{\_SIMMETSABS\_k}}}{60} \cdot \mathrm{Vgulumen} \cdot \mathrm{Cgulumen}_{\mathrm{simmets}} \\[1ex]
v_{\mathrm{GU\_\_SIMVAEXP}} &= \frac{\mathrm{Vgu}_{\mathrm{tissue}} \cdot \mathrm{GU}_{\mathrm{\_SIMVAEXP\_Vmax}} \cdot \mathrm{GU}_{\mathrm{\_simva}}}{\mathrm{GU}_{\mathrm{\_SIMVAEXP\_Km}} + \mathrm{GU}_{\mathrm{\_simva}}} \\[1ex]
v_{\mathrm{GU\_\_SIMMETSEXP}} &= \frac{\mathrm{Vgu}_{\mathrm{tissue}} \cdot \mathrm{GU}_{\mathrm{\_SIMMETSEXP\_Vmax}} \cdot \mathrm{GU}_{\mathrm{\_simmets}}}{\mathrm{GU}_{\mathrm{\_simmets}} + \mathrm{GU}_{\mathrm{\_SIMMETSEXP\_Km}}} \\[1ex]
v_{\mathrm{GU\_\_SIMVA\_CYP3A4}} &= \frac{\mathopen{}\left(\mathrm{GU}_{\mathrm{\_f\_cyp3a4}} + r_{\mathrm{cyp3a5}} \cdot f_{\mathrm{cyp3a5}}\right) \cdot \mathrm{Vgu}_{\mathrm{tissue}} \cdot \mathrm{GU}_{\mathrm{\_SIMVA\_CYP3A4\_Vmax}} \cdot \mathrm{GU}_{\mathrm{\_simva}}}{\mathrm{GU}_{\mathrm{\_simva}} + \mathrm{CYP3A4}_{\mathrm{Km}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_simva}} - v_{\mathrm{Flow\_gu\_po\_simva}} + v_{\mathrm{GU\_\_SIMVAEXP}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_simva}} - v_{\mathrm{Flow\_ki\_ve\_simva}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_li\_simva}} + v_{\mathrm{Flow\_po\_li\_simva}} - v_{\mathrm{Flow\_li\_hv\_simva}} - v_{\mathrm{LI\_\_SIMVAIMP}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_simva}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_simva}} + v_{\mathrm{Flow\_ve\_lu\_simva}} - v_{\mathrm{Flow\_lu\_ar\_simva}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_simva}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_simva}} + v_{\mathrm{Flow\_ar\_re\_simva}} - v_{\mathrm{Flow\_re\_ve\_simva}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_simva}} - v_{\mathrm{Flow\_ar\_ki\_simva}} - v_{\mathrm{Flow\_ar\_li\_simva}} + v_{\mathrm{Flow\_lu\_ar\_simva}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_re\_simva}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_simva}} + v_{\mathrm{Flow\_ki\_ve\_simva}} + v_{\mathrm{Flow\_hv\_ve\_simva}} - v_{\mathrm{Flow\_ve\_lu\_simva}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_simva}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_simva}} - v_{\mathrm{Flow\_po\_li\_simva}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_simva}} - v_{\mathrm{Flow\_hv\_ve\_simva}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_simva}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_simva}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{simva}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_SIMVAEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgulumen}_{\mathrm{simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{dissolution\_simva}} - v_{\mathrm{GU\_\_SIMVAABS}} - v_{\mathrm{GU\_\_SIMVAEXC}}}{\mathrm{Vgulumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_simacid}} - v_{\mathrm{Flow\_gu\_po\_simacid}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_simacid}} - v_{\mathrm{Flow\_ki\_ve\_simacid}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_simacid}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vli}_{\mathrm{plasma}}} \Bigl( v_{\mathrm{Flow\_ar\_li\_simacid}} + v_{\mathrm{Flow\_po\_li\_simacid}} - v_{\mathrm{Flow\_li\_hv\_simacid}} - v_{\mathrm{LI\_\_SIMACIDIMP}} \\
&\quad {} + v_{\mathrm{LI\_\_SIMACIDEXP}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_simacid}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_simacid}} + v_{\mathrm{Flow\_ve\_lu\_simacid}} - v_{\mathrm{Flow\_lu\_ar\_simacid}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_simacid}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_simacid}} + v_{\mathrm{Flow\_ar\_re\_simacid}} - v_{\mathrm{Flow\_re\_ve\_simacid}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{simacid}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_simacid}} - v_{\mathrm{Flow\_ar\_ki\_simacid}} - v_{\mathrm{Flow\_ar\_li\_simacid}} + v_{\mathrm{Flow\_lu\_ar\_simacid}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_re\_simacid}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_simacid}} + v_{\mathrm{Flow\_hv\_ve\_simacid}} - v_{\mathrm{Flow\_ve\_lu\_simacid}} + v_{\mathrm{Flow\_re\_ve\_simacid}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_simacid}} - v_{\mathrm{Flow\_po\_li\_simacid}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_simacid}} - v_{\mathrm{Flow\_hv\_ve\_simacid}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_simacid}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{simacid}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_simacid}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_simmets}} - v_{\mathrm{Flow\_gu\_po\_simmets}} + v_{\mathrm{GU\_\_SIMMETSEXP}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_simmets}} - v_{\mathrm{Flow\_ki\_ve\_simmets}} - v_{\mathrm{KI\_\_SIMMETSEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_li\_simmets}} + v_{\mathrm{Flow\_po\_li\_simmets}} - v_{\mathrm{Flow\_li\_hv\_simmets}} + v_{\mathrm{LI\_\_SIMMETSEXP}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_simmets}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_simmets}} + v_{\mathrm{Flow\_ve\_lu\_simmets}} - v_{\mathrm{Flow\_lu\_ar\_simmets}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_simmets}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_simmets}} + v_{\mathrm{Flow\_ar\_re\_simmets}} - v_{\mathrm{Flow\_re\_ve\_simmets}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_simmets}} - v_{\mathrm{Flow\_ar\_ki\_simmets}} - v_{\mathrm{Flow\_ar\_li\_simmets}} + v_{\mathrm{Flow\_lu\_ar\_simmets}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_re\_simmets}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_simmets}} + v_{\mathrm{Flow\_hv\_ve\_simmets}} - v_{\mathrm{Flow\_ve\_lu\_simmets}} + v_{\mathrm{Flow\_re\_ve\_simmets}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_simmets}} - v_{\mathrm{Flow\_po\_li\_simmets}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_simmets}} - v_{\mathrm{Flow\_hv\_ve\_simmets}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_simmets}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_simmets}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{simmets}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_SIMMETSEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{simmets}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_SIMMETSEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgulumen}_{\mathrm{simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_EHC\_simmets}} - v_{\mathrm{GU\_\_SIMMETSABS}} - v_{\mathrm{GU\_\_SIMMETSEXC}}}{\mathrm{Vgulumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_ldlc}} - v_{\mathrm{Flow\_gu\_po\_ldlc}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_ldlc}} - v_{\mathrm{Flow\_ki\_ve\_ldlc}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_li\_ldlc}} + v_{\mathrm{Flow\_po\_li\_ldlc}} - v_{\mathrm{Flow\_li\_hv\_ldlc}} - v_{\mathrm{LI\_\_LDLRLDLCIMP}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_ldlc}} - v_{\mathrm{Flow\_lu\_ar\_ldlc}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_ldlc}} - v_{\mathrm{Flow\_re\_ve\_ldlc}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_ldlc}} - v_{\mathrm{Flow\_ar\_ki\_ldlc}} - v_{\mathrm{Flow\_ar\_li\_ldlc}} + v_{\mathrm{Flow\_lu\_ar\_ldlc}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_re\_ldlc}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( -\mathrm{ldlc}_{\mathrm{net\_consumption}} + \mathrm{vldlc}_{\mathrm{conversion}} + v_{\mathrm{Flow\_ki\_ve\_ldlc}} + v_{\mathrm{Flow\_hv\_ve\_ldlc}} \\
&\quad {} - v_{\mathrm{Flow\_ve\_lu\_ldlc}} + v_{\mathrm{Flow\_re\_ve\_ldlc}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_ldlc}} - v_{\mathrm{Flow\_po\_li\_ldlc}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_ldlc}} - v_{\mathrm{Flow\_hv\_ve\_ldlc}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_vldlc}} - v_{\mathrm{Flow\_gu\_po\_vldlc}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_vldlc}} - v_{\mathrm{Flow\_ki\_ve\_vldlc}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_li\_vldlc}} + v_{\mathrm{Flow\_po\_li\_vldlc}} - v_{\mathrm{Flow\_li\_hv\_vldlc}} + v_{\mathrm{LI\_\_VLDLCEXP}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_vldlc}} - v_{\mathrm{Flow\_lu\_ar\_vldlc}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_vldlc}} - v_{\mathrm{Flow\_re\_ve\_vldlc}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_vldlc}} - v_{\mathrm{Flow\_ar\_ki\_vldlc}} - v_{\mathrm{Flow\_ar\_li\_vldlc}} + v_{\mathrm{Flow\_lu\_ar\_vldlc}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_re\_vldlc}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( -\mathrm{vldlc}_{\mathrm{conversion}} + v_{\mathrm{Flow\_ki\_ve\_vldlc}} + v_{\mathrm{Flow\_hv\_ve\_vldlc}} - v_{\mathrm{Flow\_ve\_lu\_vldlc}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_vldlc}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_vldlc}} - v_{\mathrm{Flow\_po\_li\_vldlc}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_li\_hv\_vldlc}} - v_{\mathrm{Flow\_hv\_ve\_vldlc}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_simacid}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vli}_{\mathrm{tissue}}} \Bigl( v_{\mathrm{LI\_\_SIMACIDIMP}} - v_{\mathrm{LI\_\_SIMACIDEXP}} + v_{\mathrm{LI\_\_ESTERASE}} - v_{\mathrm{LI\_\_SIMACID\_CYP3A4}} \\
&\quad {} - v_{\mathrm{LI\_\_SIMACIDMET}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_simmets}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vli}_{\mathrm{tissue}}} \Bigl( -v_{\mathrm{LI\_\_SIMMETSEXP}} + v_{\mathrm{LI\_\_SIMVA\_CYP3A4}} + v_{\mathrm{LI\_\_SIMACID\_CYP3A4}} + v_{\mathrm{LI\_\_SIMACIDMET}} \\
&\quad {} - v_{\mathrm{LI\_\_EHC\_simmets}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_SIMVAIMP}} - v_{\mathrm{LI\_\_ESTERASE}} - v_{\mathrm{LI\_\_SIMVA\_CYP3A4}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_hmgcoa}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_HMGCOASYNTHASE}} - 6 \cdot v_{\mathrm{LI\_\_HMGCOAREDUCTASE}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{LI\_\_VLDLCEXP}} + v_{\mathrm{LI\_\_LDLRRECYCLING}} + v_{\mathrm{LI\_\_HMGCOAREDUCTASE}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_hmgcoareductase}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOAREDUCTASE}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_HMGCOAREDUCTASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_hmgcoasynthase}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOASYNTHASE}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_HMGCOASYNTHASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr}}}{\mathrm{d} t} &= -\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}} + \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRRECYCLING}} + \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_LDLR}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}}{\mathrm{d} t} &= -\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRLDLCIMP}} + \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRLDLCIMP}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRRECYCLING}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr\_degraded}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_LDLR}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_simva}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_SIMVAABS}} - v_{\mathrm{GU\_\_SIMVAEXP}} - v_{\mathrm{GU\_\_SIMVA\_CYP3A4}}}{\mathrm{Vgu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_simmets}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_SIMMETSABS}} - v_{\mathrm{GU\_\_SIMMETSEXP}} + v_{\mathrm{GU\_\_SIMVA\_CYP3A4}}}{\mathrm{Vgu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{simva}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} + \mathrm{Ri}_{\mathrm{simva}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cum}_{\mathrm{dose\_simva}}}{\mathrm{d} t} &= \mathrm{Ri}_{\mathrm{simva}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{simva}}}{\mathrm{d} t} &= -v_{\mathrm{dissolution\_simva}} \cdot \mathrm{Mr}_{\mathrm{simva}} \qquad \text{(rate rule)}
\end{aligned}
$$
