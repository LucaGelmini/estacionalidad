import pandas as pd

month_translation = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}


def read_series_indices_indec() -> pd.DataFrame:
    PATH = 'https://www.indec.gob.ar/ftp/cuadros/economia/serie_mensual_indices_comex.xls'
    df = (
        pd.read_excel(PATH, skiprows=4, skipfooter=6)
        .ffill()
        .dropna(axis=1)
    )
    df.columns = ['Y', 'M', 'v_x', 'p_x', 'q_x', 'v_m', 'p_m', 'q_m']
    df.Y = df.Y.str.replace('*', '')
    df.M = df.M.str.lower().apply(lambda m: month_translation[m])
    df['ITI'] = 100*df.p_x/df.q_x

    return df
