import mysql.connector as mysql
import pandas as pd
import numpy as np
from bokeh.plotting import figure
import panel as pn

# Inicialización de las extensiones de visualización
pn.extension()

# Datos para conectar a la base de datos
configuracion_db = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'DB_IoTLampV0'
}

# Recuperar registros de la base de datos
def recuperar_registros(identificador_lampara):
    conexion = mysql.connect(**configuracion_db)
    cursor = conexion.cursor()
    query = "SELECT fecha_creacion, LampOnOff, temp_value FROM T_IoTLampV0 WHERE LampID = %s"
    cursor.execute(query, (identificador_lampara,))
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    if not registros:
        return pd.DataFrame()
    return pd.DataFrame(registros, columns=['fecha_creacion', 'LampOnOff', 'temp_value'])

# Generar gráficas a partir de los datos
def generar_graficas(id_lampara):
    datos_lampara = recuperar_registros(id_lampara)
    if datos_lampara.empty:
        return pn.pane.Markdown("No hay datos disponibles para este ID.")
    datos_lampara['fecha_creacion'] = pd.to_datetime(datos_lampara['fecha_creacion'])
    grafico_linea1 = figure(title="Estado de la Lámpara", x_axis_type="datetime", sizing_mode='stretch_width')
    grafico_linea1.line(datos_lampara['fecha_creacion'], datos_lampara['LampOnOff'], color='green', legend_label='On/Off')
    grafico_linea2 = figure(title="Temperatura Registrada", x_axis_type="datetime", sizing_mode='stretch_width')
    grafico_linea2.line(datos_lampara['fecha_creacion'], datos_lampara['temp_value'], color='red', legend_label='Temperatura')
    
    hist_estado, bordes_estado = np.histogram(datos_lampara['LampOnOff'], bins=np.arange(0, 3) - 0.5)
    grafico_hist_estado = figure(title="Histograma de Estados", height=250, sizing_mode='stretch_width')
    grafico_hist_estado.quad(top=hist_estado, bottom=0, left=bordes_estado[:-1], right=bordes_estado[1:], fill_color="blue")

    hist_temp, bordes_temp = np.histogram(datos_lampara['temp_value'], bins=15)
    grafico_hist_temp = figure(title="Histograma de Temperatura", height=250, sizing_mode='stretch_width')
    grafico_hist_temp.quad(top=hist_temp, bottom=0, left=bordes_temp[:-1], right=bordes_temp[1:], fill_color="orange")
    
    graficos = pn.Column(grafico_linea1, grafico_linea2)
    histogramas = pn.Column(grafico_hist_estado, grafico_hist_temp)
    return pn.Tabs(("Líneas", graficos), ("Histogramas", histogramas))

entrada_lamp_id = pn.widgets.TextInput(name='ID de Lámpara', value='lamp1')
boton_refresco = pn.widgets.Button(name='Refrescar', button_type='primary')
estado_visual = pn.pane.Markdown("<div style='font-size: 20px;'>Estado de la Lámpara: Desconocido</div>")
paneles_dashboard = [pn.Row(entrada_lamp_id, boton_refresco, estado_visual), pn.Row()]

# Configuración del evento de clic para actualizar el panel
def actualizar_panel(event):
    paneles_dashboard[1].objects = [generar_graficas(entrada_lamp_id.value)]
boton_refresco.on_click(actualizar_panel)

dashboard_completo = pn.Column(*paneles_dashboard, sizing_mode='stretch_width')
dashboard_completo.servable(title="Controlador de Lámpara IoT")
pn.serve(dashboard_completo)

# Configuración del servidor para permitir accesos desde IPs específicas
allowed_origins = [
    '0.0.0.0:5006',
    'localhost:5006'
]

# Servir el dashboard permitiendo el acceso desde el celular y otros dispositivos
pn.serve(dashboard_completo, port=5006, address='0.0.0.0', allow_websocket_origin=allowed_origins)
