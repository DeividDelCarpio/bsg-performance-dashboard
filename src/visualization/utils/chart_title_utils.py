# Utilidad para construir títulos de gráficos de CPU

def build_chart_title(instancia, metrica, todas_instancias=False):
    if todas_instancias:
        if metrica:
            return f"Todas las instancias - {metrica}"
        else:
            return "Todas las instancias"
    else:
        return f"{instancia} - {metrica}"
