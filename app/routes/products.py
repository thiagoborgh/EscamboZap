from fastapi import APIRouter, HTTPException, Depends
from app.models import Product, ProductCreate
from app.database import Database

router = APIRouter()
db = Database()

@router.post("/", response_model=Product)
def create_product(product: ProductCreate):
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
                       (product.name, product.price, product.description))
        conn.commit()
        product_id = cursor.lastrowid
        return Product(id=product_id, **product.dict())

@router.get("/", response_model=list[Product])
def list_products():
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, description FROM products")
        products = cursor.fetchall()
        return [Product(id=row[0], name=row[1], price=row[2], description=row[3]) for row in products]

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?",
                       (product.name, product.price, product.description, product_id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return Product(id=product_id, **product.dict())

@router.delete("/{product_id}")
def delete_product(product_id: int):
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}