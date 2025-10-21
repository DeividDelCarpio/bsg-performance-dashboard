"""
Este archivo contiene controles reutilizables para la visualización en Streamlit.
"""

import streamlit as st
from datetime import datetime, timedelta

def render_time_controls(instancias):
    col1, col2, col3, col4, col5, col6 = st.columns([4,1,2,1.5,1,1])
    # Col1: Rango de tiempo
    with col1:
        rango = st.selectbox("Rango de tiempo", ["Últimas 24 horas", "Última semana", "Último mes", "Personalizado"])
        hoy = datetime.now().date()
        fecha_inicio, fecha_fin, hora_inicio, hora_fin = None, None, None, None
        if rango == "Personalizado":
            fcol1, fcol2, fcol3, fcol4 = st.columns([1,1,1,1])      
            with fcol1:
                fecha_inicio = st.date_input("Fecha inicio", value=hoy - timedelta(days=6), key="fecha_inicio_main")
            with fcol3:
                hora_inicio = st.time_input("Hora inicio", value=datetime.strptime("00:00", "%H:%M").time(), key="hora_inicio_main")
            with fcol2:
                fecha_fin = st.date_input("Fecha fin", value=hoy, key="fecha_fin_main")
            with fcol4:
                hora_fin = st.time_input("Hora fin", value=datetime.strptime("23:59", "%H:%M").time(), key="hora_fin_main")

    # Col2: Granularidad (slider)
    with col2:
        granularidades = ["Minuto", "10 Minutos", "Hora", "Día", "Semana"]
        granularidad = st.select_slider(
            "Granularidad",
            options=granularidades,
            value="10 Minutos",
            key="granularidad_main"
        )
    # Col3: Instancia
    with col3:
        opciones_inst = ["Todas"] + instancias
        if "SERVER-BD-3\\SERVERBD3" in opciones_inst:
            default_inst_idx = opciones_inst.index("SERVER-BD-3\\SERVERBD3")
        else:
            default_inst_idx = 0  # Siempre seguro, apunta a "Todas"
        instancia = st.selectbox("Instancia", options=opciones_inst, index=default_inst_idx, key="instancia_main")
    # Col4: Métricas
    with col4:
        disable_otros = instancia == "Todas"
        c1, c2, c3 = st.columns([0.4, 0.5, 0.6])
        if disable_otros:
            with c1:
                uso = st.checkbox("U", value=True, key="uso", label_visibility="visible", disabled=False)
            with c2:
                sin_uso = False
                st.checkbox("SU", value=False, key="sin_uso", label_visibility="visible", disabled=True)
            with c3:
                uso_otro = False
                st.checkbox("UOP", value=False, key="uso_otro", label_visibility="visible", disabled=True)
        else:
            with c1:
                uso = st.checkbox("U", value=True, key="uso", label_visibility="visible", disabled=False)
            with c2:
                sin_uso = st.checkbox("SU", value=True, key="sin_uso", label_visibility="visible", disabled=False)
            with c3:
                uso_otro = st.checkbox("UOP", value=True, key="uso_otro", label_visibility="visible", disabled=False)
    # Col5: Top N (number_input)
    with col5:
        top_n = st.number_input("Indicadores", min_value=0, max_value=10, value=3, key="top_n_indicadores")
    # Col6: Dividir
    with col6:
        dividir = st.checkbox("Separar gráficos", value=True, key="dividir_graficos", label_visibility="visible")


    return rango, granularidad, instancia, uso, sin_uso, uso_otro, fecha_inicio, fecha_fin, hora_inicio, hora_fin, top_n, dividir
