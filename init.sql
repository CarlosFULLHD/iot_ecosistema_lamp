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

-- Datos para pruebas
-- Datos para lamp1 (90% de vida útil, 900 horas)
INSERT INTO T_ECOLampV0 (LampID, UsuarioID, temp_value, temp_int, set_point, wh_por_hora, LampOnOff)
VALUES
('lamp1', 'user1', 22.5, 22, 20, 50, 90), -- 90 horas por registro
('lamp1', 'user1', 22.7, 22, 20, 50, 90),
('lamp1', 'user1', 22.9, 22, 20, 50, 90),
('lamp1', 'user1', 23.0, 23, 20, 50, 90),
('lamp1', 'user1', 23.1, 23, 20, 50, 90),
('lamp1', 'user1', 23.2, 23, 20, 50, 90),
('lamp1', 'user1', 23.3, 23, 20, 50, 90),
('lamp1', 'user1', 23.4, 23, 20, 50, 90),
('lamp1', 'user1', 23.5, 23, 20, 50, 90),
('lamp1', 'user1', 23.6, 23, 20, 50, 90);


-- Datos para lamp2 (50% de vida útil, 500 horas)
INSERT INTO T_ECOLampV0 (LampID, UsuarioID, temp_value, temp_int, set_point, wh_por_hora, LampOnOff)
VALUES
('lamp2', 'user2', 22.5, 22, 20, 50, 50), -- 50 horas por registro
('lamp2', 'user2', 22.7, 22, 20, 50, 50),
('lamp2', 'user2', 22.9, 22, 20, 50, 50),
('lamp2', 'user2', 23.0, 23, 20, 50, 50),
('lamp2', 'user2', 23.1, 23, 20, 50, 50),
('lamp2', 'user2', 23.2, 23, 20, 50, 50),
('lamp2', 'user2', 23.3, 23, 20, 50, 50),
('lamp2', 'user2', 23.4, 23, 20, 50, 50),
('lamp2', 'user2', 23.5, 23, 20, 50, 50),
('lamp2', 'user2', 23.6, 23, 20, 50, 50);
