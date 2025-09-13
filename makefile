# Nombre del entorno virtual
VENV_NAME = venv

# Directorios
SRC_DIR = app
STATIC_DIR = static
TEMPLATES_DIR = templates

# Nombre de la aplicación de FastAPI
APP_NAME = app.main:app

# Comando para activar el entorno virtual
ACTIVATE_VENV = .$(VENV_NAME)/Scripts/activate

# Comando de instalación de dependencias
INSTALL = pip install -r requirements.txt

# Comando para ejecutar el servidor con uvicorn
RUN_SERVER = uvicorn $(APP_NAME) --reload

# Comando para ejecutar las pruebas (si tienes alguna configuración de pruebas)
TEST = pytest

# Comando para crear el entorno virtual
create-venv:
	python -m venv $(VENV_NAME)

# Instalación de dependencias
install: 
	$(ACTIVATE_VENV) && $(INSTALL)

# Ejecutar el servidor FastAPI
run: 
	$(ACTIVATE_VENV) && $(RUN_SERVER)

# Ejecutar las pruebas
test: 
	$(ACTIVATE_VENV) && $(TEST)

# Limpiar archivos .pyc y .pyo
clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*.pyo" -exec rm -f {} \;

# Generar un nuevo archivo requirements.txt con las dependencias actuales
freeze: 
	$(ACTIVATE_VENV) && pip freeze > requirements.txt

# Si deseas eliminar el entorno virtual
delete-venv:
	rm -rf $(VENV_NAME)

# Recarga el servidor
reload:
	$(ACTIVATE_VENV) && uvicorn $(APP_NAME) --reload

# Comando para inicializar la base de datos (esto depende de tus migraciones)
migrate-db:
	$(ACTIVATE_VENV) && alembic upgrade head

# Comando para crear las tablas iniciales (si estás usando SQLAlchemy)
init-db:
	$(ACTIVATE_VENV) && python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Limpieza y recompilación
rebuild: clean create-venv install
