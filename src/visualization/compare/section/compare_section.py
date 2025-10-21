import streamlit as st
import pandas as pd
from datetime import datetime
from src.data.cpu_data_loader import load_cpu_data, get_fecha_inicio_fin_instancia
from src.visualization.compare.controls.compare_controls import render_compare_controls
from src.visualization.compare.charts.compare_charts import plot_cpu_usage_compare
from src.visualization.compare.charts.chart_utils import build_chart_title, filter_dataframe_by_time, format_dataframe_for_plotting

def render_compare_section():
    st.subheader("Comparativo Antes vs Después y Muestreo Aleatorio")

    instancias = [
        "SERVER-BD-1\\SERVERBD1",
        "ServerDB4",
        "SERVER-BD-2\\SERVERBD2",
        "SERVER-BD-3\\SERVERBD3"
    ]
    instancias_anteriores = instancias
    instancias_actuales = instancias

    fecha_inicio_ant, _ = get_fecha_inicio_fin_instancia(instancias_anteriores[0])
    fecha_inicio_act, _ = get_fecha_inicio_fin_instancia(instancias_actuales[0])

    with st.container():
        with st.form("compare_form"):
            controles = render_compare_controls(
                instancias_anteriores, instancias_actuales, fecha_inicio_ant, fecha_inicio_act
            )
            cols = st.columns([1, 1])
            with cols[1]:
                filtrar = st.form_submit_button("Filtrar")

        if filtrar:
            metricas = []
            if controles["uso"]:
                metricas.append("Uso")
            if controles["sin_uso"]:
                metricas.append("SinUso")
            if controles["uso_otro"]:
                metricas.append("UsoOtroProceso")

            if controles["fecha_inicio_ant"] > controles["fecha_fin_ant"]:
                st.warning("La fecha de inicio anterior no puede ser mayor que la fecha fin.")
                return
            if controles["fecha_inicio_act"] > controles["fecha_fin_act"]:
                st.warning("La fecha de inicio actual no puede ser mayor que la fecha fin.")
                return

            df_ant = load_cpu_data(controles["fecha_inicio_ant"], controles["fecha_fin_ant"], controles["instancia_ant"])
            df_act = load_cpu_data(controles["fecha_inicio_act"], controles["fecha_fin_act"], controles["instancia_act"])

            def filtrar_horario(df):
                df = df.copy()
                df['FechaEvento'] = pd.to_datetime(df['FechaEvento'])
                df['hora'] = df['FechaEvento'].dt.hour
                return df[(df['hora'] >= 8) & (df['hora'] < 22)]

            if controles.get("horario_laboral", False):
                if not df_ant.empty:
                    df_ant = filtrar_horario(df_ant)
                if not df_act.empty:
                    df_act = filtrar_horario(df_act)

            granularidad_map = {
                "1 minuto": "1min",
                "5 minutos": "5min",
                "10 minutos": "10min",
                "15 minutos": "15min",
                "30 minutos": "30min",
                "1 hora": "1h",
                "Día": "D",
                "Semana": "W"
            }
            granularidad = granularidad_map.get(controles["granularidad"], "10min")

            col_grafs = st.columns(2)
            with col_grafs[0]:
                if not df_ant.empty:
                    df_grouped = df_ant.copy()
                    df_grouped['Granularidad'] = pd.to_datetime(df_grouped['FechaEvento']).dt.floor(granularidad)
                    x_col = 'Granularidad'

                    group_cols = [x_col]
                    if 'Instancia' in df_grouped.columns:
                        group_cols.append('Instancia')
                    if 'Servidor' in df_grouped.columns:
                        group_cols.append('Servidor')

                    df_grouped = df_grouped.groupby(group_cols)[metricas].mean().reset_index()
                    df_grouped['x_categoria'] = pd.to_datetime(df_grouped[x_col]).dt.strftime('%H:%M %d/%m')

                    fig_ant = plot_cpu_usage_compare(
                        df_grouped,
                        metricas=metricas,
                        x_col='Granularidad',
                        granularidad=granularidad,
                        top_n=controles["cantidad_indicadores"]
                    )
                    fig_ant.update_layout(
                        title={
                            'text': build_chart_title(controles['instancia_ant'], metricas, granularidad, "Anterior"),
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 0.92,
                            'yanchor': 'top',
                            'font': dict(size=18)
                        }
                    )
                    st.plotly_chart(fig_ant, use_container_width=True)
                else:
                    st.info(f"No hay datos para {controles['instancia_ant']} en el rango seleccionado.")
            with col_grafs[1]:
                if not df_act.empty:
                    df_grouped = df_act.copy()
                    df_grouped['Granularidad'] = pd.to_datetime(df_grouped['FechaEvento']).dt.floor(granularidad)
                    x_col = 'Granularidad'

                    group_cols = [x_col]
                    if 'Instancia' in df_grouped.columns:
                        group_cols.append('Instancia')
                    if 'Servidor' in df_grouped.columns:
                        group_cols.append('Servidor')

                    df_grouped = df_grouped.groupby(group_cols)[metricas].mean().reset_index()
                    df_grouped['x_categoria'] = pd.to_datetime(df_grouped[x_col]).dt.strftime('%H:%M %d/%m')

                    fig_act = plot_cpu_usage_compare(
                        df_grouped,
                        metricas=metricas,
                        x_col='Granularidad',
                        granularidad=granularidad,
                        top_n=controles["cantidad_indicadores"]
                    )
                    fig_act.update_layout(
                        title={
                            'text': build_chart_title(controles['instancia_ant'], metricas, granularidad, "Anterior"),
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 0.92,
                            'yanchor': 'top',
                            'font': dict(size=18)
                        }
                    )
                    st.plotly_chart(fig_act, use_container_width=True)
                else:
                    st.info(f"No hay datos para {controles['instancia_act']} en el rango seleccionado.")
