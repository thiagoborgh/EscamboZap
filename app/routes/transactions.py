from fastapi import APIRouter, HTTPException, Depends
from app.models import Transaction
from app.database import Database

router = APIRouter()
db = Database()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: Transaction):
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (product_id, buyer_id, seller_id, status) VALUES (?, ?, ?, ?)",
                       (transaction.product_id, transaction.buyer_id, transaction.seller_id, transaction.status))
        conn.commit()
        transaction_id = cursor.lastrowid
        return Transaction(id=transaction_id, **transaction.dict())

@router.get("/", response_model=list[Transaction])
def list_transactions():
    with db.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, product_id, buyer_id, seller_id, status FROM transactions")
        transactions = cursor.fetchall()
        return [Transaction(id=row[0], product_id=row[1], buyer_id=row[2], seller_id=row[3], status=row[4]) for row in transactions]