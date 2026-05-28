from fastapi import FastAPI

from backend.config.connection import engine
from backend.config.connection import Base

from backend.routes.customer_routes import router as create_customer
from backend.routes.category_routes import router as create_category
from backend.routes.product_routes import router as create_product
from backend.routes.flavor_routes import router as create_flavor
from backend.routes.filling_routes import router as create_filling
from backend.routes.decoration_router import router as create_decoration
from backend.routes.extra_routes import router as create_extra
from backend.routes.quotation_routes import router as create_quotation
from backend.routes.detail_quotation_routes import router as detail_router
from backend.routes.custom_cake_routes import router as cake_router
from backend.routes.cake_extra_routes import router as cake_extra_router
from backend.routes.size_routes import router as size_router


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(create_customer)
app.include_router(create_category)
app.include_router(create_product)
app.include_router(create_decoration)
app.include_router(create_flavor)
app.include_router(create_filling)
app.include_router(size_router)
app.include_router(create_extra)
app.include_router(create_quotation)
app.include_router(detail_router)
app.include_router(cake_router)
app.include_router(cake_extra_router)

@app.get("/")
def root():
    return{"Message": "Flor de Vainilla API"}