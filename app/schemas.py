from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Item(BaseModel):
    nombre: str  
    email: EmailStr | None = None  
    descripcion: str | None = None
    sexo: str | None = None
    area: str | None = None
    roles: List[str]
    activo: bool = True
    


class ItemCreate(Item):  
    pass  


class ItemInDB(Item):
    id: int  # autoincrementaen la DB

#
class ItemUpdate(BaseModel):  
    nombre: str | None = None
    email: EmailStr | None = None  
    descripcion: str | None = None
    sexo: str | None = None
    area: str | None = None
    roles: List[str]
    activo: bool | None = None
    


class ItemOut(Item):
    id: int  # Agregar el ID para que sea retornado en la respuesta

    class Config:
        from_attributes = True  # Permite trabajar con objetos ORM de SQLAlchemy (convertir de la DB al modelo Pydantic)
