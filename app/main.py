from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal, Base

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
    items = crud.get_items(db)  # Obtiene todos los items de la base de datos
    return templates.TemplateResponse("list.html", {"request": request, "items": items})

# Endpoint para mostrar el formulario de creación de items
@app.get("/create", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Endpoint para crear un nuevo item
@app.post("/items/")
async def crear_item(
    nombre: str = Form(...),
    email : str = Form(...),
    descripcion: str = Form(""),
    sexo: str = Form(""),
    tipo: str = Form(...),
    activo: bool = Form(False),
    db: Session = Depends(get_db)
):
    item = schemas.ItemCreate(nombre=nombre, descripcion=descripcion, sexo=sexo, tipo=tipo, activo=activo)
    crud.crear_item(db, item)
    return RedirectResponse("/", status_code=303)  # Redirige a la lista de items después de crear

# Endpoint para mostrar el formulario de edición de un item
@app.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def editar_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = crud.get_items_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return templates.TemplateResponse("editar_item.html", {"request": request, "item": item})

# Endpoint para actualizar un item (usamos POST para simular PUT)
@app.post("/items/{item_id}/edit")
async def actualizar_item(
    item_id: int, 
    nombre: str = Form(...),
    descripcion: str = Form(""),
    categoria: str = Form(""),
    tipo: str = Form(...),
    activo: bool = Form(False),
    db: Session = Depends(get_db)
):
    item = schemas.ItemUpdate(nombre=nombre, descripcion=descripcion, categoria=categoria, tipo=tipo, activo=activo)
    updated_item = crud.update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return RedirectResponse("/", status_code=303)  # Redirige a la lista de items después de la actualización

# Endpoint para eliminar un item (simulando DELETE con un POST)
@app.post("/items/{item_id}/delete")
async def eliminar_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return RedirectResponse("/", status_code=303)  # Redirige a la lista de items después de eliminar
