from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal, Base
from typing import List
import re
import json

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicialización de FastAPI
app = FastAPI()

# Configurar el sistema de plantillas
templates = Jinja2Templates(directory="app/templates")

# Montar los archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redirigir la ruta raíz a la lista de items
@app.get("/", response_class=RedirectResponse)
async def redirect_to_list():
    return RedirectResponse("/list")

# Endpoint para listar los items en formato HTML (con tabla)
@app.get("/list", response_class=HTMLResponse)
async def listar_items_html(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    
    # Deserializar roles para cada item para mostrarlos correctamente
    for item in items:
        if item.roles and isinstance(item.roles, str):
            try:
                item.roles = json.loads(item.roles)
            except:
                item.roles = []
    
    return templates.TemplateResponse("list.html", {"request": request, "items": items})

# Endpoint para mostrar el formulario de creación de items
@app.get("/create", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Función para validar el nombre
def validar_nombre(nombre: str):
    # Expresión regular para solo letras y espacios
    nombre_regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
    if not re.match(nombre_regex, nombre):
        raise ValueError("El nombre solo puede contener letras y espacios.")

# Endpoint para crear un nuevo item
@app.post("/items/")
async def crear_item(
    nombre: str = Form(...),
    email: str = Form(...),
    descripcion: str = Form(""),
    sexo: str = Form(""),
    area: str = Form(...),
    activo: bool = Form(False),
    roles: List[str] = Form([]),  
    db: Session = Depends(get_db)
):
    try:
        validar_nombre(nombre)  # Validación del nombre
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    item = schemas.ItemCreate(
        nombre=nombre,
        email=email,
        descripcion=descripcion,
        sexo=sexo,
        area=area,
        activo=activo,
        roles=roles  
    )
    crud.crear_item(db, item)
    return RedirectResponse("/", status_code=303)

# Endpoint para mostrar el formulario de edición de un item
@app.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def editar_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = crud.get_items_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    
    if item.roles and isinstance(item.roles, str):
        try:
            item.roles = json.loads(item.roles)
        except:
            item.roles = []
    
    return templates.TemplateResponse("editar_item.html", {"request": request, "item": item})

# Función para actualizar un item
@app.post("/items/{item_id}/edit")
async def actualizar_item(
    item_id: int, 
    nombre: str = Form(...),
    email: str = Form(...),
    descripcion: str = Form(""),
    sexo: str = Form(""),
    area: str = Form(...),
    activo: bool = Form(False),
    roles: List[str] = Form([]),  
    db: Session = Depends(get_db)
):
    try:
        validar_nombre(nombre)  
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    item = schemas.ItemUpdate(
        nombre=nombre,
        email=email,
        descripcion=descripcion,
        sexo=sexo,
        area=area,
        activo=activo,
        roles=roles
    )
    
    updated_item = crud.update_item(db, item_id, item)
    
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    return RedirectResponse("/list", status_code=303)

# Endpoint para eliminar un item (simulando DELETE con un POST)
@app.post("/items/{item_id}/delete")
async def eliminar_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_items_by_id(db, item_id)
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    crud.delete_item(db, item_id)
    
    return RedirectResponse("/list", status_code=303)