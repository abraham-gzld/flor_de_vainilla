from fastapi import FastAPI

from backend.config.connection import engine
from backend.config.connection import Base

from backend.models.customer import Customer
from backend.routes.customer_routes import router as create_customer
from backend.routes.category_routes import router as create_category
from backend.routes.product_routes import router as create_product


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(create_customer)
app.include_router(create_category)
app.include_router(create_product)

@app.get("/")
def root():
    return{"Message": "Flor de Vainilla API"}