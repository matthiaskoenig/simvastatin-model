# Model for simvastatin metabolism in the liver

Model `simvastatin_liver_simvastatin`, SBML Level 3 Version 2, read from simvastatin\_liver\_simvastatin.xml, written by sbmlode 0.3.0.

Model for simvastatin metabolism in the liver

Simvastatin (lactone) is taken up passively (reversible) into the hepatocytes, hydrolyzed to simvastatin acid (esterases, paraoxonases) and metabolized by CYP3A4/CYP3A5.

Simvastatin acid is taken up from the plasma by OATP1B1 (SLCO1B1) and leaves the hepatocytes by efflux; in the liver it is metabolized by CYP3A4/CYP3A5 and by glucuronidation and CYP2C8. The acid formed in the liver reaches the plasma by the efflux only, so the activity of OATP1B1 sets the clearance of the plasma acid (SLCO1B1 c.521CC: AUC of the acid 3.2-fold, Pasanen2006).

The metabolites (lumped, active and inactive) are exchanged with the plasma and excreted into the bile (enterohepatic circulation).

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

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{CYP3A4}_{\mathrm{Km}}$ | `CYP3A4_Km` | Km CYP3A4 | $0.025$ | mmol/l | ✓ |
| $f_{\mathrm{cyp3a4}}$ | `f_cyp3a4` | activity of CYP3A4 (liver) | $1$ | \- | ✓ |
| $f_{\mathrm{cyp3a5}}$ | `f_cyp3a5` | functional CYP3A5 | $0$ | \- | ✓ |
| $r_{\mathrm{cyp3a5}}$ | `r_cyp3a5` | capacity of CYP3A5 \*1/\*1 relative to CYP3A4 | $1$ | \- | ✓ |
| $f_{\mathrm{ugt}}$ | `f_ugt` | activity of the glucuronidation and CYP2C8 of simvastatin acid | $1$ | \- | ✓ |
| $f_{\mathrm{oatp1b1}}$ | `f_oatp1b1` | activity of OATP1B1 | $1$ | \- | ✓ |
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

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{SIMVAIMP}}$ | `SIMVAIMP` | SV import | $\mathrm{simva}_{\mathrm{ext}} \rightleftharpoons \mathrm{simva}$ |
| $v_{\mathrm{SIMACIDIMP}}$ | `SIMACIDIMP` | SVA import (OATP1B1) | $\mathrm{simacid}_{\mathrm{ext}} \longrightarrow \mathrm{simacid}$ |
| $v_{\mathrm{SIMACIDEXP}}$ | `SIMACIDEXP` | SVA efflux | $\mathrm{simacid} \longrightarrow \mathrm{simacid}_{\mathrm{ext}}$ |
| $v_{\mathrm{SIMMETSEXP}}$ | `SIMMETSEXP` | SVM exchange | $\mathrm{simmets} \rightleftharpoons \mathrm{simmets}_{\mathrm{ext}}$ |
| $v_{\mathrm{ESTERASE}}$ | `ESTERASE` | Esterase: SV to SVA | $\mathrm{simva} \longrightarrow \mathrm{simacid}$ |
| $v_{\mathrm{SIMVA\_CYP3A4}}$ | `SIMVA_CYP3A4` | CYP3A4: SV to SVM | $\mathrm{simva} \longrightarrow \mathrm{simmets}$ |
| $v_{\mathrm{SIMACID\_CYP3A4}}$ | `SIMACID_CYP3A4` | CYP3A4: SVA to SVM | $\mathrm{simacid} \longrightarrow \mathrm{simmets}$ |
| $v_{\mathrm{SIMACIDMET}}$ | `SIMACIDMET` | SVA to SVM (glucuronidation, CYP2C8) | $\mathrm{simacid} \longrightarrow \mathrm{simmets}$ |
| $v_{\mathrm{EHC\_simmets}}$ | `EHC_simmets` | EHC SVM | $\mathrm{simmets} \longrightarrow \mathrm{simmets}_{\mathrm{lumen}}$ |

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
v_{\mathrm{EHC\_simmets}} &= \mathrm{EHC}_{\mathrm{simmets\_k}} \cdot \mathrm{Vli} \cdot \mathrm{simmets}
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
\frac{\mathrm{d} \,\mathrm{simmets}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{EHC\_simmets}}}{\mathrm{Vlumen}}
\end{aligned}
$$
