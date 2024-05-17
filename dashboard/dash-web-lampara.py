import mysql.connector
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, FixedTicker
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import panel as pn
import threading
import time
from math import pi

from bokeh.models import ColumnDataSource, HoverTool

pn.extension()

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'DB_ECOLampV0'
}

# Función para obtener datos de la lámpara específica


def obtener_datos(lamp_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    consulta = "SELECT fecha_creacion, LampOnOff, temp_value, wh_por_hora FROM T_ECOLampV0 WHERE LampID = %s"
    cursor.execute(consulta, (lamp_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        print("No se encontraron datos.")
        return pd.DataFrame()
    df = pd.DataFrame(
        data, columns=['fecha_creacion', 'LampOnOff', 'temp_value', 'wh_por_hora'])
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
    return df

# Función para obtener datos del usuario específico


def obtener_datosusuario(usuario_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    consulta = "SELECT fecha_creacion, UsuarioID, LampID FROM T_ECOLampV0 WHERE UsuarioID = %s"
    cursor.execute(consulta, (usuario_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        print("No se encontraron datos.")
        return pd.DataFrame()
    df = pd.DataFrame(data, columns=['fecha_creacion', 'UsuarioID', 'LampID'])
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
    return df


def obtener_estado_lampara(lamp_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    consulta = "SELECT LampOnOff FROM T_ECOLampV0 WHERE LampID = %s ORDER BY fecha_creacion DESC LIMIT 1"
    cursor.execute(consulta, (lamp_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        return resultado[0]
    return None

# Función para actualizar el estado de la lámpara


def toggle_estado_lampara(event):
    lamp_id = lamp_id_input.value
    estado_actual = obtener_estado_lampara(lamp_id)
    if estado_actual is not None:
        nuevo_estado = 1 if estado_actual == 2 else 2
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        update_consulta = "UPDATE T_ECOLampV0 SET LampOnOff = %s WHERE LampID = %s"
        cursor.execute(update_consulta, (nuevo_estado, lamp_id))
        conn.commit()
        cursor.close()
        conn.close()
        estado_label.object = f"<div style='font-size: 20px; font-weight: bold;'>Estado Actual Foco: {
            'Encendido' if nuevo_estado == 2 else 'Apagado'}</div>"
        toggle_button.button_type = 'success' if nuevo_estado == 2 else 'danger'
    update_dashboard(None)


def obtener_datos_globales():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    consulta = "SELECT fecha_creacion, UsuarioID, LampID, wh_por_hora FROM T_ECOLampV0"
    cursor.execute(consulta)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        print("No se encontraron datos globales.")
        return pd.DataFrame()
    df = pd.DataFrame(
        data, columns=['fecha_creacion', 'UsuarioID', 'LampID', 'wh_por_hora'])
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
    return df

# Función para actualizar el dashboard


def update_dashboard(event):
    lamp_id = lamp_id_input.value
    usuario_id = user_id_input.value
    new_graphics = crear_graficos(lamp_id, usuario_id)
    dashboard_objects[-1].clear()
    dashboard_objects[-1].append(new_graphics)


def crear_graficos(lamp_id, usuario_id):
    datos_lamp = obtener_datos(lamp_id)
    datos_usuario = obtener_datosusuario(usuario_id)
    datos_globales = obtener_datos_globales()

    if datos_lamp.empty and datos_usuario.empty and datos_globales.empty:
        return pn.pane.Markdown("No se encontraron datos para el LampID, UsuarioID o datos globales proporcionados.")

    tabs = []

    if not datos_lamp.empty:
        p1 = figure(title="Relación fecha_creacion con LampOnOff",
                    x_axis_type="datetime", sizing_mode="stretch_width", height=250)
        p1.line(datos_lamp['fecha_creacion'], datos_lamp['LampOnOff'],
                legend_label='Estado de la Lámpara', line_color='#b4b4dc')

        p3 = figure(title="Relación fecha_creacion con temp_value",
                    x_axis_type="datetime", sizing_mode="stretch_width", height=250)
        p3.line(datos_lamp['fecha_creacion'], datos_lamp['temp_value'],
                legend_label='Valor Temperatura', line_color='#b4b4dc')

        hist, edges = np.histogram(
            datos_lamp['LampOnOff'], bins=np.arange(0, 3) - 0.5, density=True)
        p2 = figure(title="Histograma de LampOnOff",
                    sizing_mode="stretch_width", height=250)
        p2.quad(top=hist, bottom=0,
                left=edges[:-1], right=edges[1:], fill_color="#b4b4dc")

        hist_temp, edges_temp = np.histogram(
            datos_lamp['temp_value'], bins=15, density=True)
        p4 = figure(title="Histograma de temp_value",
                    sizing_mode="stretch_width", height=250)
        p4.quad(top=hist_temp, bottom=0,
                left=edges_temp[:-1], right=edges_temp[1:], fill_color="#b4b4dc")

        total_kwh = datos_lamp['wh_por_hora'].sum() / 1000
        costo_total = total_kwh * 0.84
        horas_utilizadas = datos_lamp['LampOnOff'].sum()
        vida_util = max(0, (36 - horas_utilizadas) / 36 * 100)
        consumo_label.object = f"<div style='font-size: 20px; font-weight: bold;'>Consumo total en kWh: {
            total_kwh:.4f} kWh (Bs {costo_total:.2f})</div>"
        vida_label.object = f"<div style='font-size: 20px; font-weight: bold;'>Tiempo de vida: {
            vida_util}%</div>"

        if vida_util < 10:
            vida_label.styles = {'color': 'red'}
        else:
            vida_label.styles = {'color': 'black'}

        grid_lamp = pn.GridSpec(sizing_mode='stretch_both', max_height=500)
        grid_lamp[0, 0] = p1
        grid_lamp[0, 1] = p2
        grid_lamp[1, 0] = p3
        grid_lamp[1, 1] = p4

        tabs.append(("Gráficos de Lámpara", grid_lamp))

    if not datos_usuario.empty:
        datos_usuario['UsuarioID'] = datos_usuario['UsuarioID'].astype(
            'category').cat.codes
        datos_usuario['LampID'] = datos_usuario['LampID'].astype(
            'category').cat.codes

        hist_user, edges_user = np.histogram(
            datos_usuario['UsuarioID'], bins=15, density=True)
        p5 = figure(title="Histograma de UsuarioID",
                    sizing_mode="stretch_width", height=250)
        p5.quad(top=hist_user, bottom=0,
                left=edges_user[:-1], right=edges_user[1:], fill_color="#b4b4dc")

        p6 = figure(title="Relación fecha_creacion con UsuarioID",
                    x_axis_type="datetime", sizing_mode="stretch_width", height=250)
        p6.line(datos_usuario['fecha_creacion'], datos_usuario['UsuarioID'],
                legend_label='UsuarioID', line_color='#b4b4dc')

        hist_lamp_user, edges_lamp_user = np.histogram(
            datos_usuario['LampID'], bins=15, density=True)
        p7 = figure(title="Histograma de UsuarioID Vs LampID",
                    sizing_mode="stretch_width", height=250)
        p7.quad(top=hist_lamp_user, bottom=0,
                left=edges_lamp_user[:-1], right=edges_lamp_user[1:], fill_color="#b4b4dc")

        p8 = figure(title="Relación fecha_creacion con UsuarioID",
                    x_axis_type="datetime", sizing_mode="stretch_width", height=250)
        p8.line(datos_usuario['fecha_creacion'], datos_usuario['UsuarioID'],
                legend_label='UsuarioID', line_color='#b4b4dc')

        grid_usuario = pn.GridSpec(sizing_mode='stretch_both', max_height=500)
        grid_usuario[0, 0] = p5
        grid_usuario[0, 1] = p6
        grid_usuario[1, 0] = p7
        grid_usuario[1, 1] = p8

        tabs.append(("Gráficos de Usuario", grid_usuario))

    if not datos_globales.empty:
        # Torta en porcentaje de usuarios por fecha de creación
        user_counts = datos_globales.groupby('UsuarioID').size()
        user_data = pd.Series(user_counts).reset_index(
            name='value').rename(columns={'index': 'UsuarioID'})
        user_data['angle'] = user_data['value']/user_data['value'].sum() * 2*pi
        user_data['color'] = Category20c[len(user_data)]
        p8 = figure(height=350, title="Usuarios por Fecha de Creación", toolbar_location=None,
                    tools="hover", tooltips="@UsuarioID: @value", x_range=(-0.5, 1.0))
        p8.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum(
            'angle'), line_color="white", fill_color='color', legend_field='UsuarioID', source=user_data)
        p8.axis.axis_label = None
        p8.axis.visible = False
        p8.grid.grid_line_color = None

        # Torta en porcentaje de lámparas por fecha de creación
        lamp_counts = datos_globales.groupby('LampID').size()
        lamp_data = pd.Series(lamp_counts).reset_index(
            name='value').rename(columns={'index': 'LampID'})
        lamp_data['angle'] = lamp_data['value']/lamp_data['value'].sum() * 2*pi
        lamp_data['color'] = Category20c[len(lamp_data)]
        p9 = figure(height=350, title="Lámparas por Fecha de Creación", toolbar_location=None,
                    tools="hover", tooltips="@LampID: @value", x_range=(-0.5, 1.0))
        p9.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum(
            'angle'), line_color="white", fill_color='color', legend_field='LampID', source=lamp_data)
        p9.axis.axis_label = None
        p9.axis.visible = False
        p9.grid.grid_line_color = None

        # Histograma de la frecuencia de las lámparas
        lamp_hist, lamp_edges = np.histogram(datos_globales['LampID'].astype(
            'category').cat.codes, bins=15, density=True)
        p10 = figure(title="Frecuencia de las Lámparas",
                     sizing_mode="stretch_width", height=250)
        p10.quad(top=lamp_hist, bottom=0,
                 left=lamp_edges[:-1], right=lamp_edges[1:], fill_color="#b4b4dc")

        # Consumo total de todas las lámparas en kWh
        total_global_kwh = datos_globales['wh_por_hora'].sum() / 1000
        costo_global_total = total_global_kwh * 0.84
        consumo_global_label = pn.pane.Markdown(f"<div style='font-size: 20px; font-weight: bold;'>Consumo total de todas las lámparas: {
                                                total_global_kwh:.4f} kWh (Bs {costo_global_total:.2f})</div>")

        grid_global = pn.GridSpec(sizing_mode='stretch_both', max_height=500)
        grid_global[0, 0] = p8
        grid_global[0, 1] = p9
        grid_global[1, 0] = p10
        grid_global[1, 1] = consumo_global_label

        tabs.append(("Gráficos Globales", grid_global))

    return pn.Tabs(*tabs)

# Función para actualizar el dashboard automáticamente cada 5 segundos


def auto_update_dashboard():
    while True:
        time.sleep(5)
        update_dashboard(None)


# Configuración de componentes y dashboard
lamp_id_input = pn.widgets.TextInput(name='LampID', value='lamp1')
user_id_input = pn.widgets.TextInput(name='UserID', value='user1')
update_button = pn.widgets.Button(
    name='Actualizar Dashboard', button_type='primary')
toggle_button = pn.widgets.Button(name='Estado Foco', button_type='success')
estado_label = pn.pane.Markdown(
    "<div style='font-size: 20px; font-weight: bold;'>Estado Actual Foco: Desconocido</div>")
consumo_label = pn.pane.Markdown(
    "<div style='font-size: 20px; font-weight: bold;'>Consumo total en kWh: Desconocido</div>")
vida_label = pn.pane.Markdown(
    "<div style='font-size: 20px; font-weight: bold;'>Tiempo de vida: Desconocido</div>")

update_button.on_click(update_dashboard)
toggle_button.on_click(toggle_estado_lampara)

dashboard_objects = [
    pn.Row(lamp_id_input, user_id_input, update_button, toggle_button),
    pn.Row(estado_label, consumo_label, vida_label),
    pn.Column(crear_graficos(lamp_id_input.value, user_id_input.value))
]
dashboard = pn.Column(*dashboard_objects)

# Iniciar el hilo para actualizar el dashboard automáticamente
threading.Thread(target=auto_update_dashboard, daemon=True).start()

# Servir el dashboard
dashboard.servable(title="Dashboard de la Lámpara IoT")
pn.serve(dashboard)
