CREATE DATABASE IF NOT EXISTS
DB_ECOLampV0;
USE DB_ECOLampV0;

CREATE TABLE T_ECOLampV0 (
Nreg INT AUTO_INCREMENT PRIMARY KEY,
LampID VARCHAR(50) NOT NULL,
UsuarioID VARCHAR(50) NOT NULL,
fecha_creacion TIMESTAMP DEFAULT
CURRENT_TIMESTAMP,
temp_value FLOAT NOT NULL,
temp_int INT NOT NULL,
set_point INT NOT NULL,
wh_por_hora FLOAT NOT NULL,
LampOnOff INT NOT NULL);