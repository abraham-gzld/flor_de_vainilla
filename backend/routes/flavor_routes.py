from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.config.dependencies import get_db

from backend.models.flavor import Flavor

from backend.schemas.flavor_schema import flavorCreate
from backend.schemas.flavor_schema import flavorResponse


router = APIRouter(
    prefix="/flavors",
    tags=["Flavors"]
)


@router.post("/", response_model=flavorResponse)
def create_flavor(
    flavor: flavorCreate,
    db: Session = Depends(get_db)
):

    new_flavor = Flavor(
        name=flavor.name,
        price_extra=flavor.price_extra
    )

    db.add(new_flavor)

    db.commit()

    db.refresh(new_flavor)

    return new_flavor


@router.get("/", response_model=list[flavorResponse])
def get_flavors(
    db: Session = Depends(get_db)
):

    flavors = db.query(Flavor).all()

    return flavors

@router.get("/{flavor_id}", response_model=flavorResponse)
def get_flavor(
    flavor_id: int,
    db: Session = Depends(get_db)
):

    flavor = db.query(Flavor).filter(
        Flavor.flavor_id == flavor_id
    ).first()

    if not flavor:

        raise HTTPException(
            status_code=404,
            detail="Flavor not found"
        )

    return flavor


@router.put("/{flavor_id}", response_model=flavorResponse)
def update_flavor(
    flavor_id: int,
    flavor_data: flavorCreate,
    db: Session = Depends(get_db)
):

    flavor = db.query(Flavor).filter(
        Flavor.flavor_id == flavor_id
    ).first()

    if not flavor:

        raise HTTPException(
            status_code=404,
            detail="Flavor not found"
        )

    flavor.name = flavor_data.name
    flavor.price_extra = flavor_data.price_extra

    db.commit()

    db.refresh(flavor)

    return flavor


@router.delete("/{flavor_id}")
def delete_flavor(
    flavor_id: int,
    db: Session = Depends(get_db)
):

    flavor = db.query(Flavor).filter(
        Flavor.flavor_id == flavor_id
    ).first()

    if not flavor:

        raise HTTPException(
            status_code=404,
            detail="Flavor not found"
        )

    db.delete(flavor)

    db.commit()

    return {
        "message": "Flavor deleted successfully"
    }