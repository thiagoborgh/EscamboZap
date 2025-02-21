from pydantic import BaseModel

class BuyProductRequest(BaseModel):
    product_id: int
    user_id: int

class LoginRequest(BaseModel):
    user_phone: str

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

class User(BaseModel):
    id: int
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class Transaction(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    seller_id: int
    status: str

class PaymentRequest(BaseModel):
    user: str
    amount: float

class FavoriteRequest(BaseModel):
    user_id: int
    product_id: int