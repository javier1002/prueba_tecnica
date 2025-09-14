from sqlalchemy.orm import Session
from app import models, schemas
import json

# Lógica para obtener todos los items
def get_items(db: Session):
    return db.query(models.Item).all()

# Lógica para obtener un item por ID
def get_items_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# Lógica para crear un nuevo item
def crear_item(db: Session, item: schemas.ItemCreate):
    roles_str = json.dumps(item.roles) if isinstance(item.roles, list) else item.roles
    db_item = models.Item(
        nombre=item.nombre,
        email=item.email,
        descripcion=item.descripcion,
        sexo=item.sexo,
        area=item.area,
        roles=roles_str,
        activo=item.activo,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Lógica para actualizar un item
def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = get_items_by_id(db, item_id)
    if db_item:
        item_dict = item.dict(exclude_unset=True)
        
        for key, value in item_dict.items():
            if key == 'roles' and isinstance(value, list):
                # Convertir la lista de roles a JSON string
                setattr(db_item, key, json.dumps(value))
            else:
                setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

# Lógica para eliminar un item
def delete_item(db: Session, item_id: int):
    db_item = get_items_by_id(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None