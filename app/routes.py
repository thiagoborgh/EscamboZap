from fastapi import APIRouter, HTTPException
from app.models import BuyProductRequest, LoginRequest, PaymentRequest, FavoriteRequest
from app.services import send_whatsapp_message
from app.database import Database

router = APIRouter()
db = Database()

@router.get("/")
def read_root():
    return {"message": "Bem-vindo ao escambo zap!"}

@router.get("/products/")
def get_products():
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, description FROM products")
        products = [{"id": row[0], "name": row[1], "price": row[2], "description": row[3]} for row in cursor.fetchall()]
        conn.close()
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/buy/")
def buy_product(request: BuyProductRequest):
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (product_id, buyer_id, seller_id, status) VALUES (?, ?, ?, ?)",
                       (request.product_id, request.user_id, 0, 'pending'))
        conn.commit()
        conn.close()
        return {"message": f"Produto {request.product_id} comprado por {request.user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/")
def get_transactions():
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(request: LoginRequest):
    if not request.user_phone:
        raise HTTPException(status_code=400, detail="Número de telefone obrigatório")
    if not request.user_phone.startswith('+'):
        raise HTTPException(status_code=400, detail="Número de telefone deve estar no formato E.164")
    send_whatsapp_message(request.user_phone, "Seu código de verificação é 123456")
    return {"message": "Código de verificação enviado para " + request.user_phone}

@router.post("/pay")
def process_payment(request: PaymentRequest):
    return {"message": f"Pagamento de R${request.amount:.2f} recebido de {request.user}. Transação aprovada!"}

@router.post("/favorite/")
def favorite_product(request: FavoriteRequest):
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO favorites (user_id, product_id) VALUES (?, ?)",
                       (request.user_id, request.product_id))
        conn.commit()
        conn.close()
        return {"message": f"Produto {request.product_id} favoritado pelo usuário {request.user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/favorite/")
def unfavorite_product(request: FavoriteRequest):
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM favorites WHERE user_id = ? AND product_id = ?",
                       (request.user_id, request.product_id))
        conn.commit()
        conn.close()
        return {"message": f"Produto {request.product_id} desfavoritado pelo usuário {request.user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/favorites/{user_id}")
def get_favorites(user_id: int):
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id FROM favorites WHERE user_id = ?", (user_id,))
        favorites = [row[0] for row in cursor.fetchall()]
        conn.close()
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))