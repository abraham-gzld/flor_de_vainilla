from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.size import Size

from backend.schemas.size_schema import (
    SizeCreate,
    SizeResponse
)

router = APIRouter(
    prefix="/sizes",
    tags=["Sizes"]
)

@router.post("/", response_model=SizeResponse)
def create_size(
    size: SizeCreate,
    db: Session = Depends(get_db)
):

    existing_size = db.query(Size).filter(
        Size.name == size.name
    ).first()

    if existing_size:

        raise HTTPException(
            status_code=400,
            detail="Size already exists"
        )

    new_size = Size(
        name=size.name,
        price_extra=size.price_extra
    )

    db.add(new_size)

    db.commit()

    db.refresh(new_size)

    return new_size


# =========================
# GET ALL SIZES
# =========================
@router.get("/", response_model=list[SizeResponse])
def get_sizes(
    db: Session = Depends(get_db)
):

    sizes = db.query(Size).all()

    return sizes

@router.get("/{size_id}", response_model=SizeResponse)
def get_size(
    size_id: int,
    db: Session = Depends(get_db)
):

    size = db.query(Size).filter(
        Size.size_id == size_id
    ).first()

    if not size:

        raise HTTPException(
            status_code=404,
            detail="Size not found"
        )

    return size

@router.put("/{size_id}", response_model=SizeResponse)
def update_size(
    size_id: int,
    size_data: SizeCreate,
    db: Session = Depends(get_db)
):

    size = db.query(Size).filter(
        Size.size_id == size_id
    ).first()

    if not size:

        raise HTTPException(
            status_code=404,
            detail="Size not found"
        )

    size.name = size_data.name
    size.price_extra = size_data.price_extra

    db.commit()

    db.refresh(size)

    return size

@router.delete("/{size_id}")
def delete_size(
    size_id: int,
    db: Session = Depends(get_db)
):

    size = db.query(Size).filter(
        Size.size_id == size_id
    ).first()

    if not size:

        raise HTTPException(
            status_code=404,
            detail="Size not found"
        )

    db.delete(size)

    db.commit()

    return {
        "message": "Size deleted successfully"
    }