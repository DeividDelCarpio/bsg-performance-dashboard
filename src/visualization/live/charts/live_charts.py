import pandas as pd
import plotly.graph_objects as go
from src.visualization.utils.line_chart import create_line_figure
from src.visualization.live.annotation.peak_annotations import add_peak_annotations
from src.visualization.utils.grouping_utils import group_by_granularity

def plot_cpu_usage_live(df, metricas=None, x_col='FechaEvento', granularidad="10 Minutos", top_n=3):
    """
    Gráfico de uso de CPU en vivo, con granularidad y métricas seleccionadas.
    """
    df = group_by_granularity(df, x_col, granularidad)
    df['x_categoria'] = pd.to_datetime(df[x_col], errors='coerce').dt.strftime('%H:%M %d/%m')
    agrupado = df.copy()

    fig = create_line_figure()
    green_shades = ['#2ecc40', '#27ae60', '#16a085', '#00b894', '#00cec9']  # Tonos de verde

    for idx, metrica in enumerate(metricas or ['Uso']):
        color = green_shades[idx % len(green_shades)]
        if 'Instancia' in agrupado.columns and agrupado['Instancia'].nunique() > 1:
            for instancia, df_inst in agrupado.groupby('Instancia'):
                fig.add_trace(go.Scatter(
                    x=df_inst['x_categoria'],
                    y=df_inst[metrica],
                    mode='lines',
                    name=f"{instancia} - {metrica}",
                    showlegend=True,
                    connectgaps=False,
                    line=dict(color=color, width=3)
                ))
        else:
            fig.add_trace(go.Scatter(
                x=agrupado['x_categoria'],
                y=agrupado[metrica],
                mode='lines',
                name=metrica,
                showlegend=True,
                connectgaps=False,
                line=dict(color=color, width=3)
            ))

    if not df.empty:
        dt_col = pd.to_datetime(df[x_col], errors='coerce') if not pd.api.types.is_datetime64_any_dtype(df[x_col]) else df[x_col]
        df['_dt_col'] = dt_col
        df['_dia'] = df['_dt_col'].dt.date

        ticks = []
        ticktext = []
        for fecha in sorted(df['_dia'].unique()):
            df_dia = df[df['_dia'] == fecha]
            df_dia_valid = df_dia[pd.notnull(df_dia['_dt_col'])]
            if not df_dia_valid.empty:
                for idx, row in df_dia_valid.iterrows():
                    hora = row['_dt_col'].hour
                    if hora % 2 == 0 and row['_dt_col'].minute == 0:
                        ticks.append(row['x_categoria'])
                        ticktext.append(f"{row['_dt_col'].strftime('%H:%M')}<br>{row['_dt_col'].strftime('%d/%m')}")

        df.drop(columns=['_dia', '_dt_col'], inplace=True)

        fig.update_xaxes(
            tickmode="array",
            tickvals=ticks,
            ticktext=ticktext,
            tickangle=0,
            automargin=True,
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=False   
        )

    fig.update_yaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=False   
    )

    if top_n and top_n > 0:
        for metrica in (metricas or ['Uso']):
            df_peak = df.copy()
            dt_col = pd.to_datetime(df_peak[x_col], errors='coerce') if not pd.api.types.is_datetime64_any_dtype(df_peak[x_col]) else df_peak[x_col]
            df_peak['_dia'] = dt_col.dt.date
            for dia in df_peak['_dia'].unique():
                df_dia = df_peak[df_peak['_dia'] == dia]
                if not df_dia.empty:
                    df_peaks = df_dia.sort_values(metrica, ascending=False).head(top_n)
                    for _, row in df_peaks.iterrows():
                        fecha_str = str(row['x_categoria'])
                        fig.add_annotation(
                            x=row['x_categoria'],
                            y=row[metrica],
                            text=f"<b>{row[metrica]:.1f}%</b><br><span style='font-size:10px'>{fecha_str}</span>",
                            showarrow=True,
                            arrowhead=1,
                            ax=0,
                            ay=-40,
                            bgcolor="rgba(255,255,255,0.85)",
                            bordercolor="#888",
                            borderwidth=1,
                            font=dict(size=11)
                        )
    return fig