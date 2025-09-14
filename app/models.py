from sqlalchemy import Column, Integer, String, Boolean, Text, Enum,JSON
from app.database import Base
import enum

class TipoEnum(str, enum.Enum):
    opcion1 = "Masculino"
    opcion2 = "Femenino"

class Item(Base):
    __tablename__ = "items"
    id= Column(Integer, primary_key=True, index=True)
    nombre= Column(String(255), nullable=False)
    email= Column(String(255), unique=True, nullable=False) 
    descripcion= Column(Text, nullable=True)
    sexo= Column(String(50),nullable=True)
    area= Column(String(TipoEnum),nullable=True)
    roles = Column(Text,nullable=False)
    activo= Column(Boolean, default=True)
    

