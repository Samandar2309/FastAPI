from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
import schema

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="CRUD with Database")


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.post('/product/', response_model=schema.Product)
async def create_product(product: schema.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get('/product/', response_model=List[schema.Product])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@app.get('/product/{product_id}', response_model=schema.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
