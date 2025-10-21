# BSG Performance Dashboard

Este proyecto es un dashboard interactivo en Streamlit para visualizar métricas de uso de CPU desde SQL Server (tabla [aud].[T_AuditoriaUsoCPU]).

## Instalación

1. Clona el repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura los parámetros de conexión en `config/config.yaml`.

## Ejecución

```bash
streamlit run app.py
```

## Estructura
- `app.py`: dashboard principal
- `src/`: módulos de conexión, carga y gráficos
- `config/`: configuración de conexión
- `notebooks/`: exploración de datos
- `tests/`: pruebas unitarias

## Configuración de credenciales

El archivo `config/config.yaml` contiene credenciales sensibles y está excluido del repositorio por motivos de seguridad (`.gitignore`).  
**Debes crear este archivo manualmente antes de ejecutar la aplicación** o configurar las credenciales necesarias como variables de entorno en Streamlit Cloud.

Ejemplo de estructura de `config.yaml`:
```yaml
usuario: "TU_USUARIO"
password: "TU_PASSWORD"
host: "TU_HOST"
```
