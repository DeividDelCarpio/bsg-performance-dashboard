import plotly.graph_objects as go
import pandas as pd

def add_peak_annotations(fig, df, x_col, y_col, instancia_col=None, top_n=2, por_dia=False):
    """
    Añade anotaciones a los top_n picos más altos de y_col en el gráfico fig.
    Si instancia_col está presente, busca los picos por instancia.
    Si por_dia=True, busca los picos por día (y por instancia si aplica).
    """
    if top_n == 0:
        return fig

    if por_dia:
        df = df.copy()
        try:
            df['_dia'] = pd.to_datetime(df[x_col]).dt.date
        except Exception:
            df['_dia'] = df[x_col]

    if instancia_col and instancia_col in df.columns:
        group_fields = [instancia_col]
        if por_dia:
            group_fields.append('_dia')
        for keys, df_group in df.groupby(group_fields):
            if por_dia:
                for dia, df_dia in df_group.groupby('_dia'):
                    df_peaks = df_dia.sort_values(y_col, ascending=False).drop_duplicates([x_col]).head(top_n)
                    for _, row in df_peaks.iterrows():
                        try:
                            fecha_str = pd.to_datetime(row[x_col]).strftime('%d/%m %H:%M')
                        except Exception:
                            fecha_str = str(row[x_col])
                        fig.add_annotation(
                            x=row[x_col],
                            y=row[y_col],
                            text=f"<b>{row[y_col]:.1f}%</b><br><span style='font-size:10px'>{fecha_str}</span>",
                            showarrow=True,
                            arrowhead=1,
                            ax=0,
                            ay=-40,
                            bgcolor="rgba(255,255,255,0.85)",
                            bordercolor="#888",
                            borderwidth=1,
                            font=dict(size=11)
                        )
            else:
                df_peaks = df_group.sort_values(y_col, ascending=False).drop_duplicates([x_col]).head(top_n)
                for _, row in df_peaks.iterrows():
                    try:
                        fecha_str = pd.to_datetime(row[x_col]).strftime('%d/%m %H:%M')
                    except Exception:
                        fecha_str = str(row[x_col])
                    fig.add_annotation(
                        x=row[x_col],
                        y=row[y_col],
                        text=f"<b>{row[y_col]:.1f}%</b><br><span style='font-size:10px'>{fecha_str}</span>",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40,
                        bgcolor="rgba(255,255,255,0.85)",
                        bordercolor="#888",
                        borderwidth=1,
                        font=dict(size=11)
                    )
    else:
        if por_dia:
            for dia, df_group in df.groupby('_dia'):
                df_peaks = df_group.sort_values(y_col, ascending=False).drop_duplicates([x_col]).head(top_n)
                for _, row in df_peaks.iterrows():
                    try:
                        fecha_str = pd.to_datetime(row[x_col]).strftime('%d/%m %H:%M')
                    except Exception:
                        fecha_str = str(row[x_col])
                    fig.add_annotation(
                        x=row[x_col],
                        y=row[y_col],
                        text=f"<b>{row[y_col]:.1f}%</b><br><span style='font-size:10px'>{fecha_str}</span>",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40,
                        bgcolor="rgba(255,255,255,0.85)",
                        bordercolor="#888",
                        borderwidth=1,
                        font=dict(size=11)
                    )
        else:
            df_peaks = df.sort_values(y_col, ascending=False).drop_duplicates([x_col]).head(top_n)
            for _, row in df_peaks.iterrows():
                try:
                    fecha_str = pd.to_datetime(row[x_col]).strftime('%d/%m %H:%M')
                except Exception:
                    fecha_str = str(row[x_col])
                fig.add_annotation(
                    x=row[x_col],
                    y=row[y_col],
                    text=f"<b>{row[y_col]:.1f}%</b><br><span style='font-size:10px'>{fecha_str}</span>",
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
