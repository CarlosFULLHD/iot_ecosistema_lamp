import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importar PIL

# Configuración de la base de datos
config_db = {
    'user': 'usuario0',
    'password': '',
    'host': 'localhost',
    'database': 'DB_IoTLampV0',
}

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
    lamp_id = entry_lamp_id.get()
    if lamp_id:
        nuevo_estado = not is_on
        actualizar_lamp_onoff(lamp_id, nuevo_estado)
        if is_on:
            on_button.config(image=off)
            is_on = False
        else:
            on_button.config(image=on)
            is_on = True

def actualizar_lamp_onoff(lamp_id, estado):
    nuevo_estado_lamp = 1 if estado else 0
    conn = mysql.connector.connect(**config_db)
    cursor = conn.cursor()
    consulta_update = """
        UPDATE T_IoTLampV0
        SET LampOnOff = %s
        WHERE LampID = %s
    """
    cursor.execute(consulta_update, (nuevo_estado_lamp, lamp_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Éxito", f"Estado actualizado a {'Encendido' if estado else 'Apagado'}")

# Create A Button
on_button = tk.Button(root, image=on, bd=0, command=switch)
on_button.grid(row=3, column=1, pady=10)


# Botón para actualizar LampOnOff
#boton_actualizar = tk.Button(root, text="Actualizar", command=actualizar_lamp_onoff, bg='#4CAF50', fg='white', font=('Arial', 12))
#boton_actualizar.grid(row=4, column=0, columnspan=3, pady=10)

# Ejecutar la aplicación
root.mainloop()
