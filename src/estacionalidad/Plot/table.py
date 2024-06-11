import pandas as pd
from .abstract_clases import AbstractSeasonalityChart
from typing import Literal


def calc_means(df: pd.DataFrame):
    mean_df = df.reset_index().groupby("p").mean(numeric_only=True)
    mean_df.columns = [f"mean_{col}" for col in mean_df.columns]
    return mean_df


def calc_max_min(df: pd.DataFrame):
    var_cols = df.columns
    max_dfs = []
    for col in var_cols:
        name = f"max_{col}"
        max_dfs.append(
            df[col]
            .reset_index()
            .groupby("p").max()
            .rename(columns={col: name, "y": f"y_{name}"})
        )

    max_df = pd.concat(max_dfs, axis=1)

    min_dfs = []
    for col in var_cols:
        name = f"min_{col}"
        min_dfs.append(
            df[col]
            .reset_index()
            .groupby("p").min()
            .rename(columns={col: name, "y": f"y_{name}"})
        )

    min_df = pd.concat(min_dfs, axis=1)
    return pd.concat([max_df, min_df], axis=1)


def calc_last_values(df: pd.DataFrame):
    last_value_df = df.tail(12).reset_index().set_index("p").sort_index()
    last_value_df.columns = [f"last_{col}" for col in last_value_df.columns]
    return last_value_df


class Table:
    def __init__(self, chart: AbstractSeasonalityChart, calcs: None | list[Literal["maxmin", "last", "mean"]] = None):
        """
        Args:
            chart (SeasonalityChart): The chart object.
            calcs (None | list[Literal[&quot;all&quot;, &quot;maxmin&quot;, &quot;last&quot;, &quot;mean&quot;]]): Selection of calculated columns:
                all: all the calculations aviable
                maxmin: the max and min values for a month
                mean: the mean value for each month
        """
        df = chart.df

        calcs_dfs = []
        for calc in ["maxmin", "last", "mean"]:
            if (calcs == None) or (calc in calcs):
                if calc == "mean":
                    calcs_dfs.append(calc_means(df))
                if calc == "maxmin":
                    calcs_dfs.append(calc_max_min(df))
                if calc == "last":
                    calcs_dfs.append(calc_last_values(df))

        calculated_df = pd.concat(calcs_dfs, axis=1)

        self.__calculated_df = calculated_df

    @property
    def table_df(self):
        return self.__calculated_df
