# Utilidades para agrupamiento de datos en gráficos

import pandas as pd

def group_by_granularity(df, x_col, granularidad):
    # Mapeo robusto de nombres de granularidad
    granularidad_map = {
        "1 minuto": "1 minuto",
        "Minuto": "1 minuto",
        "5 minutos": "5 minutos",
        "10 minutos": "10 minutos",
        "15 minutos": "15 minutos",
        "30 minutos": "30 minutos",
        "1 hora": "1 hora",
        "Hora": "1 hora",
        "Día": "Día",
        "Dia": "Día",
        "Semana": "Semana"
    }
    granularidad = granularidad_map.get(granularidad, granularidad)

    df = df.copy()
    # Validación: si x_col no existe, retorna el DataFrame sin modificar
    if x_col not in df.columns:
        return df

    dt = pd.to_datetime(df[x_col])
    if granularidad == "1 minuto":
        df['x_categoria'] = dt.dt.strftime('%Y-%m-%d %H:%M')
    elif granularidad == "5 minutos":
        df['x_categoria'] = dt.dt.floor('5Min').dt.strftime('%Y-%m-%d %H:%M')
    elif granularidad == "10 minutos":
        df['x_categoria'] = dt.dt.floor('10Min').dt.strftime('%Y-%m-%d %H:%M')
    elif granularidad == "15 minutos":
        df['x_categoria'] = dt.dt.floor('15Min').dt.strftime('%Y-%m-%d %H:%M')
    elif granularidad == "30 minutos":
        df['x_categoria'] = dt.dt.floor('30Min').dt.strftime('%Y-%m-%d %H:%M')
    elif granularidad == "1 hora":
        df['x_categoria'] = dt.dt.strftime('%Y-%m-%d %H:00')
    elif granularidad == "Día":
        df['x_categoria'] = dt.dt.strftime('%Y-%m-%d')
    elif granularidad == "Semana":
        df['x_categoria'] = dt.dt.to_period('W').apply(lambda r: r.start_time.strftime('%Y-%m-%d'))
    else:
        df['x_categoria'] = df[x_col].astype(str)

    return df
