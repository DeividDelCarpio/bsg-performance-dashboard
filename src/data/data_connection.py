# data_connection.py
# Conexión a SQL Server usando parámetros de config.yaml

import yaml
from sqlalchemy import create_engine


def get_engine(config_path='config/config.yaml', servidor=None):
    """
    Lee parámetros de conexión desde config.yaml y retorna un engine SQLAlchemy.
    Si se pasa 'servidor', lo usa en vez del principal del config.
    """
    with open(config_path, 'r') as f:
        params = yaml.safe_load(f)
    if servidor is None:
        server = params.get('servidor', '')
    else:
        server = servidor
    database = params.get('base_datos', '')
    username = params.get('usuario', '')
    password = params.get('password', '')
    conn_str = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    engine = create_engine(conn_str)
    return engine
