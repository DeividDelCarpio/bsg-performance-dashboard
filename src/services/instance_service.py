# instance_service.py
# Servicio para obtener instancias únicas de la base de datos

import pandas as pd
import yaml
from src.data.data_connection import get_engine

def get_instancias():
    # Cargar servidores desde config.yaml
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    servidores = [config.get('servidor', '')]
    if config.get('servidor_secundario'):
        servidores.append(config['servidor_secundario'])

    instancias = set()
    for servidor in servidores:
        engine = get_engine(servidor=servidor)
        try:
            df_inst = pd.read_sql_query(
                "SELECT DISTINCT Instancia FROM [aud].[T_AuditoriaUsoCPU] WHERE Instancia IS NOT NULL",
                engine
            )
            instancias.update(df_inst['Instancia'].dropna().unique().tolist())
        except Exception:
            pass
    return sorted(instancias)
