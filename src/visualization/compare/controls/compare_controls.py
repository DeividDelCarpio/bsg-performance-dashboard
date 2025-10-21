import streamlit as st
from datetime import datetime, timedelta


def render_compare_controls(instancias_anteriores, instancias_actuales, fecha_inicio_ant, fecha_inicio_act):

    col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,2,1,1])

    # Columna 1: Muestreo y horario laboral
    with col1:
        muestreo = st.selectbox("Muestreo", ["Diario", "Semanal", "Mensual"], index=1, key="muestreo_comp")
        horario_laboral = st.checkbox("Horario laboral (8:00-22:00)", value=False, key="horario_laboral_comp")

    # Columna 2: Instancias (anterior y actual) apiladas verticalmente
    with col2:
        instancia_ant = st.selectbox("Anterior", instancias_anteriores, key="instancia_ant_comp")
        instancia_act = st.selectbox("Actual", instancias_actuales, key="instancia_act_comp")

    # Columna 3: Fechas de inicio (dependientes de muestreo) apiladas verticalmente
    with col3:
        fecha_inicio_ant_sel = st.date_input("Inicio anterior", value=fecha_inicio_ant, key="fecha_inicio_ant_comp")
        fecha_inicio_act_sel = st.date_input("Inicio actual", value=fecha_inicio_act, key="fecha_inicio_act_comp")
        if muestreo == "Diario":
            delta = timedelta(days=1)
        elif muestreo == "Semanal":
            delta = timedelta(weeks=1)
        else:
            delta = timedelta(days=30)
        fecha_fin_ant = fecha_inicio_ant_sel + delta
        fecha_fin_act = fecha_inicio_act_sel + delta

    # Columna 4: Granularidad (innovador)
    with col4:
        granularidades = ["1 minuto", "5 minutos", "10 minutos", "15 minutos", "30 minutos", "1 hora", "Día", "Semana"]
        granularidad = st.select_slider("Granularidad", options=granularidades, value="5 minutos", key="granularidad_comp")

    # Columna 5: Métricas (checkboxes verticales)
    with col5:
        uso = st.checkbox("Uso", value=True, key="uso_comp")
        sin_uso = st.checkbox("Sin uso", value=False, key="sin_uso_comp")
        uso_otro = st.checkbox("Otro uso", value=False, key="uso_otro_comp")

    # Columna 6: Indicadores (cantidad)
    with col6:
        cantidad_indicadores = st.number_input("Indicadores", min_value=0, max_value=10, value=3, key="indicadores_comp")

    return {
        "muestreo": muestreo,
        "horario_laboral": horario_laboral,
        "instancia_ant": instancia_ant,
        "instancia_act": instancia_act,
        "fecha_inicio_ant": fecha_inicio_ant_sel,
        "fecha_fin_ant": fecha_fin_ant,
        "fecha_inicio_act": fecha_inicio_act_sel,
        "fecha_fin_act": fecha_fin_act,
        "granularidad": granularidad,
        "uso": uso,
        "sin_uso": sin_uso,
        "uso_otro": uso_otro,
        "cantidad_indicadores": cantidad_indicadores
    }
