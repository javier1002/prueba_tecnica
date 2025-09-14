# CRUD con FastAPI y MySQL

Este es un ejemplo de un CRUD utilizando **FastAPI** como framework web, **SQLAlchemy** para la manipulación de bases de datos y **MySQL** como sistema de gestión de bases de datos.

## Requisitos

- **Python 3.11**
- **MySQL** (asegúrate de tener MySQL instalado y en funcionamiento)

## Pasos para la configuración

### 1. Crear entorno virtual

Primero, crea un entorno virtual para gestionar las dependencias de Python:

```bash
python -m venv venv

#activar entorno virtual 
venv\Scripts\activate
#instalacion de dependencias
pip install fastapi
pip install uvicorn[standard]
pip install sqlalchemy
pip install pymysql
pip install python-multipart
pip install jinja2
pip install pydantic


#creacion de base de datos
CREATE DATABASE fastapi_db;
#conexion
DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/fastapi_db"

#creacion de tablas
from app.database import engine
from app import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

#iniciar servidor
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
#para recargar
uvicorn app.main:app --reload

#tabla empleados
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- nombre (VARCHAR(100), NOT NULL)
- email (VARCHAR(100), NOT NULL, UNIQUE)
- descripcion (TEXT)
- sexo (ENUM: 'Masculino', 'Femenino')
- area (ENUM: 'Administración', 'Contable', 'Archivo')
- roles (TEXT, JSON format)
- activo (BOOLEAN, DEFAULT TRUE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)