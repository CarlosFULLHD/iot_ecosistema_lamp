from machine import ADC, Pin
import network
import urequests
import json
import time
from Wifi_lib import wifi_init
from datalog import Sensor

# Configurar pines
led = Pin('LED', Pin.OUT)
ledB = Pin(12, Pin.OUT)
btn4 = Pin(21, Pin.IN, Pin.PULL_DOWN)
btn3 = Pin(20, Pin.IN, Pin.PULL_DOWN)
btn2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
btn1 = Pin(18, Pin.IN, Pin.PULL_DOWN)
ledR = Pin(6, Pin.OUT)
ledG = Pin(7, Pin.OUT)
foco = Pin(10, Pin.OUT)
# foco = Pin(8, Pin.OUT)

# Variables globales
RGB = 0
nmed = 100
nmedonoff = True
VlampOnOff = 1
potencia_lampara = 10  # Potencia de la lámpara en vatios (W)
tiempo_inicio = time.time()  # Registrar el tiempo de inicio

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

# Función para calcular el consumo energético


def calcular_consumo(tiempo_inicio, potencia_lampara):
    tiempo_actual = time.time()
    tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / \
        3600  # Convertir segundos a horas
    consumo_wh = potencia_lampara * tiempo_transcurrido
    consumo_kwh = consumo_wh / 1000
    return consumo_kwh

# Función para enviar datos


def handleSubmit():
    # Declarar VlampOnOff y tiempo_inicio como variables globales
    global VlampOnOff, tiempo_inicio
    ledR.toggle()  # Indica que se enviará un registro al servidor de DB

    # Leer valores de los sensores
    lamp_id = "lamp1"  # Puedes cambiar este ID según tus necesidades
    usuario_id = "user1"  # Cambia esto al ID del usuario
    slm35 = sensores.ReadTemperature()
    stempint = sensores.TempInt()
    ssetpoint = sensores.Setpoint()

    # Calcular consumo energético
    consumo_kwh = calcular_consumo(tiempo_inicio, potencia_lampara)

    if VlampOnOff == 1:  # estado apagado
        VlampOnOff = 2  # estado encendido
    else:
        VlampOnOff = 1  # estado apagado

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
    print(f"Lamp_id: {lamp_id}, Usuario_id: {usuario_id}, LM35 Temp: {slm35}°C, Temp Int: {
          stempint}°C, SetPoint: {ssetpoint}, Consumo kWh: {consumo_kwh}, LampOnOff: {VlampOnOff}")

    # Realizar la solicitud POST
    url = "http://192.168.91.184/insertPiPicoWPHPIoTLampV0.php"
    data = {
        'LampID': lamp_id,
        'UsuarioID': usuario_id,
        'temp_value': slm35,
        'temp_int': stempint,
        'sep_point': ssetpoint,
        'wh_por_hora': consumo_kwh * 1000,  # Convertir kWh a Wh
        'LampOnOff': VlampOnOff
    }
    datos_json = json.dumps(data)
    response = urequests.post(url, data=datos_json, headers={
                              'Content-Type': 'application/json'})
    print(response.text)
    response.close()

# URL del script PHP con parámetro LampID y UsuarioID


def handleReadAvanzado():
    lamp_id = "lamp1"  # Cambia esto al LampID que deseas consultar
    usuario_id = "user1"  # Cambia esto al UsuarioID que deseas consultar
    url = f"http://192.168.91.184/readPiPicoWPHPIoTLampV0regespLampID.php?LampID={
        lamp_id}&UsuarioID={usuario_id}"
    # Realizar una solicitud GET a la URL del script PHP con el parámetro LampID y UsuarioID
    response = urequests.get(url)

    # Verificar el código de estado de la respuesta
    if response.status_code == 200:
        # Leer y decodificar los datos JSON de la respuesta
        ultimo_registro = response.json()
        # Imprimir el último registro obtenido
        print("Último registro obtenido para LampID y UsuarioID:",
              lamp_id, usuario_id)
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
estadoFoco = 0
while True:
    led.toggle()
    # estadoFoco = handleSubmit()  # subiendo datos
    estadoFoco = handleReadAvanzado()
    VlampOnOff = estadoFoco
    if VlampOnOff == 1:
        ledB.value(0)
        foco.value(0)
    elif VlampOnOff == 2:
        ledB.value(1)
        foco.value(1)
    time.sleep(1)
