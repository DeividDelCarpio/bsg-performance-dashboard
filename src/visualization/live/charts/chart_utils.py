import pandas as pd

def filter_dataframe_by_time(df, x_col='FechaEvento', hora_inicio=0, hora_fin=23):
    """
    Filtra el DataFrame por el rango de horas especificado.
    """
    df = df.copy()
    df['hora'] = pd.to_datetime(df[x_col]).dt.hour
    df = df[(df['hora'] >= hora_inicio) & (df['hora'] <= hora_fin)]
    return df

def format_dataframe_for_plotting(df, x_col='FechaEvento'):
    """
    Formatea el DataFrame original para facilitar la graficación.
    """
    df = df.copy()
    df['x_categoria'] = pd.to_datetime(df[x_col]).dt.strftime('%H:%M %d/%m')
    return df

def build_chart_title(instancia, metricas, granularidad, rango):
    """
    Formatea el título del gráfico basado en los parámetros dados.
    """
    metricas_str = " / ".join(metricas)
    return f"{instancia} - {metricas_str} ({granularidad}, {rango})"