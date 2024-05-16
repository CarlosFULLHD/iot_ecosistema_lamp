import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Frame

# Configuración de la base de datos
config_db = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'DB_IoTLampV0',
}

def obtener_datos(lamp_id):
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta = """
        SELECT fecha_creacion, LampOnOff, temp_value
        FROM T_IoTLampV0
        WHERE LampID = %s
    """
    cursor.execute(consulta, (lamp_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data, columns=['fecha_creacion', 'LampOnOff', 'temp_value'])

def toggle_estado_lampara(lamp_id):
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta = """
        SELECT Nreg, LampOnOff
        FROM T_IoTLampV0
        WHERE LampID = %s
        ORDER BY fecha_creacion DESC
        LIMIT 1
    """
    cursor.execute(consulta, (lamp_id,))
    resultado = cursor.fetchone()
    if resultado:
        nuevo_estado = 1 if resultado[1] == 2 else 2
        update_consulta = """
            UPDATE T_IoTLampV0
            SET LampOnOff = %s
            WHERE Nreg = %s
        """
        cursor.execute(update_consulta, (nuevo_estado, resultado[0]))
        conn.commit()
        actualizar_boton_estado(nuevo_estado)
    cursor.close()
    conn.close()

def actualizar_boton_estado(estado):
    color = "green" if estado == 2 else "red"
    texto = "ON" if estado == 2 else "OFF"
    boton_estado.config(bg=color, text=texto)

def crear_dashboard(lamp_id):
    datos = obtener_datos(lamp_id)
    if datos.empty:
        messagebox.showerror("Error", "No se encontraron datos para el LampID proporcionado.")
        return
    actualizar_boton_estado(datos.iloc[-1]['LampOnOff'])
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    fig.patch.set_facecolor('#ffffff')
    configurar_graficos(axs, datos)
    mostrar_graficos_en_tkinter(fig)

def configurar_graficos(axs, datos):
    axs[0, 0].plot(datos['fecha_creacion'], datos['LampOnOff'], label='Estado de la Lámpara', color='#b4b4dc')
    axs[0, 0].set_title('Relación fecha_creacion con LampOnOff')
    axs[0, 1].plot(datos['fecha_creacion'], datos['temp_value'], label='Valor Temperatura', color='#b4b4dc')
    axs[1, 0].hist(datos['LampOnOff'], bins=[0,1,2], label='Frecuencia de Estados', color='#b4b4dc')
    axs[1, 1].hist(datos['temp_value'], bins=range(int(datos['temp_value'].min()), int(datos['temp_value'].max()) + 2), label='Frecuencia de Temp.')
    for ax in axs.flat:
        ax.legend()

def mostrar_graficos_en_tkinter(fig):
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root = tk.Tk()
root.title("Control de Lámpara IoT")
root.geometry("1000x600")  # Establece las dimensiones de la ventana
root.configure(background='#ffffff')

# Contenedor principal
main_frame = Frame(root, bg='#ffffff')
main_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)

# Contenedor para los campos de entrada y botones
input_frame = Frame(main_frame, bg='#ffffff')
input_frame.pack(pady=20)

entry_lamp_id = tk.Entry(input_frame)
entry_lamp_id.pack(side=tk.LEFT, padx=10)

boton_dashboard = tk.Button(input_frame, text="Generar Dashboard", command=lambda: crear_dashboard(entry_lamp_id.get()))
boton_dashboard.pack(side=tk.LEFT)

boton_estado = tk.Button(input_frame, text="Estado", bg="gray", command=lambda: toggle_estado_lampara(entry_lamp_id.get()))
boton_estado.pack(side=tk.LEFT, padx=10)

# Contenedor para gráficos
graph_frame = Frame(main_frame, bg='#ffffff')
graph_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
