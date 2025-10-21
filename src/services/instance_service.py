# instance_service.py
# Servicio para obtener instancias únicas de la base de datos

import pandas as pd
import yaml
from src.data.data_connection import get_engine
import streamlit as st

def get_instancias():
    # Cargar servidores desde st.secrets
    servidores = [st.secrets["SERVIDOR"]]
    if "SERVIDOR_SECUNDARIO" in st.secrets:
        servidores.append(st.secrets["SERVIDOR_SECUNDARIO"])

    instancias = set()
    for servidor in servidores:
        engine = get_engine(servidor=servidor)
        try:
            df_inst = pd.read_sql_query(
                "SELECT DISTINCT Instancia FROM [aud].[T_AuditoriaUsoCPU] WHERE Instancia IS NOT NULL",
                engine
            )
            instancias.update(df_inst['Instancia'].dropna().unique().tolist())
        except Exception as e:
            st.warning(f"Error consultando instancias en {servidor}: {e}")
    result = sorted(instancias)
    if not result:
        result = ["Todas"]
    return result