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
    'database': 'DB_ECOLampV0',
}

def obtener_datoslamp(lamp_id):
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta = """
        SELECT fecha_creacion, LampOnOff, temp_value
        FROM T_ECOLampV0
        WHERE LampID = %s
    """
    cursor.execute(consulta, (lamp_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(data, columns=['fecha_creacion', 'LampOnOff', 'temp_value'])
    print("Datos obtenidos desde la base de datos:", df)
    return df

def obtener_datosusuario(user_id):
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta = """
        SELECT fecha_creacion, UsuarioID, LampID, LampOnOff
        FROM T_ECOLampV0
        WHERE UsuarioID = %s
    """
    cursor.execute(consulta, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(data, columns=['fecha_creacion', 'UsuarioID', 'LampID', 'LampOnOff'])
    print("Datos obtenidos desde la base de datos:", df)
    return df

def obtener_todos_datos():
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta = """
        SELECT fecha_creacion, UsuarioID, LampID, temp_value
        FROM T_ECOLampV0
    """
    cursor.execute(consulta)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(data, columns=['fecha_creacion', 'UsuarioID', 'LampID', 'temp_value'])
    print("Datos obtenidos desde la base de datos:", df)
    return df

def toggle_estado_lampara(user_id, lamp_id):
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta = """
        SELECT Nreg, LampOnOff
        FROM T_ECOLampV0
        WHERE LampID = %s AND UsuarioID = %s
        ORDER BY fecha_creacion DESC
        LIMIT 1
    """
    cursor.execute(consulta, (lamp_id, user_id))
    resultado = cursor.fetchone()
    if resultado:
        nuevo_estado = 1 if resultado[1] == 2 else 2
        update_consulta = """
            UPDATE T_ECOLampV0
            SET LampOnOff = %s
            WHERE Nreg = %s
        """
        cursor.execute(update_consulta, (nuevo_estado, resultado[0]))
        conn.commit()
        print("Estado de la lámpara actualizado a:", nuevo_estado)
        actualizar_boton_estado(nuevo_estado)
    cursor.close()
    conn.close()

def actualizar_boton_estado(estado):
    color = "green" if estado == 2 else "red"
    texto = "Encendido" if estado == 2 else "Apagado"
    boton_estado.config(bg=color, text=texto)
    print("Botón de estado actualizado a:", texto)

def refrescar_dashboard_lamp():
    lamp_id = entry_lamp_id.get()
    print("Refrescando dashboard para LampID:", lamp_id)
    crear_dashboard_lamp(lamp_id)

def refrescar_dashboard_user():
    user_id = entry_user_id.get()
    print("Refrescando dashboard para UsuarioID:", user_id)
    crear_dashboard_user(user_id)

def crear_dashboard_lamp(lamp_id):
    global fig, mpl_canvas
    datos = obtener_datoslamp(lamp_id)
    if datos.empty:
        messagebox.showerror("Error", "No se encontraron datos para el LampID proporcionado.")
        return
    actualizar_boton_estado(datos.iloc[-1]['LampOnOff'])

    if 'fig' in globals():
        plt.close(fig)

    fig, axs = plt.subplots(3, 2, figsize=(12, 10), facecolor='#c8dcf0')
    axs[0, 0].plot(datos['fecha_creacion'], datos['LampOnOff'], label='Estado de la Lámpara', color='#b4b4dc')
    axs[0, 0].set_title('Relación fecha_creacion VS. LampOnOff')
    axs[0, 0].set_xlabel('Fecha')
    axs[0, 0].set_ylabel('Estado LampOnOff')
    axs[0, 0].legend()

    axs[1, 0].hist(datos['LampOnOff'], color='#b4b4dc', bins=[0, 1, 2], edgecolor='black', linewidth=1.2, label='Frecuencia de Estados')
    axs[1, 0].set_title('Histograma Frecuencia VS. LampOnOff')
    axs[1, 0].set_xlabel('Estado LampOnOff')
    axs[1, 0].set_ylabel('Frecuencia')
    axs[1, 0].legend()

    axs[0, 1].plot(datos['fecha_creacion'], datos['temp_value'], label='Valor Temperatura', color='#b4b4dc')
    axs[0, 1].set_title('Relación fecha_creacion VS. temp_value')
    axs[0, 1].set_xlabel('Fecha')
    axs[0, 1].set_ylabel('Temp. Valor (°C)')
    axs[0, 1].legend()

    axs[1, 1].hist(datos['temp_value'], color='#b4b4dc', bins=range(int(datos['temp_value'].min()), int(datos['temp_value'].max()) + 2), edgecolor='black', linewidth=1.2, label='Frecuencia de Temp.')
    axs[1, 1].set_title('Histograma Frecuencia VS. temp_value')
    axs[1, 1].set_xlabel('Temp. Valor (°C)')
    axs[1, 1].set_ylabel('Frecuencia')
    axs[1, 1].legend()

    # Calcular consumo total en kWh y mostrar
    consumo_total_kwh = datos['temp_value'].sum() / 1000  # Suponiendo temp_value representa Wh
    costo_total = consumo_total_kwh * 0.84
    axs[2, 0].text(0.5, 0.5, f'Consumo total: {consumo_total_kwh:.2f} kWh\nCosto total: {costo_total:.2f} Bs', 
                   horizontalalignment='center', verticalalignment='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    axs[2, 0].axis('off')

    # Calcular tiempo de vida útil de la lámpara
    tiempo_uso_total = datos['LampOnOff'].sum()  # Suponiendo LampOnOff representa horas de uso
    vida_util_restante = max(0, 1000 - tiempo_uso_total)
    axs[2, 1].text(0.5, 0.5, f'Tiempo de vida restante: {vida_util_restante} horas', 
                   horizontalalignment='center', verticalalignment='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    axs[2, 1].axis('off')

    plt.tight_layout()

    if 'mpl_canvas' in globals():
        mpl_canvas.get_tk_widget().pack_forget()

    mpl_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
    mpl_canvas.draw()
    mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    print("Dashboard generado para LampID:", lamp_id)

def crear_dashboard_user(user_id):
    global fig, mpl_canvas
    datos = obtener_datosusuario(user_id)
    if datos.empty:
        messagebox.showerror("Error", "No se encontraron datos para el UsuarioID proporcionado.")
        return

    if 'fig' in globals():
        plt.close(fig)

    fig, axs = plt.subplots(3, 1, figsize=(12, 10), facecolor='#c8dcf0')
    axs[0].hist(datos['LampID'], color='#b4b4dc', edgecolor='black', linewidth=1.2, label='Frecuencia por UsuarioID')
    axs[0].set_title('Histograma Frecuencia VS. UsuarioID')
    axs[0].set_xlabel('LampID')
    axs[0].set_ylabel('Frecuencia')
    axs[0].legend()

    axs[1].plot(datos['fecha_creacion'], datos['LampID'], label='Fecha de creación por UsuarioID', color='#b4b4dc')
    axs[1].set_title('Relación fecha_creacion VS. UsuarioID')
    axs[1].set_xlabel('Fecha')
    axs[1].set_ylabel('UsuarioID')
    axs[1].legend()

    axs[2].hist(datos['LampID'], color='#b4b4dc', edgecolor='black', linewidth=1.2, label='UsuarioID vs LampID')
    axs[2].set_title('Histograma UsuarioID VS. LampID')
    axs[2].set_xlabel('UsuarioID')
    axs[2].set_ylabel('LampID')
    axs[2].legend()

    plt.tight_layout()

    if 'mpl_canvas' in globals():
        mpl_canvas.get_tk_widget().pack_forget()

    mpl_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
    mpl_canvas.draw()
    mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    print("Dashboard generado para UsuarioID:", user_id)

def crear_graficos_adicionales():
    datos = obtener_todos_datos()
    if datos.empty:
        messagebox.showerror("Error", "No se encontraron datos.")
        return

    if 'fig_adicional' in globals():
        plt.close(fig_adicional)

    fig_adicional, axs = plt.subplots(2, 2, figsize=(12, 10), facecolor='#c8dcf0')
    
    # Torta en porcentaje en función de la fecha de creación y todos los usuarios
    usuarios = datos['UsuarioID'].value_counts()
    axs[0, 0].pie(usuarios, labels=usuarios.index, autopct='%1.1f%%')
    axs[0, 0].set_title('Distribución de Usuarios')

    # Torta en porcentaje en función de la fecha de creación y todas las lámparas
    lamparas = datos['LampID'].value_counts()
    axs[0, 1].pie(lamparas, labels=lamparas.index, autopct='%1.1f%%')
    axs[0, 1].set_title('Distribución de Lámparas')

    # Histograma Frecuencia Vs Lamparas
    axs[1, 0].hist(datos['LampID'], bins=len(lamparas), color='#b4b4dc', edgecolor='black', linewidth=1.2)
    axs[1, 0].set_title('Histograma Frecuencia Vs Lámparas')
    axs[1, 0].set_xlabel('LampID')
    axs[1, 0].set_ylabel('Frecuencia')

    # Consumo total de todas las lámparas de kWh
    consumo_total_kwh = datos['temp_value'].sum() / 1000  # Suponiendo temp_value representa Wh
    costo_total = consumo_total_kwh * 0.84
    axs[1, 1].text(0.5, 0.5, f'Consumo total: {consumo_total_kwh:.2f} kWh\nCosto total: {costo_total:.2f} Bs', 
                   horizontalalignment='center', verticalalignment='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    axs[1, 1].axis('off')

    plt.tight_layout()

    if 'mpl_canvas_adicional' in globals():
        mpl_canvas_adicional.get_tk_widget().pack_forget()

    mpl_canvas_adicional = FigureCanvasTkAgg(fig_adicional, master=scrollable_frame)
    mpl_canvas_adicional.draw()
    mpl_canvas_adicional.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    print("Gráficos adicionales generados.")

root = tk.Tk()
root.title("Control de Lámparas IoT y Usuarios ")
root.configure(background='#c8dcf0')

main_frame = Frame(root, bg='#c8dcf0')
main_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)
tk_canvas = Canvas(main_frame, bg='#c8dcf0')
tk_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL, command=tk_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tk_canvas.configure(yscrollcommand=scrollbar.set)
tk_canvas.bind('<Configure>', lambda e: tk_canvas.configure(scrollregion=tk_canvas.bbox("all")))
scrollable_frame = Frame(tk_canvas, bg='#c8dcf0')
tk_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

label_user_id = tk.Label(scrollable_frame, text="UserID:", bg='#c8dcf0')
label_user_id.pack(pady=(10, 0))
entry_user_id = tk.Entry(scrollable_frame)
entry_user_id.pack(pady=10)

label_lamp_id = tk.Label(scrollable_frame, text="LampID:", bg='#c8dcf0')
label_lamp_id.pack(pady=(10, 0))
entry_lamp_id = tk.Entry(scrollable_frame)
entry_lamp_id.pack(pady=10)

boton_estado = tk.Button(scrollable_frame, text="Estado", bg="gray", command=lambda: toggle_estado_lampara(entry_user_id.get(), entry_lamp_id.get()))
boton_estado.pack(pady=10)

boton_dashboard_lamp = tk.Button(scrollable_frame, text="Generar Dashboard por LampID", command=refrescar_dashboard_lamp)
boton_dashboard_lamp.pack(pady=(0, 20))

boton_dashboard_user = tk.Button(scrollable_frame, text="Generar Dashboard por UsuarioID", command=refrescar_dashboard_user)
boton_dashboard_user.pack(pady=(0, 20))

boton_graficos_adicionales = tk.Button(scrollable_frame, text="Generar Gráficos Adicionales", command=crear_graficos_adicionales)
boton_graficos_adicionales.pack(pady=(0, 20))

root.mainloop()

