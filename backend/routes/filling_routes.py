from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.filling import Filling

from backend.schemas.filling_schema import fillingCreate
from backend.schemas.filling_schema import fillingResponse


router = APIRouter(
    prefix="/fillings",
    tags=["Fillings"]
)


@router.post("/", response_model=fillingResponse)
def create_filling(
    filling: fillingCreate,
    db: Session = Depends(get_db)
):

    new_filling = Filling(
        name=filling.name,
        price_extra=filling.price_extra
    )

    db.add(new_filling)

    db.commit()

    db.refresh(new_filling)

    return new_filling


@router.get("/", response_model=list[fillingResponse])
def get_filling(
    db: Session = Depends(get_db)
):

    filling = db.query(Filling).all()

    return filling

@router.get("/{filling_id}", response_model=fillingResponse)
def get_filling(
    filling_id: int,
    db: Session = Depends(get_db)
):

    filling = db.query(Filling).filter(
        Filling.filling_id == filling_id
    ).first()

    if not filling:

        raise HTTPException(
            status_code=404,
            detail="Filling not found"
        )

    return filling


@router.put("/{filling_id}", response_model=fillingResponse)
def update_flavor(
    filling_id: int,
    filling_data: fillingCreate,
    db: Session = Depends(get_db)
):

    filling = db.query(Filling).filter(
        Filling.filling_id == filling_id
    ).first()

    if not filling:

        raise HTTPException(
            status_code=404,
            detail="Filling not found"
        )

    filling.name = filling_data.name
    filling.price_extra = filling_data.price_extra

    db.commit()

    db.refresh(filling)

    return filling


@router.delete("/{filling_id}")
def delete_flavor(
    filling_id: int,
    db: Session = Depends(get_db)
):

    filling = db.query(Filling).filter(
        Filling.filling_id == filling_id
    ).first()

    if not filling:

        raise HTTPException(
            status_code=404,
            detail="Filling not found"
        )

    db.delete(filling)

    db.commit()

    return {
        "message": "Filling deleted successfully"
    }