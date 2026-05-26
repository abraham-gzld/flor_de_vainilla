from fastapi import APIRouter
from fastapi import Depends

from fastapi import HTTPException


from sqlalchemy.orm import Session

from backend.config.dependencies import get_db
from backend.models.product import Product
from backend.models.category import Category
from backend.schemas.product_schema import productResponse
from backend.schemas.product_schema import productCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=productResponse)
def create_product(
    product: productCreate,
    db:Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.category_id == product.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_product = Product(
        category_id=product.category_id,
        name=product.name,
        description=product.description,
        base_price=product.base_price,
        active=product.active
    )
    db.add(new_product)
    db.commit()

    db.refresh(new_product)

    return new_product

@router.get('/', response_model = list[productResponse])
def get_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()
    return product


@router.put('/{product_id}')
def update_product(
    product_id: int,
    product_data: productCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        return{"message": "Product not found"}

    category = db.query(Category).filter(
        Category.category_id == product_data.category_id
    ).first()

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.category_id = product_data.category_id
    product.name = product_data.name
    product.description = product_data.description
    product.base_price = product_data.base_price
    product.active = product_data.active

    db.commit()
    db.refresh(product)
    return{
        "Message": "Product Updated successfully"
    }

@router.delete('/{product_id}')
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        return{"message": "Product not found"}

    db.delete(product)
    db.commit()
    return{
        "Message": "Product deleted successfully"
    }