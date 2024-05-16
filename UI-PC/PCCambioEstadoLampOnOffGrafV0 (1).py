import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importar PIL

# Configuración de la base de datos
config_db = {
    'user': 'root',  # Cambia esto por tu nombre de usuario MySQL
    'password': '',  # Cambia esto por tu contraseña MySQL
    'host': 'localhost',  # Cambia esto si tu servidor MySQL está en otra dirección
    'database': 'DB_ECOLampV0',  # Cambia esto por el nombre de tu base de datos
}
estadoLamp = 0

# Función para actualizar el campo LampOnOff en la base de datos
def actualizar_lamp_onoff(user_id, lamp_id, estado):
    global estadoLamp
    nuevo_estado_lamp = 2 if estado else 1

    # Conectar a la base de datos
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()

    # Consulta para obtener el ID del último registro ingresado basado en LampID y UsuarioID
    consulta_id = """
        SELECT Nreg, LampOnOff
        FROM T_ECOLampV0
        WHERE LampID = %s AND UsuarioID = %s
        ORDER BY fecha_creacion DESC
        LIMIT 1
    """

    # Ejecuta la consulta para obtener el ID del último registro
    cursor.execute(consulta_id, (lamp_id, user_id))
    resultado = cursor.fetchone()
    print(resultado)
    # Verifica si se encontró un registro
    if resultado:
        nreg = resultado[0]
        estadoLamp = resultado[1]
        # Consulta para actualizar el valor de LampOnOff en el último registro
        consulta_update = """
            UPDATE T_ECOLampV0
            SET LampOnOff = %s
            WHERE Nreg = %s
        """
        
        # Ejecuta la consulta para actualizar el campo LampOnOff
        cursor.execute(consulta_update, (nuevo_estado_lamp, nreg))

        # Confirma los cambios en la base de datos
        conn.commit()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"El valor de LampOnOff del registro con Nreg = {nreg} ha sido actualizado a {nuevo_estado_lamp}")
    else:
        # Mostrar mensaje de error si no se encuentra un registro con LampID y UsuarioID
        messagebox.showerror("Error", f"No se encontró ningún registro con LampID = {lamp_id} y UsuarioID = {user_id}")

    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

# Crear la GUI con tkinter
root = tk.Tk()
root.title("Actualizar LampOnOff")
root.configure(bg='#ffffff')
root.geometry("300x450")

# Agregar logo redimensionado
image = Image.open('logo3.png')
image = image.resize((150, 160))
logo = ImageTk.PhotoImage(image)
logo_label = tk.Label(root, image=logo, bg='#ffffff')
logo_label.grid(row=0, column=1, columnspan=3, pady=10)

# Etiqueta y entrada para UserID
label_user_id = tk.Label(root, text="UserID:", bg='#ffffff', font=('Arial', 12))
label_user_id.grid(row=1, column=0, padx=10, pady=10)
entry_user_id = tk.Entry(root)
entry_user_id.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

# Etiqueta y entrada para LampID
label_lamp_id = tk.Label(root, text="LampID:", bg='#ffffff', font=('Arial', 12))
label_lamp_id.grid(row=2, column=0, padx=10, pady=10)
entry_lamp_id = tk.Entry(root)
entry_lamp_id.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

# Variable para almacenar el estado de LampOnOff (True para Encendido, False para Apagado)
is_on = True

# Define our images for the switch with resizing and background
on_image = Image.open('on.png')
on_image = on_image.resize((100, 150))  # Ajusta el tamaño según sea necesario
on_image_with_bg = Image.new("RGBA", on_image.size, (255, 255, 255, 255))  # Fondo blanco
on_image_with_bg.paste(on_image, (0, 0), on_image)
on = ImageTk.PhotoImage(on_image_with_bg)

off_image = Image.open('off.png')
off_image = off_image.resize((100, 150))  # Ajusta el tamaño según sea necesario
off_image_with_bg = Image.new("RGBA", off_image.size, (255, 255, 255, 255))  # Fondo blanco
off_image_with_bg.paste(off_image, (0, 0), off_image)
off = ImageTk.PhotoImage(off_image_with_bg)

# Define our switch function
def switch():
    global is_on
    user_id = entry_user_id.get()
    lamp_id = entry_lamp_id.get()
    if user_id and lamp_id:
        nuevo_estado = not is_on
        actualizar_lamp_onoff(user_id, lamp_id, nuevo_estado)
        if is_on:
            on_button.config(image=off)
            is_on = False
        else:
            on_button.config(image=on)
            is_on = True
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese tanto UserID como LampID")

# Crear el botón de encendido/apagado
on_button = tk.Button(root, image=on, bd=0, command=switch)
on_button.grid(row=3, column=1, pady=10)

# Ejecutar la aplicación
root.mainloop()

