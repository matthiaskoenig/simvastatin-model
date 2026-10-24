# Model for intestinal/gut simvastatin metabolism

Model `simvastatin_intestine`, SBML Level 3 Version 2, read from simvastatin\_intestine.xml, written by sbmlode 0.3.0.

Model for intestinal/gut simvastatin metabolism

Simvastatin (lactone) is absorbed from the intestinal lumen into the enterocytes, the fraction F\_abs\_simva of it; the rest is excreted in the feces.

Simvastatin is metabolized by CYP3A4 (and CYP3A5) in the enterocytes (first pass metabolism) or exported into the gut plasma (portal vein). The intestinal availability is about 0.25 - 0.3: regular grapefruit juice, an inhibitor of the intestinal CYP3A4 only, increases the AUC of simvastatin 3.6-fold (Lilja2004).

The simvastatin metabolites from the bile (enterohepatic circulation) are absorbed with the fraction F\_abs\_simmets, the rest is excreted in the feces (only metabolites and unabsorbed simvastatin are in the feces).

The hydrolysis of simvastatin to simvastatin acid (esterases) and the metabolism of simvastatin acid take place in the liver, not in the intestine.

Food does not change the bioavailability of simvastatin (Zocor label), the model has no food effect.

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
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Ventero}$ | `Ventero` | intestinal lining (enterocytes) | $\mathrm{NaN}$ | l | ✓ |
| $\mathrm{Vapical}$ | `Vapical` | apical membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vbaso}$ | `Vbaso` | basolateral membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{simva}_{\mathrm{lumen}}$ | `simva_lumen` | simvastatin (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{simva}$ | `simva` | simvastatin (enterocytes) | $\mathrm{Vgu}$ | $0$ | mmol/l | concentration |
| $\mathrm{simva}_{\mathrm{ext}}$ | `simva_ext` | simvastatin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{simva}_{\mathrm{feces}}$ | `simva_feces` | simvastatin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{simmets}_{\mathrm{lumen}}$ | `simmets_lumen` | simvastatin metabolites (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{simmets}$ | `simmets` | simvastatin metabolites (intestine) | $\mathrm{Vgu}$ | $0$ | mmol/l | concentration |
| $\mathrm{simmets}_{\mathrm{ext}}$ | `simmets_ext` | simvastatin metabolites (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{simmets}_{\mathrm{feces}}$ | `simmets_feces` | simvastatin metabolites (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $F_{\mathrm{abs\_simva}}$ | `F_abs_simva` | fraction absorbed simvastatin | $0.85$ | \- | ✓ |
| $\mathrm{SIMVAABS}_{\mathrm{k}}$ | `SIMVAABS_k` | rate of absorption simvastatin | $1.29$ | 1/hr | ✓ |
| $F_{\mathrm{abs\_simmets}}$ | `F_abs_simmets` | fraction absorbed simvastatin metabolites | $0.536$ | \- | ✓ |
| $\mathrm{SIMMETSABS}_{\mathrm{k}}$ | `SIMMETSABS_k` | rate of absorption simvastatin metabolites | $0.226$ | 1/hr | ✓ |
| $\mathrm{CYP3A4}_{\mathrm{Km}}$ | `CYP3A4_Km` | Km CYP3A4 | $0.025$ | mmol/l | ✓ |
| $f_{\mathrm{cyp3a4}}$ | `f_cyp3a4` | activity of CYP3A4 (intestine) | $1$ | \- | ✓ |
| $f_{\mathrm{cyp3a5}}$ | `f_cyp3a5` | functional CYP3A5 | $0$ | \- | ✓ |
| $r_{\mathrm{cyp3a5}}$ | `r_cyp3a5` | capacity of CYP3A5 \*1/\*1 relative to CYP3A4 | $1$ | \- | ✓ |
| $\mathrm{SIMVA}_{\mathrm{CYP3A4\_Vmax}}$ | `SIMVA_CYP3A4_Vmax` | Vmax CYP3A4 simvastatin (intestine) | $0.0063$ | mmol/min/l | ✓ |
| $\mathrm{SIMVAEXP}_{\mathrm{Km}}$ | `SIMVAEXP_Km` | Km simvastatin export | $0.0097$ | mmol/l | ✓ |
| $\mathrm{SIMVAEXP}_{\mathrm{Vmax}}$ | `SIMVAEXP_Vmax` | Vmax simvastatin export (intestine) | $0.001$ | mmol/min/l | ✓ |
| $\mathrm{SIMMETSEXP}_{\mathrm{Km}}$ | `SIMMETSEXP_Km` | Km simvastatin metabolite export | $0.0067$ | mmol/l | ✓ |
| $\mathrm{SIMMETSEXP}_{\mathrm{Vmax}}$ | `SIMMETSEXP_Vmax` | Vmax simvastatin metabolite export (intestine) | $0.01$ | mmol/min/l | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{simva}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{simmets}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{SIMVAABS}}$ | `SIMVAABS` | absorption simvastatin | $\mathrm{simva}_{\mathrm{lumen}} \longrightarrow \mathrm{simva}$ |
| $v_{\mathrm{SIMVAEXC}}$ | `SIMVAEXC` | excretion simvastatin (feces) | $\mathrm{simva}_{\mathrm{lumen}} \longrightarrow \mathrm{simva}_{\mathrm{feces}}$ |
| $v_{\mathrm{SIMMETSABS}}$ | `SIMMETSABS` | absorption simvastatin metabolites | $\mathrm{simmets}_{\mathrm{lumen}} \longrightarrow \mathrm{simmets}$ |
| $v_{\mathrm{SIMMETSEXC}}$ | `SIMMETSEXC` | excretion simvastatin metabolites (feces) | $\mathrm{simmets}_{\mathrm{lumen}} \longrightarrow \mathrm{simmets}_{\mathrm{feces}}$ |
| $v_{\mathrm{SIMVAEXP}}$ | `SIMVAEXP` | SV export | $\mathrm{simva} \longrightarrow \mathrm{simva}_{\mathrm{ext}}$ |
| $v_{\mathrm{SIMMETSEXP}}$ | `SIMMETSEXP` | SVM export | $\mathrm{simmets} \longrightarrow \mathrm{simmets}_{\mathrm{ext}}$ |
| $v_{\mathrm{SIMVA\_CYP3A4}}$ | `SIMVA_CYP3A4` | CYP3A4: SV to SVM | $\mathrm{simva} \longrightarrow \mathrm{simmets}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{SIMVAABS}} &= \frac{F_{\mathrm{abs\_simva}} \cdot \mathrm{SIMVAABS}_{\mathrm{k}}}{60} \cdot \mathrm{Vlumen} \cdot \mathrm{simva}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{SIMVAEXC}} &= \frac{\mathopen{}\left(1 - F_{\mathrm{abs\_simva}}\right) \cdot \mathrm{SIMVAABS}_{\mathrm{k}}}{60} \cdot \mathrm{Vlumen} \cdot \mathrm{simva}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{SIMMETSABS}} &= \frac{F_{\mathrm{abs\_simmets}} \cdot \mathrm{SIMMETSABS}_{\mathrm{k}}}{60} \cdot \mathrm{Vlumen} \cdot \mathrm{simmets}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{SIMMETSEXC}} &= \frac{\mathopen{}\left(1 - F_{\mathrm{abs\_simmets}}\right) \cdot \mathrm{SIMMETSABS}_{\mathrm{k}}}{60} \cdot \mathrm{Vlumen} \cdot \mathrm{simmets}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{SIMVAEXP}} &= \frac{\mathrm{Vgu} \cdot \mathrm{SIMVAEXP}_{\mathrm{Vmax}} \cdot \mathrm{simva}}{\mathrm{SIMVAEXP}_{\mathrm{Km}} + \mathrm{simva}} \\[1ex]
v_{\mathrm{SIMMETSEXP}} &= \frac{\mathrm{Vgu} \cdot \mathrm{SIMMETSEXP}_{\mathrm{Vmax}} \cdot \mathrm{simmets}}{\mathrm{simmets} + \mathrm{SIMMETSEXP}_{\mathrm{Km}}} \\[1ex]
v_{\mathrm{SIMVA\_CYP3A4}} &= \frac{\mathopen{}\left(f_{\mathrm{cyp3a4}} + r_{\mathrm{cyp3a5}} \cdot f_{\mathrm{cyp3a5}}\right) \cdot \mathrm{Vgu} \cdot \mathrm{SIMVA}_{\mathrm{CYP3A4\_Vmax}} \cdot \mathrm{simva}}{\mathrm{simva} + \mathrm{CYP3A4}_{\mathrm{Km}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{simva}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{SIMVAABS}} - v_{\mathrm{SIMVAEXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simva}}{\mathrm{d} t} &= \frac{v_{\mathrm{SIMVAABS}} - v_{\mathrm{SIMVAEXP}} - v_{\mathrm{SIMVA\_CYP3A4}}}{\mathrm{Vgu}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simva}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SIMVAEXP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simva}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{SIMVAEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{SIMMETSABS}} - v_{\mathrm{SIMMETSEXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}}{\mathrm{d} t} &= \frac{v_{\mathrm{SIMMETSABS}} - v_{\mathrm{SIMMETSEXP}} + v_{\mathrm{SIMVA\_CYP3A4}}}{\mathrm{Vgu}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{SIMMETSEXP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{simmets}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{SIMMETSEXC}}
\end{aligned}
$$
