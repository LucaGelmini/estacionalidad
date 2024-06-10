from src.Wrangling import DataFrameAdapter, read_series_indices_indec
from src.Plot import SeassonalityChart
from matplotlib import pyplot as plt

df = read_series_indices_indec()


x = (
    SeassonalityChart(
        DataFrameAdapter(df, 'quarterly', 'Y', 'M')
        .Map("p_x", "Índice de precios de las exportaciones")
        .Map("q_x", "Índice de cantidades de las exportaciones"))
    .set_year("2014", "2024")
    .map_color("p_x", "#FFE294", "#8B0000")
    .map_color("q_x", "#ECB210", "#8B0000")
    .render())


m = (
    SeassonalityChart(
        DataFrameAdapter(df, 'quarterly', 'Y', 'M')
        .Map("p_m", "Índice de precios de las importaciones")
        .Map("q_m", "Índice de cantidades de las importaciones"))
    .set_year("2014", "2024")
    .map_color("p_m", "#CBADE0", "#8B0000")
    .map_color("q_m", "#A285A5", "#8B0000")
    .render())


c = (
    SeassonalityChart(
        DataFrameAdapter(df, 'quarterly', 'Y', 'M')
        .Map("ITI", "Índice de términos del intercambio")
    )
    .set_year("2014", "2024")
    .map_color("ITI", "#CBADE0", "#8B0000")
    .render())

plt.show()


# import pandas as pd

# df = pd.read_excel("trimestral2024.xlsx")
# df.columns = ["date", *df.columns[1:]]
# df["date"] = pd.to_datetime(df.date)
# df["year"] = df.date.dt.year
# df['quarter'] = df['date'].dt.quarter
# df[['year', 'quarter']] = df[['year', 'quarter']].astype(str)
# # df = df.set_index(['year', 'quarter'])


# adapted = (
#     DataFrameAdapter(df, 'quarterly', 'year', 'quarter')
#     .Map("X_P", "Índice de precios de las exportaciones")
#     .Map("Q_P", "Índice de cantidades de las importaciones")
# )

# c = (
#     SeassonalityChart(adapted)
#     .set_year("2014", "2024")
#     .map_color("X_P", "#FFE294", "#8B0000")
#     .map_color("Q_P", "#ECB210", "#8B0000")
#     .render())
# c.show()
