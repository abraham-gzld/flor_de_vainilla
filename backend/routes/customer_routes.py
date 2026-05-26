from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db
from backend.models.customer import Customer
from backend.schemas.customer_schema import CustomerResponse
from backend.schemas.customer_schema import customerCreate

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.post("/")
def create_customer(
    customer: customerCreate,
    db:Session = Depends(get_db)
):
    new_customer = Customer(
        name = customer.name,
        phone = customer.phone,
        address = customer.address
    )
    db.add(new_customer)
    db.commit()

    db.refresh(new_customer)

    return {
        "message": "Customer created successfully",
        "customer": {
            "id": new_customer.customer_id,
            "name": new_customer.name,
            "phone": new_customer.phone
        }
    }

@router.get(
    '/',
    response_model = list[CustomerResponse]
)
def get_customer(
    db: Session = Depends(get_db)
):
    customers = db.query(Customer).all()
    return customers


@router.put('/{customer_id}')
def update_customer(
    customer_id: int,
    customer_data: customerCreate,
    db: Session = Depends(get_db)
):
    customer_id = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not customer_id:
        return{"message": "Customer not found"}

    customer_id.name = customer_data.name
    customer_id.phone = customer_data.phone
    customer_id.address = customer_data.address

    db.commit()
    db.refresh(customer_id)
    return{
        "Message": "Customer updated successfully"
    }

@router.delete('/{customer_id}')
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer_id = db.query(Customer).filter(Customer.customer_id == customer_id).first()

    if not customer_id:
        return{"message": "Customer not found"}

    db.delete(customer_id)
    db.commit()
    return{
        "Message": "Customer deleted successfully"
    }