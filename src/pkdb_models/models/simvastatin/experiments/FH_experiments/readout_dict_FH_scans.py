"""The quantities, simvastatin doses and panels of the figures of the FH experiments.

The figures of the familial hypercholesterolemia (FH) experiments and of the
calibrations share them: a quantity of `readout_dict` is plotted into the row
of `axes` (`axes_liver` for the liver model) with its label, color and unit.
"""

from typing import TypedDict

from matplotlib.typing import LineStyleType


class Readout(TypedDict):
    """A quantity of the figures: its selection, labels, color and units."""

    sid: str
    y_label: str
    label: str
    color: str
    #: unit of the figures
    unit: str
    #: unit of the selection in the model
    model_unit: str


class DoseProtocol(TypedDict):
    """A daily oral dose of simvastatin and its style in the figures."""

    #: the dose part of the simulation ids
    key: str
    #: the dose [mg]
    dose: float
    color: str
    alpha: float
    marker: str
    linestyle: LineStyleType


#: the time to the steady state of a FH type and the time of the treatment [weeks]
time_FH_steadystate: int = 52
time_SV_treatment: int = 52


#: the quantities of the figures
readout_dict: dict[str, Readout] = {
    "plasma simva": {
        "sid": "[Cve_simva]",
        "y_label": "Plasma concentration",
        "label": "Plasma SV",
        "color": "black",
        "unit": "nM",
        "model_unit": "mmol/l",
    },
    "plasma simacid": {
        "sid": "[Cve_simacid]",
        "y_label": "Plasma concentration",
        "label": "Plasma SVA",
        "color": "blue",
        "unit": "nM",
        "model_unit": "mmol/l",
    },
    "plasma ldlc": {
        "sid": "[Cve_ldlc]",
        "y_label": "Plasma LDL-C",
        "label": "Plasma LDL-C",
        "color": "black",
        "unit": "mM",
        "model_unit": "mmol/l",
    },
    "plasma vldlc": {
        "sid": "[Cve_vldlc]",
        "y_label": "Plasma VLDL-C",
        "label": "Plasma VLDL-C",
        "color": "tab:blue",
        "unit": "mM",
        "model_unit": "mmol/l",
    },
    "hepatic cho": {
        "sid": "[LI__cho]",
        "y_label": "Hepatic cholesterol",
        "label": "Hepatic cholesterol",
        "color": "black",
        "unit": "mM",
        "model_unit": "mmol/l",
    },
    # ldlr
    "LDLR": {
        "sid": "LI__ldlr",
        "y_label": "LDLR pool",
        "label": "LDLR",
        "color": "tab:red",
        "unit": "1/litre",
        "model_unit": "1/litre",
    },
    "LDLR-LDLC complex": {
        "sid": "LI__ldlr_ldlc",
        "y_label": "LDLR pool",
        "label": "LDLR-LDL-C",
        "color": "tab:blue",
        "unit": "1/litre",
        "model_unit": "1/litre",
    },
    "LDLR membrane": {
        "sid": "LI__ldlr_membrane",
        "y_label": "LDLR pool",
        "label": "LDLR membrane",
        "color": "tab:orange",
        "unit": "1/litre",
        "model_unit": "1/litre",
    },
    # -----------------------------------
    # fractions ldlr
    "LDLR total": {
        "sid": "LI__ldlr_total",
        "label": "LDLR total",
        "y_label": "Fraction of\ntotal LDLR",
        "color": "black",
        "unit": "dimensionless",
        "model_unit": "dimensionless",
    },
    "LDLR fraction": {
        "sid": "LI__ldlr_fraction",
        "y_label": "Fraction of\ntotal LDLR",
        "label": "LDLR",
        "color": "tab:red",
        "unit": "dimensionless",
        "model_unit": "dimensionless",
    },
    "LDLR-LDLC fraction": {
        "sid": "LI__ldlr_ldlc_fraction",
        "y_label": "Fraction of\ntotal LDLR",
        "label": "LDLR-LDL-C",
        "color": "tab:blue",
        "unit": "dimensionless",
        "model_unit": "dimensionless",
    },
    "LDLR membrane fraction": {
        "sid": "LI__ldlr_membrane_fraction",
        "y_label": "Fraction of\ntotal LDLR",
        "label": "LDLR membrane",
        "color": "tab:orange",
        "unit": "dimensionless",
        "model_unit": "dimensionless",
    },
    # ---------------------------------------
    "LDLR degradation": {
        "sid": "LI__DEGRADATION_LDLR",
        "y_label": "LDLR rates",
        "label": "LDLR degradation",
        "color": "tab:red",
        "unit": "mmole/hr",
        "model_unit": "mmole/min",
    },
    "LDLR synthesis": {
        "sid": "LI__SYNTHESIS_LDLR",
        "y_label": "LDLR rates",
        "label": "LDLR synthesis",
        "color": "tab:blue",
        "unit": "mmole/hr",
        "model_unit": "mmole/min",
    },
    "LDLR-LDLC binding/uptake": {
        "sid": "LI__LDLRLDLCIMP",
        "y_label": "LDLR rates",
        "label": "LDL-C binding/uptake",
        "color": "tab:green",
        "unit": "mmole/hr",
        "model_unit": "mmole/min",
    },
    "LDLR membrane transport": {
        "sid": "LI__LDLR_TO_MEMBRANE",
        "y_label": "LDLR rates",
        "label": "LDLR membrane transport",
        "color": "tab:orange",
        "unit": "mmole/hr",
        "model_unit": "mmole/min",
    },
    "LDLR recycling": {
        "sid": "LI__LDLRRECYCLING",
        "y_label": "LDLR rates",
        "label": "LDLR recycling",
        "color": "tab:brown",
        "unit": "mmole/hr",
        "model_unit": "mmole/min",
    },
    "LDLR turnover": {
        "sid": "LI__TURNOVER_LDLR",
        "y_label": "LDLR rates",
        "label": "LDLR turnover",
        "color": "tab:purple",
        "unit": "mmole/hr",
        "model_unit": "mmole/min",
    },
    # Rates liver LDLC in [mg/day]
    "LDLC liver synthesis": {
        "sid": "LI__v_synthesis",
        "y_label": "LDL-C liver\nrates ",
        "label": "Cholesterol synthesis",
        "color": "tab:green",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC liver net export": {
        "sid": "LI__v_net_export",
        "y_label": "LDL-C liver\nrates ",
        "label": "LDL-C liver net export",
        "color": "black",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC liver uptake": {
        "sid": "LI__v_uptake",
        "y_label": "LDL-C liver\nrates ",
        "label": "LDL-C uptake",
        "color": "tab:blue",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC liver export": {
        "sid": "LI__v_export",
        "y_label": "LDL-C liver\nrates ",
        "label": "VLDL-C export",
        "color": "tab:red",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    # whole body rates in [mg/day]
    "LDLC liver net balance": {
        "sid": "LI__v_liver_balance",  # [mg/day]
        "y_label": "LDL-C plasma\nrates ",
        "label": "LDL-C net liver balance",
        "color": "tab:orange",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC net consumption": {
        "sid": "v_ldlc_net_consumption",  # [mg/day]
        "y_label": "LDL-C plasma\nrates ",
        "label": "LDL-C net consumption",
        "color": "tab:green",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC utilization": {
        "sid": "v_ldlc_utilization",  # [mg/day]
        "y_label": "LDL-C plasma\nrates ",
        "label": "LDL-C utilization",
        "color": "tab:red",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC loss": {
        "sid": "v_ldlc_loss",  # [mg/day]
        "y_label": "LDL-C plasma\nrates",
        "label": "LDL-C loss",
        "color": "tab:brown",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "LDLC diet": {
        "sid": "v_ldlc_diet",  # [mg/day]
        "y_label": "LDL-C plasma\nrates ",
        "label": "LDL-C diet",
        "color": "tab:purple",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    "VLDLC LDLC conversion": {
        "sid": "v_vldlc_conversion",  # [mg/day]
        "y_label": "LDL-C plasma\nrates ",
        "label": "VLDL-C to LDL-C conversion",
        "color": "tab:blue",
        "unit": "g/day",
        "model_unit": "mg/day",
    },
    # whole-body rates in [mmole/min]
    "LDLC loss rate": {
        "sid": "ldlc_loss",
        "y_label": "LDL-C plasma loss",
        "label": "LDL-C plasma loss",
        "color": "tab:blue",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC diet rate": {
        "sid": "ldlc_diet",
        "y_label": "LDL-C plasma diet",
        "label": "LDL-C plasma diet",
        "color": "tab:purple",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC utlilization rate": {
        "sid": "ldlc_utilization",
        "y_label": "LDL-C plasma utilization",
        "label": "LDL-C plasma utilization",
        "color": "tab:orange",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC synthesis rate": {
        "sid": "LI__HMGCOAREDUCTASE",
        "y_label": "LDL-C synthesis",
        "label": "LDL-C synthesis",
        "color": "tab:green",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC export rate": {
        "sid": "LI__VLDLCEXP",
        "y_label": "LDL-C export",
        "label": "LDL-C export",
        "color": "tab:red",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC liver net export rate": {
        "sid": "LI__v_net_export_rate",
        "y_label": "LDL-C export",
        "label": "LDL-C export",
        "color": "black",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC uptake rate": {
        "sid": "LI__LDLRLDLCIMP",
        "y_label": "LDL-C uptake",
        "label": "LDL-C uptake",
        "color": "tab:blue",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
    "LDLC consumption rate": {
        "sid": "ldlc_net_consumption",
        "y_label": "LDL-C net consumption",
        "label": "LDL-C net consumption",
        "color": "indigo",
        "unit": "mmole/min",
        "model_unit": "mmole/min",
    },
}

#: colors of the simvastatin doses [mg]
colors_dose: dict[float, str] = {
    0: "black",
    2: "yellow",
    2.5: "yellow",
    5: "#ffeda0",
    10: "#fed976",
    13: "#fed976",
    20: "#fd8d3c",
    40: "#fc4e2a",
    80: "#e31a1c",
    160: "#b10026",
}

#: the daily oral doses of simvastatin of the FH experiments, `control` without
simvastatin_protocol: dict[str, DoseProtocol] = {
    "control": {
        "key": "simva_po_0mg",
        "dose": 0,
        "color": colors_dose[0],
        "alpha": 1,
        "marker": "o",
        "linestyle": "dashed",
    },
    "2.5 mg": {
        "key": "simva_po_2_5mg",
        "dose": 2.5,
        "color": colors_dose[2.5],
        "alpha": 0.16,
        "marker": "o",
        "linestyle": "solid",
    },
    "5 mg": {
        "key": "simva_po_5mg",
        "dose": 5,
        "color": colors_dose[5],
        "alpha": 0.32,
        "marker": "o",
        "linestyle": "solid",
    },
    "10 mg": {
        "key": "simva_po_10mg",
        "dose": 10,
        "color": colors_dose[10],
        "alpha": 0.48,
        "marker": "o",
        "linestyle": "solid",
    },
    "20 mg": {
        "key": "simva_po_20mg",
        "dose": 20,
        "color": colors_dose[20],
        "alpha": 0.64,
        "marker": "s",
        "linestyle": "solid",
    },
    "40 mg": {
        "key": "simva_po_40mg",
        "dose": 40,
        "color": colors_dose[40],
        "alpha": 0.8,
        "marker": "o",
        "linestyle": "solid",
    },
    "80 mg": {
        "key": "simva_po_80mg",
        "dose": 80,
        "color": colors_dose[80],
        "alpha": 1.0,
        "marker": "o",
        "linestyle": "solid",
    },
    "160 mg": {
        "key": "simva_po_160mg",
        "dose": 160,
        "color": colors_dose[160],
        "alpha": 1.0,
        "marker": "o",
        "linestyle": "solid",
    },
}

#: the row of a quantity of `readout_dict` in the figures of the body model
axes: dict[str, int] = {
    # [mM]
    "plasma simva": 0,
    "plasma simacid": 0,
    # [mM]
    "plasma ldlc": 1,
    "plasma vldlc": 1,
    # [mM]
    "hepatic cho": 2,
    # [1/litre]
    "LDLR": 3,
    "LDLR-LDLC complex": 3,
    "LDLR membrane": 3,
    # [dimensionless]
    "LDLR fraction": 4,
    "LDLR-LDLC fraction": 4,
    "LDLR membrane fraction": 4,
    # [mmole/hr]
    "LDLR degradation": 5,
    "LDLR synthesis": 5,
    "LDLR membrane transport": 5,
    "LDLR recycling": 5,
    "LDLR-LDLC binding/uptake": 5,
    "LDLR turnover": 5,
    # [mg/day]
    "LDLC liver net export": 6,
    "LDLC liver uptake": 6,
    "LDLC liver export": 6,
    "LDLC liver synthesis": 6,
    # [mg/day]
    "LDLC loss": 7,  # whole body rate
    "LDLC diet": 7,  # whole body rate
    "LDLC net consumption": 7,  # whole body rate
    "VLDLC LDLC conversion": 7,  # whole body rate
}

#: the row of a quantity of `readout_dict` in the figures of the liver model
axes_liver: dict[str, int] = {
    # [mM]
    "plasma ldlc": 0,
    # [mM]
    "hepatic cho": 1,
    # [1/litre]
    "LDLR": 2,
    "LDLR-LDLC complex": 2,
    "LDLR membrane": 2,
    "LDLR total": 2,
    # [dimensionless]
    "LDLR fraction": 3,
    "LDLR-LDLC fraction": 3,
    "LDLR membrane fraction": 3,
    # [mmole/hr]
    "LDLR degradation": 4,
    "LDLR synthesis": 4,
    "LDLR membrane transport": 4,
    "LDLR recycling": 4,
    "LDLR-LDLC binding/uptake": 4,
    "LDLR turnover": 4,
    # [mg/day]
    "LDLC liver net export": 5,
    "LDLC liver uptake": 5,
    "LDLC liver export": 5,
    "LDLC liver synthesis": 5,
    # [mmole/min]
    "LDLC liver net export rate": 6,
    "LDLC uptake rate": 6,
    "LDLC export rate": 6,
}
