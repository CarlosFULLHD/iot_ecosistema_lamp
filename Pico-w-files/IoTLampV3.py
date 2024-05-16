from machine import ADC, Pin
import network
import urequests
import json
import time
import random
from Wifi_lib import wifi_init
from datalog import Sensor

# Configurar pines
led = Pin('LED', Pin.OUT)
foco = Pin(13, Pin.OUT)
btn4 = Pin(19, Pin.IN, Pin.PULL_DOWN)
btn3 = Pin(18, Pin.IN, Pin.PULL_DOWN)
btn2 = Pin(21, Pin.IN, Pin.PULL_DOWN)
btn1 = Pin(20, Pin.IN, Pin.PULL_DOWN)
ledR = Pin(6, Pin.OUT)
ledG = Pin(7, Pin.OUT)
ledB = Pin(8, Pin.OUT)

# Variables globales
RGB = 0
nmed = 100
nmedonoff = True
VlampOnOff = 1

# Inicializar objetos
pinadc = 26  # Pin del LM35
pinsetpoint = 27  # Pin del ADC del setpoint

# Sensor de temperatura
sensores = Sensor(pinadc, pinsetpoint)

# Inicializar conexión Wi-Fi
wifi_init()

# Función para mapear valores
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Función para enviar datos
def handleSubmit():
    global VlampOnOff  # Declarar VlampOnOff como variable global
    ledR.toggle()  # indica se enviara un registro al servidor de DB
    # Leer valores de los sensores
    lamp_id = "lamp1"  # Puedes cambiar este ID según tus necesidades
    slm35 = sensores.ReadTemperature()
    stempint = sensores.TempInt()
    ssetpoint = sensores.Setpoint()
    if VlampOnOff == 1:    # estado apagado
        VlampOnOff = 2     # estado encendido
    else:
        VlampOnOff = 1       # estado apagado
    # Promediar los valores si nmedonoff es verdadero
    if nmedonoff:
        slm35, stempint, ssetpoint = 0, 0, 0
        for _ in range(nmed):
            slm35 += sensores.ReadTemperature()
            stempint += sensores.TempInt()
            ssetpoint += sensores.Setpoint()
        slm35 /= nmed
        stempint /= nmed
        ssetpoint /= nmed
    # Mapear el setpoint
    ssetpoint = map_value(ssetpoint, 0, 65535, 0, 50)
    # Imprimir valores de depuración
    print(f"Lamp_id: {lamp_id},  UsuarioID: {UsuarioID},  LM35 Temp: {slm35}°C, Temp Int: {stempint}°C, SetPoint: {ssetpoint}, LampOnOff: {VlampOnOff}")

    # Realizar la solicitud POST
    url = f"http://192.168.41.196/insertPiPicoWPHPIoTLampV0.php"
    data = {
        'UsuarioID': UsuarioID,
        'LampID': lamp_id,
        'temp_value': slm35,
        'temp_int': stempint,
        'sep_point': ssetpoint,
        'LampOnOff': VlampOnOff
    }
    datos_json = json.dumps(data)
    response = urequests.post(url, data=datos_json, headers={'Content-Type': 'application/json'})
    print(response.text)
    response.close()

    
# URL del script PHP con parámetro LampID
def handleReadAvanzado(lamp_id):
    url = f"http://192.168.41.196/readPiPicoWPHPIoTLampV0regespLampID.php?LampID={lamp_id}"
    # Realizar una solicitud GET a la URL del script PHP con el parámetro LampID
    response = urequests.get(url)
    
    # Verificar el código de estado de la respuesta
    if response.status_code == 200:
        # Leer y decodificar los datos JSON de la respuesta
        ultimo_registro = response.json()
        
        # Imprimir el último registro obtenido
        print("Último registro obtenido para LampID:", lamp_id)
        print(ultimo_registro)
        print("LampOnOff:", ultimo_registro['LampOnOff'])
        print("\n")  # Separador para cada registro
    else:
        print("Error al obtener datos. Código de estado:", response.status_code)
    
    # Cerrar la respuesta
    response.close()
    return int(ultimo_registro['LampOnOff'])

# Función de manejo de interrupciones
def handle_interrupt(pin):
    handleSubmit()

# Configurar interrupción externa en el pin 18
btn4.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

# Bucle principal
estadoFoco=0
while True:
    led.toggle()
    #estadoFoco=handleReadAvanzado()
    #handleSubmit()
    VlampOnOff=estadoFoco
    if VlampOnOff == 1:
        ledB.value(0)
        foco.value(0)
    elif VlampOnOff == 2:
        ledB.value(1)
        foco.value(1)
    time.sleep(1)
