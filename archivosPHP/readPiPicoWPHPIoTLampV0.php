<!-- readPiPicoWPHPIoTLampV0.php -->
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
// Consulta SQL para leer datos de la tabla tbl_temp
$sql = "SELECT * FROM T_ECOLampV0";
// Ejecutar la consulta SQL
$result = $conn->query($sql);
// Verificar si hay resultados
if ($result->num_rows > 0) {
    // Crear un array para almacenar los resultados
    $data = array();
    // Recorrer los resultados y agregarlos al array
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    // Devolver los datos como JSON
    echo json_encode($data);
} else {
    echo json_encode(array("message" => "No se encontraron registros."));
}
// Cerrar la conexión
$conn->close();
?>