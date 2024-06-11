import pandas as pd
from typing import Iterable, Literal
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.lines as mlines
from dataclasses import dataclass
from ..Plot.config import *
from ..Wrangling import DataFrameAdapter
from .table import Table
from .abstract_clases import AbstractSeasonalityChart


@dataclass
class LegendOptions:
    show = True
    loc: Literal[
        'best', 'upper right', 'upper left',
        'lower left', 'lower right', 'right',
        'center left', 'center right', 'lower center',
        'upper center', 'center'
    ] = 'best'


@dataclass
class AxesConfig:
    xmargin = 0
    xticks = []
    xtickslables = []
    ylabel = "Índice 2004 = 100"
    linewidth = 2
    legend = LegendOptions()

    def apply(self, ax: Axes):
        ax.margins(x=self.xmargin)
        ax.set_xticks(self.xticks)
        ax.set_xticklabels(self.xtickslables)
        ax.set_ylabel(self.ylabel, fontsize=20)

    def apply_all(self, axes: Iterable[Axes]):
        for ax in axes:
            self.apply(ax)


class SeasonalityChart(AbstractSeasonalityChart):
    begin = None
    end = None
    axconfig = AxesConfig()

    def __init__(self, data: DataFrameAdapter) -> None:
        self.data = None
        self.data = data
        self.begin = self.data.df.index[0][0]
        self.end = self.data.df.index[-1][0]

        self.fig, self.ax = plt.subplots()
        self.axconfig.apply(self.ax)
        self.proxy_lines = []
        self.table = Table(self)

        for idx, a_series in enumerate(self.data.series):
            a_series["trace_color"] = "red"
            a_series["mean_color"] = "blue"
            self.data.series[idx] = a_series

    def __set_plot_data(self, col_name: str):
        df = self.df[col_name]
        df.name = 'value'
        df = (
            df.reset_index()
            .sort_values(['p', 'y'])
            .reset_index()
            .drop('index', axis=1))
        dfs = df.groupby('p')

        max_points = int(self.end)-int(self.begin)

        def fix_df_size(df: pd.DataFrame, subdf_number: int):
            """All the subseries of the same size filled with NA if there's any data"""
            df = df.reset_index(drop=True)

            new_index = pd.RangeIndex(
                start=0, stop=max_points+1)
            df = df.reindex(new_index)
            new_index = pd.RangeIndex(
                start=(subdf_number-1)*(max_points+1), stop=(subdf_number)*(max_points+1))
            df.index = new_index
            return df

        dfs = [
            fix_df_size(df, idx)
            for idx, df in dfs]

        return dfs

    def __render_line(self, a_series: dict, ax: Axes):
        for df in self.__set_plot_data(a_series['col_name']):
            ax.plot(df.index, df.value,
                    color=a_series['trace_color'], linewidth=self.axconfig.linewidth, label=a_series["full_name"])
            mean_value = df.groupby('p')['value'].transform('mean')
            ax.plot(df.index, mean_value,
                    color=a_series['mean_color'], linewidth=self.axconfig.linewidth)
            ax.axvline(x=df.index[0], color='black',
                       linestyle='--', linewidth=self.axconfig.linewidth)
            ax.tick_params(axis='y', which='major',
                           labelsize=15)
        self.proxy_lines.append(mlines.Line2D(
            [], [], color=a_series["trace_color"], label=a_series["full_name"]))

        legend_options = self.axconfig.legend
        if legend_options.show:
            ax.legend(handles=self.proxy_lines, loc=legend_options.loc)

    def render(self):
        for a_series in self.data.series:
            ax = self.ax
            self.__render_line(a_series, ax)

        return self.fig

    def set_year(self, begin: str | None = None, end: str | None = None):
        self.begin = self.data.df.index.y[0] if begin is None else begin
        self.end = self.data.df.index.y[-1] if end is None else end
        return self

    def map_color(self, trace_id: str, trace_color: str = 'red', mean_color: str = 'blue'):
        def __set_color_to_series(series: dict):
            if series["col_name"] != trace_id:
                return series
            series["trace_color"] = trace_color
            series["mean_color"] = mean_color
            return series

        self.data.series = map(__set_color_to_series, self.data.series)
        return self

    def show(self) -> None:
        plt.show()

    @property
    def df(self):
        df = self.data.df.query('y>=@self.begin & y<=@self.end')
        return df

    def set_axconfig(self, config: AxesConfig):
        self.axconfig = config
        return self
