CREATE TABLE items(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    Correo TEXT,
    sexo ENUM('tipo1', 'tipo2'),
    area VARCHAR(100),
    descripcion VARCHAR(100),
    tipo ENUM('tipo1', 'tipo2'),
   
    activo BOOLEAN DEFAULT TRUE,
);