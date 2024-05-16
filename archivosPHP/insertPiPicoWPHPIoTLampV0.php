<?php
// Configuración de la base de datos
$servername = "localhost"; // Cambia esto si tu servidor MySQL está en otra dirección
$username = "root"; // Cambia esto por tu nombre de usuario MySQL
$password = ""; // Cambia esto por tu contraseña MySQL
$database = "DB_ECOLampV0"; // Cambia esto por el nombre de tu base de datos

// Crear una conexión
$conn = new mysqli($servername, $username, $password, $database);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Verificar si se reciben datos mediante POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Leer el cuerpo de la solicitud POST
    $json_data = file_get_contents('php://input');
    
    // Decodificar los datos JSON
    $data = json_decode($json_data, true);
    
    // Comprobar si la decodificación fue exitosa
    if ($data === null) {
        echo "Error: Datos JSON no válidos.";
    } else {
        // Datos que se reciben desde JSON
        $lampID = isset($data['LampID']) ? $data['LampID'] : '';
        $usuarioID = isset($data['UsuarioID']) ? $data['UsuarioID'] : '';
        $temp_value = isset($data['temp_value']) ? (float) $data['temp_value'] : 0.0;
        $temp_int = isset($data['temp_int']) ? (float) $data['temp_int'] : 0.0;
        $sep_point = isset($data['sep_point']) ? (float) $data['sep_point'] : 0.0;
        $wh_por_hora = isset($data['wh_por_hora']) ? (float) $data['wh_por_hora'] : 0.0;
        $lampOnOff = isset($data['LampOnOff']) ? (int) $data['LampOnOff'] : 0;
        
        // Preparar la declaración SQL
        $stmt = $conn->prepare("INSERT INTO T_ECOLampV0 (LampID, UsuarioID, temp_value, temp_int, sep_point, wh_por_hora, LampOnOff) VALUES (?, ?, ?, ?, ?, ?, ?)");

        // Verificar si la preparación fue exitosa
        if ($stmt) {
            // Vincular los parámetros
            $stmt->bind_param("ssddddd", $lampID, $usuarioID, $temp_value, $temp_int, $sep_point, $wh_por_hora, $lampOnOff);
            
            // Ejecutar la declaración
            if ($stmt->execute()) {
                echo "Nuevo registro insertado con éxito";
            } else {
                echo "Error: " . $stmt->error;
            }

            // Cerrar la declaración
            $stmt->close();
        } else {
            echo "Error: " . $conn->error;
        }
    }
} else {
    echo "Por favor, envía los datos mediante POST en formato JSON.";
}

// Cerrar la conexión
$conn->close();
?>
