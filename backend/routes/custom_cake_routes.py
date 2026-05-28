from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from decimal import Decimal
from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.custom_cake import CustomCake
from backend.models.detail_quotation import DetailQuotation
from backend.models.quotation import Quotation
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

    flavor = db.query(Flavor).filter(
        Flavor.flavor_id == cake.flavor_id
    ).first()

    filling = db.query(Filling).filter(
        Filling.filling_id == cake.filling_id
    ).first()

    decoration = db.query(Decoration).filter(
        Decoration.decoration_id == cake.decoration_id
    ).first()

    if not size or not flavor or not filling or not decoration:
        raise HTTPException(
            status_code=404,
            detail="Invalid cake configuration"
        )

    # =========================
    # PRICE CALCULATION
    # =========================

    BASE_CAKE_PRICE = Decimal("500")

    final_price = (
        BASE_CAKE_PRICE +
        size.price_extra +
        flavor.price_extra +
        filling.price_extra +
        decoration.price_extra
    )

    existing_cake = db.query(CustomCake).filter(
        CustomCake.detail_id == cake.detail_id
    ).first()

    if existing_cake:

        raise HTTPException(
            status_code=400,
            detail="This detail already has a custom cake"
        )

    # =========================
    # CREATE CAKE
    # =========================

    new_cake = CustomCake(
        detail_id=cake.detail_id,

        size_id=cake.size_id,
        flavor_id=cake.flavor_id,
        filling_id=cake.filling_id,
        decoration_id=cake.decoration_id,

        servings=cake.servings,

        base_price=BASE_CAKE_PRICE,
        final_price=final_price,

        description=cake.description
    )

    db.add(new_cake)

    # =========================
    # UPDATE DETAIL
    # =========================

    detail.unit_price = final_price
    detail.subtotal = final_price * detail.quantity

    # =========================
    # UPDATE QUOTATION
    # =========================

    quotation = detail.quotation

    quotation_total = Decimal("0")

    for item in quotation.details:
        quotation_total += item.subtotal

    quotation.subtotal = quotation_total
    quotation.total = quotation_total

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

#ENDPOINT TO CALCULATE
# RECALCULATE QUOTATION
@router.post("/{quotation_id}/recalculate")
def recalculate_quotation(
    quotation_id: int,
    db: Session = Depends(get_db)
):

    quotation = db.query(Quotation).filter(
        Quotation.quotation_id == quotation_id
    ).first()

    if not quotation:

        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    quotation_total = Decimal("0")

    for detail in quotation.details:

        # UPDATE DETAIL SUBTOTAL
        detail.subtotal = (
            detail.unit_price * detail.quantity
        )

        quotation_total += detail.subtotal

    quotation.subtotal = quotation_total
    quotation.total = quotation_total

    db.commit()

    return {
        "message": "Quotation recalculated successfully",
        "quotation_id": quotation.quotation_id,
        "total": float(quotation.total)
    }
