from abc import ABC, abstractmethod
import pandas as pd
from matplotlib.figure import Figure
from ..Wrangling import DataFrameAdapter


class AbstractSeasonalityChart(ABC):
    @abstractmethod
    def __init__(self, data: DataFrameAdapter) -> None:
        pass

    @abstractmethod
    def set_year(self):
        pass

    @abstractmethod
    def map_color(
        self, trace_id: str, trace_color: str = "red", mean_color: str = "blue"
    ):
        pass

    @abstractmethod
    def set_axconfig(self, config):
        pass

    @abstractmethod
    def render(self) -> Figure:
        pass

    @property
    @abstractmethod
    def df(self) -> pd.DataFrame:
        pass
