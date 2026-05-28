from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.detail_quotation import DetailQuotation
from backend.models.quotation import Quotation
from backend.models.product import Product

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

    return new_detail