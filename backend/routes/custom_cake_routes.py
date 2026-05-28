from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.custom_cake import CustomCake
from backend.models.detail_quotation import DetailQuotation
from backend.models.size import Size
from backend.models.flavor import Flavor
from backend.models.filling import Filling
from backend.models.decoration import Decoration

from backend.schemas.custom_cake_schema import (
    customCakeCreate,
    customCakeResponse
)

router = APIRouter(
    prefix="/custom-cakes",
    tags=["Custom Cakes"]
)

# =========================
# CREATE CUSTOM CAKE
# =========================
@router.post("/", response_model=customCakeResponse)
def create_custom_cake(
    cake: customCakeCreate,
    db: Session = Depends(get_db)
):

    detail = db.query(DetailQuotation).filter(
        DetailQuotation.detail_id == cake.detail_id
    ).first()

    if not detail:

        raise HTTPException(
            status_code=404,
            detail="Detail quotation not found"
        )

    size = db.query(Size).filter(
        Size.size_id == cake.size_id
    ).first()

    if not size:

        raise HTTPException(
            status_code=404,
            detail="Size not found"
        )

    flavor = db.query(Flavor).filter(
        Flavor.flavor_id == cake.flavor_id
    ).first()

    if not flavor:

        raise HTTPException(
            status_code=404,
            detail="Flavor not found"
        )

    filling = db.query(Filling).filter(
        Filling.filling_id == cake.filling_id
    ).first()

    if not filling:

        raise HTTPException(
            status_code=404,
            detail="Filling not found"
        )

    decoration = db.query(Decoration).filter(
        Decoration.decoration_id == cake.decoration_id
    ).first()

    if not decoration:

        raise HTTPException(
            status_code=404,
            detail="Decoration not found"
        )

    final_price = (
        cake.base_price +
        float(size.price_extra) +
        float(flavor.price_extra) +
        float(filling.price_extra) +
        float(decoration.price_extra)
    )

    new_cake = CustomCake(
        detail_id=cake.detail_id,
        size_id=cake.size_id,
        flavor_id=cake.flavor_id,
        filling_id=cake.filling_id,
        decoration_id=cake.decoration_id,
        servings=cake.servings,
        base_price=cake.base_price,
        final_price=final_price,
        description=cake.description
    )

    db.add(new_cake)

    db.commit()

    db.refresh(new_cake)

    return new_cake


# =========================
# GET ALL CUSTOM CAKES
# =========================
@router.get("/", response_model=list[customCakeResponse])
def get_custom_cakes(
    db: Session = Depends(get_db)
):

    cakes = db.query(CustomCake).all()

    return cakes


# =========================
# GET CUSTOM CAKE BY ID
# =========================
@router.get("/{cake_id}", response_model=customCakeResponse)
def get_custom_cake(
    cake_id: int,
    db: Session = Depends(get_db)
):

    cake = db.query(CustomCake).filter(
        CustomCake.cake_id == cake_id
    ).first()

    if not cake:

        raise HTTPException(
            status_code=404,
            detail="Custom cake not found"
        )

    return cake


# =========================
# DELETE CUSTOM CAKE
# =========================
@router.delete("/{cake_id}")
def delete_custom_cake(
    cake_id: int,
    db: Session = Depends(get_db)
):

    cake = db.query(CustomCake).filter(
        CustomCake.cake_id == cake_id
    ).first()

    if not cake:

        raise HTTPException(
            status_code=404,
            detail="Custom cake not found"
        )

    db.delete(cake)

    db.commit()

    return {
        "message": "Custom cake deleted successfully"
    }