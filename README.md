# Estacionalidad!

## Getting started
´´´bash
pip install estacionalidad
´´´

## Example using INDEC (Argentina) foreign trade price and quantities index

´´´python

from estacionalidad.Wrangling import DataFrameAdapter, read_series_indices_indec
from estacionalidad.Plot import SeasonalityChart, AxesConfig
from matplotlib import pyplot as plt

df = read_series_indices_indec()

axes_config = AxesConfig()
axes_config.ylabel = "Índice 2004 = 100"
axes_config.nticks = 20


x = (
    SeasonalityChart(
        DataFrameAdapter(df, 'quarterly', 'Y', 'M')
        .Map("p_x", "Índice de precios de las exportaciones")
        .Map("q_x", "Índice de cantidades de las exportaciones"))
    .set_year("2014", "2024")
    .map_color("p_x", "#FFE294", "#8B0000")
    .map_color("q_x", "#ECB210", "#8B0000")
    .set_axconfig(axes_config))


m = (
    SeasonalityChart(
        DataFrameAdapter(df, 'quarterly', 'Y', 'M')
        .Map("p_m", "Índice de precios de las importaciones")
        .Map("q_m", "Índice de cantidades de las importaciones"))
    .set_year("2014", "2024")
    .map_color("p_m", "#CBADE0", "#8B0000")
    .map_color("q_m", "#A285A5", "#8B0000")
    .set_axconfig(axes_config))


iti = (
    SeasonalityChart(
        DataFrameAdapter(df, 'quarterly', 'Y', 'M')
        .Map("ITI", "Índice de términos del intercambio")
    )
    .set_year("2014", "2024")
    .map_color("ITI", "#CBADE0", "#8B0000")
    .set_axconfig(axes_config))

axes_config.linewidth = 2
axes_config.legend.loc = "lower center"

for plot in (x, m, iti):
    plot.render()

print(x.table.table_df)

plt.show()

´´´