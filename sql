CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    nombre VARCHAR(100) NOT NULL,               
    email VARCHAR(100) NOT NULL UNIQUE,         
    descripcion TEXT,                          
    sexo ENUM('Masculino', 'Femenino') NOT NULL, 
    area ENUM('Administración', 'Contable', 'Archivo') NOT NULL, 
    roles VARCHAR(255),                         
    activo BOOLEAN DEFAULT TRUE,                
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
);