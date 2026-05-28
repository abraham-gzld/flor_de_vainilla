from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.extra import Extra

from backend.schemas.extra_schema import extraCreate
from backend.schemas.extra_schema import extraResponse


router = APIRouter(
    prefix="/extras",
    tags=["Extras"]
)


@router.post("/", response_model=extraResponse)
def create_extra(
    extra: extraCreate,
    db: Session = Depends(get_db)
):

    new_extra = Extra(
        name=extra.name,
        price_extra=extra.price_extra
    )

    db.add(new_extra)

    db.commit()

    db.refresh(new_extra)

    return new_extra


@router.get("/", response_model=list[extraResponse])
def get_extras(
    db: Session = Depends(get_db)
):

    extras = db.query(Extra).all()

    return extras

@router.get("/{extra_id}", response_model=extraResponse)
def get_extra(
    extra_id: int,
    db: Session = Depends(get_db)
):

    extra = db.query(Extra).filter(
        Extra.extra_id == extra_id
    ).first()

    if not extra:

        raise HTTPException(
            status_code=404,
            detail="Extra not found"
        )

    return extra

@router.put("/{extra_id}", response_model=extraResponse)
def update_extra(
    extra_id: int,
    extra_data: extraCreate,
    db: Session = Depends(get_db)
):

    extra = db.query(Extra).filter(
        Extra.extra_id == extra_id
    ).first()

    if not extra:

        raise HTTPException(
            status_code=404,
            detail="Extra not found"
        )

    extra.name = extra_data.name
    extra.price_extra = extra_data.price_extra

    db.commit()

    db.refresh(extra)

    return extra


@router.delete("/{extra_id}")
def delete_extra(
    extra_id: int,
    db: Session = Depends(get_db)
):

    extra = db.query(Extra).filter(
        Extra.extra_id == extra_id
    ).first()

    if not extra:

        raise HTTPException(
            status_code=404,
            detail="Extra not found"
        )

    db.delete(extra)

    db.commit()

    return {
        "message": "Extra deleted successfully"
    }