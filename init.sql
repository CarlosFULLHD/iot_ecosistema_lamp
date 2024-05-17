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
sep_point INT NOT NULL,
wh_por_hora FLOAT NOT NULL,
LampOnOff INT NOT NULL);

-- Datos para pruebas
INSERT INTO `t_ecolampv0` (`Nreg`, `LampID`, `UsuarioID`, `fecha_creacion`, `temp_value`, `temp_int`, `sep_point`, `wh_por_hora`, `LampOnOff`) VALUES
(1, 'lamp1', 'user1', '2024-05-16 22:27:53', 22.5, 22, 20, 0.5, 1),
(2, 'lamp2', 'user2', '2024-05-16 22:27:53', 23, 23, 21, 0.6, 2),
(3, 'lamp1', 'user1', '2024-05-16 22:27:53', 22.8, 22, 20, 0.5, 1),
(4, 'lamp2', 'user2', '2024-05-16 22:27:53', 23.2, 23, 21, 0.6, 2),
(5, 'lamp1', 'user1', '2024-05-16 22:27:53', 23.1, 22, 20, 0.5, 2),
(6, 'lamp2', 'user2', '2024-05-16 22:27:53', 24, 23, 21, 0.6, 1),
(7, 'lamp1', 'user1', '2024-05-16 22:27:53', 22.9, 22, 20, 0.5, 1),
(8, 'lamp2', 'user2', '2024-05-16 22:27:53', 23.5, 23, 21, 0.6, 2),
(9, 'lamp3', 'user3', '2024-05-16 22:27:53', 21.5, 21, 19, 0.4, 1),
(10, 'lamp3', 'user3', '2024-05-16 22:27:53', 21.8, 21, 19, 0.4, 1),
(11, 'lamp3', 'user3', '2024-05-16 22:27:53', 22.1, 21, 19, 0.4, 2),
(12, 'lamp3', 'user3', '2024-05-16 22:27:53', 22.3, 21, 19, 0.4, 1),
(13, 'lamp3', 'user3', '2024-05-16 22:27:53', 22.7, 21, 19, 0.4, 2),
(14, 'lamp3', 'user3', '2024-05-16 22:27:53', 23, 21, 19, 0.4, 1),
(15, 'lamp1', 'user4', '2024-05-16 22:27:53', 20, 20, 18, 0.3, 2),
(16, 'lamp2', 'user4', '2024-05-16 22:27:53', 20.5, 20, 18, 0.3, 2),
(17, 'lamp3', 'user4', '2024-05-16 22:27:53', 21, 20, 18, 0.3, 1),
(18, 'lamp1', 'user4', '2024-05-16 22:27:53', 21.5, 20, 18, 0.3, 1),
(19, 'lamp2', 'user4', '2024-05-16 22:27:53', 22, 20, 18, 0.3, 1),
(20, 'lamp3', 'user4', '2024-05-16 22:27:53', 22.5, 20, 18, 0.3, 2);

-- Registros para lamp1 con wh_por_hora corregido a 0.5
INSERT INTO `t_ecolampv0` (`Nreg`, `LampID`, `UsuarioID`, `fecha_creacion`, `temp_value`, `temp_int`, `sep_point`, `wh_por_hora`, `LampOnOff`) VALUES
(21, 'lamp1', 'user1', '2024-05-17 03:28:03', 22.5, 22, 20, 90, 2),
(22, 'lamp1', 'user1', '2024-05-17 03:28:03', 22.7, 22, 20,90, 2),
(23, 'lamp1', 'user1', '2024-05-17 03:28:03', 22.9, 22, 20, 90, 2),
(24, 'lamp1', 'user1', '2024-05-17 03:28:03', 23, 23, 20, 90, 2),
(25, 'lamp1', 'user1', '2024-05-17 03:28:03', 23.1, 23, 20, 90, 2),
(26, 'lamp1', 'user1', '2024-05-17 03:28:03', 23.2, 23, 20,90, 2),
(27, 'lamp1', 'user1', '2024-05-17 03:28:03', 23.3, 23, 20, 90, 2),
(28, 'lamp1', 'user1', '2024-05-17 03:28:03', 23.4, 23, 20,90, 2),
(29, 'lamp1', 'user1', '2024-05-17 03:28:03', 23.5, 23, 20, 90, 2),
(30, 'lamp1', 'user1', '2024-05-17 03:28:03', 23.6, 23, 20, 90,2);

-- Registros para lamp2 con wh_por_hora corregido a 0.6
INSERT INTO `t_ecolampv0` (`Nreg`, `LampID`, `UsuarioID`, `fecha_creacion`, `temp_value`, `temp_int`, `sep_point`, `wh_por_hora`, `LampOnOff`) VALUES
(31, 'lamp2', 'user2', '2024-05-17 03:28:03', 22.5, 22, 20,90, 2),
(32, 'lamp2', 'user2', '2024-05-17 03:28:03', 22.7, 22, 20, 90, 2),
(33, 'lamp2', 'user2', '2024-05-17 03:28:03', 22.9, 22, 20, 90, 2),
(34, 'lamp2', 'user2', '2024-05-17 03:28:03', 23, 23, 20, 90, 2),
(35, 'lamp2', 'user2', '2024-05-17 03:28:03', 23.1, 23, 20,90, 2),
(36, 'lamp2', 'user2', '2024-05-17 03:28:03', 23.2, 23, 20, 90, 2),
(37, 'lamp2', 'user2', '2024-05-17 03:28:03', 23.3, 23, 20, 90, 2),
(38, 'lamp2', 'user2', '2024-05-17 03:28:03', 23.4, 23, 20, 90, 2),
(39, 'lamp2', 'user2', '2024-05-17 03:28:03', 23.5, 23, 20, 90, 2),
(40, 'lamp2', 'user2', '2024-05-17 03:28:03', 23.6, 23, 20, 90, 2);
