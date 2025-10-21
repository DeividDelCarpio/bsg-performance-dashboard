# data_connection.py
# Conexión a SQL Server usando parámetros de st.secrets

import streamlit as st
from sqlalchemy import create_engine


def get_engine(servidor=None):
    """
    Lee parámetros de conexión desde st.secrets y retorna un engine SQLAlchemy.
    Si se pasa 'servidor', lo usa en vez del principal de los secrets.
    """
    if servidor is None:
        server = st.secrets["SERVIDOR"]
    else:
        server = servidor
    database = st.secrets["BASE_DATOS"]
    username = st.secrets["USUARIO"]
    password = st.secrets["PASSWORD"]
    conn_str = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    engine = create_engine(conn_str)
    return engine
