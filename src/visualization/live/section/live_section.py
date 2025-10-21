import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.data.cpu_data_loader import load_cpu_data, load_cpu_data_by_hour
from src.visualization.live.controls.live_controls import render_time_controls
from src.visualization.live.charts.chart_utils import (
    filter_dataframe_by_time,
    format_dataframe_for_plotting,
    build_chart_title,
)
from src.visualization.live.charts.live_charts import plot_cpu_usage_live
from src.visualization.live.charts.categorical_charts import plot_cpu_usage_categorical

def render_live_section():
    st.subheader("Visualización de Uso de CPU (En Vivo)")
    from src.services.instance_service import get_instancias
    instancias = get_instancias()
    with st.container():
        form = st.form("live_form")
        with form:
            (
                rango, granularidad, instancia, uso, sin_uso, uso_otro, fecha_inicio, fecha_fin, hora_inicio, hora_fin, top_n, dividir
            ) = render_time_controls(instancias)
            cols = st.columns([1, 1])
            with cols[1]:
                filtrar = st.form_submit_button("Filtrar")

            if filtrar:
                metricas = []
                if uso:
                    metricas.append("Uso")
                if sin_uso:
                    metricas.append("SinUso")
                if uso_otro:
                    metricas.append("UsoOtroProceso")
                import datetime as dt

                instancia_param = None if instancia == "Todas" else instancia
                df = None
                dt_now = dt.datetime.now()
                if rango == "Personalizado":
                    fecha_inicio_dt = dt.datetime.combine(fecha_inicio, hora_inicio or dt.time.min)
                    fecha_fin_dt = dt.datetime.combine(fecha_fin, hora_fin or dt.time.max)
                    df = load_cpu_data_by_hour(fecha_inicio_dt, fecha_fin_dt, hora_inicio, hora_fin, instancia_param)
                    df = filter_dataframe_by_time(df, x_col='FechaEvento', hora_inicio=hora_inicio.hour, hora_fin=hora_fin.hour)
                    df = format_dataframe_for_plotting(df, x_col='FechaEvento')
                elif rango == "Últimas 24 horas":
                    fecha_fin_dt = dt_now
                    fecha_inicio_dt = fecha_fin_dt - dt.timedelta(days=1)
                    df = load_cpu_data(fecha_inicio_dt, fecha_fin_dt, instancia_param)
                    df = format_dataframe_for_plotting(df, x_col='FechaEvento')
                elif rango == "Última semana":
                    fecha_fin_dt = dt_now
                    fecha_inicio_dt = fecha_fin_dt - dt.timedelta(days=6)
                    df = load_cpu_data(fecha_inicio_dt, fecha_fin_dt, instancia_param)
                    df = format_dataframe_for_plotting(df, x_col='FechaEvento')
                elif rango == "Último mes":
                    fecha_fin_dt = dt_now
                    fecha_inicio_dt = (fecha_fin_dt.replace(day=1) - dt.timedelta(days=1)).replace(day=1)
                    df = load_cpu_data(fecha_inicio_dt, fecha_fin_dt, instancia_param)
                    df = format_dataframe_for_plotting(df, x_col='FechaEvento')
                else:
                    st.warning("Selecciona un rango de tiempo válido.")
                    return

                if df is not None and not df.empty and metricas:
                    def groupby_cols(x_col):
                        cols = [x_col]
                        if 'Instancia' in df.columns:
                            cols.append('Instancia')
                        if 'Servidor' in df.columns:
                            cols.append('Servidor')
                        return cols

                    df_grouped = df.copy()
                    if granularidad == "Minuto":
                        x_col = 'FechaEvento'
                    elif granularidad == "10 Minutos":
                        df_grouped['DiezMin'] = pd.to_datetime(df_grouped['FechaEvento']).dt.floor('10T')
                        x_col = 'DiezMin'
                    elif granularidad == "Hora":
                        df_grouped['Hora'] = pd.to_datetime(df_grouped['FechaEvento']).dt.floor('h')
                        x_col = 'Hora'
                    elif granularidad == "Día":
                        df_grouped['Día'] = pd.to_datetime(df_grouped['FechaEvento']).dt.date
                        x_col = 'Día'
                    elif granularidad == "Semana":
                        df_grouped['Semana'] = pd.to_datetime(df_grouped['FechaEvento']).dt.to_period('W').apply(lambda r: r.start_time.date())
                        x_col = 'Semana'
                    else:
                        x_col = 'FechaEvento'

                    group_cols = groupby_cols(x_col)
                    df_grouped = df_grouped.groupby(group_cols)[metricas].mean().reset_index()

                    if dividir:
                        if instancia == "Todas" and "Instancia" in df_grouped.columns:
                            instancias_unicas = df_grouped["Instancia"].unique()
                            for inst in instancias_unicas:
                                df_inst = df_grouped[df_grouped["Instancia"] == inst]
                                for metrica in metricas:
                                    if rango == "Personalizado":
                                        fig = plot_cpu_usage_categorical(
                                            df_inst, [metrica], x_col=x_col, granularidad=granularidad, top_n=top_n
                                        )
                                    else:
                                        fig = plot_cpu_usage_live(
                                            df_inst, [metrica], x_col=x_col, granularidad=granularidad, top_n=top_n
                                        )
                                    title_text = build_chart_title(inst, [metrica], granularidad, rango)
                                    fig.update_layout(
                                        title={
                                            'text': title_text,
                                            'y': 0.92,
                                            'x': 0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top',
                                            'font': dict(size=18)
                                        }
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                        else:
                            for metrica in metricas:
                                if rango == "Personalizado":
                                    fig = plot_cpu_usage_categorical(
                                        df_grouped, [metrica], x_col=x_col, granularidad=granularidad, top_n=top_n
                                    )
                                else:
                                    fig = plot_cpu_usage_live(
                                        df_grouped, [metrica], x_col=x_col, granularidad=granularidad, top_n=top_n
                                    )
                                title_text = build_chart_title(instancia, [metrica], granularidad, rango)
                                fig.update_layout(
                                    title={
                                        'text': title_text,
                                        'y': 0.92,
                                        'x': 0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top',
                                        'font': dict(size=18)
                                    }
                                )
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        if rango == "Personalizado":
                            fig = plot_cpu_usage_categorical(
                                df_grouped, metricas, x_col=x_col, granularidad=granularidad, top_n=top_n
                            )
                        else:
                            fig = plot_cpu_usage_live(
                                df_grouped, metricas, x_col=x_col, granularidad=granularidad, top_n=top_n
                            )
                        title_text = build_chart_title(instancia, metricas, granularidad, rango)
                        fig.update_layout(
                            title={
                                'text': title_text,
                                'y': 0.92,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'font': dict(size=18)
                            }
                        )
                        st.plotly_chart(fig, use_container_width=True)
                elif not metricas:
                    st.warning("Selecciona al menos una métrica para graficar.")
                else:
                    st.warning("No hay datos para el rango seleccionado.")
