from pydantic import BaseModel, EmailStr

class Item(BaseModel):
    nombre: str  # Campo obligatorio
    email: EmailStr | None = None  
    descripcion: str | None = None
    categoria: str | None = None
    tipo: str | None = None
    activo: bool = True
    


class ItemCreate(Item):  
    pass  


class ItemInDB(Item):
    id: int  # Esto agrega el campo id que será autoincrementado en la DB

#
class ItemUpdate(BaseModel):  
    nombre: str | None = None
    email: EmailStr | None = None  
    descripcion: str | None = None
    categoria: str | None = None
    tipo: str | None = None
    activo: bool | None = None
    


class ItemOut(Item):
    id: int  # Agregar el ID para que sea retornado en la respuesta

    class Config:
        from_attributes = True  # Permite trabajar con objetos ORM de SQLAlchemy (convertir de la DB al modelo Pydantic)
