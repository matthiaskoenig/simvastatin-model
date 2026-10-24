# Model for simvastatin and cholesterol metabolism in the liver

Model `simvastatin_liver`, SBML Level 3 Version 2, read from simvastatin\_liver.xml, written by sbmlode 0.3.0.

Model for simvastatin and cholesterol metabolism in the liver

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vbaso}$ | `Vbaso` | basolateral membrane | $1$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vapical}$ | `Vapical` | apical membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vli}$ | `Vli` | liver | $1.5$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{simacid}$ | `simacid` | simvastatin acid (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{simmets}$ | `simmets` | simvastatin metabolites (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{simva}_{\mathrm{ext}}$ | `simva_ext` | simvastatin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{simacid}_{\mathrm{ext}}$ | `simacid_ext` | simvastatin acid (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{simmets}_{\mathrm{ext}}$ | `simmets_ext` | simvastatin metabolites (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{simva}$ | `simva` | simvastatin (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{simmets}_{\mathrm{lumen}}$ | `simmets_lumen` | simvastatin metabolites (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{ldlc}_{\mathrm{ext}}$ | `ldlc_ext` | ldl-cholesterol (plasma) | $\mathrm{Vext}$ | $3$ | mmol/l | concentration, boundary |
| $\mathrm{vldlc}_{\mathrm{ext}}$ | `vldlc_ext` | vldl-cholesterol (plasma) | $\mathrm{Vext}$ | $1$ | mmol/l | concentration |
| $\mathrm{acoa}$ | `acoa` | acetyl-CoA (liver) | $\mathrm{Vli}$ | $0.043$ | mmol/l | concentration, boundary |
| $\mathrm{hmgcoa}$ | `hmgcoa` | HMG-CoA (liver) | $\mathrm{Vli}$ | $0.022$ | mmol/l | concentration |
| $\mathrm{cho}$ | `cho` | cholesterol (liver) | $\mathrm{Vli}$ | $0.02$ | mmol/l | concentration |
| $\mathrm{hmgcoareductase}$ | `hmgcoareductase` | HMG-CoA reductase (liver) | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{hmgcoasynthase}$ | `hmgcoasynthase` | HMG-CoA synthase (liver) | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{ldlr}$ | `ldlr` | LDLR | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{ldlr}_{\mathrm{membrane}}$ | `ldlr_membrane` | LDLR membrane | $\mathrm{Vbaso}$ |  | \- | amount |
| $\mathrm{ldlr}_{\mathrm{ldlc}}$ | `ldlr_ldlc` | LDLR-LDLC complex | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{ldlr}_{\mathrm{degraded}}$ | `ldlr_degraded` | LDLR degraded | $\mathrm{Vli}$ |  | \- | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{CYP3A4}_{\mathrm{Km}}$ | `CYP3A4_Km` | Km CYP3A4 | $0.025$ | mmol/l | ✓ |
| $f_{\mathrm{cyp3a4}}$ | `f_cyp3a4` | activity of CYP3A4 (liver) | $1$ | \- | ✓ |
| $f_{\mathrm{cyp3a5}}$ | `f_cyp3a5` | functional CYP3A5 | $0$ | \- | ✓ |
| $r_{\mathrm{cyp3a5}}$ | `r_cyp3a5` | capacity of CYP3A5 \*1/\*1 relative to CYP3A4 | $1$ | \- | ✓ |
| $f_{\mathrm{ugt}}$ | `f_ugt` | activity of the glucuronidation and CYP2C8 of simvastatin acid | $1$ | \- | ✓ |
| $f_{\mathrm{oatp1b1}}$ | `f_oatp1b1` | activity of OATP1B1 | $1$ | \- | ✓ |
| $\mathrm{cf}_{\mathrm{units\_per\_mmole}}$ | `cf_units_per_mmole` | conversion factor for dimensionless species | $1$ | 1/mmol | ✓ |
| $\mathrm{conversion}_{\mathrm{min\_per\_day}}$ | `conversion_min_per_day` | conversion factor min to hours | $1440$ | min/day | ✓ |
| $\mathrm{simmets}_{\mathrm{inhibitor\_activity}}$ | `simmets_inhibitor_activity` | HMG-CoA Reductase inhibitor activity of simmets | $0.4$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{ldlc}}$ | `Mr_ldlc` | Molecular weight cho \[g/mole\] | $386.654$ | g/mol | ✓ |
| $v_{\mathrm{cho\_ref}}$ | `v_cho_ref` | reference cholesterol turnover \[mg/day\] | $1000$ | mg/day | ✓ |
| $\mathrm{SYNTHESIS}_{\mathrm{HMG\_Vmax}}$ | `SYNTHESIS_HMG_Vmax` | Protein synthesis Vmax for HMGR and HMGS | $0.001$ | mmol/min/l | ✓ |
| $\mathrm{DEGRADATION}_{\mathrm{HMG\_Vmax}}$ | `DEGRADATION_HMG_Vmax` | Protein degradation Vmax for HMGR and HMGS | $0.0003$ | mmol/min/l | ✓ |
| $\mathrm{HMG}_{\mathrm{kr\_cho}}$ | `HMG_kr_cho` | Protein regulation kr for HMGR and HMGS | $0.02$ | mmol/l | ✓ |
| $\mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax}}$ | `DEGRADATION_LDLR_Vmax` | Protein degradation Vmax for LDLR | $0.0006$ | mmol/min/l | ✓ |
| $\mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax}}$ | `SYNTHESIS_LDLR_Vmax` | Protein synthesis Vmax for LDLR |  | mmol/min/l |  |
| $\mathrm{LDLR}_{\mathrm{kr\_cho}}$ | `LDLR_kr_cho` | Protein regulation kr for LDLR | $0.02$ | mmol/l | ✓ |
| $\mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax\_f}}$ | `SYNTHESIS_LDLR_Vmax_f` | scaling factor for synthesis Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax\_f}}$ | `DEGRADATION_LDLR_Vmax_f` | scaling factor for degradation Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{SIMVAIMP}_{\mathrm{Km}}$ | `SIMVAIMP_Km` | Km for simvastatin import | $0.0097$ | mmol/l | ✓ |
| $\mathrm{SIMVAIMP}_{\mathrm{Vmax}}$ | `SIMVAIMP_Vmax` | Vmax for simvastatin import | $1$ | mmol/min/l | ✓ |
| $\mathrm{SIMACIDIMP}_{\mathrm{Km}}$ | `SIMACIDIMP_Km` | Km for simvastatin acid import | $0.0036$ | mmol/l | ✓ |
| $\mathrm{SIMACIDIMP}_{\mathrm{Vmax}}$ | `SIMACIDIMP_Vmax` | Vmax for simvastatin acid import | $0.000155861593241634$ | mmol/min/l | ✓ |
| $\mathrm{SIMACIDEXP}_{\mathrm{k}}$ | `SIMACIDEXP_k` | rate of simvastatin acid efflux | $0.925$ | 1/min | ✓ |
| $\mathrm{SIMMETSEXP}_{\mathrm{Km}}$ | `SIMMETSEXP_Km` | Km for simvastatin metabolites exchange | $0.0067$ | mmol/l | ✓ |
| $\mathrm{SIMMETSEXP}_{\mathrm{Vmax}}$ | `SIMMETSEXP_Vmax` | Vmax for simvastatin metabolites exchange | $0.744$ | mmol/min/l | ✓ |
| $\mathrm{ESTERASE}_{\mathrm{Km}}$ | `ESTERASE_Km` | Km esterase | $0.0008$ | mmol/l | ✓ |
| $\mathrm{ESTERASE}_{\mathrm{Vmax}}$ | `ESTERASE_Vmax` | Vmax esterase | $0.000355497735581453$ | mmol/min/l | ✓ |
| $\mathrm{SIMVA}_{\mathrm{CYP3A4\_Vmax}}$ | `SIMVA_CYP3A4_Vmax` | Vmax CYP3A4 simvastatin (liver) | $0.071371880652173$ | mmol/min/l | ✓ |
| $\mathrm{SIMACID}_{\mathrm{CYP3A4\_Vmax}}$ | `SIMACID_CYP3A4_Vmax` | Vmax CYP3A4 simvastatin acid (liver) | $0.0015$ | mmol/min/l | ✓ |
| $\mathrm{SIMACIDMET}_{\mathrm{k}}$ | `SIMACIDMET_k` | rate of the metabolism of simvastatin acid not by CYP3A4 | $16$ | 1/min | ✓ |
| $\mathrm{EHC}_{\mathrm{simmets\_k}}$ | `EHC_simmets_k` | rate of biliary excretion of the simvastatin metabolites | $3.02803101810212$ | 1/min | ✓ |
| $\mathrm{VLDLCEXP}_{\mathrm{Vmax}}$ | `VLDLCEXP_Vmax` | Vmax VLDL-cholesterol export | $2.5$ | \- | ✓ |
| $\mathrm{VLDLCEXP}_{\mathrm{Km\_cho}}$ | `VLDLCEXP_Km_cho` | Km VLDL-cholesterol export | $0.0005$ | mmol/l | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Kcat}}$ | `LDLRLDLCIMP_Kcat` |  | $6$ | \- | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Km}}$ | `LDLRLDLCIMP_Km` | Km LDLR-LDLC binding | $3$ | mmol/l | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Ki\_ldlr\_ldlc}}$ | `LDLRLDLCIMP_Ki_ldlr_ldlc` | Ki LDLR-LDLC complex on uptake | $0.1$ | \- | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Km\_f}}$ | `LDLRLDLCIMP_Km_f` |  | $1$ | \- | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Kcat\_f}}$ | `LDLRLDLCIMP_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LDLRMEMBRANE}_{\mathrm{Kcat}}$ | `LDLRMEMBRANE_Kcat` |  | $0.025$ | mmol/min/l | ✓ |
| $\mathrm{LDLRMEMBRANE}_{\mathrm{Kcat\_f}}$ | `LDLRMEMBRANE_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LDLRMEMBRANE}_{\mathrm{Keq}}$ | `LDLRMEMBRANE_Keq` |  | $10$ | \- | ✓ |
| $\mathrm{LDLRRECYCLING}_{\mathrm{Kcat}}$ | `LDLRRECYCLING_Kcat` |  | $0.0125$ | mmol/min/l | ✓ |
| $\mathrm{LDLRRECYCLING}_{\mathrm{Kcat\_f}}$ | `LDLRRECYCLING_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{HMGCOASYNTHASE}_{\mathrm{Kcat}}$ | `HMGCOASYNTHASE_Kcat` | kcat HMG-CoA synthase | $245$ | l/mmol | ✓ |
| $\mathrm{HMGCOASYNTHASE}_{\mathrm{Ki\_hmgcoa}}$ | `HMGCOASYNTHASE_Ki_hmgcoa` | Ki HMG-CoA synthase (product inhibition by HMG-CoA) | $0.022$ | mmol/l | ✓ |
| $\mathrm{HMGCOAREDUCTASE}_{\mathrm{Kcat}}$ | `HMGCOAREDUCTASE_Kcat` | kcat HMG-CoA reductase | $0.7$ | \- | ✓ |
| $\mathrm{HMGCOAREDUCTASE}_{\mathrm{Km}}$ | `HMGCOAREDUCTASE_Km` | Km HMG-CoA | $0.004$ | mmol/l | ✓ |
| $\mathrm{HMGCOAREDUCTASE}_{\mathrm{Ki\_simacid}}$ | `HMGCOAREDUCTASE_Ki_simacid` | Ki HMG-CoA reductase for simvastatin acid and the active metabolites | $9.16748418506532 \times 10^{-7}$ | mmol/l | ✓ |
| $\mathrm{ldlr}_{\mathrm{total}}$ | `ldlr_total` | Total LDLR |  | \- |  |
| $\mathrm{ldlr}_{\mathrm{fraction}}$ | `ldlr_fraction` | LDLR fraction |  | \- |  |
| $\mathrm{ldlr}_{\mathrm{membrane\_fraction}}$ | `ldlr_membrane_fraction` | LDLR membrane fraction |  | \- |  |
| $\mathrm{ldlr}_{\mathrm{ldlc\_fraction}}$ | `ldlr_ldlc_fraction` | LDLR-LDLC fraction |  | \- |  |
| $v_{\mathrm{cho\_reference}}$ | `v_cho_reference` | reference cholesterol turnover \[mmole/min\] |  | mmol/min |  |
| $v_{\mathrm{synthesis}}$ | `v_synthesis` | total synthesized cholesterol |  | mg/day |  |
| $v_{\mathrm{recycling}}$ | `v_recycling` | LDLR recycling and cholesterol release into free cholesterol |  | mg/day |  |
| $v_{\mathrm{uptake}}$ | `v_uptake` | cholesterol uptake (LDL receptor) |  | mg/day |  |
| $v_{\mathrm{export}}$ | `v_export` | cholesterol export (VLDL) |  | mg/day |  |
| $v_{\mathrm{reference}}$ | `v_reference` | cholesterol reference flux |  | mg/day |  |
| $v_{\mathrm{net\_export\_rate}}$ | `v_net_export_rate` | cholesterol net export rate (VLDL) |  | mmol/min |  |
| $v_{\mathrm{net\_export}}$ | `v_net_export` | cholesterol net export (VLDL) |  | mg/day |  |
| $v_{\mathrm{liver\_balance}}$ | `v_liver_balance` | cholesterol liver balance |  | mg/day |  |
| $\mathrm{TURNOVER}_{\mathrm{LDLR}}$ | `TURNOVER_LDLR` | total turnover of LDL-R expression |  | mmol/min |  |
| $\mathrm{active}_{\mathrm{inhibitors}}$ | `active_inhibitors` | active HMG-CoA reductase inhibitors in liver |  | mmol/l |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{hmgcoareductase} &= 1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{hmgcoasynthase} &= 1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{ldlr} &= 0.1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{ldlr}_{\mathrm{membrane}} &= 0.8 \cdot \mathrm{Vbaso} \\[1ex]
\mathrm{ldlr}_{\mathrm{ldlc}} &= 0.1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{ldlr}_{\mathrm{degraded}} &= 0 \cdot \mathrm{Vli}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{ldlr}_{\mathrm{total}} &= \mathrm{ldlr} + \mathrm{ldlr}_{\mathrm{membrane}} + \mathrm{ldlr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{ldlr}_{\mathrm{fraction}} &= \frac{\mathrm{ldlr}}{\mathrm{ldlr}_{\mathrm{total}}} \\[1ex]
\mathrm{ldlr}_{\mathrm{membrane\_fraction}} &= \frac{\mathrm{ldlr}_{\mathrm{membrane}}}{\mathrm{ldlr}_{\mathrm{total}}} \\[1ex]
\mathrm{ldlr}_{\mathrm{ldlc\_fraction}} &= \frac{\mathrm{ldlr}_{\mathrm{ldlc}}}{\mathrm{ldlr}_{\mathrm{total}}} \\[1ex]
v_{\mathrm{cho\_reference}} &= \frac{\frac{v_{\mathrm{cho\_ref}}}{\mathrm{Mr}_{\mathrm{ldlc}}}}{\mathrm{conversion}_{\mathrm{min\_per\_day}}} \\[1ex]
\mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax}} &= 0.4 \cdot \mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax}} \\[1ex]
v_{\mathrm{reference}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
\mathrm{active}_{\mathrm{inhibitors}} &= \mathrm{simacid} + \mathrm{simmets}_{\mathrm{inhibitor\_activity}} \cdot \mathrm{simmets} \\[1ex]
v_{\mathrm{export}} &= v_{\mathrm{VLDLCEXP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{uptake}} &= v_{\mathrm{LDLRLDLCIMP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{net\_export\_rate}} &= v_{\mathrm{VLDLCEXP}} - v_{\mathrm{LDLRLDLCIMP}} \\[1ex]
v_{\mathrm{net\_export}} &= v_{\mathrm{net\_export\_rate}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{recycling}} &= v_{\mathrm{LDLRRECYCLING}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{synthesis}} &= v_{\mathrm{HMGCOAREDUCTASE}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{liver\_balance}} &= v_{\mathrm{synthesis}} + v_{\mathrm{uptake}} - v_{\mathrm{export}} \\[1ex]
\mathrm{TURNOVER}_{\mathrm{LDLR}} &= v_{\mathrm{SYNTHESIS\_LDLR}} - v_{\mathrm{DEGRADATION\_LDLR}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{SIMVAIMP}}$ | `SIMVAIMP` | SV import | $\mathrm{simva}_{\mathrm{ext}} \rightleftharpoons \mathrm{simva}$ |  |
| $v_{\mathrm{SIMACIDIMP}}$ | `SIMACIDIMP` | SVA import (OATP1B1) | $\mathrm{simacid}_{\mathrm{ext}} \longrightarrow \mathrm{simacid}$ |  |
| $v_{\mathrm{SIMACIDEXP}}$ | `SIMACIDEXP` | SVA efflux | $\mathrm{simacid} \longrightarrow \mathrm{simacid}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{SIMMETSEXP}}$ | `SIMMETSEXP` | SVM exchange | $\mathrm{simmets} \rightleftharpoons \mathrm{simmets}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{ESTERASE}}$ | `ESTERASE` | Esterase: SV to SVA | $\mathrm{simva} \longrightarrow \mathrm{simacid}$ |  |
| $v_{\mathrm{SIMVA\_CYP3A4}}$ | `SIMVA_CYP3A4` | CYP3A4: SV to SVM | $\mathrm{simva} \longrightarrow \mathrm{simmets}$ |  |
| $v_{\mathrm{SIMACID\_CYP3A4}}$ | `SIMACID_CYP3A4` | CYP3A4: SVA to SVM | $\mathrm{simacid} \longrightarrow \mathrm{simmets}$ |  |
| $v_{\mathrm{SIMACIDMET}}$ | `SIMACIDMET` | SVA to SVM (glucuronidation, CYP2C8) | $\mathrm{simacid} \longrightarrow \mathrm{simmets}$ |  |
| $v_{\mathrm{EHC\_simmets}}$ | `EHC_simmets` | EHC SVM | $\mathrm{simmets} \longrightarrow \mathrm{simmets}_{\mathrm{lumen}}$ |  |
| $v_{\mathrm{VLDLCEXP}}$ | `VLDLCEXP` | VLDL-cholesterol export | $\mathrm{cho} \longrightarrow \mathrm{vldlc}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{LDLRLDLCIMP}}$ | `LDLRLDLCIMP` | LDLR-LDLC binding &amp; internalization | $\mathrm{ldlc}_{\mathrm{ext}} + \mathrm{ldlr}_{\mathrm{membrane}} \longrightarrow \mathrm{ldlr}_{\mathrm{ldlc}}$ | $\mathrm{ldlr}_{\mathrm{ldlc}}$ |
| $v_{\mathrm{LDLR\_TO\_MEMBRANE}}$ | `LDLR_TO_MEMBRANE` | LDLR membrane transport | $\mathrm{ldlr} \rightleftharpoons \mathrm{ldlr}_{\mathrm{membrane}}$ |  |
| $v_{\mathrm{LDLRRECYCLING}}$ | `LDLRRECYCLING` | LDLR recycling | $\mathrm{ldlr}_{\mathrm{ldlc}} \longrightarrow \mathrm{ldlr} + \mathrm{cho}$ |  |
| $v_{\mathrm{HMGCOASYNTHASE}}$ | `HMGCOASYNTHASE` | HMG-CoA synthase | $3 \, \mathrm{acoa} \longrightarrow \mathrm{hmgcoa}$ | $\mathrm{hmgcoasynthase}, \mathrm{hmgcoa}$ |
| $v_{\mathrm{HMGCOAREDUCTASE}}$ | `HMGCOAREDUCTASE` | HMG-CoA reductase | $6 \, \mathrm{hmgcoa} \longrightarrow \mathrm{cho}$ | $\mathrm{simacid}, \mathrm{simmets}, \mathrm{hmgcoareductase}$ |
| $v_{\mathrm{SYNTHESIS\_HMGCOAREDUCTASE}}$ | `SYNTHESIS_HMGCOAREDUCTASE` | HMGCOAREDUCTASE synthesis | $\varnothing \longrightarrow \mathrm{hmgcoareductase}$ | $\mathrm{cho}$ |
| $v_{\mathrm{DEGRADATION\_HMGCOAREDUCTASE}}$ | `DEGRADATION_HMGCOAREDUCTASE` | HMGCOAREDUCTASE degradation | $\mathrm{hmgcoareductase} \longrightarrow \varnothing$ | $\mathrm{cho}$ |
| $v_{\mathrm{SYNTHESIS\_HMGCOASYNTHASE}}$ | `SYNTHESIS_HMGCOASYNTHASE` | HMGCOASYNTHASE synthesis | $\varnothing \longrightarrow \mathrm{hmgcoasynthase}$ | $\mathrm{cho}$ |
| $v_{\mathrm{DEGRADATION\_HMGCOASYNTHASE}}$ | `DEGRADATION_HMGCOASYNTHASE` | HMGCOASYNTHASE degradation | $\mathrm{hmgcoasynthase} \longrightarrow \varnothing$ | $\mathrm{cho}$ |
| $v_{\mathrm{SYNTHESIS\_LDLR}}$ | `SYNTHESIS_LDLR` | LDLR synthesis | $\varnothing \longrightarrow \mathrm{ldlr}$ | $\mathrm{cho}$ |
| $v_{\mathrm{DEGRADATION\_LDLR}}$ | `DEGRADATION_LDLR` | LDLR degradation | $\mathrm{ldlr} \longrightarrow \mathrm{ldlr}_{\mathrm{degraded}}$ | $\mathrm{cho}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{SIMVAIMP}} &= \frac{\frac{\mathrm{Vli} \cdot \mathrm{SIMVAIMP}_{\mathrm{Vmax}}}{\mathrm{SIMVAIMP}_{\mathrm{Km}}} \cdot \mathopen{}\left(\mathrm{simva}_{\mathrm{ext}} - \mathrm{simva}\right)}{1 + \frac{\mathrm{simva}_{\mathrm{ext}}}{\mathrm{SIMVAIMP}_{\mathrm{Km}}} + \frac{\mathrm{simva}}{\mathrm{SIMVAIMP}_{\mathrm{Km}}}} \\[1ex]
v_{\mathrm{SIMACIDIMP}} &= \frac{f_{\mathrm{oatp1b1}} \cdot \mathrm{Vli} \cdot \mathrm{SIMACIDIMP}_{\mathrm{Vmax}} \cdot \mathrm{simacid}_{\mathrm{ext}}}{\mathrm{simacid}_{\mathrm{ext}} + \mathrm{SIMACIDIMP}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{SIMACIDEXP}} &= \mathrm{SIMACIDEXP}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{simacid} \\[1ex]
v_{\mathrm{SIMMETSEXP}} &= \frac{\frac{\mathrm{Vli} \cdot \mathrm{SIMMETSEXP}_{\mathrm{Vmax}}}{\mathrm{SIMMETSEXP}_{\mathrm{Km}}} \cdot \mathopen{}\left(\mathrm{simmets} - \mathrm{simmets}_{\mathrm{ext}}\right)}{1 + \frac{\mathrm{simmets}_{\mathrm{ext}}}{\mathrm{SIMMETSEXP}_{\mathrm{Km}}} + \frac{\mathrm{simmets}}{\mathrm{SIMMETSEXP}_{\mathrm{Km}}}} \\[1ex]
v_{\mathrm{ESTERASE}} &= \frac{\mathrm{Vli} \cdot \mathrm{ESTERASE}_{\mathrm{Vmax}} \cdot \mathrm{simva}}{\mathrm{simva} + \mathrm{ESTERASE}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{SIMVA\_CYP3A4}} &= \frac{\mathopen{}\left(f_{\mathrm{cyp3a4}} + r_{\mathrm{cyp3a5}} \cdot f_{\mathrm{cyp3a5}}\right) \cdot \mathrm{Vli} \cdot \mathrm{SIMVA}_{\mathrm{CYP3A4\_Vmax}} \cdot \mathrm{simva}}{\mathrm{simva} + \mathrm{CYP3A4}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{SIMACID\_CYP3A4}} &= \frac{\mathopen{}\left(f_{\mathrm{cyp3a4}} + r_{\mathrm{cyp3a5}} \cdot f_{\mathrm{cyp3a5}}\right) \cdot \mathrm{Vli} \cdot \mathrm{SIMACID}_{\mathrm{CYP3A4\_Vmax}} \cdot \mathrm{simacid}}{\mathrm{simacid} + \mathrm{CYP3A4}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{SIMACIDMET}} &= f_{\mathrm{ugt}} \cdot \mathrm{SIMACIDMET}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{simacid} \\[1ex]
v_{\mathrm{EHC\_simmets}} &= \mathrm{EHC}_{\mathrm{simmets\_k}} \cdot \mathrm{Vli} \cdot \mathrm{simmets} \\[1ex]
v_{\mathrm{VLDLCEXP}} &= \frac{\mathrm{VLDLCEXP}_{\mathrm{Vmax}} \cdot v_{\mathrm{cho\_reference}} \cdot \mathrm{cho}}{\mathrm{cho} + \mathrm{VLDLCEXP}_{\mathrm{Km\_cho}}} \\[1ex]
v_{\mathrm{LDLRLDLCIMP}} &= \frac{\frac{v_{\mathrm{cho\_reference}} \cdot \mathrm{LDLRLDLCIMP}_{\mathrm{Kcat}} \cdot \mathrm{LDLRLDLCIMP}_{\mathrm{Kcat\_f}} \cdot \mathrm{ldlr}_{\mathrm{membrane}} \cdot \mathrm{ldlc}_{\mathrm{ext}}}{\mathrm{LDLRLDLCIMP}_{\mathrm{Km}} \cdot \mathrm{LDLRLDLCIMP}_{\mathrm{Km\_f}} + \mathrm{ldlc}_{\mathrm{ext}}} \cdot 1}{1 + \frac{\mathrm{ldlr}_{\mathrm{ldlc}}}{\mathrm{LDLRLDLCIMP}_{\mathrm{Ki\_ldlr\_ldlc}}}} \\[1ex]
v_{\mathrm{LDLR\_TO\_MEMBRANE}} &= \mathrm{Vli} \cdot \mathrm{LDLRMEMBRANE}_{\mathrm{Kcat}} \cdot \mathrm{LDLRMEMBRANE}_{\mathrm{Kcat\_f}} \cdot \mathopen{}\left(\mathrm{ldlr} - \frac{\mathrm{ldlr}_{\mathrm{membrane}}}{\mathrm{LDLRMEMBRANE}_{\mathrm{Keq}}}\right) \\[1ex]
v_{\mathrm{LDLRRECYCLING}} &= \mathrm{Vli} \cdot \mathrm{LDLRRECYCLING}_{\mathrm{Kcat}} \cdot \mathrm{LDLRRECYCLING}_{\mathrm{Kcat\_f}} \cdot \mathrm{ldlr}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{HMGCOASYNTHASE}} &= \frac{\mathrm{HMGCOASYNTHASE}_{\mathrm{Kcat}} \cdot v_{\mathrm{cho\_reference}} \cdot \mathrm{hmgcoasynthase} \cdot \mathrm{acoa}}{1 + \frac{\mathrm{hmgcoa}}{\mathrm{HMGCOASYNTHASE}_{\mathrm{Ki\_hmgcoa}}}} \\[1ex]
v_{\mathrm{HMGCOAREDUCTASE}} &= \frac{\mathrm{HMGCOAREDUCTASE}_{\mathrm{Kcat}} \cdot v_{\mathrm{cho\_reference}} \cdot \mathrm{hmgcoareductase} \cdot \mathrm{hmgcoa}}{\mathrm{HMGCOAREDUCTASE}_{\mathrm{Km}} \cdot \mathopen{}\left(1 + \frac{\mathrm{simacid} + \mathrm{simmets}_{\mathrm{inhibitor\_activity}} \cdot \mathrm{simmets}}{\mathrm{HMGCOAREDUCTASE}_{\mathrm{Ki\_simacid}}}\right) + \mathrm{hmgcoa}} \\[1ex]
v_{\mathrm{SYNTHESIS\_HMGCOAREDUCTASE}} &= \frac{\mathrm{SYNTHESIS}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{Vli}}{1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}} \\[1ex]
v_{\mathrm{DEGRADATION\_HMGCOAREDUCTASE}} &= \mathrm{DEGRADATION}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{hmgcoareductase} \cdot \mathrm{Vli} \cdot \mathopen{}\left(1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}\right) \\[1ex]
v_{\mathrm{SYNTHESIS\_HMGCOASYNTHASE}} &= \frac{\mathrm{SYNTHESIS}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{Vli}}{1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}} \\[1ex]
v_{\mathrm{DEGRADATION\_HMGCOASYNTHASE}} &= \mathrm{DEGRADATION}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{hmgcoasynthase} \cdot \mathrm{Vli} \cdot \mathopen{}\left(1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}\right) \\[1ex]
v_{\mathrm{SYNTHESIS\_LDLR}} &= \frac{\mathrm{Vli} \cdot \mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax}} \cdot \mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax\_f}}}{1 + \frac{\mathrm{cho}}{\mathrm{LDLR}_{\mathrm{kr\_cho}}}} \\[1ex]
v_{\mathrm{DEGRADATION\_LDLR}} &= \mathrm{Vli} \cdot \mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax}} \cdot \mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax\_f}} \cdot \mathrm{ldlr} \cdot \mathopen{}\left(1 + \frac{\mathrm{cho}}{\mathrm{LDLR}_{\mathrm{kr\_cho}}}\right)
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{simacid}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vli}} \Bigl( v_{\mathrm{SIMACIDIMP}} - v_{\mathrm{SIMACIDEXP}} + v_{\mathrm{ESTERASE}} - v_{\mathrm{SIMACID\_CYP3A4}} \\
&\quad {} - v_{\mathrm{SIMACIDMET}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vli}} \Bigl( -v_{\mathrm{SIMMETSEXP}} + v_{\mathrm{SIMVA\_CYP3A4}} + v_{\mathrm{SIMACID\_CYP3A4}} + v_{\mathrm{SIMACIDMET}} \\
&\quad {} - v_{\mathrm{EHC\_simmets}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{simva}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{SIMVAIMP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simacid}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{SIMACIDIMP}} + v_{\mathrm{SIMACIDEXP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SIMMETSEXP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simva}}{\mathrm{d} t} &= \frac{v_{\mathrm{SIMVAIMP}} - v_{\mathrm{ESTERASE}} - v_{\mathrm{SIMVA\_CYP3A4}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{EHC\_simmets}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{vldlc}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{VLDLCEXP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hmgcoa}}{\mathrm{d} t} &= \frac{v_{\mathrm{HMGCOASYNTHASE}} - 6 \cdot v_{\mathrm{HMGCOAREDUCTASE}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cho}}{\mathrm{d} t} &= \frac{-v_{\mathrm{VLDLCEXP}} + v_{\mathrm{LDLRRECYCLING}} + v_{\mathrm{HMGCOAREDUCTASE}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hmgcoareductase}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{SYNTHESIS\_HMGCOAREDUCTASE}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_HMGCOAREDUCTASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hmgcoasynthase}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{SYNTHESIS\_HMGCOASYNTHASE}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_HMGCOASYNTHASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}}{\mathrm{d} t} &= -\mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLR\_TO\_MEMBRANE}} + \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRRECYCLING}} + \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{SYNTHESIS\_LDLR}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_LDLR}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}_{\mathrm{membrane}}}{\mathrm{d} t} &= -\mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRLDLCIMP}} + \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLR\_TO\_MEMBRANE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRLDLCIMP}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRRECYCLING}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}_{\mathrm{degraded}}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_LDLR}}
\end{aligned}
$$
