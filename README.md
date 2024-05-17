# Proyecto IoT para Monitoreo y Control de Lámparas

### Integrantes:

- Rosario Calisaya
- Natalia Gutierrez
- Carlos Nina
- Bernardo Duran
- Jhousef Silva
- Omar Rodriguez

## Objetivo del Proyecto

El objetivo de este proyecto es desarrollar un sistema IoT para el monitoreo y control de lámparas, utilizando una Raspberry Pi Pico W. El sistema permite insertar, leer y visualizar datos de las lámparas, además de generar gráficos y análisis sobre el consumo energético y la vida útil de las mismas.

## Estructura del Proyecto

### Archivos Principales

- **insertPiPicoWPHPIoTLampV0.php**: Archivo PHP para insertar datos en la base de datos.
- **readPiPicoWPHPIoTLampV0.php**: Archivo PHP para leer todos los datos de la base de datos.
- **readPiPicoWPHPIoTLampV0regespLampID.php**: Archivo PHP para leer datos específicos de una lámpara basados en su ID.
- **datalog.py**: Script Python para generar gráficos y análisis de datos de la base de datos.
- **IoTLampV3.py**: Script Python para enviar datos simulados desde la Raspberry Pi Pico W al servidor.
- **secrets.py**: Archivo Python que contiene las credenciales de la red WiFi y la dirección IP del servidor.
- **Wifi_lib.py**: Librería Python para manejar la conexión WiFi y la comunicación con el servidor.
- **PCCambioEstadoLampOnOffGrafV0 (1).py**: Script Python para generar un gráfico de la relación entre la fecha de creación y el estado de encendido/apagado de la lámpara.
- **init.sql**: Script SQL para crear la base de datos y la tabla necesaria.

### Base de Datos

La base de datos se llama `DB_ECOLampV0` y contiene una tabla `T_ECOLampV0` con los siguientes campos:

- `Nreg`: Número de registro (clave primaria, autoincremental).
- `LampID`: ID de la lámpara.
- `UsuarioID`: ID del usuario.
- `fecha_creacion`: Fecha y hora de creación del registro.
- `temp_value`: Valor de temperatura.
- `temp_int`: Valor entero de temperatura.
- `sep_point`: Punto de separación.
- `LampOnOff`: Estado de la lámpara (encendido/apagado).
- `wh_por_hora`: Consumo en watts por hora.

### Funcionalidades

- **Insertar Datos**: Inserta datos de las lámparas en la base de datos a través del archivo PHP `insertPiPicoWPHPIoTLampV0.php`.
- **Leer Datos**: Lee todos los datos de la tabla a través del archivo PHP `readPiPicoWPHPIoTLampV0.php`.
- **Leer Datos por LampID**: Lee datos específicos de una lámpara basados en su ID a través del archivo PHP `readPiPicoWPHPIoTLampV0regespLampID.php`.
- **Generar Gráficos**: Genera gráficos y análisis de datos usando los scripts Python `datalog.py` y `PCCambioEstadoLampOnOffGrafV0 (1).py`.
- **Enviar Datos Simulados**: Envía datos simulados desde la Raspberry Pi Pico W al servidor utilizando el script `IoTLampV3.py`.

### Instalación y Configuración

1. **Configurar la Base de Datos**: Ejecutar el script `init.sql` para crear la base de datos y la tabla necesaria.

   ```sql
   CREATE DATABASE IF NOT EXISTS DB_ECOLampV0;
   USE DB_ECOLampV0;

   CREATE TABLE T_ECOLampV0 (
       Nreg INT AUTO_INCREMENT PRIMARY KEY,
       LampID VARCHAR(50) NOT NULL,
       UsuarioID VARCHAR(50) NOT NULL,
       fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       temp_value FLOAT NOT NULL,
       temp_int INT NOT NULL,
       sep_point INT NOT NULL,
       wh_por_hora FLOAT NOT NULL,
       LampOnOff INT NOT NULL
   );
   ```
