from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import materials_service
from app.schemas.material import Material as MaterialSchema
from app.schemas.material import MaterialCreate, MaterialUpdate

router = APIRouter()


@router.get("", response_model=list[MaterialSchema])
def list_materials(db: Session = Depends(get_database_session)):
    return materials_service.list_materials(db)


@router.post("", response_model=MaterialSchema, status_code=201)
def create_material(payload: MaterialCreate, db: Session = Depends(get_database_session)):
    return materials_service.create_material(db, payload)


@router.get("/{material_id}", response_model=MaterialSchema)
def get_material(material_id: int, db: Session = Depends(get_database_session)):
    return materials_service.get_material(db, material_id)


@router.patch("/{material_id}", response_model=MaterialSchema)
def update_material(
    material_id: int,
    payload: MaterialUpdate,
    db: Session = Depends(get_database_session),
):
    return materials_service.update_material(db, material_id, payload)

@router.delete("/{material_id}", status_code=204)
def delete_material(material_id: int, db: Session = Depends(get_database_session)): 
    materials_service.delete_material(db, material_id)
    return None