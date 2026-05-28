from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

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

    existing = db.query(CakeExtra).filter(
        CakeExtra.cake_id == data.cake_id,
        CakeExtra.extra_id == data.extra_id
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Extra already added to cake"
        )

    new_extra = CakeExtra(
        cake_id=data.cake_id,
        extra_id=data.extra_id
    )

    db.add(new_extra)

    cake.final_price += extra.price_extra

    db.commit()

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