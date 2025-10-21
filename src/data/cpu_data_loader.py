# cpu_data_loader.py
# Función para consultar y cargar datos de uso de CPU

import pandas as pd
import streamlit as st
from src.data.data_connection import get_engine

def load_cpu_data(fecha_inicio, fecha_fin, instancia=None, hora_inicio=None, hora_fin=None, filtrar_hora=False, incluir_secundario=True):
    """
    Ejecuta una consulta sobre [aud].[T_AuditoriaUsoCPU] filtrando por fechas y opcionalmente por instancia.
    """
    # Cargar servidores desde st.secrets
    servidores = [(st.secrets["SERVIDOR"], 'Principal')]
    if incluir_secundario and "SERVIDOR_SECUNDARIO" in st.secrets:
        servidores.append((st.secrets["SERVIDOR_SECUNDARIO"], 'Secundario'))

    dfs = []
    for servidor, nombre_servidor in servidores:
        engine = get_engine(servidor=servidor)
        query = """
            SELECT *, ? as Servidor FROM [aud].[T_AuditoriaUsoCPU]
            WHERE FechaEvento >= ? AND FechaEvento <= ?
        """
        params = [nombre_servidor, fecha_inicio, fecha_fin]
        if instancia:
            query += " AND Instancia = ?"
            params.append(instancia)
        df = pd.read_sql_query(query, engine, params=tuple(params))
        if filtrar_hora and hora_inicio and hora_fin and not df.empty:
            df['FechaEvento'] = pd.to_datetime(df['FechaEvento'])
            df = df[df['FechaEvento'].dt.time.between(hora_inicio, hora_fin)]
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def load_cpu_data_by_hour(fecha_inicio, fecha_fin, hora_inicio, hora_fin, instancia=None, incluir_secundario=True):
    """
    Consulta datos filtrando por fecha y por rango de horas (en SQL).
    """
    servidores = [(st.secrets["SERVIDOR"], 'Principal')]
    if incluir_secundario and "SERVIDOR_SECUNDARIO" in st.secrets:
        servidores.append((st.secrets["SERVIDOR_SECUNDARIO"], 'Secundario'))

    dfs = []
    for servidor, nombre_servidor in servidores:
        engine = get_engine(servidor=servidor)
        query = """
            SELECT *, ? as Servidor FROM [aud].[T_AuditoriaUsoCPU]
            WHERE FechaEvento >= ? AND FechaEvento <= ?
              AND CAST(CONVERT(varchar(8), FechaEvento, 108) AS time) >= ?
              AND CAST(CONVERT(varchar(8), FechaEvento, 108) AS time) <= ?
        """
        params = [nombre_servidor, fecha_inicio, fecha_fin, 
                  str(hora_inicio) if isinstance(hora_inicio, str) else hora_inicio.strftime("%H:%M:%S"),
                  str(hora_fin) if isinstance(hora_fin, str) else hora_fin.strftime("%H:%M:%S")]
        if instancia:
            query += " AND Instancia = ?"
            params.append(instancia)
        query += " ORDER BY FechaEvento ASC"
        df = pd.read_sql_query(query, engine, params=tuple(params))
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()
    

def get_fecha_inicio_fin_instancia(instancia):
    """
    Retorna la fecha de inicio y fin (primer y último FechaEvento) para una instancia dada.
    """
    servidores = [st.secrets["SERVIDOR"]]
    if "SERVIDOR_SECUNDARIO" in st.secrets:
        servidores.append(st.secrets["SERVIDOR_SECUNDARIO"])

    fechas_inicio = []
    fechas_fin = []
    for servidor in servidores:
        engine = get_engine(servidor=servidor)
        query_inicio = """
            SELECT TOP 1 FechaEvento FROM aud.T_AuditoriaUsoCPU
            WHERE Instancia = ?
            ORDER BY FechaEvento ASC
        """
        query_fin = """
            SELECT TOP 1 FechaEvento FROM aud.T_AuditoriaUsoCPU
            WHERE Instancia = ?
            ORDER BY FechaEvento DESC
        """
        fecha_inicio = pd.read_sql_query(query_inicio, engine, params=(instancia,))
        fecha_fin = pd.read_sql_query(query_fin, engine, params=(instancia,))
        if not fecha_inicio.empty:
            fechas_inicio.append(pd.to_datetime(fecha_inicio['FechaEvento'].iloc[0]))
        if not fecha_fin.empty:
            fechas_fin.append(pd.to_datetime(fecha_fin['FechaEvento'].iloc[0]))
    fecha_inicio_val = min(fechas_inicio) if fechas_inicio else None
    fecha_fin_val = max(fechas_fin) if fechas_fin else None
    return fecha_inicio_val, fecha_fin_val