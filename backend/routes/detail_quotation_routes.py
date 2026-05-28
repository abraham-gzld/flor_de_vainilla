from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from decimal import Decimal

from backend.config.dependencies import get_db

from backend.schemas.detail_quotation_schema import (detailQuantityUpdate)
from backend.models.detail_quotation import DetailQuotation
from backend.models.quotation import Quotation
from backend.models.product import Product
from backend.utils.quotation_utils import (
    recalculate_quotation_totals
)

from backend.schemas.detail_quotation_schema import (
    detailQuotationCreate,
    detailQuotationResponse,
    detailQuantityUpdate
)

from backend.schemas.detail_quotation_schema import (
    detailQuotationCreate,
    detailQuotationResponse
)

router = APIRouter(
    prefix="/detail-quotations",
    tags=["Detail Quotations"]
)

@router.post("/", response_model=detailQuotationResponse)
def create_detail(
    detail: detailQuotationCreate,
    db: Session = Depends(get_db)
):

    quotation = db.query(Quotation).filter(
        Quotation.quotation_id == detail.quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    if detail.product_id:

        product = db.query(Product).filter(
            Product.product_id == detail.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

    new_detail = DetailQuotation(
        quotation_id=detail.quotation_id,
        product_id=detail.product_id,
        product_type=detail.product_type,
        quantity=detail.quantity,
        unit_price=detail.unit_price,
        subtotal=detail.subtotal,
        comment=detail.comment
    )

    db.add(new_detail)
    db.commit()
    db.refresh(new_detail)

    recalculate_quotation_totals(quotation)
    db.commit()
    db.refresh(new_detail)

    return new_detail

# UPDATE QUOATITY
# UPDATE DETAIL QUANTITY
@router.put("/{detail_id}/quantity")
def update_detail_quantity(
    detail_id: int,
    data: detailQuantityUpdate,
    db: Session = Depends(get_db)
):

    detail = db.query(DetailQuotation).filter(
        DetailQuotation.detail_id == detail_id
    ).first()

    if not detail:

        raise HTTPException(
            status_code=404,
            detail="Detail not found"
        )

    if data.quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    detail.quantity = data.quantity

    detail.subtotal = (
        detail.unit_price * detail.quantity
    )

    quotation = detail.quotation

    recalculate_quotation_totals(quotation)

    db.commit()

    return {
        "message": "Quantity updated successfully",
        "detail_id": detail.detail_id,
        "quantity": detail.quantity,
        "subtotal": float(detail.subtotal)
    }

# DELETE
# DELETE DETAIL
@router.delete("/{detail_id}")
def delete_detail(
    detail_id: int,
    db: Session = Depends(get_db)
):

    detail = db.query(DetailQuotation).filter(
        DetailQuotation.detail_id == detail_id
    ).first()

    if not detail:

        raise HTTPException(
            status_code=404,
            detail="Detail not found"
        )

    quotation = detail.quotation

    db.delete(detail)

    db.commit()

    # RECALCULATE TOTALS
    quotation_total = Decimal("0")

    remaining_details = db.query(DetailQuotation).filter(
        DetailQuotation.quotation_id == quotation.quotation_id
    ).all()

    for item in remaining_details:
        quotation_total += item.subtotal

    quotation.subtotal = quotation_total
    quotation.total = quotation_total

    db.commit()

    return {
        "message": "Detail deleted successfully"
    }
