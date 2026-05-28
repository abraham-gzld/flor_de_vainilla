from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.decoration import Decoration

from backend.schemas.decoration_schema import decorationCreate
from backend.schemas.decoration_schema import decorationResponse


router = APIRouter(
    prefix="/decorations",
    tags=["Decorations"]
)


@router.post("/", response_model=decorationResponse)
def create_decoration(
    decoration: decorationCreate,
    db: Session = Depends(get_db)
):

    new_decoration = Decoration(
        name=decoration.name,
        price_extra=decoration.price_extra
    )

    db.add(new_decoration)

    db.commit()

    db.refresh(new_decoration)

    return new_decoration


@router.get("/", response_model=list[decorationResponse])
def get_decorations(
    db: Session = Depends(get_db)
):

    decorations = db.query(Decoration).all()

    return decorations

@router.get("/{decoration_id}", response_model=decorationResponse)
def get_decoration(
    decoration_id: int,
    db: Session = Depends(get_db)
):

    decoration = db.query(Decoration).filter(
        Decoration.decoration_id == decoration_id
    ).first()

    if not decoration:

        raise HTTPException(
            status_code=404,
            detail="Decoration not found"
        )

    return decoration


@router.put("/{decoration_id}", response_model=decorationResponse)
def update_decoration(
    decoration_id: int,
    decoration_data: decorationCreate,
    db: Session = Depends(get_db)
):

    decoration = db.query(Decoration).filter(
        Decoration.decoration_id == decoration_id
    ).first()

    if not decoration:

        raise HTTPException(
            status_code=404,
            detail="Decoration not found"
        )

    decoration.name = decoration_data.name
    decoration.price_extra = decoration_data.price_extra

    db.commit()

    db.refresh(decoration)

    return decoration


@router.delete("/{decoration_id}")
def delete_decoration(
    decoration_id: int,
    db: Session = Depends(get_db)
):

    decoration = db.query(Decoration).filter(
        Decoration.decoration_id == decoration_id
    ).first()

    if not decoration:

        raise HTTPException(
            status_code=404,
            detail="Decoration not found"
        )

    db.delete(decoration)

    db.commit()

    return {
        "message": "Decoration deleted successfully"
    }