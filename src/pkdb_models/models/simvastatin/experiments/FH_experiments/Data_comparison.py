"""Comparison of the LDL-C data of the cholesterol studies with the simulations.

A figure script of the manuscript, not a simulation experiment: it compares the
observed absolute and relative change of the LDL-C of the studies with the
change predicted for every FH type, and reads the results of earlier runs which
were saved (`save_results=True`):

```python
from pkdb_models.models.simvastatin import MODEL
from pkdb_models.models.simvastatin.experiments.FH_experiments import (
    FH_scan_simulation,
)
from pkdb_models.models.simvastatin.simulations import EXPERIMENTS

# the datasets and simulations of the studies, `studies/<study>/`
MODEL.run_experiments(EXPERIMENTS["studies"], output_dir="studies", save_results=True)
# the scan of the doses, `scans/FH_scan_simulation/`
MODEL.run_experiments(FH_scan_simulation, output_dir="scans", save_results=True)
```

The directories are relative to `MODEL.simulation_dir`, as the groups of
`run_simulation`: `DataComparison.results_studies` and
`DataComparison.results_scan`. The figures are written into
`MODEL.results_dir`:

```bash
python Data_comparison.py
```
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TypedDict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from matplotlib.typing import LineStyleType

from pkdb_models.models.simvastatin import (
    DATA_PATH_CHOLESTEROL,
    DATA_PATH_SIMVASTATIN,
    MODEL,
)
from pkdb_models.models.simvastatin.experiments.base_experiment import FontKwargs
from pkdb_models.models.simvastatin.experiments.FH_experiments.readout_dict_FH_scans import (
    colors_dose,
    simvastatin_protocol,
)
from pkdb_models.models.simvastatin.experiments.simva_helpers import colormap_SV_dose

logger = logging.getLogger(__name__)


class StudyDatasets(TypedDict):
    """The LDL-C datasets of a study and the simulations they are compared with."""

    datasets: list[str]
    tasks: list[str]


class TickKwargs(TypedDict):
    """Font of the tick labels."""

    weight: str
    fontsize: int


@dataclass
class ObservedData:
    """The LDL-C dataset of a study.

    Attributes:
        intervention: the dose of simvastatin [mg], for the color.
        data: the dataset with the time in weeks, rounded to 2 digits.
        group_count: the number of subjects at time 0, for the marker size.
        timepoints: the times of the dataset, the first time is 0.
    """

    intervention: float
    data: pd.DataFrame
    group_count: np.ndarray
    timepoints: pd.Series


@dataclass
class PredictedChanges:
    """The predicted LDL-C of a study for every FH type at the times of the data.

    Every frame has a column per FH type and the `mean`, `min`, `max` and `sd`
    over the FH types.

    Attributes:
        relative_change: the relative change of the LDL-C [%].
        absolute_change: the absolute change of the LDL-C [mM].
        concentration: the LDL-C [mM].
    """

    relative_change: pd.DataFrame
    absolute_change: pd.DataFrame
    concentration: pd.DataFrame


class DataComparison:
    """Comparison of the observed and the predicted change of the LDL-C."""

    #: the results of the studies, a directory per study
    results_studies: ClassVar[Path] = MODEL.simulation_dir / "studies"
    #: the results of `FH_scan_simulation`
    results_scan: ClassVar[Path] = MODEL.simulation_dir / "scans" / "FH_scan_simulation"

    #: the LDL-C datasets of the studies and their simulations
    datasets: ClassVar[dict[str, StudyDatasets]] = {
        # studies with reported concentrations
        "Geiss2002": {
            "datasets": ["Tab1_ldl_c_SIM_FH", "Tab1_ldl_c_SIM_diabetics"],
            "tasks": ["simva_po_FH", "simva_po_diabetics"],
        },
        "Keech1994": {
            "datasets": ["Fig1_ldl_c_SIM20", "Fig1_ldl_c_SIM40"],
            "tasks": ["simva_po_20mg", "simva_po_40mg"],
        },
        "Kosoglou2002": {
            "datasets": ["Tab4_ldl_c_SIM10", "Tab4_ldl_c_SIM20"],
            "tasks": ["simva_po_10mg", "simva_po_20mg"],
        },
        "Li2003": {
            "datasets": ["Tab2_ldl_c_SIM20", "Tab2_ldl_c_SIM40"],
            "tasks": ["simva_po_20mg", "simva_po_40mg"],
        },
        "Loria1993": {"datasets": ["Tab2_ldl_c"], "tasks": ["simva_po_80mg"]},
        "Moelgaard1988": {
            "datasets": ["Tab1_ldl_c", "Tab2_ldl_c"],
            "tasks": ["simva_po_FH_trial", "simva_po_PHC_trial"],
        },
        "Mol1988": {
            "datasets": ["Tab2_ldl_c_group1", "Tab2_ldl_c_group2", "Tab2_ldl_c_group3"],
            "tasks": ["simva_po_group1", "simva_po_group2", "simva_po_group3"],
        },
        "Ntanios1999": {
            "datasets": ["Fig1_ldl_c"],
            "tasks": ["simva_po_all"],
        },
        "Nishio2005": {
            "datasets": ["Fig2_ldl_c_control"],
            "tasks": ["simva_po_5mg_control_cho"],
        },
        "Owens1991": {
            "datasets": ["Fig1_ldl_c_SIM20", "Fig1_ldl_c_SIM40"],
            "tasks": ["simva_po_20mg", "simva_po_40mg"],
        },
        "Pietro1989": {
            "datasets": ["Fig1_ldl_c_SIM20", "Fig1_ldl_c_SIM40"],
            "tasks": ["simva_po_20mg", "simva_po_40mg"],
        },
        "Saito1991": {
            "datasets": [
                "Tab6_ldl_c_2_5mg_morning",
                "Tab6_ldl_c_2_5mg_evening",
                "Tab6_ldl_c_5mg_morning",
                "Tab6_ldl_c_5mg_evening",
            ],
            "tasks": [
                "simva_po_2_5mg_morning",
                "simva_po_2_5mg_evening",
                "simva_po_5mg_morning",
                "simva_po_5mg_evening",
            ],
        },
        "Walker1990": {
            "datasets": [
                "Tab3_ldl_c_SIM2_5",
                "Tab3_ldl_c_SIM5",
                "Tab3_ldl_c_SIM10",
                "Tab3_ldl_c_SIM20",
            ],
            "tasks": [
                "simva_po_2_5mg",
                "simva_po_5mg",
                "simva_po_10mg",
                "simva_po_20mg",
            ],
        },
        # ----------------------------------------------------------------------
        # studies with reported concentration changes
        "Crouse1999": {
            "datasets": [
                "Tab1_ldl_c_SIM40_relative_change",
                "Tab1_ldl_c_SIM80_relative_change",
            ],
            "tasks": ["simva_po_40mg", "simva_po_80mg"],
        },
        "Davidson1997": {
            "datasets": [
                "Tab1_ldl_c_SIM40_relative_change",
                "Tab1_ldl_c_SIM80_relative_change",
                "Tab1_ldl_c_SIM160_relative_change",
            ],
            "tasks": ["simva_po_40mg", "simva_po_80mg", "simva_po_160mg"],
        },
        "Isaacsohn2003": {
            "datasets": [
                "Tab3_ldl_c_SIM20_relative_change",
                "Tab3_ldl_c_SIM40_relative_change",
                "Tab3_ldl_c_SIM80_relative_change",
            ],
            "tasks": ["simva_po_20mg", "simva_po_40mg", "simva_po_80mg"],
        },
        "Jones1998a": {
            "datasets": [
                "Tab1_2_ldl_c_SIM10_relative_change",
                "Tab1_2_ldl_c_SIM20_relative_change",
                "Tab1_2_ldl_c_SIM40_relative_change",
            ],
            "tasks": ["simva_po_10mg", "simva_po_20mg", "simva_po_40mg"],
        },
        "Mol1986": {
            "datasets": [
                "Tab2_ldl_c_SIM2_5_once_relative_change",
                "Tab2_ldl_c_SIM2_5_twice_relative_change",
                "Tab2_ldl_c_SIM10_once_relative_change",
                "Tab2_ldl_c_SIM10_twice_relative_change",
                "Tab2_ldl_c_SIM40_once_relative_change",
                "Tab2_ldl_c_SIM40_twice_relative_change",
            ],
            "tasks": [
                "simva_po_2_5mg_once",
                "simva_po_2_5mg_twice",
                "simva_po_10mg_once",
                "simva_po_10mg_twice",
                "simva_po_40mg_once",
                "simva_po_40mg_twice",
            ],
        },
        "Recto2000": {
            "datasets": [
                "Tab2_ldl_c_SIM20_relative_change",
                "Tab2_ldl_c_SIM40_relative_change",
            ],
            "tasks": ["simva_po_20mg", "simva_po_40mg"],
        },
        "Sivkov2021": {
            "datasets": [
                "Tab3_ldl_c_521TT_relative_change",
                "Tab4_ldl_c_3435TT_relative_change",
            ],
            "tasks": ["simva_po_10mg_521TT", "simva_po_10mg_3435TT"],
        },
        "Tuomilehto1995": {
            "datasets": [
                "Fig1_ldl_c_SIM2_5_relative_change",
                "Fig1_ldl_c_SIM5_relative_change",
                "Fig1_ldl_c_SIM10_relative_change",
                "Fig1_ldl_c_SIM20_relative_change",
                "Fig1_ldl_c_SIM40_relative_change",
            ],
            "tasks": [
                "simva_po_2_5mg",
                "simva_po_5mg",
                "simva_po_10mg",
                "simva_po_20mg",
                "simva_po_40mg",
            ],
        },
    }

    FH_types: ClassVar[list[str]] = [
        "FH_type1",
        "FH_type2_6",
        "FH_type3",
        "FH_type4",
        "FH_type5",
        "PCSK9",
    ]

    # the weights of DejaVu Sans, normal and bold: it has no semibold and no
    # medium weight, matplotlib warns and takes bold and normal
    axis_label_kwargs: ClassVar[FontKwargs] = {"weight": "bold", "size": 16}
    title_kwargs: ClassVar[FontKwargs] = {"weight": "bold", "size": 25}
    annotation_kwargs: ClassVar[FontKwargs] = {"weight": "normal", "size": 8}
    tick_kwargs: ClassVar[TickKwargs] = {"weight": "normal", "fontsize": 12}

    def get_data(self, study: str, dataset_id: str) -> ObservedData:
        """Get the LDL-C dataset of a study.

        Args:
            study: the study, e.g. `Crouse1999`.
            dataset_id: the dataset of the study, without the study.

        Returns:
            The dataset, its dose of simvastatin and its number of subjects.
        """
        data_df = pd.read_csv(
            self.results_studies / study / f"{study}_{dataset_id}.tsv", sep="\t"
        )

        study_info_path = (
            DATA_PATH_SIMVASTATIN if study == "Nishio2005" else DATA_PATH_CHOLESTEROL
        )
        # get df for intervention dose
        intervention_df = pd.read_csv(
            study_info_path / study / f".{study}_TabInterventions.tsv", sep="\t"
        )

        if not dataset_id.endswith("relative_change"):
            data_df = data_df.loc[data_df["measurement_type"] == "concentration"]

        data_df = self.normalize_time_to_weeks(data_df)

        # get SV dose from interventions df: the first intervention of the
        # dataset which the table lists, a dataset can name several
        # (Saito1991: "SIM2_5_morning, placebo_at_the_end")
        names = [name.strip() for name in str(data_df["intervention"][0]).split(",")]
        row = intervention_df.loc[intervention_df["name"].isin(names)].iloc[0]
        column = "value" if "value" in intervention_df.columns else "mean"
        intervention = float(row[column])

        data_df["time"] = np.around(np.array(data_df["time"]), 2)

        # Add dummy timepoint at time = 0 for appearance in plot
        if data_df["time"][0] != 0:
            data_df.loc[0, "time"] = 0
        timepoints = data_df["time"]

        # get group count from group df for the marker size
        group_count = data_df["count"].loc[data_df["time"] == 0].values

        return ObservedData(
            intervention=intervention,
            data=data_df,
            group_count=group_count,
            timepoints=timepoints,
        )

    def get_predictions(
        self, study: str, task_id: str, timepoints: pd.Series
    ) -> PredictedChanges:
        """Get the predicted LDL-C of a study for every FH type.

        Args:
            study: the study, e.g. `Crouse1999`.
            task_id: the simulation of the study, without the FH type.
            timepoints: the times of the data [weeks].

        Returns:
            The predicted LDL-C and its changes at the times of the data.
        """
        # get data from simulation experiments
        df_tasks_complete = pd.DataFrame(columns=["time"])

        for FH_type in self.FH_types:
            df_task = pd.read_csv(
                self.results_studies / study / f"{study}_task_{task_id}_{FH_type}.tsv",
                sep="\t",
            )
            df_task = df_task.loc[:, ["time", "[Cve_ldlc]", "PODOSE_simva"]]
            df_task = df_task.drop_duplicates(keep="first")
            # all time points in unit weeks
            df_task["time"] = df_task["time"] / (60 * 24 * 7)

            df_task = df_task.loc[df_task["time"] >= 0]
            df_task = df_task.reset_index()
            # Add dummy timepoint at time = 0 for appearance in plot
            if df_task["time"][0] != 0:
                df_task.loc[0, "time"] = 0

            if FH_type == "FH_type1":
                df_tasks_complete["time"] = df_task["time"]
            df_tasks_complete[FH_type] = df_task["[Cve_ldlc]"]

        df_tasks_complete["time"] = np.around(np.array(df_tasks_complete["time"]), 2)
        df_tasks_complete["time"] = df_tasks_complete["time"].drop_duplicates(
            keep="first"
        )

        df_tasks_complete = (
            df_tasks_complete.loc[df_tasks_complete["time"].isin(timepoints)]
            .drop_duplicates(keep="first")
            .reset_index()
        )

        # use task df to calculate relative change and do statistical analysis
        df_task_relative = self.calculate_relative_change_FH(df_tasks_complete.copy())
        # use task df to calculate absolute change and do statistical analysis
        df_task_absolute = self.calculate_absolute_change_FH(df_tasks_complete.copy())

        return PredictedChanges(
            relative_change=self.calculate_FH_means(df_task_relative),
            absolute_change=self.calculate_FH_means(df_task_absolute),
            concentration=self.calculate_FH_means(df_tasks_complete.copy()),
        )

    def normalize_time_to_weeks(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Convert the times of a dataset to weeks."""
        # the times in weeks are not integers
        dataframe["time"] = dataframe["time"].astype(float)
        for idx, row in dataframe.iterrows():
            if row["time_unit"] == "min":
                dataframe.at[idx, "time"] = row["time"] / (60 * 24 * 7)
            elif row["time_unit"] == "hr":
                dataframe.at[idx, "time"] = row["time"] / (24 * 7)
            elif row["time_unit"] == "day":
                dataframe.at[idx, "time"] = row["time"] / 7
            elif row["time_unit"] == "weeks":
                dataframe.at[idx, "time"] = row["time"] / 1
            dataframe.at[idx, "time_unit"] = "weeks"
        return dataframe

    def calculate_FH_means(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add the mean, minimum, maximum and standard deviation over the FH types."""
        df_copied = df.copy()
        df_copied = df_copied.drop(columns=["index"])

        df["mean"] = df_copied.iloc[:, 1:6].mean(numeric_only=True, axis=1)
        df["min"] = df_copied.iloc[:, 1:6].min(numeric_only=True, axis="columns")
        df["max"] = df_copied.iloc[:, 1:6].max(numeric_only=True, axis="columns")
        df["sd"] = df_copied.iloc[:, 1:6].std(numeric_only=True, axis="columns")
        return df

    def calculate_relative_change_FH(self, df: pd.DataFrame) -> pd.DataFrame:
        """Relative change of every FH type to its first value [%]."""
        for fh_type in self.FH_types:
            dframe = df[fh_type]
            baseline = dframe[0]
            df[fh_type] = [
                float(((value - baseline) / baseline) * 100) for value in dframe
            ]
        return df

    def calculate_absolute_change_FH(self, df: pd.DataFrame) -> pd.DataFrame:
        """Absolute change of every FH type to its first value."""
        for fh_type in self.FH_types:
            dframe = df[fh_type]
            baseline = dframe[0]
            df[fh_type] = [float(value - baseline) for value in dframe]
        return df

    def relative_change(self, dframe: pd.Series) -> list[float]:
        """Relative change to the first value [%]."""
        baseline = dframe[0]
        return [float(((value - baseline) / baseline) * 100) for value in dframe]

    def absolute_change(self, dframe: pd.Series) -> list[float]:
        """Absolute change to the first value."""
        baseline = dframe[0]
        return [float(value - baseline) for value in dframe]

    def absolute_change_from_relative_change(self, dframe: pd.DataFrame) -> list[float]:
        """Absolute change [mM] of the relative change [%] and the baseline."""
        absolute_change_list = []
        for _, row in dframe.iterrows():
            if row["baseline_unit"] == "mg/dl":
                # mg/dl / g/mol = mmol/l
                absolute_change_list.append(
                    (row["baseline"] * row["mean"] / 100) / 38.67
                )
            else:
                absolute_change_list.append(row["baseline"] * row["mean"] / 100)
        return absolute_change_list

    def scale_marker(self, groupsize: float | np.ndarray) -> np.ndarray:
        """Scale the marker by the group size.

        The area of the marker (pi*r^2) is proportional to the group size.
        """
        return np.sqrt(np.multiply(groupsize, np.pi))

    def uncertainty_propagation_linear(
        self, array1: np.ndarray | pd.Series, array2: np.ndarray | pd.Series
    ) -> np.ndarray:
        """Uncertainty propagation of the SDs of two arrays of independent variables.

        The uncertainty is the root of the sum of the squared errors.
        """
        return np.sqrt(np.add(np.power(array1, 2), np.power(array2, 2)))

    def uncertainty_propagation_worst_case(
        self, array1: np.ndarray, array2: np.ndarray
    ) -> np.ndarray:
        """Uncertainty propagation of the SDs of two arrays of independent variables.

        The uncertainty is the worst case, the sum of both errors.
        """
        return np.add(array1, array2)

    def absolute_error_of_relative_error(
        self,
        relative_change_sd: np.ndarray | pd.Series,
        relative_change_values: np.ndarray | list[float],
        absolute_change_values: np.ndarray | list[float],
    ) -> np.ndarray:
        """SD of the absolute change from the errors of the relative change.

        The coefficient of variation (CV) of the relative change is applied to
        the values of the absolute change. Assumption: the CV stays constant
        when calculating the absolute change from the relative change:
        CV = SD_relative/VALUES_relative -> SD_absolute = CV * values_absolute.
        """
        CV = np.array(relative_change_sd) / np.array(relative_change_values)
        return CV * np.array(absolute_change_values)

    def mean_LDLC(self) -> float:
        """Mean baseline LDL-C of the datasets [mM], weighted by the subjects."""
        ldlc_weighted = 0
        ldlc_unweighted = 0
        subjects_all = 0
        n_datasets = 0
        for study_id, value in self.datasets.items():
            n_subjects_dataset = 0
            for data_id in value["datasets"]:
                data = self.get_data(study_id, data_id.replace("_relative_change", ""))
                df = data.data

                baseline_ldlc = df["mean"][0]
                baseline_ldlc_unit = df["mean_unit"][0]
                if baseline_ldlc_unit == "mg/dl":
                    baseline_ldlc = baseline_ldlc / 38.67  # mg/dl / g/mol = mmol/l

                group_count = data.group_count
                # remember datasets
                n_datasets = n_datasets + 1

                # remember number of subjects
                subjects_all = subjects_all + group_count

                # add unweighted ldlc up
                ldlc_unweighted = ldlc_unweighted + baseline_ldlc

                # calculate weighted ldlc and add it up
                weighted_ldlc = baseline_ldlc * group_count
                ldlc_weighted = ldlc_weighted + weighted_ldlc

                n_subjects_dataset = n_subjects_dataset + group_count
            logger.info("Subjects in %s: %s", study_id, n_subjects_dataset)

        mean_ldlc_unweighted = ldlc_unweighted / n_datasets
        logger.info(
            "non-weighted ldlc: %s with subjects: %s and number datasets: %s",
            mean_ldlc_unweighted,
            subjects_all,
            n_datasets,
        )

        mean_ldlc_weighted = ldlc_weighted / subjects_all
        logger.info(
            "weighted ldlc: %s with subjects: %s", mean_ldlc_weighted, subjects_all
        )
        return mean_ldlc_weighted

    def scan_simulation_data(self, simva_key: str) -> pd.DataFrame:
        """The LDL-C changes of `FH_scan_simulation` of a dose over the FH types."""
        simva_info = simvastatin_protocol[simva_key]

        df = pd.DataFrame()
        df_conc = pd.DataFrame()
        df_absolute = pd.DataFrame()
        df_relative = pd.DataFrame()
        for fh_type in self.FH_types:
            task_id = f"task_{simva_info['key']}_{fh_type}"
            tsv_path = self.results_scan / f"FH_scan_simulation_{task_id}.tsv"

            df_csv = pd.read_csv(tsv_path, sep="\t")
            df_csv = df_csv.drop_duplicates(keep="first")
            df_csv = df_csv.loc[df_csv["time"] >= 0]
            df_csv = df_csv.reset_index()
            time_vec = df_csv["time"] / (60 * 24 * 7)
            df["time"] = time_vec
            df_conc["time"] = time_vec
            df_relative["time"] = time_vec
            df_absolute["time"] = time_vec

            df_conc[fh_type] = df_csv["[Cve_ldlc]"]

            baseline_single = df_conc[fh_type].loc[df_conc["time"] == 0]
            df_absolute[f"{fh_type} absolute change"] = (
                df_conc[fh_type] - baseline_single.values[0]
            )
            df_relative[f"{fh_type} relative change"] = (
                (df_conc[fh_type] - baseline_single.values[0])
                / baseline_single.values[0]
                * 100
            )

        # calculate mean and max across the columns of FH types
        df["mean"] = df_conc.iloc[:, 1:6].mean(axis="columns")
        df["min"] = df_conc.iloc[:, 1:6].min(axis="columns")
        df["max"] = df_conc.iloc[:, 1:6].max(axis="columns")

        df["absolute change mean"] = df_absolute.iloc[:, 1:6].mean(axis="columns")
        df["absolute change min"] = df_absolute.iloc[:, 1:6].min(axis="columns")
        df["absolute change max"] = df_absolute.iloc[:, 1:6].max(axis="columns")

        df["relative change mean"] = df_relative.iloc[:, 1:6].mean(axis="columns")
        df["relative change min"] = df_relative.iloc[:, 1:6].min(axis="columns")
        df["relative change max"] = df_relative.iloc[:, 1:6].max(axis="columns")

        return df

    def observed_changes(
        self, dataset_id: str, data: ObservedData
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Observed relative and absolute change of the LDL-C of a dataset.

        Args:
            dataset_id: the dataset of the study.
            data: the dataset.

        Returns:
            The relative change [%], its SD (0 if the study has none) and the
            absolute change [mM].
        """
        if dataset_id.endswith("relative_change"):
            # data that reports relative change data with or without SDs
            relative_change_observed = np.array(data.data["mean"].values)
            # calculate absolute change from relative change
            absolute_change_observed = np.array(
                self.absolute_change_from_relative_change(data.data)
            )
            if "mean_sd" in list(data.data.columns):
                relative_change_observed_sd = np.array(data.data["mean_sd"].fillna(0))
            else:
                # if data has no mean sd, fill up the vector with zeros
                relative_change_observed_sd = np.zeros(len(absolute_change_observed))
        else:
            # concentration data without SDs
            relative_change_observed = np.array(self.relative_change(data.data["mean"]))
            absolute_change_observed = np.array(self.absolute_change(data.data["mean"]))
            relative_change_observed_sd = np.zeros(len(absolute_change_observed))
        return (
            relative_change_observed,
            relative_change_observed_sd,
            absolute_change_observed,
        )

    def create_figure_single_FH(self) -> dict[str, FigureMPL]:
        """Observed versus predicted change of the LDL-C for every FH type."""
        figures: dict[str, FigureMPL] = {}

        # ------------------------------------------------------
        # create plots for all FH types
        # ------------------------------------------------------
        fig, axs = plt.subplots(nrows=2, ncols=6, figsize=(36, 12), sharey="row")
        fig.subplots_adjust(
            left=0.05, right=0.91, top=0.92, bottom=0.1, wspace=0.05, hspace=0.22
        )

        # the title and the column of the FH types
        FH_dict: dict[str, tuple[str, int]] = {
            "FH_type1": ("FH class 1\nLDLR synthesis", 0),
            "FH_type2_6": ("FH class 2 & 6\nLDLR membrane transport", 1),
            "FH_type3": ("FH class 3\nLDLR-LDL binding", 2),
            "FH_type4": ("FH class 4\nLDLR-LDL internalization", 3),
            "FH_type5": ("FH class 5\nLDLR recycling", 4),
            "PCSK9": ("PCSK9 mutation\nLDLR degradation", 5),
        }

        axs[0, 0].set_ylabel(
            "Observed absolute reduction\nLDL-C [mM]", **self.axis_label_kwargs
        )
        axs[1, 0].set_ylabel(
            "Observed relative reduction\nLDL-C [%]", **self.axis_label_kwargs
        )

        # plot datapoints
        for study_id, value in self.datasets.items():
            for dataset_id, task_id in zip(
                value["datasets"], value["tasks"], strict=True
            ):
                data = self.get_data(study_id, dataset_id)
                predictions = self.get_predictions(study_id, task_id, data.timepoints)
                linestyle = "dashed" if task_id.endswith("twice") else "solid"

                # the number of subjects at time 0
                markersize = self.scale_marker(data.group_count).item()

                # calculate and plot absolute and relative change
                for fh_key, (title, ax_column) in FH_dict.items():
                    # title and xlabels
                    axs[0, ax_column].set_title(title, **self.title_kwargs)
                    axs[0, ax_column].set_xlabel(
                        "Predicted absolute reduction\nLDL-C [mM]",
                        **self.axis_label_kwargs,
                    )
                    axs[1, ax_column].set_xlabel(
                        "Predicted relative reduction\nLDL-C [%]",
                        **self.axis_label_kwargs,
                    )

                    # get data
                    (
                        relative_change_observed,
                        relative_change_observed_sd,
                        absolute_change_observed,
                    ) = self.observed_changes(dataset_id, data)

                    relative_change_predicted = np.array(
                        predictions.relative_change[fh_key].values
                    )
                    absolute_change_predicted = np.array(
                        predictions.absolute_change[fh_key].values
                    )

                    # use coefficient of variation to calculate the SD of the
                    # absolute change from relative change SDs
                    absolute_change_observed_sd = self.absolute_error_of_relative_error(
                        relative_change_observed_sd,
                        relative_change_observed,
                        absolute_change_observed,
                    )

                    # set color once
                    color = colormap_SV_dose(data.intervention)

                    # plot everything
                    axs[0, ax_column].errorbar(
                        absolute_change_predicted[0],
                        absolute_change_observed[0],
                        yerr=absolute_change_observed_sd[0],
                        color="black",
                        linestyle=linestyle,
                        linewidth=1.0,
                        capsize=0.0,
                        alpha=0.5,
                        markersize=markersize,
                        marker="o",
                        markerfacecolor=color,
                    )

                    axs[0, ax_column].errorbar(
                        absolute_change_predicted[1:],
                        absolute_change_observed[1:],
                        yerr=absolute_change_observed_sd[1:],
                        color="black",
                        linestyle=linestyle,
                        linewidth=1.0,
                        capsize=0.0,
                        alpha=0.5,
                        markersize=markersize,
                        marker="o",
                        markerfacecolor=color,
                    )
                    axs[1, ax_column].errorbar(
                        x=relative_change_predicted[0],
                        y=relative_change_observed[0],
                        yerr=relative_change_observed_sd[0],
                        color="black",
                        linestyle=linestyle,
                        linewidth=1.0,
                        capsize=0.0,
                        alpha=0.5,
                        markersize=markersize,
                        marker="o",
                        markerfacecolor=color,
                    )
                    axs[1, ax_column].errorbar(
                        x=relative_change_predicted[1:],
                        y=relative_change_observed[1:],
                        yerr=relative_change_observed_sd[1:],
                        color="black",
                        linestyle=linestyle,
                        linewidth=1.0,
                        capsize=0.0,
                        alpha=0.5,
                        markersize=markersize,
                        marker="o",
                        markerfacecolor=color,
                    )

                    axs[0, ax_column].annotate(
                        study_id,
                        (absolute_change_predicted[-1], absolute_change_observed[-1]),
                        **self.annotation_kwargs,
                    )
                    axs[1, ax_column].annotate(
                        study_id,
                        (relative_change_predicted[-1], relative_change_observed[-1]),
                        **self.annotation_kwargs,
                    )

        # coordinates for unity line
        coordinate_absolute = [-10, 0]
        coordinate_relative = [-100, 0]
        for k in range(6):
            for n_row, coordinate in enumerate(
                [coordinate_absolute, coordinate_relative]
            ):
                axs[n_row, k].plot(coordinate, coordinate, color="black", alpha=0.9)

            axs[0, k].set_xlim(-7.5, 0)
            axs[0, k].set_ylim(-7.5, 0)
            axs[1, k].set_xlim(-77, 0)
            axs[1, k].set_ylim(-77, 0)

            axs[0, k].get_xaxis().set_ticks([0, -1, -2, -3, -4, -5, -6, -7])
            axs[1, k].get_xaxis().set_ticks([0, -10, -20, -30, -40, -50, -60, -70])

            axs[0, k].get_yaxis().set_ticks([0, -1, -2, -3, -4, -5, -6, -7])
            axs[1, k].get_yaxis().set_ticks([0, -10, -20, -30, -40, -50, -60, -70])

            for n_row in range(2):
                axs[n_row, k].invert_xaxis()
                axs[n_row, k].invert_yaxis()

        axs[0, 5].legend(
            handles=self._dosing_handles(),
            ncol=1,
            loc="upper left",
            bbox_to_anchor=(1.03, 0.8),
            prop={"size": 20},
        )
        axs[1, 5].legend(
            handles=self._dose_handles(),
            ncol=1,
            loc="upper left",
            bbox_to_anchor=(1.03, 1.6),
            prop={"size": 20},
        )
        axs[1, 4].legend(
            handles=self._marker_size_handles(),
            ncol=1,
            loc="upper left",
            bbox_to_anchor=(2.2, 0.8),
            prop={"size": 20},
        )

        fig.show()
        fig.savefig(MODEL.results_dir / "Data_comparison_single_FH.svg", format="svg")

        figures["plot_supplement"] = fig
        return figures

    def _dosing_handles(self) -> list[Line2D]:
        """Legend of the line styles of the dosing schemes."""
        handles = []
        schemes: list[LineStyleType] = ["solid", "dashed"]
        for scheme in schemes:
            label = "Once daily\ndosing" if scheme == "solid" else "Twice daily\ndosing"
            handles.append(Line2D([], [], color="black", label=label, linestyle=scheme))
        return handles

    def _dose_handles(self) -> list[Line2D]:
        """Legend of the marker colors of the doses of simvastatin."""
        handles = []
        for dose in colors_dose:
            if dose in [0, 2, 13]:
                continue
            color = colormap_SV_dose(dose)
            handles.append(
                Line2D(
                    [],
                    [],
                    marker="o",
                    color=color,
                    label=f"{dose} mg SV",
                    markerfacecolor=color,
                    markeredgecolor="black",
                )
            )
        return handles

    def _marker_size_handles(self) -> list[Line2D]:
        """Legend of the marker sizes of the numbers of subjects."""
        return [
            Line2D(
                [],
                [],
                marker="o",
                markersize=float(self.scale_marker(marker)),
                color="black",
                label=str(marker),
            )
            for marker in [1, 10, 30, 50, 100]
        ]

    def create_figure_summary(self) -> dict[str, FigureMPL]:
        """Observed and predicted change of the LDL-C over time and the residuals."""
        figures: dict[str, FigureMPL] = {}
        # ------------------------------------------------------
        # CREATE SUMMARY PLOT
        # ------------------------------------------------------
        fig_summary, axs_summary = plt.subplots(
            nrows=2,
            ncols=3,
            figsize=(26, 13),
        )
        fig_summary.subplots_adjust(
            top=0.99,
            left=0.05,
            bottom=0.08,
            right=0.89,
            wspace=0.21,
            hspace=0.21,
        )

        # ---------------------------------------------------------------
        # plot the scan simulation experiment in column with index 1
        for simva_key, simva_info in simvastatin_protocol.items():
            if simva_key == "control":
                # `FH_scan_simulation` has no simulations without simvastatin
                continue
            simva_df = self.scan_simulation_data(simva_key=simva_key)
            color = colormap_SV_dose(dose=simva_info["dose"])
            for k, change_type in enumerate(["absolute", "relative"]):
                axs_summary[k, 1].fill_between(
                    simva_df["time"],
                    simva_df[f"{change_type} change max"],
                    simva_df[f"{change_type} change min"],
                    facecolor=color,
                    alpha=0.3,
                )

                axs_summary[k, 1].plot(
                    simva_df["time"],
                    simva_df[f"{change_type} change mean"],
                    color=color,
                )

        # plot datapoints
        for study_id, value in self.datasets.items():
            for dataset_id, task_id in zip(
                value["datasets"], value["tasks"], strict=True
            ):
                data = self.get_data(study_id, dataset_id)
                predictions = self.get_predictions(study_id, task_id, data.timepoints)

                # the number of subjects at time 0
                markersize = self.scale_marker(data.group_count).item()
                linestyle = "dashed" if task_id.endswith("twice") else "solid"
                time = np.array(data.data["time"].values)
                time_length = len(time)
                # add random noise to time vector
                time = time + np.random.uniform(-0.25, 0.25, time_length)

                # calculate and plot absolute and relative change from data
                (
                    relative_change_observed,
                    relative_change_observed_sd,
                    absolute_change_observed,
                ) = self.observed_changes(dataset_id, data)

                # use coefficient of variation to calculate the SD of the
                # absolute change from relative change SDs
                absolute_change_observed_sd = self.absolute_error_of_relative_error(
                    relative_change_observed_sd,
                    relative_change_observed,
                    absolute_change_observed,
                )

                # set color once for every datapoints
                color = colormap_SV_dose(data.intervention)

                # plot everything
                axs_summary[0, 1].errorbar(
                    x=time[0],
                    y=absolute_change_observed[0],
                    yerr=absolute_change_observed_sd[0],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[0, 1].errorbar(
                    x=time[1:],
                    y=absolute_change_observed[1:],
                    yerr=absolute_change_observed_sd[1:],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[1, 1].errorbar(
                    x=time[0],
                    y=relative_change_observed[0],
                    yerr=relative_change_observed_sd[0],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[1, 1].errorbar(
                    x=time[1:],
                    y=relative_change_observed[1:],
                    yerr=relative_change_observed_sd[1:],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )

                axs_summary[0, 1].annotate(
                    study_id,
                    (time[-1] + 0.15, absolute_change_observed[-1]),
                    **self.annotation_kwargs,
                )
                axs_summary[1, 1].annotate(
                    study_id,
                    (time[-1] + 0.15, relative_change_observed[-1]),
                    **self.annotation_kwargs,
                )

                # -----------------------------------
                # plot predicted vs observed change in column with index 0
                axs_summary[0, 0].errorbar(
                    x=predictions.absolute_change["mean"][0],
                    y=absolute_change_observed[0],
                    yerr=absolute_change_observed_sd[0],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )

                axs_summary[0, 0].errorbar(
                    x=predictions.absolute_change["mean"][1:],
                    y=absolute_change_observed[1:],
                    yerr=absolute_change_observed_sd[1:],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[0, 0].hlines(
                    xmin=predictions.absolute_change["min"],
                    xmax=predictions.absolute_change["max"],
                    y=absolute_change_observed,
                    color="black",
                    linestyle="solid",
                    linewidth=1.0,
                    alpha=0.5,
                )

                axs_summary[1, 0].errorbar(
                    x=predictions.relative_change["mean"][0],
                    y=relative_change_observed[0],
                    yerr=relative_change_observed_sd[0],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[1, 0].errorbar(
                    x=predictions.relative_change["mean"][1:],
                    y=relative_change_observed[1:],
                    yerr=relative_change_observed_sd[1:],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[1, 0].hlines(
                    xmin=predictions.relative_change["min"],
                    xmax=predictions.relative_change["max"],
                    y=relative_change_observed,
                    color="black",
                    linestyle="solid",
                    linewidth=1.0,
                    alpha=0.5,
                )

                axs_summary[0, 0].annotate(
                    study_id,
                    (
                        (predictions.absolute_change["mean"].values)[-1] - 0.15,
                        absolute_change_observed[-1],
                    ),
                    **self.annotation_kwargs,
                )
                axs_summary[1, 0].annotate(
                    study_id,
                    (
                        (predictions.relative_change["mean"].values)[-1] - 0.15,
                        relative_change_observed[-1],
                    ),
                    **self.annotation_kwargs,
                )
                # --------------------------------------------------------------
                # plot residuals in column with index 2
                # calculate residuals and corresponding SDs using uncertainty
                # propagation
                absolute_change_residuals = np.subtract(
                    predictions.absolute_change["mean"],
                    absolute_change_observed,
                )
                absolute_change_residuals_sd = self.uncertainty_propagation_linear(
                    predictions.absolute_change["sd"],
                    absolute_change_observed_sd,
                )

                relative_change_residuals = np.subtract(
                    predictions.relative_change["mean"],
                    relative_change_observed,
                )
                relative_change_residuals_sd = self.uncertainty_propagation_linear(
                    predictions.relative_change["sd"],
                    relative_change_observed_sd,
                )

                axs_summary[0, 2].errorbar(
                    time[0],
                    absolute_change_residuals[0],
                    yerr=absolute_change_residuals_sd[0],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[0, 2].errorbar(
                    time[1:],
                    absolute_change_residuals[1:],
                    yerr=absolute_change_residuals_sd[1:],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )

                axs_summary[1, 2].errorbar(
                    time[0],
                    relative_change_residuals[0],
                    yerr=relative_change_residuals_sd[0],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )
                axs_summary[1, 2].errorbar(
                    time[1:],
                    relative_change_residuals[1:],
                    yerr=relative_change_residuals_sd[1:],
                    color="black",
                    capsize=0.0,
                    linestyle=linestyle,
                    linewidth=1.0,
                    alpha=0.5,
                    marker="o",
                    markersize=markersize,
                    markerfacecolor=color,
                )

                axs_summary[0, 2].annotate(
                    study_id,
                    (time[-1] + 0.15, absolute_change_residuals.values[-1]),
                    **self.annotation_kwargs,
                )
                axs_summary[1, 2].annotate(
                    study_id,
                    (time[-1] + 0.15, relative_change_residuals.values[-1]),
                    **self.annotation_kwargs,
                )

        # ----------------------------------------------------------------------

        # plot adjustments
        axs_summary[0, 1].set_ylabel(
            "Absolute change LDLC [mM]", **self.axis_label_kwargs
        )
        axs_summary[1, 1].set_ylabel(
            "Relative change LDLC [%]", **self.axis_label_kwargs
        )

        # ----------------------------------------------------
        # plot adjustments labels for column 0
        for n_row in range(2):
            axs_summary[n_row, 0].plot(
                0, 0, color="black", marker="o", markersize=15, markerfacecolor="black"
            )

        axs_summary[0, 0].set_ylabel(
            "Observed absolute change\nLDL-C [mM]", **self.axis_label_kwargs
        )
        axs_summary[0, 0].set_xlabel(
            "Predicted absolute change\nLDL-C [mM]", **self.axis_label_kwargs
        )

        axs_summary[1, 0].set_ylabel(
            "Observed relative change\nLDL-C [%]", **self.axis_label_kwargs
        )
        axs_summary[1, 0].set_xlabel(
            "Predicted relative change\nLDL-C [%]", **self.axis_label_kwargs
        )

        axs_summary[0, 2].set_ylabel(
            "Residuals absolute change\nLDL-C [mM] (Predicted-Observed)",
            **self.axis_label_kwargs,
        )
        axs_summary[1, 2].set_ylabel(
            "Residuals relative change\nLDL-C [%]  (Predicted-Observed)",
            **self.axis_label_kwargs,
        )

        # coordinates for unity line
        coordinate_absolute = [-10, 0]
        coordinate_relative = [-100, 0]
        for n_row, coordinate in enumerate([coordinate_absolute, coordinate_relative]):
            axs_summary[n_row, 0].plot(coordinate, coordinate, color="black", alpha=0.9)

        # plot adjustments
        axs_summary[0, 2].get_yaxis().set_ticks([4, 3, 2, 1, 0, -1, -2, -3, -4])
        axs_summary[0, 2].set_ylim(-4, 4)
        axs_summary[1, 2].get_yaxis().set_ticks([40, 30, 20, 10, 0, -10, -20, -30, -40])
        axs_summary[1, 2].set_ylim(-40, 40)

        for k in range(2):
            for n_col in [1, 2]:
                axs_summary[k, n_col].set_xlim(-1, 30)
                axs_summary[k, n_col].set_xlabel(
                    "Time [weeks]", **self.axis_label_kwargs
                )

        for k in range(2):
            axs_summary[k, 2].hlines(y=0, xmin=-5, xmax=201, color="black", alpha=1.0)

        for n_col in range(2):
            axs_summary[0, n_col].set_ylim(-7, -0.5)
            axs_summary[1, n_col].set_ylim(-70, -5)
            axs_summary[0, n_col].get_yaxis().set_ticks([0, -1, -2, -3, -4, -5, -6, -7])
            axs_summary[1, n_col].get_yaxis().set_ticks(
                [0, -10, -20, -30, -40, -50, -60, -70]
            )

        axs_summary[0, 0].set_xlim(-7, -0.5)
        axs_summary[1, 0].set_xlim(-70, -3)
        axs_summary[0, 0].get_xaxis().set_ticks([0, -1, -2, -3, -4, -5, -6, -7])
        axs_summary[1, 0].get_xaxis().set_ticks([0, -10, -20, -30, -40, -50, -60, -70])
        axs_summary[0, 0].get_yaxis().set_ticks([0, -1, -2, -3, -4, -5, -6, -7])
        axs_summary[1, 0].get_yaxis().set_ticks([0, -10, -20, -30, -40, -50, -60, -70])

        axs_summary[0, 0].invert_xaxis()
        axs_summary[1, 0].invert_xaxis()
        axs_summary[0, 0].invert_yaxis()
        axs_summary[1, 0].invert_yaxis()

        axs_summary[0, 1].legend(
            handles=self._dose_handles(),
            ncol=1,
            loc="upper left",
            bbox_to_anchor=(2.23, 0.2),
            prop={"size": 19},
        )
        axs_summary[0, 2].legend(
            handles=self._dosing_handles(),
            ncol=1,
            loc="upper left",
            bbox_to_anchor=(1.02, 0.6),
            prop={"size": 19},
        )
        axs_summary[1, 2].legend(
            handles=self._marker_size_handles(),
            ncol=1,
            loc="upper left",
            bbox_to_anchor=(1.09, 0.7),
            prop={"size": 19},
        )

        fig_summary.show()
        fig_summary.savefig(MODEL.results_dir / "Data_comparison.svg", format="svg")
        figures["plot_summary"] = fig_summary
        return figures


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    DataComparison().mean_LDLC()
    DataComparison().create_figure_summary()
    DataComparison().create_figure_single_FH()
