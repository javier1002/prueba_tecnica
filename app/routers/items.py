from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter()
#Jinja es un motor de plantillas web para el lenguaje de programación Python
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
      yield db
    finally:
      print(' finished')
      db.close()

@router.get("/items/", response_model=list[schemas.ItemOut])
def listar_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@router.get("/items/", response_class=HTMLResponse)

def listar_items(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return templates.TemplateResponse("items/list.html", {"request": request, "items": items})

@router.post("/items/create", response_class=HTMLResponse)
def create_item(nombre: str = Form(...), descripcion: str = Form(""), email: str=Form(""), sexo: str = Form(""), roles:str = Form(...), area:str = Form(...), activo: bool = Form(False), db: Session = Depends(get_db)):
    item = schemas.ItemCreate(nombre=nombre, descripcion=descripcion, email=email, sexo=sexo, area=area, activo=activo, roles=roles.split(","))
    crud.create_item(db, item)
    return RedirectResponse("/", status_code=303)               