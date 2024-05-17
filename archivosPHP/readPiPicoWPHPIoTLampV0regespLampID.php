<!-- readPiPicoWPHPIoTLampV0regespLampID.php -->
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

// Verificar si se ha recibido el parámetro LampID y UsuarioID en la solicitud GET
if (isset($_GET['LampID']) && isset($_GET['UsuarioID'])) {
    $lampID = $conn->real_escape_string($_GET['LampID']);
    $usuarioID = $conn->real_escape_string($_GET['UsuarioID']);
    
    // Consulta SQL para obtener el último registro basado en LampID y UsuarioID
    $sql = "SELECT * FROM T_ECOLampV0 WHERE LampID = '$lampID' AND UsuarioID = '$usuarioID' ORDER BY fecha_creacion DESC LIMIT 1";
    $result = $conn->query($sql);

    // Crear un array para almacenar los resultados
    $datos = array();

    // Verificar si hay resultados
    if ($result->num_rows > 0) {
        // Obtener el último registro y agregarlo al array
        $row = $result->fetch_assoc();
        $datos = $row;
    } else {
        $datos["error"] = "No se encontraron registros para LampID y UsuarioID proporcionados";
    }

    // Cerrar la conexión a la base de datos
    $conn->close();

    // Devolver los datos en formato JSON
    header('Content-Type: application/json');
    echo json_encode($datos);
} else {
    echo json_encode(["error" => "LampID y/o UsuarioID no proporcionado(s) en la solicitud"]);
}
?>
