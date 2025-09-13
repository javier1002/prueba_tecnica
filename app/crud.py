from sqlalchemy.orm import Session
from app import models, schemas

# Lógica para obtener todos los items
def get_items(db: Session):
    return db.query(models.Item).all()

# Lógica para obtener un item por ID
def get_items_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# Lógica para crear un nuevo item
def crear_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        nombre=item.nombre,
        email=item.email,
        descripcion=item.descripcion,
        categoria=item.categoria,
        tipo=item.tipo,
        activo=item.activo,
        
    )
    db.add(db_item)
    db.commit()  # Realiza la acción en la base de datos
    db.refresh(db_item)  # Refresca el objeto para obtener la versión actualizada de la base de datos
    return db_item

# Lógica para actualizar un item
def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = get_items_by_id(db, item_id)
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():  # Solo actualiza los valores que fueron modificados
            setattr(db_item, key, value)
        db.commit()  # Ejecuta el commit solo una vez
        db.refresh(db_item)  # Refresca el objeto actualizado
        return db_item
    return None  # Si no se encuentra el item, retorna None

# Lógica para eliminar un item
def delete_item(db: Session, item_id: int):
    db_item = get_items_by_id(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()  # Elimina el item de la base de datos
        return db_item  # Devuelve el item eliminado
    return None  # Si no se encuentra el item, retorna None
