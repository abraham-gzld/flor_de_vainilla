from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from decimal import Decimal
from backend.utils.quotation_utils import (
    recalculate_quotation_totals
)

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.custom_cake import CustomCake
from backend.models.extra import Extra
from backend.models.cake_extra import CakeExtra

from backend.schemas.cake_extra_schema import (
    cakeExtraCreate,
    cakeExtraResponse
)

router = APIRouter(
    prefix="/cake-extras",
    tags=["Cake Extras"]
)

# =========================
# ADD EXTRA TO CAKE
# =========================
@router.post("/")
def add_extra_to_cake(
    data: cakeExtraCreate,
    db: Session = Depends(get_db)
):

    cake = db.query(CustomCake).filter(
        CustomCake.cake_id == data.cake_id
    ).first()

    if not cake:

        raise HTTPException(
            status_code=404,
            detail="Cake not found"
        )

    extra = db.query(Extra).filter(
        Extra.extra_id == data.extra_id
    ).first()

    if not extra:

        raise HTTPException(
            status_code=404,
            detail="Extra not found"
        )

    # =========================
    # VALIDATE DUPLICATES
    # =========================

    existing_extra = db.query(CakeExtra).filter(
        CakeExtra.cake_id == data.cake_id,
        CakeExtra.extra_id == data.extra_id
    ).first()

    if existing_extra:

        raise HTTPException(
            status_code=400,
            detail="Extra already added to cake"
        )

    # =========================
    # CREATE RELATION
    # =========================

    new_cake_extra = CakeExtra(
        cake_id=data.cake_id,
        extra_id=data.extra_id
    )

    db.add(new_cake_extra)

    # =========================
    # UPDATE PRICES
    # =========================

    cake.final_price += extra.price_extra

    detail = cake.detail

    detail.unit_price = cake.final_price

    detail.subtotal = (
        detail.unit_price * detail.quantity
    )

    quotation = detail.quotation

    quotation_total = Decimal("0")

    for item in quotation.details:
        quotation_total += item.subtotal

    quotation.subtotal = quotation_total
    quotation.total = quotation_total

    db.commit()

    db.refresh(new_cake_extra)

    return {
        "message": "Extra added successfully"
    }


# =========================
# REMOVE EXTRA FROM CAKE
# =========================
@router.delete("/")
def remove_extra_from_cake(
    cake_id: int,
    extra_id: int,
    db: Session = Depends(get_db)
):

    cake_extra = db.query(CakeExtra).filter(
        CakeExtra.cake_id == cake_id,
        CakeExtra.extra_id == extra_id
    ).first()

    if not cake_extra:

        raise HTTPException(
            status_code=404,
            detail="Cake extra not found"
        )

    cake = db.query(CustomCake).filter(
        CustomCake.cake_id == cake_id
    ).first()

    extra = db.query(Extra).filter(
        Extra.extra_id == extra_id
    ).first()

    cake.final_price -= float(extra.price_extra)

    db.delete(cake_extra)

    db.commit()

    return {
        "message": "Extra removed successfully"
    }

# DELETE EXTRA FROM CAKE
@router.delete("/{cake_id}/{extra_id}")
def remove_extra_from_cake(
    cake_id: int,
    extra_id: int,
    db: Session = Depends(get_db)
):

    cake_extra = db.query(CakeExtra).filter(
        CakeExtra.cake_id == cake_id,
        CakeExtra.extra_id == extra_id
    ).first()

    if not cake_extra:

        raise HTTPException(
            status_code=404,
            detail="Extra not found in cake"
        )

    cake = cake_extra.cake
    extra = cake_extra.extra

    # REMOVE EXTRA PRICE
    cake.final_price -= extra.price_extra

    # UPDATE DETAIL
    detail = cake.detail

    detail.unit_price = cake.final_price
    detail.subtotal = (
        detail.quantity * cake.final_price
    )

    # UPDATE QUOTATION
    quotation = detail.quotation

    recalculate_quotation_totals(quotation)

    db.delete(cake_extra)

    db.commit()

    return {
        "message": "Extra removed successfully"
    }