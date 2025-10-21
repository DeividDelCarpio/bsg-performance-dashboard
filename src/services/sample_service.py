# sample_service.py
# Servicio para obtener muestra aleatoria de datos

import pandas as pd
from src.data.data_connection import get_engine

def get_sample(n=20):
    engine = get_engine()
    try:
        df_sample = pd.read_sql_query(f"SELECT TOP {n} * FROM [aud].[T_AuditoriaUsoCPU] ORDER BY NEWID()", engine)
        return df_sample
    except Exception as e:
        return pd.DataFrame()
