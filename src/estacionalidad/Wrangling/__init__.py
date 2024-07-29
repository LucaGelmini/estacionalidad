import pandas as pd
from typing import Literal
from .read_series_indices_indec import read_series_indices_indec


class DataFrameAdapter:
    __raw_df: pd.DataFrame
    series: list[dict[str, str | None]] = []
    periodicity: Literal["monthly", "quarterly"]
    df: pd.DataFrame

    def __init__(
        self,
        df: pd.DataFrame,
        periodicity: Literal["monthly", "quarterly"],
        year_col: str,
        period_col: str,
    ) -> None:
        self.__raw_df = df
        self.periodicity = periodicity
        self.__raw_df = self.__raw_df.rename(columns={year_col: "y", period_col: "p"})
        self.series = []

        self.__raw_df = self.__raw_df.set_index(["y", "p"])
        self.df = pd.DataFrame(index=self.__raw_df.index)

    def Map(self, col_name: str, full_name: str, description: str | None = None):
        new_mapped: dict[str, str | None] = dict(
            col_name=col_name, full_name=full_name, description=description
        )
        self.series.append(new_mapped)
        self.df[col_name] = self.__raw_df[col_name]
        return self
