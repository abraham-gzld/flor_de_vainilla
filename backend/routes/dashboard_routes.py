from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.config.dependencies import get_db

from backend.models.quotation import Quotation
from backend.models.customer import Customer

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    total_customers = db.query(Customer).count()

    total_quotations = db.query(Quotation).count()

    total_sales = db.query(
        func.sum(Quotation.total)
    ).scalar()

    return {

        "customers": total_customers,

        "quotations": total_quotations,

        "sales": float(total_sales or 0)
    }