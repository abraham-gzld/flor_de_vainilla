from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.quotation import Quotation
from backend.models.customer import Customer

from backend.schemas.quotation_schema import (
    quotationCreate,
    quotationResponse
)

router = APIRouter(
    prefix="/quotations",
    tags=["Quotations"]
)

# CREATE QUOTATION
@router.post("/", response_model=quotationResponse)
def create_quotation(
    quotation: quotationCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.customer_id == quotation.customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    new_quotation = Quotation(
        customer_id=quotation.customer_id,
        subtotal=quotation.subtotal,
        total=quotation.total,
        status=quotation.status,
        note=quotation.note
    )

    db.add(new_quotation)

    db.commit()

    db.refresh(new_quotation)

    return new_quotation


# GET ALL QUOTATIONS
@router.get("/", response_model=list[quotationResponse])
def get_quotations(
    db: Session = Depends(get_db)
):

    quotations = db.query(Quotation).all()

    return quotations


# GET QUOTATION BY ID
@router.get("/{quotation_id}", response_model=quotationResponse)
def get_quotation(
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

    return quotation


# GET FULL QUOTATION
@router.get("/{quotation_id}/full")
def get_full_quotation(
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

    details_response = []

    for detail in quotation.details:

        detail_data = {
            "detail_id": detail.detail_id,
            "product_type": detail.product_type,
            "quantity": detail.quantity,
            "unit_price": float(detail.unit_price),
            "subtotal": float(detail.subtotal),
            "comment": detail.comment
        }

        # SIMPLE PRODUCT
        if detail.product_type == "simple_product":

            detail_data["product"] = {
                "product_id": detail.product.product_id,
                "name": detail.product.name,
                "description": detail.product.description,
                "base_price": float(detail.product.base_price)
            }

        # CUSTOM CAKE
        elif detail.product_type == "custom_cake":

            cake = detail.custom_cake

            extras = []

            for extra in cake.extras:

                extras.append({
                    "extra_id": extra.extra.extra_id,
                    "name": extra.extra.name,
                    "price_extra": float(extra.extra.price_extra)
                })

            detail_data["custom_cake"] = {

                "cake_id": cake.cake_id,

                "size": {
                    "size_id": cake.size.size_id,
                    "name": cake.size.name,
                    "price_extra": float(cake.size.price_extra)
                },

                "flavor": {
                    "flavor_id": cake.flavor.flavor_id,
                    "name": cake.flavor.name,
                    "price_extra": float(cake.flavor.price_extra)
                },

                "filling": {
                    "filling_id": cake.filling.filling_id,
                    "name": cake.filling.name,
                    "price_extra": float(cake.filling.price_extra)
                },

                "decoration": {
                    "decoration_id": cake.decoration.decoration_id,
                    "name": cake.decoration.name,
                    "price_extra": float(cake.decoration.price_extra)
                },

                "servings": cake.servings,

                "base_price": float(cake.base_price),

                "final_price": float(cake.final_price),

                "description": cake.description,

                "extras": extras
            }

        details_response.append(detail_data)

    return {

        "quotation_id": quotation.quotation_id,

        "quotation_date": quotation.quotation_date,

        "status": quotation.status,

        "subtotal": float(quotation.subtotal),

        "total": float(quotation.total),

        "note": quotation.note,

        "customer": {
            "customer_id": quotation.customer.customer_id,
            "name": quotation.customer.name,
            "phone": quotation.customer.phone,
            "address": quotation.customer.address
        },

        "details": details_response
    }


# UPDATE QUOTATION
@router.put("/{quotation_id}", response_model=quotationResponse)
def update_quotation(
    quotation_id: int,
    quotation_data: quotationCreate,
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

    customer = db.query(Customer).filter(
        Customer.customer_id == quotation_data.customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    quotation.customer_id = quotation_data.customer_id
    quotation.subtotal = quotation_data.subtotal
    quotation.total = quotation_data.total
    quotation.status = quotation_data.status
    quotation.note = quotation_data.note

    db.commit()

    db.refresh(quotation)

    return quotation


# DELETE QUOTATION
@router.delete("/{quotation_id}")
def delete_quotation(
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

    db.delete(quotation)

    db.commit()

    return {
        "message": "Quotation deleted successfully"
    }

@router.put("/{quotation_id}/approve")
def approve_quotation(
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

    quotation.status = "approved"

    db.commit()

    return {
        "message": "Quotation approved"
    }

@router.put("/{quotation_id}/cancel")
def cancel_quotation(
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

    quotation.status = "canceled"

    db.commit()

    return {
        "message": "Quotation canceled"
    }