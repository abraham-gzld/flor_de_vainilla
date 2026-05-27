from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db
from backend.models.category import Category
from backend.schemas.category_schema import categoryResponse
from backend.schemas.category_schema import categoryCreate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=categoryResponse)
def create_category(
    category: categoryCreate,
    db:Session = Depends(get_db)
):
    new_category = Category(
        name = category.name,
    )
    db.add(new_category)
    db.commit()

    db.refresh(new_category)

    return {
        "message": "Category created successfully",
        "customer": {
            "id": new_category.category_id,
            "name": new_category.name,
        }
    }

@router.get('/', response_model = list[categoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    category = db.query(Category).all()
    return category


@router.put('/{category_id}')
def update_category(
    category_id: int,
    category_data: categoryCreate,
    db: Session = Depends(get_db)
):
    category_id = db.query(Category).filter(Category.category_id == category_id).first()

    if not category_id:
        return{"message": "Customer not found"}

    category_id.name = category_data.name

    db.commit()
    db.refresh(category_id)
    return{
        "Message": "Category deleted successfully"
    }

@router.delete('/{category_id}')
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category_id = db.query(Category).filter(Category.category_id == category_id).first()

    if not category_id:
        return{"message": "Category not found"}

    db.delete(category_id)
    db.commit()
    return{
        "Message": "Category deleted successfully"
    }